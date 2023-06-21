install-requirements:
	pip install -r requirements.txt

create-blocks:
	python blocks/make_docker_block.py
	python blocks/make_gh_block.py

pgdatabase-up:
	docker-compose up -d

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

run: install-requirements create-blocks pgdatabase-up prefect-start create-deployment
