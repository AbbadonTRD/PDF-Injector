#!/usr/bin/env python3
"""
Simple PDF Tracker Creator - Creates PDFs with embedded tracking
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
    
    # Add more content
    c.setFillColorRGB(0, 0, 0)  # Reset to black
    c.setFont("Helvetica", 12)
    y_pos = height - 300
    
    additional_content = [
        "This is a test document with embedded tracking.",
        "",
        "When this PDF is opened in a browser or compatible",
        "PDF viewer, it will automatically send a request",
        "to the tracking server.",
        "",
        "The tracking is completely invisible to the user",
        "and logs the following information:",
        "• IP address",
        "• User agent (browser/OS)",
        "• Timestamp",
        "• Geographic location (if available)",
        "",
        "Check the server logs to see tracking data!"
    ]
    
    for line in additional_content:
        c.drawString(50, y_pos, line)
        y_pos -= 20
    
    c.save()
    print(f"✅ Created trackable PDF: {filename}")
    print(f"🎯 Tracking URL: {tracking_url}")
    return filename

def main():
    """Create a tracked PDF and open it"""
    filename = "tracked_document.pdf"
    server_url = "http://localhost:5000"
    
    # Create the PDF
    create_trackable_pdf(
        filename, 
        server_url, 
        "This is a demonstration of PDF tracking technology."
    )
    
    print(f"\n🚀 PDF created successfully!")
    print(f"📄 File: {filename}")
    print(f"🌐 Server: {server_url}")
    print(f"\n📋 Next steps:")
    print(f"1. Make sure the tracker server is running: py tracker.py")
    print(f"2. Open {filename} in a web browser")
    print(f"3. Check logs.txt to see tracking data")
    print(f"\n🔗 Or open directly: file://{os.path.abspath(filename)}")

if __name__ == "__main__":
    main()
