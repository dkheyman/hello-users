install:
	npm install --save serverless
	npm install --save serverless-dynamodb-local
	npm install --save serverless-wsgi
	npm install --save serverless-offline
	npm install --save serverless-python-requirements
	pip install -r requirements.txt

run-local:
	sls dynamodb install
	sls dynamodb start
	sls wsgi serve

deploy:
	sls deploy

test-local:
	sls dynamodb install
	sls dynamodb start &
	sls wsgi serve && python tests.py FQDN="http://localhost" PORT="5000"
