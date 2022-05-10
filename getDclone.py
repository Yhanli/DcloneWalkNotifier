#%%
import requests
import json
from database import *
from model import StatusController
from telegram import *
from datetime import datetime


url = "https://diablo2.io/dclone_api.php?sk=p&sd=d&ladder=1&hc=2&plat_pc=1&plat_switch=0&plat_playstation=0&plat_xbox=0&region=0"


#%%
res = requests.get(url)
data = json.loads(res.text)


#%%
print(datetime.now())

# %%
database = DcloneDB()
for record in data:
    status = StatusController(record)
    if status.status_not_exist():
        send_notification(status)


# %%
