import os

from google.cloud import bigquery


def insert(json_list, table_name):
    bq_client = bigquery.Client()
    table_id = f"disco-name-210809.myslackchannel.{table_name}"

    errors = bq_client.insert_rows_json(table_id, json_list)
    if errors != []:
        print("Encountered errors while inserting rows: {}".format(errors))
