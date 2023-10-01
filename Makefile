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

####################################################################################################################
# Port forwarding to local machine

cloud-dagster:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 3001:$$(terraform -chdir=./terraform output -raw ec2_public_dns):3000 && open http://localhost:3001 && rm private_key.pem

cloud-metabase:
	terraform -chdir=./terraform output -raw private_key > private_key.pem && chmod 600 private_key.pem && ssh -o "IdentitiesOnly yes" -i private_key.pem ubuntu@$$(terraform -chdir=./terraform output -raw ec2_public_dns) -N -f -L 3002:$$(terraform -chdir=./terraform output -raw ec2_public_dns):3001 && open http://localhost:3002 && rm private_key.pem

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
