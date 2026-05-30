import os
import requests
import numpy as np
import urllib3
import xmltodict

from datetime import datetime, timedelta

urllib3.disable_warnings()

# =========================
# API KEY
# =========================

AUTH = "CWA-07ED3858-3F36-4ED2-B98D-10C947BFF34B"

# =========================

SAVE_DIR = "backend/crawler/radar_data"

os.makedirs(SAVE_DIR, exist_ok=True)

# =========================
# 下載單張雷達
# =========================

def download_radar_xml(url):

    res = requests.get(
        url,
        verify=False
    )

    if res.status_code != 200:
        print("下載失敗")
        return None

    data = xmltodict.parse(res.text)

    content = data["cwaopendata"]["dataset"]["contents"]["content"]

    if isinstance(content, dict):
        content = content["#text"]

    vals = np.array(
        content.split(","),
        dtype=np.float32
    )

    grid = vals.reshape(881, 921)

    grid[grid < 0] = 0

    return grid

# =========================
# 更新雷達
# =========================

def update():

    now = datetime.now()

    before = now - timedelta(days=1)

    timeFrom = before.strftime("%Y-%m-%dT%H:%M:%S")

    timeTo = now.strftime("%Y-%m-%dT%H:%M:%S")

    url = (
        "https://opendata.cwa.gov.tw/historyapi/v1/getMetadata/O-A0059-001"
        f"?Authorization={AUTH}"
        "&format=JSON"
        f"&timeFrom={timeFrom}"
        f"&timeTo={timeTo}"
    )

    print("============================")
    print("更新雷達資料")
    print("============================")

    res = requests.get(
        url,
        verify=False
    )

    try:
        data = res.json()

    except Exception as e:
        print("JSON解析失敗")
        print(e)
        return

    try:
        time_list = data["dataset"]["resources"]["resource"]["data"]["time"]

    except Exception as e:
        print("資料格式錯誤")
        print(e)
        return

    for item in time_list:

        dt = item["DateTime"]

        product_url = item["ProductURL"]

        filename = datetime.fromisoformat(
            dt.replace("+08:00", "")
        ).strftime("%Y%m%d_%H%M.npy")

        save_path = os.path.join(
            SAVE_DIR,
            filename
        )

        if os.path.exists(save_path):

            print("已存在:", filename)

            continue

        try:

            grid = download_radar_xml(product_url)

            if grid is None:
                continue

            np.save(save_path, grid)

            print("已儲存:", save_path)

        except Exception as e:

            print("失敗:", filename)

            print(e)

# =========================

if __name__ == "__main__":
    update()