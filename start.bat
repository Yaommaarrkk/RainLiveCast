@echo off

chcp 65001

title RainLiveCast

echo ============================
echo 更新雷達資料
echo ============================

python backend/crawler/update_radar.py

echo ============================
echo 更新雨量資料
echo ============================

python backend/crawler/update_rainfall.py

echo ============================
echo 訓練模型
echo ============================

python -m backend.model.train

echo ============================
echo 啟動 FastAPI
echo ============================

start cmd /k "python -m uvicorn backend.api.main:app --reload"

echo ============================
echo 啟動 React
echo ============================

cd frontend

npm start