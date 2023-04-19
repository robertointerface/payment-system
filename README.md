# payment-system
Payment system implemented by an aws state machine.

This project is NOT production ready, the purpose of the project is not to run this state machine <br>
on AWS, the purpose is to show State machine orchestration WITH a good CI/CD methodology.

# WHAT TO LOOK FOR.
1 - Cloudformation usage, couldformation file on cloudformation/cfn.yml
2 - State machine built with python package 'stepfunctions'.
3 - State machine being deployed with CircleCI, the state machine and cloudformation Stack <br>
are deployed with the Git branch name, this way multiple users can work and test the state machine <br>
at the same time, otherwise you have multiple users tyring to deploy state machine with name <br>
STAGING-state-machine-name. Also, user gets the option to delete deployed cloudformation Stack <br>
with CircleCI web interface by just pushing a button.

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
- Lambdas are deployed just as package code, lambdas can be deployed by means of Dockerfile if prefered.