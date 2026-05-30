import React, { useEffect, useState } from "react";

import axios from "axios";

import WeatherCard from "./components/WeatherCard";

function App() {

    const [weatherData, setWeatherData] = useState(null);

    const [viewMode, setViewMode] = useState("rain");

    // =========================

    useEffect(() => {

        fetchData();

        const timer = setInterval(() => {

            fetchData();

        }, 60000);

        return () => clearInterval(timer);

    }, []);

    // =========================

    const fetchData = async () => {

        try {

            const res = await axios.get(
                "http://127.0.0.1:8000/predict"
            );

            console.log(res.data);

            setWeatherData(res.data);

        } catch (err) {

            console.error(err);
        }
    };

    // =========================

    const renderMap = () => {

        if (!weatherData) {

            return (
                <div
                    style={{
                        color: "white",
                        marginTop: "20px"
                    }}
                >
                    載入中...
                </div>
            );
        }

        const data = viewMode === "radar"
            ? weatherData.radar
            : weatherData.rain_probability;

        return (

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: `repeat(${data[0].length}, 4px)`,
                    gap: "1px",
                    marginTop: "20px"
                }}
            >

                {data.flat().map((v, idx) => {

                    let color = "#000";

                    if (viewMode === "radar") {

                        if (v > 45) color = "red";
                        else if (v > 30) color = "orange";
                        else if (v > 15) color = "yellow";
                        else if (v > 5) color = "green";
                        else color = "#001122";

                    } else {

                        if (v > 70) color = "#0044ff";
                        else if (v > 40) color = "#33aaff";
                        else if (v > 10) color = "#88ddff";
                        else color = "#eeeeee";
                    }

                    return (

                        <div
                            key={idx}
                            style={{
                                width: "4px",
                                height: "4px",
                                background: color
                            }}
                        />

                    );
                })}

            </div>
        );
    };

    // =========================

    return (

        <div
            style={{
                background: "#111",
                minHeight: "100vh",
                padding: "20px",
                color: "white"
            }}
        >

            <h1>
                RainLiveCast
            </h1>

            <div
                style={{
                    marginTop: "20px"
                }}
            >

                <button
                    onClick={() => setViewMode("radar")}
                    style={{
                        marginRight: "10px"
                    }}
                >
                    雷達迴波圖
                </button>

                <button
                    onClick={() => setViewMode("rain")}
                >
                    降雨機率圖
                </button>

            </div>

            {renderMap()}

            <WeatherCard
                data={weatherData}
            />

        </div>
    );
}

export default App;