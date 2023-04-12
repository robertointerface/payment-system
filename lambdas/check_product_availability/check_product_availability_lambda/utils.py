import boto3
from botocore.exceptions import ClientError
from boto3 import Session

def get_string_secret(secret_name: str, region_name: str) -> str:
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        else:
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        secret = get_secret_value_response['SecretString']
        return secret



def get_current_user_or_role_credentials():
    """Returns AWS read only credentials for either the current user or the current IAM role executed on the server.

    Returns:
        A set of frozen credentials constituting an access key, a secret key and a token.
    """
    session = Session()
    credentials = session.get_credentials()

    # Credentials are refreshable, so accessing your access key / secret key
    # separately can lead to a race condition. Use this to get an actual matched set.
    return credentials.get_frozen_credentials()