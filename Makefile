SHELL = /usr/bin/env bash -xeuo pipefail

stack_name:=fukuoka-de-longi-card-reader-cloud
template_path:=dist/packaged.yml

isort:
	poetry run isort -rc src

black:
	poetry run black src

format: isort black

lint:
	poetry run flake8 src/handlers

build:
	pwd_dir=$$PWD; \
	cd src/layers/modules; \
	docker build -t my-build .; \
	docker run --name my-container my-build pip3 install -r requirements.txt -t ./python; \
	docker cp my-container:/workdir/python .; \
	docker rm my-container; \
	docker rmi my-build; \
	cd $$pwd_dir

package:
	rm -rf dist/
	mkdir dist/
	poetry run sam package --s3-bucket $$SAM_ARTIFACT_BUCKET --output-template-file $(template_path) --template-file sam.yml

deploy: package
	poetry run sam deploy \
		--stack-name $(stack_name) \
		--template-file $(template_path) \
		--capabilities CAPABILITY_IAM \
		--role-arn $$CLOUDFORMATION_DEPLOY_ROLE_ARN \
		--no-fail-on-empty-changeset
	poetry run aws cloudformation describe-stacks \
		--stack-name $(stack_name) \
		--query Stacks[0].Outputs