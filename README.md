# API Tester - Desktop Application

A Postman-like desktop application for testing APIs, built with Python and Tkinter. Perfect for developers who want a lightweight, offline API testing tool.

## Features

✅ **Core Features**
- Send HTTP requests (GET, POST, PUT, DELETE, PATCH, HEAD)
- Custom headers in JSON format
- Request body support (JSON/text)
- Real-time response status and timing
- Response display in multiple formats (Body, Headers, Pretty JSON)
- Export responses to JSON/TXT files
- Copy response to clipboard

✅ **Data Management**
- Automatic request history (last 50 requests)
- View historical requests
- Local JSON storage (no cloud required)

✅ **User Experience**
- Clean, modern GUI
- Threading for non-blocking requests
- Color-coded status indicators
- Pre-filled example URL (httpbin.org)
- Professional layout with request/response split

## Requirements

- Python 3.7 or higher
- Tkinter (usually comes with Python)
- requests library

## Installation & Setup

### Option 1: Quick Start (Windows/Mac/Linux)

```bash
# 1. Navigate to project directory
cd api_tester

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python main.py
```

### Option 2: Using Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Usage Guide

### 1. Basic GET Request
- **URL**: `https://httpbin.org/get` (default)
- **Method**: GET
- **Headers**: Leave default
- **Click**: 🚀 Send Request
- **Result**: See response in Body tab

### 2. POST Request with JSON
- **URL**: `https://httpbin.org/post`
- **Method**: POST
- **Headers**: 
  ```json
  {
      "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
      "name": "John",
      "email": "john@example.com"
  }
  ```
- **Click**: 🚀 Send Request

### 3. View Response
- **Body Tab**: Raw response from server
- **Headers Tab**: Response headers from server
- **Pretty Tab**: Formatted JSON (if applicable)

### 4. Export Response
- Menu → File → Export Response
- Choose format: JSON or TXT
- Select save location

### 5. View History
- Menu → File → View History
- See last 20 requests with timestamps and status codes

## Project Structure

```
api_tester/
├── main.py                      # Entry point - run this file
├── requirements.txt             # Python dependencies
├── ui/
│   ├── __init__.py
│   └── main_window.py          # GUI and request logic
├── data/
│   └── history.json            # Request history (auto-created)
└── README.md                    # This file
```

## Code Explanation

### main.py
- Entry point for the application
- Creates Tkinter root window
- Initializes APITesterUI class

### ui/main_window.py
- **APITesterUI class**: Main GUI controller
- **create_request_form()**: Left panel with URL, method, headers, body
- **create_response_display()**: Right panel with response tabs
- **send_request()**: Handles API calls in separate thread
- **display_response()**: Shows response in UI
- **save_to_history()**: Stores requests locally
- **export_response()**: Saves response to file

## Testing with httpbin.org

httpbin.org is a free service for testing HTTP requests. Here are examples:

### Test GET
```
URL: https://httpbin.org/get
Method: GET
Expected: Returns your request details
```

### Test POST
```
URL: https://httpbin.org/post
Method: POST
Body: {"test": "data"}
Expected: Echoes back your posted data
```

### Test Delay
```
URL: https://httpbin.org/delay/2
Method: GET
Expected: Response after 2 seconds (test timeout)
```

### Test Status Codes
```
URL: https://httpbin.org/status/404
Method: GET
Expected: 404 Not Found status code
```

## Troubleshooting

### Issue: "No module named requests"
```bash
pip install requests
```

### Issue: "Tkinter not found"
- **Windows**: Already included, reinstall Python with "tcl/tk and IDLE"
- **Mac**: `brew install python-tk`
- **Linux**: `sudo apt-get install python3-tk`

### Issue: "Connection timeout"
- Check your internet connection
- Verify the URL is correct
- The timeout is set to 10 seconds

### Issue: App won't start
- Make sure you're in the `api_tester` directory
- Check Python version: `python --version` (should be 3.7+)
- Verify dependencies: `pip list | grep requests`

## Features Explained

### Threading
Requests run in background threads so the GUI stays responsive while waiting for API responses.

### History Storage
- Automatically saves last 50 requests in `data/history.json`
- View anytime via Menu → File → View History
- No setup required, works offline

### Export Functionality
- Export current response as JSON or TXT
- Save with custom filename
- Preserves formatting

### Response Tabs
- **Body**: Original response text
- **Headers**: Response HTTP headers
- **Pretty**: Auto-formatted JSON (if applicable)

## Future Enhancements

Possible additions:
- Collections/folders for organizing requests
- Authentication presets (Basic, Bearer token)
- Syntax highlighting for JSON
- Search/filter in response
- Multiple concurrent requests
- Dark theme toggle
- Request templates
- Environment variables support

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+E | Export (from File menu) |
| Ctrl+Q | Exit |
| Ctrl+L | Clear form |

## Building Standalone Executable

To create a .exe file (Windows):

```bash
pip install pyinstaller

pyinstaller --onefile --windowed --add-data "ui:ui" --icon=app.ico main.py
```

The .exe will be in the `dist/` folder.

## Dependencies Explained

- **requests**: Makes HTTP requests to APIs
- **tkinter**: Built-in Python GUI framework (no installation needed)
- **json**: Built-in, handles JSON parsing
- **threading**: Built-in, prevents GUI freezing during requests

## Author Notes

- This application is beginner-friendly and fully documented
- All code is modular and easy to extend
- No external dependencies except `requests`
- Works on Windows, Mac, and Linux
- Source code is clear and well-commented

## License

Free to use and modify for personal/educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Verify URL format and internet connection
3. Check response headers for API-specific errors

---

Happy API Testing! 🚀
