// Devium widget pack: weather from Open-Meteo (free, no account).
.pragma library
.import "Net.js" as Net

function url(lat, lon, imperial) {
    return "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon +
        "&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m,is_day" +
        "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset,uv_index_max" +
        "&timezone=auto&forecast_days=5" + (imperial ? "&temperature_unit=fahrenheit&wind_speed_unit=mph" : "");
}

var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

function model(j, loc, imperial) {
    if (!j || !j.current) return { ok: false, place: loc ? loc.name : "", error: "No weather data" };
    var c = j.current, d = j.daily || {};
    var w = Net.weather(c.weather_code, c.is_day);
    var days = [];
    for (var i = 0; i < (d.time || []).length; i++) {
        var dt = new Date(d.time[i] + "T12:00");
        days.push({ day: i === 0 ? "Today" : DAYS[dt.getDay()], icon: Net.weather(d.weather_code[i], 1).icon,
                    hi: Math.round(d.temperature_2m_max[i]) + "°", lo: Math.round(d.temperature_2m_min[i]) + "°",
                    rain: d.precipitation_probability_max ? d.precipitation_probability_max[i] : null });
    }
    return {
        ok: true, place: loc.name, icon: w.icon, text: w.text,
        temp: Math.round(c.temperature_2m) + "°", feels: "Feels " + Math.round(c.apparent_temperature) + "°",
        wind: Math.round(c.wind_speed_10m) + (imperial ? " mph" : " km/h"), humidity: c.relative_humidity_2m + "%",
        uv: d.uv_index_max ? Math.round(d.uv_index_max[0]) : null,
        sun: d.sunrise ? "☀ " + d.sunrise[0].substr(11, 5) + "  ☾ " + d.sunset[0].substr(11, 5) : "",
        days: days
    };
}

function load(place, imperial, done) {
    Net.locate(place, function (loc, err) {
        if (!loc) { done({ ok: false, place: "", error: err }); return; }
        Net.getJson(url(loc.lat, loc.lon, imperial), function (j, e) {
            done(j ? model(j, loc, imperial) : { ok: false, place: loc.name, error: e });
        });
    });
}
