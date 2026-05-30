import React from "react";

function getWeatherIcon(prob) {

    if (prob < 10) {
        return "☀️";
    }

    if (prob < 40) {
        return "⛅";
    }

    if (prob < 70) {
        return "☁️";
    }

    return "🌧️";
}

export default function WeatherCard({ data }) {

    if (!data || !data.rain_probability) {

        return (
            <div
                style={{
                    marginTop: "20px"
                }}
            >
                載入中...
            </div>
        );
    }

    const rain = data.rain_probability;

    let sum = 0;

    let count = 0;

    for (let y = 0; y < rain.length; y++) {

        for (let x = 0; x < rain[y].length; x++) {

            sum += rain[y][x];

            count++;
        }
    }

    const mean_probability = Math.round(
        sum / count
    );

    const icon = getWeatherIcon(
        mean_probability
    );

    return (

        <div
            style={{
                background: "#222",
                padding: "20px",
                borderRadius: "10px",
                width: "250px",
                marginTop: "20px"
            }}
        >

            <h2>
                天氣預測
            </h2>

            <div
                style={{
                    fontSize: "64px"
                }}
            >
                {icon}
            </div>

            <h3>
                降雨機率：
                {mean_probability}%
            </h3>

        </div>
    );
}