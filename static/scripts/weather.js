// Weather page: the city comes from the query string (the form submits to
// /weather?city=...), the lookup goes through the shared API so the
// OpenWeatherMap key stays server-side.
const WEATHER_API = "https://kiln-api.travisroth.dev/weather";

function showAnimation(status) {
  const s = (status || "").toLowerCase();
  document.querySelector(".rain").style.display = s.includes("rain") || s.includes("drizzle") ? "block" : "none";
  document.querySelector(".sun").style.display = s.includes("clear") ? "block" : "none";
  document.querySelector(".clouds").style.display = s.includes("cloud") ? "block" : "none";
}

async function lookup(city) {
  const result = document.getElementById("weather-result");
  const error = document.getElementById("weather-error");
  const loading = document.getElementById("weather-loading");
  result.hidden = true;
  error.hidden = true;
  loading.hidden = false;
  showAnimation("");

  try {
    const res = await fetch(WEATHER_API + "?city=" + encodeURIComponent(city));
    if (!res.ok) {
      document.getElementById("weather-error-title").textContent =
        res.status === 404 ? "City Not Found" : "Weather lookup is unavailable right now";
      error.hidden = false;
      return;
    }
    const w = await res.json();
    document.getElementById("weather-city").textContent = w.city;
    document.getElementById("weather-status").textContent = w.status;
    document.getElementById("weather-temp").textContent = w.temp_f.toFixed(1);
    document.getElementById("weather-feels").textContent = w.feels_like_f.toFixed(1);
    document.getElementById("weather").dataset.status = w.status;
    showAnimation(w.status);
    result.hidden = false;
  } catch (e) {
    document.getElementById("weather-error-title").textContent = "Weather lookup is unavailable right now";
    error.hidden = false;
  } finally {
    loading.hidden = true;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const city = new URLSearchParams(window.location.search).get("city");
  if (city && city.trim()) {
    document.getElementById("city").value = city;
    lookup(city.trim());
  } else {
    document.getElementById("weather-loading").hidden = true;
  }
  const burger = document.querySelector(".burger-menu");
  if (burger) burger.addEventListener("click", () => document.querySelector(".nav-links").classList.toggle("active"));
});
