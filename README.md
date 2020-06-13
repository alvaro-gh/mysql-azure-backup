# MySQL backup (dump) and sync to Azure Blob Storage

This is a simple service that uses mysqldump to dump a list of databases and then uploads the files to an Azure Container (Blob Storage). This is a work in progress, currently backups are performed **every hour at minute zero**.<br>

Based on [Python's official Docker image (tag: 3.8.3-alpine)](https://hub.docker.com/_/python).

## Requirements

- An Azure subscription with a Storage Account already setup and an existing container named `mysql` on it. See [Microsoft's official documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) for indications. You need the `AZURE_STORAGE_CONNECTION_STRING` for the Docker container.

- A MySQL Server with read access to the databases you want to back up, I strongly suggest using read only grants.

- Docker.

## Environment variables

- `MYSQL_HOST`: the MySQL server you want to back up, defaults to `127.0.0.1`.

- `MYSQL_PORT`: the MySQL server port, defaults to `3306`.

- `MYSQL_DATABASES`: list of databases you want to back up. This is parsed as a list, example: `db1 db2 db3`, so, for example `MYSQL_DATABASES='db1 db2 db3'`.

- `MYSQL_USER`: MySQL user to connect to MySQL server.

- `MYSQL_PASSWORD`: MySQL user password to connect to MySQL.

- `AZURE_STORAGE_CONNECTION_STRING`: string used to connect to Azure's Blob Storage, please read [Microsoft's official documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) on the topic.

## How to

```
$ docker pull mdlee/mysql-azure-backup

# In this case I have AZURE_STORAGE_CONNECTION_STRING already setup in my environment
$ docker run -it --rm -e "MYSQL_DATABASES='testing'" -e "AZURE_STORAGE_CONNECTION_STRING=$AZURE_STORAGE_CONNECTION_STRING" -e 'MYSQL_USER=mysql' -e 'MYSQL_PASSWORD=mySecret1234' mysql-backup
```


## TODO

- Use unix socket to connect to MySQL.

- Create Storage Account/Container if required.

- Allow customizable schedule.

- Use Docker secrets for variables.
