import ReactMarkdown from "react-markdown"
import { useState, useEffect, useRef } from "react"
import "./App.css"

function App() {
  const [places, setPlaces] = useState([])
  const [district, setDistrict] = useState("")
  const [days, setDays] = useState(2)
  const [itinerary, setItinerary] = useState("")
  const [loading, setLoading] = useState(false)
  const [search, setSearch] = useState("")
  const [weather, setWeather] = useState(null)
  const [weatherLoading, setWeatherLoading] = useState(false)
  const [recommendations, setRecommendations] = useState([])
  const sessionId = useRef(Math.random().toString(36).substring(7))

  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/places/")
      .then(res => res.json())
      .then(data => setPlaces(data.data))
  }, [])

  function generateItinerary() {
    setLoading(true)
    fetch("http://127.0.0.1:5000/api/itinerary/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ district: district, days: days })
    })
      .then(res => res.json())
      .then(data => {
        setItinerary(data.itinerary)
        setLoading(false)
      })
  }

  function getWeather() {
    setWeatherLoading(true)
    fetch(`http://127.0.0.1:5000/api/weather/?district=${district}`)
      .then(res => res.json())
      .then(data => {
        setWeather(data.data)
        setWeatherLoading(false)
      })
  }

  function trackClick(placeId) {
    fetch("http://127.0.0.1:5000/api/recommend/click", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ place_id: placeId, session_id: sessionId.current })
    })
    .then(() => {
      fetch(`http://127.0.0.1:5000/api/recommend/?session_id=${sessionId.current}`)
        .then(res => res.json())
        .then(data => {
          console.log(data)
          setRecommendations(data.data)
        })
    })
  }

  const filteredPlaces = places.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className="container">
      <div className="header">
        <h1>Smart Tourism Jharkhand</h1>
        <p>Discover the beauty of Jharkhand</p>
      </div>

      <h2 className="section-title">Places to Visit</h2>
      <input
        type="text"
        placeholder="Search places..."
        value={search}
        onChange={e => setSearch(e.target.value)}
        className="search-input"
      />
      <div className="places-grid">
        {filteredPlaces.map(place => (
          <div className="place-card" key={place.id} onClick={() => trackClick(place.id)} style={{cursor: "pointer"}}>
            <span className={`category-badge badge-${place.category}`}>{place.category}</span>
            <h3>{place.name}</h3>
            <p className="district">{place.district}</p>
            <p>{place.description}</p>
          </div>
        ))}
      </div>

      {recommendations.length > 0 && (
        <div style={{marginBottom: "40px"}}>
          <h2 className="section-title">Recommended For You</h2>
          <div className="places-grid">
            {recommendations.map(place => (
              <div className="place-card" key={place.id}>
                <span className={`category-badge badge-${place.category}`}>{place.category}</span>
                <h3>{place.name}</h3>
                <p className="district">{place.district}</p>
                <p>{place.description}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="planner">
        <h2>Plan Your Trip</h2>
        <input
          type="text"
          placeholder="Enter district (e.g. Ranchi)"
          value={district}
          onChange={e => setDistrict(e.target.value)}
        />
        <input
          type="number"
          placeholder="Number of days"
          value={days}
          onChange={e => setDays(e.target.value)}
        />
        <button onClick={getWeather} style={{marginBottom: "15px", backgroundColor: "#1e40af"}}>
          {weatherLoading ? "Loading..." : "Check Weather"}
        </button>

        {weather && (
          <div className="weather-card">
            <h4>🌤 Weather in {weather.district}</h4>
            <p>🌡 Temperature: {weather.temperature}°C (Feels like {weather.feels_like}°C)</p>
            <p>💧 Humidity: {weather.humidity}%</p>
            <p>🌬 Wind: {weather.wind_speed} m/s</p>
            <p>☁ {weather.description}</p>
          </div>
        )}

        <button onClick={generateItinerary}>
          {loading ? "Generating..." : "Generate Itinerary"}
        </button>

        {itinerary && (
          <div className="itinerary">
            <h3>Your Itinerary</h3>
            <ReactMarkdown>{itinerary}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}

export default App