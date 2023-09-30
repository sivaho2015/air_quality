##############################################################################################################################
# Spin up, shut down, and restart Docker containers
up:
	docker compose --env-file .env up --build -d

down:
	docker compose down --volumes

restart:
	down up

####################################################################################################################
# Set up cloud infrastructure
tf-init:
	terraform -chdir=./terraform init

infra-up:
	terraform -chdir=./terraform apply

infra-down:
	terraform -chdir=./terraform destroy

infra-config:
	terraform -chdir=./terraform output

##############################################################################################################################
# Auto formatting, testing, type checks, and lint checks

format:
	docker exec formatter python -m black -S --line-length 79 .

isort:
	docker exec formatter isort .

pytest:
	docker exec formatter pytest /code/test

type:
	docker exec formatter mypy --ignore-missing-imports /code

lint:
	docker exec formatter flake8 /code

ci: isort format type lint pytest
