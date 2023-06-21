import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
from prefect import flow, task
from prefect.tasks import task_input_hash
from sqlalchemy import create_engine

load_dotenv()
DB_PARAMS = {
    "host": "localhost",
    "port": "5433",
    "user": os.environ.get("PGDATABASE_USER"),
    "password": os.environ.get("PGDATABASE_PASSWORD"),
    "db": os.environ.get("PGDATABASE_DB"),
    "table_name": "usa_jobs"
}
TEMP_FILE_PATH = "./data/data.json"

@task(name="clear_output_file", log_prints=True)
def clear_output_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

@task(
    name="extract",
    log_prints=True,
    cache_key_fn=task_input_hash
)
def extract(keyword: str, page:int=1):
    url = "https://data.usajobs.gov/api/search"
    headers = {
        'Host': 'data.usajobs.gov',
        'User-Agent': os.environ.get("USA_JOBS_USER_AGENT"),
        'Authorization-Key': os.environ.get("USA_JOBS_AUTHORIZATION_KEY")
    }

    all_results = []
    has_next = True
        
    while has_next:
        params = {
            'Keyword': keyword,
            'ResultsPerPage': 500,
            'Fields': 'Min',
            "Page": page
        }
        print(f"Extracting...")
        response = requests.get(url, params=params, headers=headers).json()
        number_of_pages = int(response["SearchResult"]["UserArea"]["NumberOfPages"])
        print(f"Extracted {page} / {number_of_pages} pages.")

        all_results.extend(response["SearchResult"]["SearchResultItems"])
        has_next = page < number_of_pages
        page += 1

    print("No more pages. Extraction complete. Saving to file...")
    with open(TEMP_FILE_PATH, "a") as file:
        json.dump(all_results, file)
        print(f"Results saved to {TEMP_FILE_PATH}.")

@task(
    name="transform",
    log_prints=True,
    cache_key_fn=task_input_hash
)
def transform(path):
    with open(path, 'r') as f:
        jobs = json.load(f)
    
        parsed_response = [
            {
                "job_id": job["MatchedObjectId"],
                "title": job["MatchedObjectDescriptor"]["PositionTitle"],
                "uri": job["MatchedObjectDescriptor"]["PositionURI"],
                "location": job["MatchedObjectDescriptor"]["PositionLocationDisplay"],
                "organization": job["MatchedObjectDescriptor"]["OrganizationName"],
                "min_salary": job["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MinimumRange"],
                "max_salary": job["MatchedObjectDescriptor"]["PositionRemuneration"][0]["MaximumRange"],
                "salary_interval": job["MatchedObjectDescriptor"]["PositionRemuneration"][0]["Description"],
                "posted_at": job["MatchedObjectDescriptor"]["PublicationStartDate"],
                "_loaded_at": datetime.now()
            }
            for job in jobs
        ]
        df = pd.DataFrame(parsed_response)

        df["min_salary"] = pd.to_numeric(df["min_salary"])
        df["max_salary"] = pd.to_numeric(df["max_salary"])
        df["posted_at"] = pd.to_datetime(df["posted_at"])
        
        return df

@task(log_prints=True)
def load(df, user, password, host, port, db, table_name):
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    try:
        df.head(n=0).to_sql(
            name=table_name,
            con=engine,
            index_label="id",
        )
    except:
        print("Table already exists. Appending rows...")
    
    df.to_sql(
        name=table_name,
        con=engine,
        index_label="id",
        if_exists='replace'
    )

    print(f"Load complete.")

@flow
def main_flow():
    clear_output_file(TEMP_FILE_PATH)
    extract('data engineering')
    df = transform(TEMP_FILE_PATH)
    load(df, **DB_PARAMS)
    clear_output_file(TEMP_FILE_PATH)

if __name__ == "__main__":
    main_flow()