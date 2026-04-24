import requests

url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0058-004?Authorization=CWA-6DD5E231-E295-442B-911C-09E75C0EC2BC&downloadType=WEB&format=JSON"

res = requests.get(url, verify=False)
data = res.json()

img_url = data["cwaopendata"]["dataset"]["resource"]["ProductURL"]

print(img_url)

img = requests.get(img_url).content

with open("get_reflectivity_pic.png", "wb") as f:
    f.write(img)