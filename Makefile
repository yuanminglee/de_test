install-requirements:
	pip install -r requirements.txt

create-blocks:
	python blocks/make_docker_block.py
	python blocks/make_gh_block.py

create-deployment:
	prefect deployment build flows/etl.py:main_flow \
		-n etl-gh-docker \
		-q prefect-agent \
		-o deployments/etl-docker-deployment \
		--apply

run: install-requirements create-blocks create-deployment
