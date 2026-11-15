// Devium widget pack: sea conditions from Open-Meteo's free Marine API (no account needed).
.pragma library
.import "Net.js" as Net

function marineUrl(lat, lon) {
    return "https://marine-api.open-meteo.com/v1/marine?latitude=" + lat + "&longitude=" + lon +
        "&current=wave_height,wave_direction,wave_period,swell_wave_height,swell_wave_period,swell_wave_direction,sea_surface_temperature" +
        "&hourly=wave_height,sea_level_height_msl&timezone=auto&forecast_days=2";
}
function windUrl(lat, lon) {
    return "https://api.open-meteo.com/v1/forecast?latitude=" + lat + "&longitude=" + lon +
        "&current=wind_speed_10m,wind_direction_10m,wind_gusts_10m,temperature_2m,is_day&daily=sunrise,sunset" +
        "&wind_speed_unit=kmh&timezone=auto&forecast_days=1";
}

function hhmm(iso) { return iso ? iso.substr(11, 5) : ""; }

// How the sea feels, from wave height (m) and gusts (km/h)
function rating(h, gust) {
    var r = h < 0.5 ? ["Calm", "good"] : h < 1.25 ? ["Slight", "good"] : h < 2.5 ? ["Moderate", "warn"] :
            h < 4 ? ["Rough", "bad"] : ["Very rough", "bad"];
    if (gust >= 62) r = ["Gale", "bad"];
    else if (gust >= 45 && r[1] === "good") r = [r[0] + ", windy", "warn"];
    return { text: r[0], level: r[1] };
}

// Turn the two Open-Meteo answers into what the widget shows.
function model(m, w, loc, imperial) {
    var c = m && m.current ? m.current : {};
    if (c.wave_height === null || c.wave_height === undefined)
        return { ok: false, place: loc ? loc.name : "", error: "No sea data for " + (loc ? loc.name : "here") +
                 ". Type a beach or harbour in the widget settings." };
    var ft = imperial ? 3.28084 : 1, hu = imperial ? " ft" : " m";
    var wc = w && w.current ? w.current : {};
    var knots = wc.wind_speed_10m !== undefined ? wc.wind_speed_10m / 1.852 : null;
    var res = {
        ok: true, place: loc.name,
        waves: (c.wave_height * ft).toFixed(1) + hu,
        period: c.wave_period ? Math.round(c.wave_period) + " s" : "",
        waveDir: Net.compass(c.wave_direction), waveArrow: Net.arrow(c.wave_direction),
        swell: c.swell_wave_height !== null && c.swell_wave_height !== undefined ?
               (c.swell_wave_height * ft).toFixed(1) + hu + (c.swell_wave_period ? " @ " + Math.round(c.swell_wave_period) + " s" : "") : "–",
        swellDir: Net.compass(c.swell_wave_direction),
        water: c.sea_surface_temperature === null || c.sea_surface_temperature === undefined ? "–" :
               (imperial ? Math.round(c.sea_surface_temperature * 9 / 5 + 32) + "°F" : c.sea_surface_temperature.toFixed(1) + "°C"),
        wind: knots === null ? "–" : Math.round(knots) + " kn",
        windSub: knots === null ? "" : "from " + Net.compass(wc.wind_direction_10m) + (wc.wind_gusts_10m ? " · gusts " + Math.round(wc.wind_gusts_10m / 1.852) + " kn" : ""),
        windArrow: Net.arrow(wc.wind_direction_10m),
        sun: w && w.daily && w.daily.sunrise ? "☀ " + hhmm(w.daily.sunrise[0]) + "  ☾ " + hhmm(w.daily.sunset[0]) : "",
        rating: rating(c.wave_height, wc.wind_gusts_10m || 0),
        tide: null, tideText: "", curve: [], nowAt: 0
    };
    // Tide: the sea level over the next 24 hours, and the next high and low water
    var hr = m.hourly || {};
    var lv = hr.sea_level_height_msl || [], times = hr.time || [];
    if (lv.length > 3 && lv.some(function (v) { return v !== null; })) {
        var now = c.time ? c.time.substr(0, 13) : "";
        var i0 = 0;
        for (var i = 0; i < times.length; i++) if (times[i].substr(0, 13) === now) { i0 = i; break; }
        var start = Math.max(0, i0 - 3), end = Math.min(lv.length, i0 + 22);
        res.curve = lv.slice(start, end).map(function (v) { return v === null ? 0 : v; });
        res.nowAt = (i0 - start) / Math.max(1, res.curve.length - 1);
        var rising = lv[Math.min(lv.length - 1, i0 + 1)] > lv[i0];
        var next = [];
        for (var k = i0 + 1; k < Math.min(lv.length - 1, i0 + 26) && next.length < 2; k++) {
            if (lv[k] === null) continue;
            if (lv[k] > lv[k - 1] && lv[k] >= lv[k + 1]) next.push("high " + hhmm(times[k]));
            if (lv[k] < lv[k - 1] && lv[k] <= lv[k + 1]) next.push("low " + hhmm(times[k]));
        }
        res.tide = rising ? "rising" : "falling";
        res.tideText = "Tide " + res.tide + (next.length ? " · " + next.join(", ") : "");
    }
    return res;
}

// Fetch everything: done(model)
function load(place, imperial, done) {
    Net.locate(place, function (loc, err) {
        if (!loc) { done({ ok: false, place: "", error: err }); return; }
        Net.getJson(marineUrl(loc.lat, loc.lon), function (m, e1) {
            if (!m) { done({ ok: false, place: loc.name, error: e1 }); return; }
            Net.getJson(windUrl(loc.lat, loc.lon), function (w, e2) {
                done(model(m, w, loc, imperial));
            });
        });
    });
}
