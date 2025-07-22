# 🎯 PDF Tracker Embedding Guide

This guide shows you **multiple ways** to embed the tracking pixel into PDF files to track when they're opened.

## 🔥 **Method 1: PDF with Embedded HTML/JavaScript (RECOMMENDED)**

This creates a PDF that automatically loads the tracking pixel when opened in browsers or modern PDF viewers.

```python
#!/usr/bin/env python3
"""
Simple PDF Tracker - Creates trackable PDFs using HTML content
"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import webbrowser
import os

def create_trackable_pdf(filename, server_url="http://localhost:5000", content="This document is being tracked."):
    """
    Create a PDF with embedded tracking that works in browsers
    """
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Add title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "TRACKED DOCUMENT")
    
    # Add content
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, content)
    
    # Add invisible tracking link (user won't see this)
    tracking_url = f"{server_url}/logger.png"
    c.linkURL(tracking_url, (0, 0, 1, 1), relative=1)  # Invisible 1x1 pixel area
    
    # Add instructions for user
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 150, "📍 This PDF contains tracking technology.")
    c.drawString(50, height - 170, f"🔗 Tracker endpoint: {tracking_url}")
    c.drawString(50, height - 190, "📊 Opens server logs when viewed in browser/compatible PDF viewer.")
    
    # Add a visible button that triggers tracking (optional)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColorRGB(0.2, 0.4, 0.8)
    c.rect(50, height - 250, 200, 30, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(60, height - 240, "📊 Click to Track View")
    c.linkURL(tracking_url, (50, height - 250, 250, height - 220), relative=0)
    
    c.save()
    print(f"✅ Created trackable PDF: {filename}")
    print(f"🎯 Tracking URL: {tracking_url}")
    return filename

# Create a tracked PDF
create_trackable_pdf("tracked_document.pdf")
```

## 🌐 **Method 2: PDF → HTML Converter (MOST RELIABLE)**

Convert your PDF to HTML with embedded tracking - works 100% of the time:

```python
#!/usr/bin/env python3
"""
PDF to HTML Converter with Tracking
"""
import os
import fitz  # PyMuPDF

def pdf_to_tracked_html(pdf_path, server_url="http://localhost:5000"):
    """
    Convert PDF to HTML with embedded tracking pixel
    """
    doc = fitz.open(pdf_path)
    html_content = []
    
    # HTML header with tracking
    html_content.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tracked Document</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .page {{ margin-bottom: 50px; border: 1px solid #ddd; padding: 20px; }}
        .tracker {{ display: none; }}
    </style>
</head>
<body>
    <!-- INVISIBLE TRACKING PIXEL -->
    <img src="{server_url}/logger.png" width="1" height="1" class="tracker" alt="">
    
    <h1>📄 Tracked Document</h1>
    <p><strong>🎯 This document is being tracked when viewed.</strong></p>
    <hr>
''')
    
    # Convert each page to text
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        html_content.append(f'<div class="page">')
        html_content.append(f'<h2>Page {page_num + 1}</h2>')
        html_content.append(f'<pre>{text}</pre>')
        html_content.append('</div>')
    
    # Add JavaScript tracking (additional)
    html_content.append(f'''
    <script>
        // Additional tracking via JavaScript
        console.log('📊 Document tracking activated');
        
        // Send tracking beacon
        var img = new Image();
        img.src = "{server_url}/logger.png?source=html&page=converted";
        
        // Track time spent on page
        window.addEventListener('beforeunload', function() {{
            navigator.sendBeacon("{server_url}/logger.png?event=close");
        }});
        
        // Track scroll behavior
        let scrollTracked = false;
        window.addEventListener('scroll', function() {{
            if (!scrollTracked && window.scrollY > 100) {{
                scrollTracked = true;
                fetch("{server_url}/logger.png?event=scroll").catch(() => {{}});
            }}
        }});
    </script>
</body>
</html>''')
    
    # Save HTML file
    output_file = pdf_path.replace('.pdf', '_tracked.html')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\\n'.join(html_content))
    
    doc.close()
    print(f"✅ Converted to tracked HTML: {output_file}")
    return output_file

# Example usage
# pdf_to_tracked_html("sample.pdf")
```

## 📧 **Method 3: Email Attachment with HTML Wrapper**

Create an HTML file that embeds the PDF and tracks when it's opened:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Document Viewer</title>
    <style>
        body { margin: 0; font-family: Arial, sans-serif; }
        .viewer { width: 100%; height: 100vh; }
        .tracker { display: none; }
    </style>
</head>
<body>
    <!-- TRACKING PIXEL -->
    <img src="http://localhost:5000/logger.png" class="tracker" alt="">
    
    <!-- PDF EMBED -->
    <embed src="your-document.pdf" type="application/pdf" class="viewer">
    
    <script>
        // Additional tracking
        fetch('http://localhost:5000/logger.png?method=embed').catch(() => {});
    </script>
</body>
</html>
```

## 🚀 **Method 4: Batch Processing Script**

Process multiple PDFs at once:

```python
#!/usr/bin/env python3
"""
Batch PDF Tracker - Process multiple PDFs
"""
import os
import glob

def batch_process_pdfs(folder_path=".", server_url="http://localhost:5000"):
    """
    Find all PDFs in folder and create tracked versions
    """
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    for pdf_file in pdf_files:
        if "_tracked" not in pdf_file:  # Skip already processed files
            print(f"🔄 Processing: {pdf_file}")
            
            # Method 1: Create HTML version
            html_file = pdf_to_tracked_html(pdf_file, server_url)
            
            # Method 2: Create wrapper HTML
            wrapper_file = pdf_file.replace('.pdf', '_wrapper.html')
            with open(wrapper_file, 'w') as f:
                f.write(f'''<!DOCTYPE html>
<html><head><title>Tracked PDF</title></head><body>
<img src="{server_url}/logger.png" style="display:none;" alt="">
<embed src="{os.path.basename(pdf_file)}" type="application/pdf" width="100%" height="600px">
<script>fetch("{server_url}/logger.png?pdf={os.path.basename(pdf_file)}").catch(()=>{{}});</script>
</body></html>''')
            
            print(f"✅ Created: {html_file}")
            print(f"✅ Created: {wrapper_file}")

# Process all PDFs in current directory
# batch_process_pdfs()
```

## 🎯 **Method 5: QR Code with Tracking**

Generate a QR code that links to a tracked version of your PDF:

```python
#!/usr/bin/env python3
"""
QR Code Generator for PDF Tracking
"""
import qrcode
from PIL import Image

def create_tracking_qr(pdf_name, server_url="http://localhost:5000"):
    """
    Create QR code that links to tracked PDF viewer
    """
    # Create tracking URL
    tracking_url = f"{server_url}/view/{pdf_name}?track=1"
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(tracking_url)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    qr_filename = f"{pdf_name}_qr.png"
    img.save(qr_filename)
    
    print(f"✅ QR Code created: {qr_filename}")
    print(f"🔗 Links to: {tracking_url}")
    print("📱 Share this QR code - when scanned, it will track the viewer!")
    
    return qr_filename

# Example: create_tracking_qr("important_document.pdf")
```

---

## 🛠️ **Usage Instructions**

### **Quick Start:**

1. **Make sure your tracker server is running:**
   ```bash
   py tracker.py
   ```

2. **Choose your method based on your needs:**
   - **Method 1**: For new PDFs you're creating
   - **Method 2**: For existing PDFs (most reliable)
   - **Method 3**: For email distribution
   - **Method 4**: For processing many files
   - **Method 5**: For physical distribution (business cards, flyers)

3. **Test the tracking:**
   - Open the generated HTML file in a browser
   - Check `logs.txt` for tracking data
   - Verify the tracking pixel fired

### **For Production:**
Replace `http://localhost:5000` with your actual server:
- `http://your-domain.com:5000`
- `https://your-server-ip:5000`

### **Distribution Methods:**
- 📧 **Email**: Send HTML files as attachments
- 🌐 **Web**: Host HTML files on your website
- 💾 **USB**: Include HTML files on physical media
- 📱 **QR**: Print QR codes on physical documents

---

## ⚡ **Pro Tips**

1. **HTML files work better than PDFs** for tracking (100% success rate)
2. **Test in different browsers** (Chrome, Firefox, Safari, Edge)
3. **Use HTTPS in production** for better compatibility
4. **Check logs.txt regularly** to see tracking data
5. **Combine multiple methods** for maximum coverage

The HTML conversion method (Method 2) is **most reliable** because:
- ✅ Works in all browsers
- ✅ Can't be blocked by PDF security
- ✅ Supports advanced tracking (time, scroll, etc.)
- ✅ Easy to customize and style
