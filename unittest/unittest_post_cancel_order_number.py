import pandas as pd
from io import StringIO
import logging
from pydantic import BaseModel

class Payload(BaseModel):
    order_number: str
    status: str
    processed: bool
    cancel_datetime: str
    udt: str

def isVarInt(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False

json_payload = """
{
"order_number": "9999999",
"status": "cancelled",
"processed": false,
"cancel_datetime": "2023-12-26 11:29:30 +0800",
"udt": "2023-12-26 11:29:30 +0800"
}
"""

def post_cancel_order_number(payload: str): 
    df_payload = pd.read_json(StringIO(payload), orient='index').T
    df_payload['order_number'] = df_payload['order_number'].apply(lambda x: 'KS'+x if isVarInt(x) else x)
    breakpoint()
    # remove timezone info
    for x in ['cancel_datetime', 'udt']:
        df_payload[x] = df_payload[x].apply(lambda x: x.replace(' +0800', ''))

    # dbC.insertTableData(table_name="freshdesk_ticket_status", df=df_payload)
    logging.info(f"Order Number {df_payload['order_number'][0]}: Inserted")
    return f"Order Number {df_payload['order_number'][0]}: Inserted"

if __name__ == '__main__':
    post_cancel_order_number(json_payload)