import boto3
import pyboto3
import time
import sys
from src.codecommit.client_locator import CODECOMMITClient
from src.dynamodb.dynamo_db import read_table_commits
from src.dynamodb.dynamo_db import add_item_commits
from src.dynamodb.dynamo_db import delete_item_commits
from src.dynamodb.dynamo_db import add_item_pcid
from src.dynamodb.dynamo_db import delete_item_pcid
from src.dynamodb.dynamo_db import create_table_pcid
from src.dynamodb.dynamo_db import create_table_commits
from src.dynamodb.dynamo_db import read_table_pcid
# A class for putting, commiting and deleting files from AWS code commit
class codeCommit:

    # get commits from DynamoDB table and assign to a temp variable
    commits = 0
    try:
        temp = read_table_commits()
        commits = temp['Items'][0]['commits']
    except:
        print("table not created yet so using commits = 0")
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.codecommit"""


    # A method to commit a file to AWS code commit
    def commit_file(self, commit_id, repo_name, branch_name, author_name, auth_email, file_path, file_content, commit_message):
        return self._client.create_commit(
            repositoryName=repo_name,
            branchName=branch_name,
            authorName=author_name,
            parentCommitId=commit_id,
            email=auth_email,
            commitMessage=commit_message,
            keepEmptyFolders=True,
            putFiles=[
                {
                    'filePath': file_path,
                    'fileContent': file_content
                }
            ]
        )

    # A method to commit a file to AWS code commit
    def commit_file_new_repo(self, repo_name, branch_name, author_name, auth_email, file_path, file_content, commit_message):
        return self._client.create_commit(
            repositoryName=repo_name,
            branchName=branch_name,
            authorName=author_name,
            email=auth_email,
            commitMessage=commit_message,
            keepEmptyFolders=True,
            putFiles=[
                {
                    'filePath': file_path,
                    'fileContent': file_content
                }
            ]
        )

    # A method for deleting files in AWS code commit
    def delete_file(self, repo_name, branch_name, author_name, auth_email, commit_message, file_path):
        return self._client.create_commit(
            repositoryName=repo_name,
            branchName=branch_name,
            authorName=author_name,
            email=auth_email,
            commitMessage=commit_message,
            keepEmptyFolders=True,
            deleteFiles=[
                {
                    'filePath': file_path,
                    'isMove': True
                },
            ]
        )

    # A method to put a file, unfortunately needs the parent commit id so not great
    def put_file(self, repo_name, branch_name, file_content, file_path, cid, commit_message, author_name, author_email):
        return self._client.put_file(
            repositoryName=repo_name,
            branchName=branch_name,
            fileContent=file_content,
            filePath=file_path,
            fileMode='NORMAL',
            parentCommitId=cid,
            commitMessage=commit_message,
            name=author_name,
            email=author_email
        )

    # A method to create a repo
    def create_repository(self, repo_name, repo_description):
        return self._client.create_repository(
            repositoryName=repo_name,
            repositoryDescription=repo_description
        )

    # a method to setup the initial repo, create the file and some logic that will get the parent commit id and allow a new commit using that
    def post_data_to_repo(self, username, data_to_post):
        author_name = username
        author_email = "Billy@Bob.com"
        branch = "master"
        repo = "terraform"
        file_path = "terraform/request.json"
        commit_message = "Terraform commit"
        ccommit_client = CODECOMMITClient().get_client()
        cclient = codeCommit(ccommit_client)
        # if commits = 0 then create a repo and the initial file
        # If the repo is already in use or created this will fail as commit ID can only be empty in an empty repo
        if (codeCommit.commits == 0):
            try:
                # create terraform repo
                create_table_pcid()
                create_table_commits()
                time.sleep(15)
                add_item_commits(0)
                cclient.create_repository(repo, "A repo for Terraform request response data")
                print("terraform repo created")

                # class calls method and assigns the api response
                commit_response = cclient.commit_file_new_repo(repo, branch, author_name, author_email, file_path,
                                                               data_to_post, commit_message)
                print("great this worked so repo must have been created with an empty directory")
                # get the commit ID of the first commit
                parent_commit_id = commit_response['commitId']
                add_item_pcid(parent_commit_id)
                #assign current commits to temp
                temp = read_table_commits()
                delete_item_commits(codeCommit.commits)
                # Add the variable to the commits variable, will always pull the highest commit number from the table as it will be the last one entered
                codeCommit.commits = temp['Items'][0]['commits']
                #Increment commits
                codeCommit.commits += 1
                # add to dynamodb table
                add_item_commits(codeCommit.commits)
            except:
                print("directory already exists or is not an empty directory")
                print("directory already exists or is not an empty directory", file=sys.stderr)
        # if this is the second commit we can use the commit ID
        else:
            try:
                # Add the file using the cid (commit id) of the put file
                temp = read_table_pcid()
                parent_commit_id = temp['Items'][0]['pcid']
                # remove old pcid from table
                delete_item_pcid(parent_commit_id)
                commit_response = cclient.commit_file(parent_commit_id, repo, branch, author_name, author_email, file_path,
                                                      data_to_post, commit_message)
                parent_commit_id = commit_response['commitId']
                #Add the new parent commit id to the table
                add_item_pcid(parent_commit_id)
                #add commits to temp variable
                temp = read_table_commits()
                #delete from table to save space
                delete_item_commits(codeCommit.commits)
                #re add temp to codecommit.commits
                codeCommit.commits = temp['Items'][0]['commits']
                # Increment commits
                codeCommit.commits += 1
                #add to dynamodb table
                add_item_commits(codeCommit.commits)
            except:
                print("system error")
                print("system error", file=sys.stderr)