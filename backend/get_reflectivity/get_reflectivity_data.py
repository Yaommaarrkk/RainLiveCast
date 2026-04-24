import xmltodict
import requests
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os
import urllib3

urllib3.disable_warnings()

def get_one_data(url):

    res = requests.get(url, verify=False)
    res.raise_for_status()
    print("content-type:", res.headers.get("Content-Type"))
    
    data = xmltodict.parse(res.text)

    content_json = data["cwaopendata"]["dataset"]["contents"]["content"]
    dataTime_json = data["cwaopendata"]["dataset"]["datasetInfo"]["parameterSet"]["DateTime"]

    if isinstance(content_json, dict):
        content_json = content_json.get("#text", "")

    vals = np.array(content_json.split(","), dtype=float)
        
    grid = vals.reshape(881, 921)
    grid[grid < 0] = 0

    # print(grid.shape)

    # plt.imshow(grid, origin="lower", cmap="jet", vmin=0, vmax=60)
    # plt.colorbar()
    # plt.show()

    t = datetime.fromisoformat(dataTime_json.replace("+08:00", ""))

    return grid.astype(np.float32)
