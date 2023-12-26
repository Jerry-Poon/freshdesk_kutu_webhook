import pandas as pd
from io import StringIO

json_payload = """
{
"order_number": "KS9999999",
"status": "cancelled",
"processed": false,
"cancel_datetime": "2023-12-26 11:29:30 +0800",
"udt": "2023-12-26 11:29:30 +0800"
}
"""

df = pd.read_json(StringIO(json_payload), orient='index').T
for x in ['cancel_datetime', 'udt']:
    df[x] = df[x].apply(lambda x: x.replace(' +0800', ''))
print(df['order_number'][0])
breakpoint()