import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import urllib.parse
import urllib3
from get_reflectivity_data import get_one_data

urllib3.disable_warnings()

save_dir = "reflectivity_pic"
os.makedirs(save_dir, exist_ok=True)

authorization_key = "CWA-6DD5E231-E295-442B-911C-09E75C0EC2BC" # API授權碼

def get_history_idList():

    url = f"https://opendata.cwa.gov.tw/historyapi/v1/getDataId/?Authorization={authorization_key}" # 查API編號
    res = requests.get(url, verify=False)
    print(res.status_code)
    print(res.json())

def get_history_data(timeFrom, timeTo):
    timeFrom_enc = urllib.parse.quote(timeFrom)
    timeTo_enc = urllib.parse.quote(timeTo)

    url = ( # 查歷史雷達迴波data
        "https://opendata.cwa.gov.tw/historyapi/v1/getMetadata/O-A0059-001"
        f"?Authorization={authorization_key}"
        f"&format=JSON"
        f"&timeFrom={timeFrom_enc}"
        f"&timeTo={timeTo_enc}"
    )
    res = requests.get(url, verify=False)
    data = res.json()

    time_list = data["dataset"]["resources"]["resource"]["data"]["time"]
    for item in time_list:
        dt = item["DateTime"]
        url = item["ProductURL"]

        print("下載:", dt)

        grid = get_one_data(url)

        t = datetime.fromisoformat(dt.replace("+08:00", ""))

        filename = t.strftime(f"{save_dir}/%Y%m%d_%H%M.npy")

        np.save(filename, grid) # 以後使用np.load

        print("已存至:", os.path.abspath(filename))
        

get_history_idList()
get_history_data("2026-04-24T15:00:00", "2026-04-24T17:00:00")