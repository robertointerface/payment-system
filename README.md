# payment-system
Display AWS DevOps skills, Cloudformation, CI/CD, serverless, State Machine, create a Payment system implemented by an aws state machine.

This project is NOT production ready, the purpose of the project is not to run this state machine <br>
on AWS, the purpose is to show State machine orchestration WITH a good CI/CD methodology.

![Model](https://github.com/robertointerface/payment-system/blob/staging/state-machine-cropped.png)

# WHAT TO LOOK FOR.
1 - Cloudformation usage, couldformation file on cloudformation/cfn.yml <br>
2 - State machine built with python package 'stepfunctions' in state_machine/payment_state_machine_definition.py . <br>
3 - Lambdas are defined under directory lambdas. <br>
4 - State machine being deployed with CircleCI where circleci YML file is under .circleci/config.yml,
the state machine and cloudformation Stack are deployed with the Git branch name, this way multiple users can work and test
the state machine at the same time, otherwise you have multiple users tyring to deploy state machine with the same name.
STAGING-state-machine-name. Also, user gets the option to delete deployed cloudformation Stack with CircleCI web interface by just pushing a button.
5 - Lambdas 'check_product_availability' & 'pay-order' are quite modular, when for example the payment
methodology (by credit card, bank account or user credit) can be specified as environment variables when
creating the lambda and lambda will use specific classes depending on those environment variables. <br>
6 - Unit testing on the AWS Lambdas have coverage and results are saved on xml files which allows for easier inspection on CircleCI of test results.<br>
7 - Package management is done with Poetry which is more painful to learn than just pip BUT it will save
a lot of problems in the future as it keeps good track of all dependencies.
6 - Lambdas use MongoDB database, As the state machine lives inside a VPC and the
MongoDB database is created on another VPC cluster, a peering connection was created 
between those VPCs so only state machine VCP can try to connect to MongoDB

# IMPROVEMENTS THAT NEED TO BE DONE
- Data access should be done by means of a Rest API, GRAPHQL or any other third <br>
party style but data should not be access directly form the lambdas by Pymongo. <br>
Microservices architecture needs to be followed and having a microservice for data <br>
access is essential.
- Data handlers are repeated, this should be made a third party library and deployed to <br>
AWS, this is apart from the previous step, so we should have a REST API or GRAPHQL and also <br>
a library in code artifact that calls the REST API or GraphQL.
- Building state machine should be done with Terraform or Pulumi as seems to be a more robust way to do it <br>
with more available options to configure plus those project have and will have better maintenance in the future.
- Again there is code repetition on some 'utils' functions like get 'get_current_user_or_role_credentials' <br>
these functions should be on a third party library and uploaded to aws 'codeartifact'.
- Unit testing is included in the CI/CD BUT we should also have end-to-end testing where we actually test the <br>
deployed pipeline.
- CI/CD should also have documentation build/deployment.
- Lambdas are deployed just as package code, lambdas can be deployed by means of Dockerfile if prefered.


# Running Tests

Each lambda has its own unit testing, to run tests on each lambda you need
first to install dependencies from poetry.lock file.

If you don't have poetry, install poetry with command as below <br>

curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.3.2 python3.8 -

Navigate to the directory where poetry lock file is and run: <br>

poetry install <br>
or as below for install development and testing dependencies also.
poetry install --with dev 


Most Tests need a local mongodb running, to do so you can just get the docker
image with the command below.

docker run -it -v mongodata:/data/db -p 27017:27017 --name mongodb -d mongo

