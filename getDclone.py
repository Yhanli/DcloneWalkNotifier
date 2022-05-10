#%%
import requests
import json
from database import *
from model import StatusController
from telegram import *
from datetime import datetime
import time


url = "https://diablo2.io/dclone_api.php?sk=p&sd=d&ladder=1&hc=2&plat_pc=1&plat_switch=0&plat_playstation=0&plat_xbox=0&region=0"

database = DcloneDB()

#%%
for i in range(3):
    res = requests.get(url)
    data = json.loads(res.text)

    for record in data:
        status = StatusController(record)
        if status.status_not_exist():
            send_notification(status)
    time.sleep(20)

# %%
print(datetime.now())
