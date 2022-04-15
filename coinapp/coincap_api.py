#%%
import logging
import sys
from typing import Any, Dict, List

import requests

headers = {"Authorization": "Bearer 519265c1-c502-4b70-b93f-19549435d26a"}



def get_exchange_data() -> List[Dict[str, Any]]:
    url = 'http://api.coincap.io/v2/candles?exchange=okex&interval=m5&baseId=ethereum&quoteId=bitcoin&start=1628330000000&end=1628411045604'

    try:
        r = requests.get(url,headers=headers)
    except requests.ConnectionError as ce:
        logging.error(f"There was an error with the request, {ce}")
        sys.exit(1)
    return r.json().get('data', [])

get_exchange_data()
# %%
