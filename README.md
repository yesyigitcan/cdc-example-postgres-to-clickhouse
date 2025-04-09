# A CDC (Change Data Capture) Example
Debezium is an open source project that provides a low latency data streaming platform for change data capture (CDC).

This repository contains a demonstration of the CDC concept that aims to create the environment on a Docker platform.

Documentation about the clickhouse client on python can be found <a href="https://clickhouse.com/docs/integrations/python">here</a>.

## Project Environment

In order to have the setup required for this project, you need to have a Docker installed in your computer. It is mandatory to create Docker containers using the compose file inside the project repository.

The compose file generates multiple containers which the technologies used by may be replaced with any other alternative:

-   PostgreSQL (Source Database)
-   Clickhouse (Target Data Warehouse)
-   Debezium Connect (CDC Tool)
-   Debezium UI (User-Interface for CDC Tool)
-   Apache Kafka (Streams between Debezium and a Python Consumer)
-   Apache Spark - Master (Operates the sync operation, it may be replaced with a basic python server)
-   Apache Spark - Worker

## Python Packages

- json
- <a href="https://pypi.org/project/kafka-python/">kafka-python</a>
- <a href="https://pypi.org/project/clickhouse-connect/">clickhouse-connect</a>

## Docker Environment

Since the technologies used for the scenario imitated in the Docker containers, it is important to keep the data used for the operation persistent. For this reason, it is important to keep meta data folders for each container as data volumes on Docker.

Also, the containers have to communicate each other for some operations like database connection etc. So a common network is declared to have open communication between the containers.

## Scenario

There is a table in a source database (PostgreSQL) which stores currency data. The data team has been requested to create a copy of this table in an existing centralized data warehouse (Clickhouse). Also, for any change like INSERT, DELETE, UPDATE on the source table (PostgreSQL), same change should be applied to the copy of this table (Clickhouse).

Debezium server listens for a change on the source table by its Postgres connector. Whenever a CRUD operation is applied to the source table, Debezium catches the change and push a message to the Kafka Broker.

The message in the queue gets consumed by a consumer client. It identifies the transaction (INSERT, DELETE, UPDATE) and applies it to the copy table in the data warehouse.

With all this effort, both tables serve the same data representation.

## Operations

* Create the Docker containers using the compose file

      docker-compose up -d

* Create a Postgre connector in Debezium UI (You can also push configuration file directly into the container)

  ![image](https://github.com/user-attachments/assets/48894397-f084-4d6d-8e90-1b20e2001650)

* Create the tables for both source and target (SQL scripts located in the folder <b><a href="https://github.com/yesyigitcan/cdc-example-postgres-to-clickhouse/tree/main/sql">SQL</a></b>)

* Execute the Python consumer script which is located in the folder <b><a href="https://github.com/yesyigitcan/cdc-example-postgres-to-clickhouse/tree/main/cdc">CDC</a></b>

## Debezium Change Log

<b>"op": "c"</b> stands for <b>INSERT</b> operation.

<b>"op": "u"</b> stands for <b>UPDATE</b> operation.

<b>"op": "d"</b> stands for <b>DELETE</b> operation.


    {
        "schema": {
            "type": "struct",
            "fields": [
                {
                    "type": "struct",
                    "fields": [
                        {
                            "type": "int64",
                            "optional": true,
                            "name": "io.debezium.time.MicroTimestamp",
                            "version": 1,
                            "default": 0,
                            "field": "create_time"
                        },
                        {
                            "type": "int32",
                            "optional": true,
                            "name": "io.debezium.time.Date",
                            "version": 1,
                            "field": "currency_date"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "field": "currency_code"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "field": "currency_name"
                        },
                        {
                            "type": "double",
                            "optional": true,
                            "field": "value_to_try"
                        }
                    ],
                    "optional": true,
                    "name": "postgres.public.dw_currency.Value",
                    "field": "before"
                },
                {
                    "type": "struct",
                    "fields": [
                        {
                            "type": "int64",
                            "optional": true,
                            "name": "io.debezium.time.MicroTimestamp",
                            "version": 1,
                            "default": 0,
                            "field": "create_time"
                        },
                        {
                            "type": "int32",
                            "optional": true,
                            "name": "io.debezium.time.Date",
                            "version": 1,
                            "field": "currency_date"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "field": "currency_code"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "field": "currency_name"
                        },
                        {
                            "type": "double",
                            "optional": true,
                            "field": "value_to_try"
                        }
                    ],
                    "optional": true,
                    "name": "postgres.public.dw_currency.Value",
                    "field": "after"
                },
                {
                    "type": "struct",
                    "fields": [
                        {
                            "type": "string",
                            "optional": false,
                            "field": "version"
                        },
                        {
                            "type": "string",
                            "optional": false,
                            "field": "connector"
                        },
                        {
                            "type": "string",
                            "optional": false,
                            "field": "name"
                        },
                        {
                            "type": "int64",
                            "optional": false,
                            "field": "ts_ms"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "name": "io.debezium.data.Enum",
                            "version": 1,
                            "parameters": {
                                "allowed": "true,last,false,incremental"
                            },
                            "default": "false",
                            "field": "snapshot"
                        },
                        {
                            "type": "string",
                            "optional": false,
                            "field": "db"
                        },
                        {
                            "type": "string",
                            "optional": true,
                            "field": "sequence"
                        },
                        {
                            "type": "string",
                            "optional": false,
                            "field": "schema"
                        },
                        {
                            "type": "string",
                            "optional": false,
                            "field": "table"
                        },
                        {
                            "type": "int64",
                            "optional": true,
                            "field": "txId"
                        },
                        {
                            "type": "int64",
                            "optional": true,
                            "field": "lsn"
                        },
                        {
                            "type": "int64",
                            "optional": true,
                            "field": "xmin"
                        }
                    ],
                    "optional": false,
                    "name": "io.debezium.connector.postgresql.Source",
                    "field": "source"
                },
                {
                    "type": "string",
                    "optional": false,
                    "field": "op"
                },
                {
                    "type": "int64",
                    "optional": true,
                    "field": "ts_ms"
                },
                {
                    "type": "struct",
                    "fields": [
                        {
                            "type": "string",
                            "optional": false,
                            "field": "id"
                        },
                        {
                            "type": "int64",
                            "optional": false,
                            "field": "total_order"
                        },
                        {
                            "type": "int64",
                            "optional": false,
                            "field": "data_collection_order"
                        }
                    ],
                    "optional": true,
                    "name": "event.block",
                    "version": 1,
                    "field": "transaction"
                }
            ],
            "optional": false,
            "name": "postgres.public.dw_currency.Envelope",
            "version": 1
        },
        "payload": {
            "before": null,
            "after": {
                "create_time": 1744118880481291,
                "currency_date": 20186,
                "currency_code": "DUM",
                "currency_name": "DUM Dummy",
                "value_to_try": -3.0
            },
            "source": {
                "version": "2.4.0.Final",
                "connector": "postgresql",
                "name": "postgres",
                "ts_ms": 1744118880481,
                "snapshot": "false",
                "db": "debezium",
                "sequence": "[\"23081120\",\"23081176\"]",
                "schema": "public",
                "table": "dw_currency",
                "txId": 504,
                "lsn": 23081176,
                "xmin": null
            },
            "op": "c",
            "ts_ms": 1744118880856,
            "transaction": null
        }
    }

## Consumer Log

![image](https://github.com/user-attachments/assets/ae682b25-447e-4fe9-8c98-0352752a7f0f)

## Source Screenshot

![image](https://github.com/user-attachments/assets/a5b5f505-8490-45f1-81b8-aceefb6d9986)

## Target Screenshot

![image](https://github.com/user-attachments/assets/e5d230d3-9692-4439-8a9b-9757722217d1)


