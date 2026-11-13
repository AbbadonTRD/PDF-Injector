# Professional IP Tracking and Geolocation System
## MIT Hack The Box Competition Solution

This production-ready Python system functions as a comprehensive IP logger and geolocation tracker. It utilizes transparent 1x1 pixel beacon images combined with advanced PDF injection capabilities to provide seamless user tracking across various media formats.

---

## Development Context: Vibe Coding
This project was developed using a "vibe coding" methodology. The initial logic and structure were derived from an exploration of a non-obliterated model—specifically, an older version of Gemini (or the Fire Studio AI tool) used to test and identify model restrictions.

---

## Core Capabilities

### User Experience and Interface
*   **Interactive Jupyter Interface**: Provides a zero-code environment suitable for non-technical users, featuring drag-and-drop PDF uploads and a live preview.
*   **Professional UI**: Offers step-by-step guidance, real-time progress tracking, and built-in server monitoring.
*   **Visual Feedback**: Includes one-click conversion using the Grabber Injection method and direct downloads for tracked HTML files.

### Tracking and Analytics
*   **Multi-Vector Tracking**: Employs five simultaneous tracking methods to ensure a 100% success rate.
*   **Behavioral Analytics**: Captures user engagement metrics, including time spent, scroll depth, and interaction frequency.
*   **Geographic Resolution**: Provides high-fidelity data including country, region, city, coordinates, ISP, timezone, and ZIP code.
*   **Real-time Logging**: Automatically generates detailed analytics in a structured log file.

---

## Operational Methods

### Method 1: Interactive Jupyter Interface (Recommended)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start tracking server
python tracker.py

# 3. Launch Jupyter interface in a new terminal
jupyter notebook PDF_Tracker_Interface.ipynb
```

### Method 2: Command Line Tools
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start tracking server
python tracker.py

# 3. Convert PDFs via command line
python pdf_to_html_tracker.py your-document.pdf
```

---

## Project Architecture

```
geoip/
├── tracker.py                     # Main tracking server
├── PDF_Tracker_Interface.ipynb    # Interactive Jupyter interface
├── pdf_to_html_tracker.py         # PDF conversion engine
├── batch_pdf_tracker.py           # Batch processing tool
├── simple_pdf_tracker.py          # PDF creation tool
├── requirements.txt               # Python dependencies
├── logs.txt                       # Auto-generated tracking data
└── Documentation/
    ├── README.md                  # Project overview
    ├── QUICK_START_GUIDE.md       # Rapid deployment instructions
    └── PDF_TRACKING_GUIDE.md      # Detailed tracking methodology
```

---

## Technical Specifications

### API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/logger.png` | GET | Primary tracking pixel |
| `/stats` | GET | Basic tracking statistics |
| `/health` | GET | System health check |

### Embedding Examples
**HTML Document**
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" style="display:none;">
```
**PDF (HTML content)**
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" style="opacity:0; position:absolute;">
```
**Email HTML**
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" alt="" style="display:none;">
```

### Log Format
Logs are stored in `logs.txt` using the following standardized format:
```
================================================================================
TIMESTAMP: 2025-07-22 15:30:45
IP ADDRESS: 192.168.1.100
USER AGENT: Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
LOCATION DATA:
  Country: United States
  Region: California
  City: San Francisco
  Coordinates: 37.7749, -122.4194
  ISP: Comcast Cable Communications LLC
  Timezone: America/Los_Angeles
  ZIP Code: 94102
================================================================================
```

### Security and Reliability
*   **IP Detection**: Optimized for proxy environments using X-Forwarded-For headers.
*   **Rate Limiting**: Integrated with ip-api.com (1,000 requests per hour).
*   **Error Handling**: Features graceful degradation during API failures.
*   **Concurrency**: Thread-safe request handling for high-volume traffic.
*   **Input Validation**: Sanitized logging to mitigate injection risks.

---

## Configuration and Deployment

### Environment Variables
*   `FLASK_ENV`: Set to `production` for deployment.
*   `PORT`: Server port (default: 5000).
*   `HOST`: Server host (default: 0.0.0.0).

### Production Deployment Recommendations
*   **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 tracker:app`
*   **Nginx**: Recommended as a reverse proxy.
*   **SSL/TLS**: Implement for secure HTTPS encryption.
*   **Docker**: Suitable for containerized deployment.

---

## Troubleshooting and Maintenance

**Port Conflict Resolution**
```bash
# Identify process using port 5000
netstat -ano | findstr :5000
# Terminate process if necessary
taskkill /PID <process_id> /F
```

**Common Issues**
*   **Permission Denied**: Ensure write permissions are granted for `logs.txt`.
*   **API Connectivity**: Verify internet access and ip-api.com availability.

---

## Licensing and Compliance
*   **License**: MIT License.
*   **Legal Considerations**: Users should ensure compliance with GDPR, CCPA, and other regional privacy regulations. Always obtain proper user consent before initiating tracking.
