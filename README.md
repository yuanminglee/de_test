# Tasman Data Engineer - Assessment Task
​
Many thanks for taking the time to complete this assessment for the position of Data Engineer at Tasman!
​
The assessment sets out a series of tasks that progressively increase in complexity. We don’t necessarily expect you to 
finish them all. We encourage you to send the code our way after you have spent the time you are comfortable with. We don't expect everyone to finish all tasks,
If pushed for time, please describe how you would have completed the remaining tasks. However, we do expect that 
the sections you have completed are production-ready and are representative of the standard of work you are capable of.
​
The assessment is an end-to-end task which includes:
- Connecting to a novel data source, 
- Making sense of the data,
- Containerising it for ease of use
- Description of cloud implementation
​
This is highly representative of the work you will be asked to do at Tasman. We care a lot about good understanding of the requirements, collaboration and early feedback – so if you get stuck or 
have any questions, please do not hesitate to reach out.
​
## Dataset
- The USA Jobs reporting database (https://www.usajobs.gov/) is a very extensive repository of all job openings in the US government.
- It has a big, well-documented RESTful API documented [here](https://developer.usajobs.gov/API-Reference)
- The API can be accessed through the [root URL](https://data.usajobs.gov/api/). We will share an API key via email.
​
​
## Assessment
1. Write a simple ETL script that performs a search of the USAJOBS API, with the criteria detailed in the `Search Criteria` subsection. 
2. The script should load the data into a database (of your choice) container, that **persists data on the host**. 
3. Containerise the extraction service, so it can be run daily to populate the database. 
4. Describe which cloud services you would use to implement this in a cloud provider of your choosing. What are some 
   pros and cons of your technology choice? 
​
### Search Criteria
- Perform a search of jobs that have `data engineering` as a *keyword*. 
- Parse a subset of fields from the response that a job-seeker based in Chicago with 5 years of experience, would find 
  useful in their own database of job postings. At the very least, retrieve the following fields: `PositionTitle`, 
  `PositionURI`, `PositionLocation`, `PositionRemuneration`. 
​
​
## What we are looking for
- Quality, readability, and clarity of intent. 
- Informative README document that provides context and instructions on usage and deployment.
- A sensibly structured codebase, using modern tooling.
- A clear database design of table(s) and (if necessary) data models.
- In the ETL script: separation of concerns, extensibility, robustness. Good handling of the API responses. Appropriate handling of errors, and respecting the API rate limits.
- Finally, we have to be able to run and reproduce what you build. Make sure we can run the service locally, with minimal additional work, and starting from scratch (assuming we have Docker and Python installed).
- Secure credential management
​
​
## Further comments
- Feel free to use any tools, packages, utilities or services you want to accomplish this.
- Deliver your codebase and scripts in a Git repository, with a view to presenting a working version of it 
  in the Technical Interview.