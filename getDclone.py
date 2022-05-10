#%%
import requests
import json
from database import *
from model import StatusController
from telegram import *
from datetime import datetime
import time


url = "https://diablo2.io/dclone_api.php"

database = DcloneDB()

#%%
for i in range(3):
    print("request dclone data")
    res = requests.get(url)
    data = json.loads(res.text)

    print("process dclone data")
    for record in data:
        status = StatusController(record)
        if status.status_not_exist():
            send_notification(status)
    time.sleep(20)

# %%
print(datetime.now())
