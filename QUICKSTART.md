# API Tester - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: Install Dependencies
```bash
cd api_tester
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python main.py
```

The app will open immediately with a sample URL ready to test!

---

## 📋 First Test (Copy & Paste)

The app comes pre-loaded with `https://httpbin.org/get`

1. Click **🚀 Send Request**
2. See the response in the tabs below
3. Done! ✅

---

## 🎯 What's Included

✅ **Request Form** (Left Side)
- URL input with default example
- HTTP method dropdown (GET, POST, PUT, DELETE, PATCH, HEAD)
- Headers editor (JSON format)
- Request body editor
- Send & Clear buttons

✅ **Response Display** (Right Side)
- Body tab: Raw response
- Headers tab: Response headers
- Pretty tab: Formatted JSON
- Status indicator with color coding
- Response time in milliseconds
- Copy button for response

✅ **Menu Options**
- Export Response as JSON/TXT
- View Request History (last 20)
- Exit application

---

## 📝 Example Requests

### GET Request (Default)
Already loaded! Just click Send.

### POST Request
```
URL: https://httpbin.org/post
Method: POST
Body:
{
    "name": "Your Name",
    "message": "Hello API!"
}
Click: Send Request
```

### DELETE Request
```
URL: https://httpbin.org/delete
Method: DELETE
Click: Send Request
```

---

## 💾 Data Storage

- All requests automatically saved to `data/history.json`
- Last 50 requests kept
- View anytime via File → View History

---

## 🐛 Troubleshooting

**"No module named requests"**
```bash
pip install requests
```

**App won't start**
```bash
python --version  # Should be 3.7+
python main.py    # Run from api_tester folder
```

**Can't reach httpbin.org**
- Check internet connection
- Try any public API: `https://api.github.com/users/github`

---

## 📚 Project Files Explained

```
api_tester/
├── main.py                    # Start here! Launches the app
├── requirements.txt           # Dependencies (just 'requests')
├── README.md                  # Full documentation
├── QUICKSTART.md              # This file
├── ui/
│   ├── __init__.py           # Package marker
│   └── main_window.py        # All UI code (≈400 lines, well-commented)
└── data/
    └── history.json          # Auto-created, stores request history
```

---

## 🎓 Learning the Code

Start with **main.py** (10 lines):
- Shows how to launch the app
- Very simple entry point

Then explore **ui/main_window.py** (400 lines):
- `create_request_form()` - builds left panel
- `create_response_display()` - builds right panel
- `send_request()` - handles API calls
- `display_response()` - shows results
- Well-commented throughout

---

## ✨ Features You'll Love

🔄 **Non-blocking UI** - Requests run in background, GUI stays responsive
📊 **Color Status** - Green (200s), Orange (400s), Red (500s)
⏱️ **Response Timing** - See exactly how long requests take
📋 **Copy Button** - One-click copy response to clipboard
💾 **Auto-save** - History saved automatically
📤 **Export** - Save responses locally

---

## 🚀 Next Steps

1. **Test it** - Run `python main.py` and try a request
2. **Explore** - Try different HTTP methods and APIs
3. **Extend it** - Code is modular, easy to add features
4. **Deploy** - Create executable with PyInstaller (see README.md)

---

Happy Testing! 🎉
