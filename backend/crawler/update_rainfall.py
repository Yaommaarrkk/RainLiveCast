import requests
import json
import urllib3
import os

urllib3.disable_warnings()

API_KEY = "CWA-07ED3858-3F36-4ED2-B98D-10C947BFF34B"

SAVE_PATH = "backend/crawler/rainfall_data.json"

# =========================

def update_rainfall():

    print("=" * 28)
    print("更新雨量資料")
    print("=" * 28)

    url = (
        "https://opendata.cwa.gov.tw/api/v1/rest/datastore/"
        f"O-A0002-001?Authorization={API_KEY}&format=JSON"
    )

    try:

        res = requests.get(
            url,
            verify=False,
            timeout=30
        )

        print("status:", res.status_code)

        data = res.json()

        # DEBUG
        # print(json.dumps(data, indent=2, ensure_ascii=False))

        records = data.get("records", {})

        stations = records.get("Station", [])

        rainfall_list = []

        for station in stations:

            try:

                station_name = station.get(
                    "StationName",
                    "未知"
                )

                geo = station.get(
                    "GeoInfo",
                    {}
                )

                coordinates = geo.get(
                    "Coordinates",
                    []
                )

                lat = None
                lon = None

                if len(coordinates) > 0:

                    for c in coordinates:

                        if c.get("CoordinateName") == "TWD67":

                            lat = c.get("StationLatitude")
                            lon = c.get("StationLongitude")

                weather = station.get(
                    "WeatherElement",
                    {}
                )

                rain = weather.get(
                    "Now",
                    {}
                )

                rain_value = rain.get(
                    "Precipitation",
                    0
                )

                if rain_value in ["-998.00", "-999.00"]:

                    rain_value = 0

                rainfall_list.append({

                    "station": station_name,

                    "lat": lat,

                    "lon": lon,

                    "rainfall": float(rain_value)

                })

            except Exception as e:

                print("單站解析失敗:", e)

        # 儲存
        with open(
            SAVE_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                rainfall_list,
                f,
                ensure_ascii=False,
                indent=2
            )

        print("雨量站數:", len(rainfall_list))

        print("已儲存:", SAVE_PATH)

    except Exception as e:

        print("雨量資料解析失敗")

        print(e)

# =========================

if __name__ == "__main__":

    update_rainfall()