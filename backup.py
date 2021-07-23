import datetime
import logging
import os
import requests
import schedule
import subprocess
import sys
import time
import uuid

# from azure.storage.blob._models import StorageErrorException
from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Environment variables
## MySQL
db_host = os.getenv('MYSQL_HOST', '127.0.0.1')
db_port = os.getenv('MYSQL_PORT', '3306')
db_name = os.getenv('MYSQL_DATABASES', None)
db_user = os.getenv('MYSQL_USER', None)
db_pass = os.getenv('MYSQL_PASSWORD', None)
## Azure
az_st_conn_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING', None)
slack_webhook = os.getenv('SLACK_WEBHOOK', None)

def check_envars():
    logging.info('Checking environment variables')
    if db_name is None:
        logging.error('MYSQL_DATABASES variable is not set.')
        sys.exit(1)
    if db_user is None:
        logging.error('MYSQL_USER variable is not set.')
        sys.exit(1)
    if db_pass is None:
        logging.error('MYSQL_PASSWORD variable is not set.')
        sys.exit(1)
    if az_st_conn_string is None:
        logging.error('AZURE_STORAGE_CONNECTION_STRING variable is not set')
        sys.exit(1)

def mysqldump(db):
    dump_command = 'mysqldump --single-transaction -u' + db_user + ' -p' + db_pass + ' -h' + db_host + ' -P' + db_port + ' ' + db
    dump_file = '/tmp/' + db + '-' + datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S') + '.sql'

    logging.info('Running mysqldump for ' + db)
    try:
        p = subprocess.check_output(dump_command, shell=True)
        logging.info('Writing dump to ' + dump_file)
        with open(dump_file, 'wb') as f:
            f.write(p)
        sync(dump_file)
    except subprocess.CalledProcessError as ex:
        logging.error('Error while running mysqldump: ' + ex.output.decode('utf-8'))
        slackit('MySQL Backup process has crashed.')

def sync(file):
    blob_service_client = BlobServiceClient.from_connection_string(az_st_conn_string)
    blob_client = blob_service_client.get_blob_client('mysqlbackup', blob=os.path.basename(file).replace("'", ""))

    logging.info('Uploading' + file + ' to Azure on container mysqlbackup')
    try:
        with open(file, 'rb') as f:
            blob_client.upload_blob(f)
            if os.path.exists(file):
                os.remove(file)
            else:
                logging.error('Unable to remove file ' + file)
    except AzureError as ex:
        logging.error('Error while uploading the file to Azure, error code: ' + str(ex.error_code))

def backup():
    logging.info('Starting backups...')
    for db in db_name.split():
        logging.info('Backing up ' + db)
        mysqldump(db)
    slackit('MySQL Backup process has finished.')

def slackit(message):
    r = requests.post(slack_webhook, json={"text":message})

logging.info('MySQL backup service started on ' + str(datetime.datetime.now()))
# Batman begins
check_envars()

# Schedule definition
schedule.every().hour.at(':00').do(backup)

while True:
    schedule.run_pending()
    time.sleep(1)
