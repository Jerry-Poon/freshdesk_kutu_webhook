from typing import Union
from fastapi import FastAPI, Request
import pandas as pd
from src import util, config
import uvicorn
import io
import google.cloud.logging
import logging

settings = config.Settings
client = google.cloud.logging.Client()
client.setup_logging()


dbC=util.dbConnector(db_name=settings.db_name, 
                     db_user=settings.db_user, 
                     db_password=settings.db_password, 
                     db_host=settings.db_host, 
                     db_port=settings.db_port)
db_connection = dbC.cnx
dbC.test_query(target_table=settings.table_name)

app = FastAPI()
@app.post("/cancel_order")
def post_cancel_order_number(payload: Request):
    logging.info(payload)
    df_payload = pd.read_json(io.StringIO(payload), orient='index').T

    # remove timezone info
    for x in ['cancel_datetime', 'udt']:
        df_payload[x] = df_payload[x].apply(lambda x: x.replace(' +0800', ''))

    dbC.insertTableData(table_name="freshdesk_ticket_status", df=df_payload)
    logging.info(f"Order Number {df_payload['order_number'][0]}: Inserted")
    return f"Order Number {df_payload['order_number'][0]}: Inserted"

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, workers=2, port=8080)