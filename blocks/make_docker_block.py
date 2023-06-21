from prefect.infrastructure.docker import DockerContainer
import os
from dotenv import load_dotenv

load_dotenv()

docker_block = DockerContainer(
    image="prefecthq/prefect:latest",  # insert your image here
    image_pull_policy="ALWAYS",
    auto_remove=True,
    env=os.environ
)

docker_block.save("etl", overwrite=True)
