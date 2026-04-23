# 🗑️ BinTrack ZA

**Never miss a bin collection day in South Africa again!**

BinTrack ZA is a colorful, user-friendly web application that helps South African residents stay on top of their waste collection schedules across different municipalities.

---

## 🌟 Features

✨ **Vibrant & Colorful UI** - Eye-catching gradient backgrounds and smooth animations  
📍 **Area Selection** - Easily select your suburb from a comprehensive dropdown list  
📅 **Smart Status Updates** - Real-time collection status with countdown timers  
🚀 **Fast & Responsive** - Built with FastAPI and Tailwind CSS  
🌐 **Supports Multiple Providers**:
- **Pikitup** (Gauteng)
- **City of Cape Town** (Western Cape)

---

## 🎯 How It Works

1. Open the application in your browser
2. Select your suburb from the dropdown menu
3. Get instant information about:
   - Next collection day
   - Days remaining until collection
   - Current collection status
   - Your waste collection provider

### Status Colors

- 🟢 **Green** - Collection is today
- 🔴 **Red** - Action required (put bins out tonight)
- 🟡 **Yellow** - Reminder (collection tomorrow)
- 🔵 **Blue** - Upcoming collection

---

## 📦 Supported Suburbs

### Gauteng (Pikitup)
- Braamfontein
- Sandton
- Soweto

### Western Cape (City of Cape Town)
- Sea Point
- Gardens
- Rondebosch
- Table View
- Constantia
- Muizenberg
- Durbanville
- Somerset West
- Camps Bay
- Bellville

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+
- pip

### Installation

1. **Clone/Navigate to the project:**
   ```bash
   cd BinTracker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

4. **Open in browser:**
   Navigate to `http://localhost:8000` in your web browser

---

## 📋 Project Structure

```
BinTracker/
├── main.py           # FastAPI backend with collection logic
├── index.html        # Interactive frontend with gradient UI
├── requirements.txt  # Python dependencies
└── README.md        # This file
```

---

## 🛠️ Tech Stack

**Backend:**
- **FastAPI** - Modern, fast Python web framework
- **Uvicorn** - ASGI web server

**Frontend:**
- **HTML5** - Semantic markup
- **Tailwind CSS** - Utility-first CSS framework
- **Vanilla JavaScript** - Dynamic UI interactions
- **Font Awesome** - Icon library

---

## 📝 API Endpoints

### GET `/suburbs`
Returns a list of all supported suburbs
```json
["Braamfontein", "Sandton", "Soweto", ...]
```

### GET `/check/{suburb}`
Returns collection status for a specific suburb
```json
{
  "suburb": "Sandton",
  "provider": "Pikitup",
  "collection_day": "Friday",
  "days_remaining": 2,
  "status": "Upcoming",
  "message": "Next collection is on Friday.",
  "color": "blue"
}
```

---

## 🎨 Customization

### Add More Suburbs
Edit the `SUBURBS` dictionary in `main.py`:
```python
SUBURBS = {
    'Your Suburb': {'day': 'Monday', 'provider': 'Provider Name'},
    ...
}
```

### Change Colors
Modify the color mappings in `main.py` or customize Tailwind classes in `index.html`.

---

## 🐛 Troubleshooting

**Port 8000 already in use?**
```bash
python main.py  # Change port in code if needed
```

**CORS Issues?**
The backend is configured to accept requests from any origin. If you encounter issues, ensure the frontend URL matches your backend configuration.

---

## 📧 Contact

Built with ❤️ by **Sandisiwe Ngcuka**

Keep South Africa clean, one bin at a time! 🌍

---

## 📄 License

This project is open source and available for personal and educational use.
