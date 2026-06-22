import ReactMarkdown from "react-markdown"
import { useState, useEffect } from "react"
import "./App.css"

function App() {
  const [places, setPlaces] = useState([])
  const [district, setDistrict] = useState("")
  const [days, setDays] = useState(2)
  const [itinerary, setItinerary] = useState("")
  const [loading, setLoading] = useState(false)

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

  return (
    <div className="container">
      <div className="header">
        <h1>Smart Tourism Jharkhand</h1>
        <p>Discover the beauty of Jharkhand</p>
      </div>

      <h2 style={{marginBottom: "20px"}}>Places to Visit</h2>
      <div className="places-grid">
        {places.map(place => (
          <div className="place-card" key={place.id}>
            <h3>{place.name}</h3>
            <p className="district">{place.district}</p>
            <p>{place.description}</p>
          </div>
        ))}
      </div>

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