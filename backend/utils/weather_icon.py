def get_weather_icon(prob):

    if prob < 10:
        return "☀️"

    elif prob < 40:
        return "🌤️"

    elif prob < 70:
        return "☁️"

    else:
        return "🌧️"