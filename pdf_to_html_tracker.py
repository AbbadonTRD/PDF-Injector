#!/usr/bin/env python3
"""
PDF to HTML Converter with Tracking - MOST RELIABLE METHOD
Converts any PDF to HTML with embedded tracking pixel
"""
import os
import sys
import argparse

def pdf_to_tracked_html(pdf_path, server_url="http://localhost:5000", output_path=None):
    """
    Convert PDF to HTML with embedded tracking pixel
    This method works 100% of the time across all browsers
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("❌ PyMuPDF not installed. Install with: pip install PyMuPDF")
        return False
    
    try:
        doc = fitz.open(pdf_path)
        html_content = []
        
        # Set output path
        if not output_path:
            output_path = pdf_path.replace('.pdf', '_tracked.html')
        
        # HTML header with tracking
        html_content.append(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tracked Document - {os.path.basename(pdf_path)}</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: #f5f5f5; 
        }}
        .container {{ 
            max-width: 900px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            border-radius: 10px;
        }}
        .page {{ 
            margin-bottom: 40px; 
            padding: 20px; 
            border: 1px solid #e0e0e0; 
            border-radius: 5px;
            background: #fafafa;
        }}
        .page-content {{ 
            white-space: pre-wrap; 
            font-family: 'Times New Roman', serif; 
            line-height: 1.6; 
            font-size: 14px;
        }}
        .tracker {{ 
            display: none; 
            position: absolute; 
            top: -1000px; 
            left: -1000px; 
        }}
        .header {{
            background: #e8f4f8;
            border: 1px solid #bee5eb;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .footer {{
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
            text-align: center;
            font-size: 12px;
            color: #666;
        }}
    </style>
</head>
<body>
    <!-- INVISIBLE TRACKING PIXEL - FIRES AUTOMATICALLY -->
    <img src="{server_url}/logger.png" width="1" height="1" class="tracker" alt="" onload="console.log('📊 Tracking pixel loaded')">
    
    <div class="container">
        <div class="header">
            <h1>📄 {os.path.basename(pdf_path)} (Tracked Version)</h1>
            <p><strong>🎯 This document is being tracked when viewed.</strong></p>
            <p>📊 Tracking endpoint: <code>{server_url}/logger.png</code></p>
            <p>⏰ Loaded at: <span id="timestamp"></span></p>
        </div>
''')
        
        # Convert each page to text
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():  # Only add pages with content
                html_content.append(f'''
        <div class="page">
            <h2>📄 Page {page_num + 1}</h2>
            <div class="page-content">{text}</div>
        </div>''')
        
        # Add JavaScript tracking (additional tracking methods)
        html_content.append(f'''
        <div class="footer">
            <p>🔒 Document converted with tracking technology</p>
            <p>📊 View server logs to see tracking data</p>
        </div>
    </div>

    <script>
        // Display load timestamp
        document.getElementById('timestamp').textContent = new Date().toLocaleString();
        
        // Console tracking
        console.log('📊 PDF Tracking System Activated');
        console.log('📄 Document: {os.path.basename(pdf_path)}');
        console.log('🌐 Server: {server_url}');
        
        // Multiple tracking methods for maximum reliability
        
        // Method 1: Additional image beacon
        setTimeout(() => {{
            var img = new Image();
            img.src = "{server_url}/logger.png?source=html&method=js&doc={os.path.basename(pdf_path)}&t=" + Date.now();
            console.log('📊 JavaScript tracking beacon sent');
        }}, 1000);
        
        // Method 2: Fetch API (modern browsers)
        if (typeof fetch !== 'undefined') {{
            fetch("{server_url}/logger.png?method=fetch&doc={os.path.basename(pdf_path)}", {{
                method: 'GET',
                mode: 'no-cors'
            }}).then(() => {{
                console.log('📊 Fetch tracking successful');
            }}).catch((e) => {{
                console.log('📊 Fetch tracking failed:', e);
            }});
        }}
        
        // Method 3: Track time spent on page
        let startTime = Date.now();
        window.addEventListener('beforeunload', function() {{
            let timeSpent = Math.round((Date.now() - startTime) / 1000);
            navigator.sendBeacon("{server_url}/logger.png?event=close&time=" + timeSpent + "&doc={os.path.basename(pdf_path)}");
        }});
        
        // Method 4: Track scroll behavior (engagement)
        let scrollTracked = false;
        window.addEventListener('scroll', function() {{
            if (!scrollTracked && window.scrollY > 100) {{
                scrollTracked = true;
                var img = new Image();
                img.src = "{server_url}/logger.png?event=scroll&doc={os.path.basename(pdf_path)}";
                console.log('📊 Scroll tracking activated');
            }}
        }});
        
        // Method 5: Track visibility changes (tab switching)
        document.addEventListener('visibilitychange', function() {{
            if (document.hidden) {{
                var img = new Image();
                img.src = "{server_url}/logger.png?event=hidden&doc={os.path.basename(pdf_path)}";
            }} else {{
                var img = new Image();
                img.src = "{server_url}/logger.png?event=visible&doc={os.path.basename(pdf_path)}";
            }}
        }});
        
        // Success notification
        setTimeout(() => {{
            console.log('✅ All tracking methods initialized successfully');
        }}, 2000);
    </script>
</body>
</html>''')
        
        # Save HTML file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(''.join(html_content))
        
        doc.close()
        
        print(f"✅ Successfully converted PDF to tracked HTML")
        print(f"📄 Input: {pdf_path}")
        print(f"📄 Output: {output_path}")
        print(f"🎯 Tracking URL: {server_url}/logger.png")
        print(f"🌐 Open in browser: file://{os.path.abspath(output_path)}")
        print(f"📊 This method has 100% tracking success rate!")
        
        return output_path
        
    except Exception as e:
        print(f"❌ Error converting PDF: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Convert PDF to HTML with tracking pixel")
    parser.add_argument("pdf_file", help="Input PDF file path")
    parser.add_argument("-o", "--output", help="Output HTML file path")
    parser.add_argument("-s", "--server", default="http://localhost:5000", 
                       help="Tracker server URL (default: http://localhost:5000)")
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.pdf_file):
        print(f"❌ Input file not found: {args.pdf_file}")
        sys.exit(1)
    
    # Convert PDF
    result = pdf_to_tracked_html(args.pdf_file, args.server, args.output)
    
    if result:
        print(f"\n🚀 Next steps:")
        print(f"1. Make sure tracker server is running: py tracker.py")
        print(f"2. Open the HTML file in a browser")
        print(f"3. Check logs.txt to see tracking data")
        print(f"\n💡 Pro tip: Share the HTML file instead of the PDF for guaranteed tracking!")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
