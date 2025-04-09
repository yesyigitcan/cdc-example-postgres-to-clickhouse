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
-   Apache Kafka (Streams between Debezium and a Consumer)
-   Apache Spark Master (Operates the sync operation, it may be replaced with a basic python server)
-   Apache Spark Worker

## Docker Environment

Since the technologies used for the scenario imitated in the Docker containers, it is important to keep the data used for the operation persistent. For this reason, it is important to keep meta data folders for each container as data volumes on Docker.

Also, the containers have to communicate each other for some operations like database connection etc. So a common network is declared to have open communication between the containers.

## Scenario

There is a table in a source database (PostgreSQL) which stores currency data. The data team has been requested to create a copy of this table in an existing centralized data warehouse (Clickhouse). Also, for any change like INSERT, DELETE, UPDATE on the source table (PostgreSQL), same change should be applied to the copy of this table (Clickhouse).

Debezium server listens for a change on the source table by its Postgres connector. Whenever a CRUD operation is applied to the source table, Debezium catches the change and push a message to the Kafka Broker.

The message in the queue gets consumed by a consumer client. It identifies the transaction (INSERT, DELETE, UPDATE) and applies it to the copy table in the data warehouse.

With all this effort, both tables serve the same data representation.
