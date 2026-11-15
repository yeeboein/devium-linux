// Devium widget pack: fetching data and finding where you are.
.pragma library

function getJson(url, done) {
    var x = new XMLHttpRequest();
    x.onreadystatechange = function () {
        if (x.readyState !== XMLHttpRequest.DONE) return;
        if (x.status >= 200 && x.status < 300) {
            try { done(JSON.parse(x.responseText), ""); } catch (e) { done(null, "Bad answer from the server"); }
        } else {
            done(null, x.status === 0 ? "No internet" : "Server error " + x.status);
        }
    };
    x.open("GET", url);
    x.setRequestHeader("User-Agent", "Devium-widgets/1.0");
    x.send();
}

// Where are you? A place name typed in the widget settings, or your approximate location from your
// IP address (city level, looked up at ipapi.co, falling back to ipwho.is). done({lat, lon, name}, error)
function locate(place, done) {
    if (place && place.trim().length) {
        getJson("https://geocoding-api.open-meteo.com/v1/search?count=1&language=en&name=" + encodeURIComponent(place.trim()),
            function (j, err) {
                if (!j || !j.results || !j.results.length) { done(null, err || "Couldn't find \"" + place + "\""); return; }
                var r = j.results[0];
                done({ lat: r.latitude, lon: r.longitude, name: r.name + (r.country_code ? ", " + r.country_code : "") }, "");
            });
        return;
    }
    getJson("https://ipapi.co/json/", function (j, err) {
        if (j && j.latitude !== undefined) {
            done({ lat: j.latitude, lon: j.longitude, name: j.city || j.region || j.country_name || "Your area" }, "");
            return;
        }
        getJson("https://ipwho.is/", function (k, err2) {
            if (k && k.success !== false && k.latitude !== undefined)
                done({ lat: k.latitude, lon: k.longitude, name: k.city || k.country || "Your area" }, "");
            else
                done(null, "Couldn't find your location. Type a place in the widget settings.");
        });
    });
}

var COMPASS = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
function compass(deg) { return deg === null || deg === undefined ? "" : COMPASS[Math.round(((deg % 360) + 360) % 360 / 22.5) % 16]; }
// an arrow pointing where the wind / waves are GOING (they're reported as where they come FROM)
function arrow(deg) { var a = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]; return deg === null || deg === undefined ? "" : a[Math.round(((deg % 360) + 360) % 360 / 45) % 8]; }

// WMO weather codes (Open-Meteo) -> [emoji by day, emoji at night, words]
function weather(code, day) {
    var t = {
        0: ["☀️", "🌙", "Clear"], 1: ["🌤️", "🌙", "Mostly clear"], 2: ["⛅", "☁️", "Partly cloudy"], 3: ["☁️", "☁️", "Cloudy"],
        45: ["🌫️", "🌫️", "Fog"], 48: ["🌫️", "🌫️", "Icy fog"],
        51: ["🌦️", "🌧️", "Light drizzle"], 53: ["🌦️", "🌧️", "Drizzle"], 55: ["🌧️", "🌧️", "Heavy drizzle"],
        56: ["🌧️", "🌧️", "Freezing drizzle"], 57: ["🌧️", "🌧️", "Freezing drizzle"],
        61: ["🌦️", "🌧️", "Light rain"], 63: ["🌧️", "🌧️", "Rain"], 65: ["🌧️", "🌧️", "Heavy rain"],
        66: ["🌧️", "🌧️", "Freezing rain"], 67: ["🌧️", "🌧️", "Freezing rain"],
        71: ["🌨️", "🌨️", "Light snow"], 73: ["🌨️", "🌨️", "Snow"], 75: ["❄️", "❄️", "Heavy snow"], 77: ["🌨️", "🌨️", "Snow grains"],
        80: ["🌦️", "🌧️", "Showers"], 81: ["🌧️", "🌧️", "Showers"], 82: ["⛈️", "⛈️", "Heavy showers"],
        85: ["🌨️", "🌨️", "Snow showers"], 86: ["❄️", "❄️", "Snow showers"],
        95: ["⛈️", "⛈️", "Thunderstorm"], 96: ["⛈️", "⛈️", "Thunderstorm, hail"], 99: ["⛈️", "⛈️", "Thunderstorm, hail"]
    };
    var w = t[code] || ["🌡️", "🌡️", "—"];
    return { icon: day === 0 ? w[1] : w[0], text: w[2] };
}
