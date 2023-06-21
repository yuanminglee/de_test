from prefect.infrastructure.container import DockerContainer
import os
from dotenv import load_dotenv

load_dotenv()

docker_block = DockerContainer(
    image="prefecthq/prefect:latest",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
    env={
        "POSTGRES_USER": os.environ.get("POSTGRES_USER"),
        "POSTGRES_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "POSTGRES_DB": os.environ.get("POSTGRES_DB"),
        "PGADMIN_DEFAULT_EMAIL": os.environ.get("PGADMIN_DEFAULT_EMAIL"),
        "PGADMIN_DEFAULT_PASSWORD": os.environ.get("PGADMIN_DEFAULT_PASSWORD"),
        "USA_JOBS_AUTHORIZATION_KEY": os.environ.get("USA_JOBS_AUTHORIZATION_KEY"),
        "USA_JOBS_USER_AGENT": os.environ.get("USA_JOBS_USER_AGENT")
    }
)

docker_block.save("etl", overwrite=True)
