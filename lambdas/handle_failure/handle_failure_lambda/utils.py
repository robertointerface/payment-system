import boto3
from botocore.exceptions import ClientError
from boto3 import Session


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