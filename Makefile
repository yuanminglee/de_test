install-requirements:
	pip install -r requirements.txt

pgdatabase-up:
	docker-compose up -d

create-blocks:
	python blocks/make_docker_block.py
	python blocks/make_gh_block.py

prefect-start:
	prefect orion start
	prefect agent start  --work-queue "default-agent-pool"

create-deployment:
	prefect deployment build flows/etl.py:main_flow \
		-n etl-gh-docker \
		-q default-agent-pool \
		-sb github/etl \
		-ib docker-container/etl \
		-o deployments/etl-docker-deployment \
		--apply

run: install-requirements pgdatabase-up create-blocks prefect-start
