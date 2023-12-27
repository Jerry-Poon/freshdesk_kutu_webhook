from typing import Union
from fastapi import FastAPI
import pandas as pd
from src import util, config
from src.util import isVarInt
import uvicorn
from io import StringIO
import google.cloud.logging
import logging

Settings = config.Settings
Payload = config.Payload
client = google.cloud.logging.Client()
client.setup_logging()

# Get connection
dbC=util.dbConnector(db_name=Settings.db_name, 
                     db_user=Settings.db_user, 
                     db_password=Settings.db_password, 
                     db_host=Settings.db_host, 
                     db_port=Settings.db_port)
db_connection = dbC.cnx
# dbC.test_query(target_table=settings.table_name)

app = FastAPI()
@app.post("/cancel_order")
def post_cancel_order_number(payload: Payload): 
    df_payload = pd.DataFrame.from_dict(payload.dict(), orient='index').T

    # Patch KS heading
    df_payload['order_number'] = df_payload['order_number'].apply(lambda x: 'KS'+x if isVarInt(x) else x)

    # remove timezone info
    for x in ['cancel_datetime', 'udt']:
        df_payload[x] = df_payload[x].apply(lambda x: x.replace(' +0800', ''))

    dbC.insertTableData(table_name="freshdesk_ticket_status", df=df_payload)
    logging.info(f"Order Number {df_payload['order_number'][0]}: Inserted")
    return f"Order Number {df_payload['order_number'][0]}: Inserted"

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, workers=2, port=8080)