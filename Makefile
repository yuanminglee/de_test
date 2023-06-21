install-requirements:
	pip install -r requirements.txt

pgdatabase-up:
	docker-compose up -d

create-blocks:
	python blocks/make_docker_block.py
	python blocks/make_gh_block.py

prefect-start:
	prefect orion start
	prefect agent start  --work-queue "local-work"

run: install-requirements pgdatabase-up create-blocks prefect-start
