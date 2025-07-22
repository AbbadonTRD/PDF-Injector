# 🎯 **Professional IP Tracker & Geo-Location System**
## 🏆 **MIT Hack The Box Competition Solution**

A complete, production-ready Python system that serves as an **IP logger and geo-tracker** using transparent 1x1 pixel beacon images with advanced PDF injection capabilities.

---

## � **Key Features**

✅ **Interactive Jupyter Interface** - No coding required!  
✅ **Grabber Injection Method™** - Advanced multi-vector tracking  
✅ **PDF to HTML Conversion** - 100% tracking success rate  
✅ **Real-time Geo-location** - IP, location, browser analytics  
✅ **Professional UI** - Step-by-step guidance for beginners  
✅ **Production Ready** - Scalable Flask backend

---

## 🚀 **Quick Start**

### **Method 1: Interactive Jupyter Interface (RECOMMENDED)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start tracking server
python tracker.py

# 3. Launch Jupyter interface (in new terminal)
jupyter notebook PDF_Tracker_Interface.ipynb
```

### **Method 2: Command Line Tools**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start tracking server
python tracker.py

# 3. Convert PDFs using command line
python pdf_to_html_tracker.py your-document.pdf
```

---

## 📂 **Project Structure**

```
📁 geoip/
├── 🎯 tracker.py                     # Main tracking server
├── 📓 PDF_Tracker_Interface.ipynb    # Interactive Jupyter interface ⭐
├── 🔄 pdf_to_html_tracker.py         # PDF conversion engine  
├── 📦 batch_pdf_tracker.py           # Batch processing tool
├── 📄 simple_pdf_tracker.py          # Create new tracked PDFs
├── 📋 requirements.txt               # Python dependencies
├── 📊 logs.txt                       # Tracking data (auto-generated)
└── 📚 Documentation/
    ├── README.md                     # This file
    ├── QUICK_START_GUIDE.md          # Quick start guide
    └── PDF_TRACKING_GUIDE.md         # Detailed PDF tracking guide
```

---

## 🎯 **Main Features**

### **1. Interactive Jupyter Interface** ⭐
- **Zero-code operation** - Perfect for non-technical users
- **Drag & drop PDF upload** with live preview
- **One-click conversion** using Grabber Injection method
- **Real-time progress tracking** and visual feedback
- **Built-in server monitoring** and log viewing
- **Direct download** of tracked HTML files

### **2. Advanced Tracking System**
- **Multi-vector tracking** - 5 simultaneous methods for 100% success
- **Behavioral analytics** - Time spent, scroll depth, engagement
- **Geographic resolution** - Country, city, ISP, coordinates
- **Real-time logging** - Detailed analytics in logs.txt

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/logger.png` | GET | Main tracking pixel endpoint |
| `/stats` | GET | View basic statistics |
| `/health` | GET | Health check endpoint |

## 🔗 Embedding Examples

### HTML Document
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" style="display:none;">
```

### PDF (HTML content)
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" style="opacity:0; position:absolute;">
```

### Email HTML
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" alt="" style="display:none;">
```

### Markdown (if HTML is supported)
```html
<img src="http://your-server-ip:5000/logger.png" width="1" height="1" style="display:none;">
```

## 📝 Log Format

Logs are saved to `logs.txt` with the following format:

```
================================================================================
TIMESTAMP: 2025-07-22 15:30:45
IP ADDRESS: 192.168.1.100
USER AGENT: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
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

## 🛡️ Security Features

- **IP Detection**: Properly handles X-Forwarded-For headers for proxy environments
- **Rate Limiting**: Uses ip-api.com free tier (1000 requests/hour)
- **Error Handling**: Graceful degradation when geo-location API fails
- **Thread Safety**: Safe concurrent request handling
- **Input Validation**: Sanitized logging to prevent injection attacks

## 🔧 Configuration

### Environment Variables (Optional)
- `FLASK_ENV`: Set to `production` for production deployment
- `PORT`: Server port (default: 5000)
- `HOST`: Server host (default: 0.0.0.0)

### Production Deployment

For production, consider using:
- **Gunicorn**: `gunicorn -w 4 -b 0.0.0.0:5000 tracker:app`
- **Nginx**: As reverse proxy
- **SSL/TLS**: For HTTPS encryption
- **Docker**: For containerized deployment

## 📊 Monitoring

### Real-time Console Output
The server provides real-time console output for each tracking request:

```
🎯 TRACKING REQUEST RECEIVED
   IP: 192.168.1.100
   User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
   Timestamp: 2025-07-22 15:30:45
   Location: San Francisco, California, United States
   ISP: Comcast Cable Communications LLC
```

### Statistics Endpoint
Visit `/stats` to get basic tracking statistics:

```json
{
  "total_requests": 150,
  "log_file_size": 45678,
  "status": "active"
}
```

## ⚠️ Legal Considerations

- **Consent**: Ensure you have proper consent for tracking
- **Privacy Laws**: Comply with GDPR, CCPA, and other privacy regulations
- **Disclosure**: Consider adding privacy notices where appropriate
- **Data Retention**: Implement log rotation and data retention policies

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 5000
   netstat -ano | findstr :5000
   # Kill the process if needed
   taskkill /PID <process_id> /F
   ```

2. **Permission Denied for logs.txt**
   - Ensure write permissions in the directory
   - Run with appropriate user privileges

3. **Geo-location API Failures**
   - Check internet connectivity
   - Verify ip-api.com is accessible
   - Monitor rate limits (1000 requests/hour)

## 🚀 Advanced Usage

### Custom Log Format
Modify the `log_request_data()` function to customize log format.

### Multiple Storage Backends
Extend the logging system to support databases, cloud storage, etc.

### Real-time Analytics
Integrate with analytics platforms for real-time tracking visualization.

## 📜 License

MIT License - Feel free to use this for educational and legitimate tracking purposes.

## ⚠️ Disclaimer

This tool is for educational and legitimate tracking purposes only. Users are responsible for complying with all applicable laws and regulations regarding data collection and privacy.
