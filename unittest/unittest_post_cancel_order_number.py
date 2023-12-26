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

json_payload = """
{
"order_number": "KS9999999",
"status": "cancelled",
"processed": false,
"cancel_datetime": "2023-12-26 11:29:30 +0800",
"udt": "2023-12-26 11:29:30 +0800"
}
"""
def post_cancel_order_number(payload: Payload): 
    logging.info(payload)
    df_payload = pd.read_json(StringIO(payload), orient='index').T
    for x in ['cancel_datetime', 'udt']:
        df_payload[x] = df_payload[x].apply(lambda x: x.replace(' +0800', ''))
    print(df_payload['order_number'][0])
    breakpoint()

if __name__ == '__main__':
    post_cancel_order_number(json_payload)