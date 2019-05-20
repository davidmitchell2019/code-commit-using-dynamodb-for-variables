from src.codecommit.code_commit import codeCommit
from src.codecommit.client_locator import CODECOMMITClient
from src.dynamodb.dynamo_db import create_table_commits
from src.dynamodb.dynamo_db import add_item_commits
from src.dynamodb.dynamo_db import delete_item_commits
from src.dynamodb.dynamo_db import read_table_commits
import time
def main():
    #TODO: exception handling and testing, run final tests after Friday's re factoring
    username = "David"
    data = "here is my 3d commit"
    ccommit_client = CODECOMMITClient().get_client()
    cclient = codeCommit(ccommit_client)
    cclient.post_data_to_repo(username, data)





if __name__ == '__main__':
    main()
