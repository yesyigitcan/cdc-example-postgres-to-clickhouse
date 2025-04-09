import json
from kafka import KafkaConsumer
import clickhouse_connect
from datetime import datetime, timedelta

# Credentials you declared in the compose file
client = clickhouse_connect.get_client(host='clickhouse', port=8123, username='xxxx', password='xxxx')

consumer = KafkaConsumer(bootstrap_servers='kafka-broker:9092', group_id='python_cdc_consumer')
consumer.subscribe(['postgres.public.dw_currency'])


key_column_name = 'id'
for msg in consumer:
    if not msg or not msg.value:
        continue

    data = json.loads(msg.value.decode())

    schema = data['schema']
    payload = data['payload']

    operationType = payload['op']
    source = payload['source']

    del data
    if operationType == 'c':
        after = payload['after']
        after['create_time'] = datetime.fromtimestamp(after['create_time'] / 1_000_000)
        after['currency_date'] = datetime(1970, 1, 1) + timedelta(days=after['currency_date'])

        data = list(after.values())
        cols = list(after.keys())
        
        client.insert('clkdb.dw_currency_postgres', [data], column_names=cols)
        print(f"INSERT - {data}")
    elif operationType == 'd':
        id = payload['before']['id']
        client.command(f"delete from clkdb.dw_currency_postgres where id = '{id}'")
        print(f"DELETE - id: {id}")
    elif operationType == 'u':
        after = payload['after']
        after['create_time'] = datetime.fromtimestamp(after['create_time'] / 1_000_000)
        after['currency_date'] = datetime(1970, 1, 1) + timedelta(days=after['currency_date'])

        data = list(after.values())
        cols = list(after.keys())
        
        id = after['id']
        client.command(f"delete from clkdb.dw_currency_postgres where id = '{id}'")
        client.insert('clkdb.dw_currency_postgres', [data], column_names=cols)
        
        print(f"UPDATE - {data}")
