# 🏔️ Smart Tourism Jharkhand

> An AI-powered full-stack travel planning platform for Jharkhand, India — combining LLM-based itinerary generation, ML recommendations, real-time weather, and Redis caching.

**Live Demo:** [smart-tourism-jharkhand.vercel.app](https://smart-tourism-jharkhand.vercel.app)  
**Backend API:** [smart-tourism-jharkhand.onrender.com](https://smart-tourism-jharkhand.onrender.com)  
**GitHub:** [github.com/aryan7radhe/smart-tourism-jharkhand](https://github.com/aryan7radhe/smart-tourism-jharkhand)

---

## ✨ Features

### 🤖 AI Trip Planner
- Powered by **Groq (Llama 3.3-70B)**
- Generates route-optimized, day-by-day itineraries
- Groups nearby places on the same day to minimize travel time
- Includes realistic opening hours and travel tips for each slot
- Morning → temples/waterfalls, Afternoon → museums/zoos, Evening → markets/hills

### 🧠 ML Recommendation System
- **Content-based filtering** using TF-IDF vectorization + cosine similarity (scikit-learn)
- Tracks user click behavior via MongoDB Atlas
- Recommends similar places based on browsing pattern
- Session-based tracking without requiring user login

### 🌤️ Live Weather Integration
- Real-time weather via **OpenWeatherMap API**
- Shows temperature, humidity, wind speed, and conditions
- Cached with Redis for 1 hour to reduce API calls

### ⚡ Redis Caching
- **Upstash Redis** for serverless caching
- Itinerary responses cached for 24 hours
- Weather cached for 1 hour
- Reduces Groq API calls by ~80% for repeated requests

### 🔍 Search & Filter
- Real-time search by place name
- Category badges (Waterfall, Wildlife, Religious, Nature)
- Instant filtering without page reload

### 📊 Visual Itinerary Timeline
- Animated flashcard-style timeline
- Morning 🌅 / Afternoon ☀️ / Evening 🌙 slots
- Travel tips highlighted in orange
- Reason for timing shown for each activity

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|-----------|---------|
| Flask | REST API framework |
| Groq (Llama 3.3-70B) | AI itinerary generation |
| Scikit-learn | TF-IDF + cosine similarity for recommendations |
| MongoDB Atlas | Click tracking and user behavior storage |
| Upstash Redis | Response caching |
| OpenWeatherMap API | Live weather data |
| Gunicorn | Production WSGI server |

### Frontend
| Technology | Purpose |
|-----------|---------|
| React + Vite | UI framework |
| useState / useEffect / useRef | State management |
| react-markdown | Markdown rendering |
| CSS3 Animations | Timeline flashcard UI |

### DevOps
| Technology | Purpose |
|-----------|---------|
| Render | Backend deployment |
| Vercel | Frontend deployment |
| GitHub | Version control + CI/CD |

---

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/places/` | Get all tourist places |
| GET | `/api/places/<id>` | Get place by ID |
| GET | `/api/places/search?q=` | Search places by name |
| GET | `/api/places/filter?category=` | Filter by category/district |
| POST | `/api/itinerary/` | Generate AI itinerary |
| GET | `/api/weather/?district=` | Get live weather |
| POST | `/api/recommend/click` | Track place click |
| GET | `/api/recommend/?session_id=` | Get ML recommendations |

---

## 🧪 ML Pipeline

```
User clicks Place A (waterfall) → MongoDB stores click
User clicks Place B (waterfall) → MongoDB stores click
User clicks Place C (waterfall) → MongoDB stores click
         ↓
TF-IDF vectorizes place descriptions
Cosine similarity compares user profile vs all places
         ↓
Recommends: Lodh Falls, Usri Falls, Dassam Falls
```

**Why TF-IDF + Cosine Similarity?**
- Works without user login (session-based)
- No cold start problem for places (content-based, not collaborative)
- Interpretable — can explain why a place was recommended
- Lightweight — runs in milliseconds on free tier

---

## 📁 Project Structure

```
smart-tourism-jharkhand/
├── backend/
│   ├── app.py                  # Flask app, blueprint registration
│   ├── config.py               # Environment config
│   ├── requirements.txt        # Python dependencies
│   ├── routes/
│   │   ├── places.py           # Place listing, search, filter
│   │   ├── itinerary.py        # AI itinerary generation + caching
│   │   ├── weather.py          # Weather API + caching
│   │   └── recommend.py        # ML recommendation system
│   ├── utils/
│   │   ├── db.py               # MongoDB connection
│   │   └── cache.py            # Redis caching utilities
│   └── data/
│       ├── india_tourism_dataset.json   # Kaggle dataset (100 destinations)
│       └── tourism_budget.csv           # Processed budget data
└── frontend/
    ├── src/
    │   ├── App.jsx             # Main React component
    │   └── App.css             # Styling
    └── package.json
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB Atlas account
- Groq API key (free at console.groq.com)
- OpenWeatherMap API key (free)
- Upstash Redis account (free)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `.env` file in `backend/`:
```
GROQ_API_KEY=your_groq_key
OPENWEATHER_API_KEY=your_openweather_key
MONGODB_URI=your_mongodb_uri
UPSTASH_REDIS_REST_URL=your_upstash_url
UPSTASH_REDIS_REST_TOKEN=your_upstash_token
```

```bash
python app.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

---

## 🌍 Deployment

| Service | Platform | URL |
|--------|---------|-----|
| Frontend | Vercel | smart-tourism-jharkhand.vercel.app |
| Backend | Render (Free) | smart-tourism-jharkhand.onrender.com |
| Database | MongoDB Atlas (Free) | Cloud hosted |
| Cache | Upstash Redis (Free) | Cloud hosted |

---

## 📊 Dataset

Budget estimation analysis uses the **Indian Tourist Destinations Dataset** (Kaggle):
- 100 Indian tourist destinations
- 54 features per destination
- Budget/mid-range/luxury daily cost ranges in INR
- East India region averages used for Jharkhand estimation:
  - Budget: ₹1,517/day
  - Mid-range: ₹3,050/day  
  - Luxury: ₹6,033/day

---

## 🔮 Future Roadmap

- [ ] User authentication (JWT)
- [ ] Trip budget estimator API route
- [ ] Google Maps Distance Matrix for real route optimization
- [ ] Crowd prediction using seasonal ML model
- [ ] Docker containerization
- [ ] Rate limiting and API security
- [ ] Expand to all 24 districts of Jharkhand

---

## 👨‍💻 Developer

**Aryan (Shubham Verma)**  
B.Tech CSE (AI & ML), Final Year  
Galgotias College of Engineering & Technology, Greater Noida  
GitHub: [@aryan7radhe](https://github.com/aryan7radhe)  
LinkedIn: [linkedin.com/in/shubham-verma-b178b6336](https://linkedin.com/in/shubham-verma-b178b6336)

---

*Built with ❤️ for Jharkhand Tourism*
