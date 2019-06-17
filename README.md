# Hello Users Serverless Application

## Items included

- Here we have a server/ folder, where the serverless application lives. It runs on Python 3.7 using the Serverless Application Framework on AWS, and can be deployed and manipulated using the Makefile.

## Architecture

A detailed image of the infrastructure architecture can be found [here](diagram.png).

## Testing

- For testing, I added a couple of plugins for DynamoDB offline mode.
- In order to test, simply run `make test-local`, after `make install`.
- By default the DynamoDB offline server will run on port 8000, and the local server will run on 5000. The testing makes sure the behavior for GET and PUT is as expected.

## Deploying

- In order to deploy, please run `make deploy`. This assumes you have configured the local AWS_PROFILE and AWS_DEFAULT_REGION variables accordingly. If not, please do the following:
    - `export AWS_ACCESS_KEY_ID=<access_key_id>`
    - `export AWS_SECRET_ACCESS_KEY=<secret access key>`
    - `export AWS_DEFAULT_REGION=us-east-1`
