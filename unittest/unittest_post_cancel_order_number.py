import pandas as pd
from io import StringIO

json_payload = """
{"order_number": "KS123455",   "status": "cancelled",   "processed": true,   "cancel_datetime": "2023-12-16 16:15:04" }
"""

df = pd.read_json(StringIO(json_payload), orient='index').T
print(df['order_number'][0])
breakpoint()