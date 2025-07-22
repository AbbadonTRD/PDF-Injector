#!/usr/bin/env python3
"""
Batch PDF Tracker - Process multiple PDFs with tracking
"""
import os
import glob
import argparse

def batch_track_pdfs(folder_path=".", server_url="http://localhost:5000", method="html"):
    """
    Find all PDFs in folder and create tracked versions
    """
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in: {folder_path}")
        return
    
    print(f"🔍 Found {len(pdf_files)} PDF files")
    print(f"📁 Folder: {os.path.abspath(folder_path)}")
    print(f"🌐 Server: {server_url}")
    print(f"⚙️  Method: {method}")
    print("=" * 60)
    
    processed = 0
    
    for pdf_file in pdf_files:
        if "_tracked" in pdf_file:  # Skip already processed files
            print(f"⏭️  Skipping (already processed): {os.path.basename(pdf_file)}")
            continue
            
        print(f"🔄 Processing: {os.path.basename(pdf_file)}")
        
        try:
            if method == "html":
                # Convert to HTML (most reliable)
                from pdf_to_html_tracker import pdf_to_tracked_html
                result = pdf_to_tracked_html(pdf_file, server_url)
                if result:
                    print(f"✅ Created HTML: {os.path.basename(result)}")
            
            elif method == "wrapper":
                # Create HTML wrapper
                wrapper_file = pdf_file.replace('.pdf', '_wrapper.html')
                with open(wrapper_file, 'w', encoding='utf-8') as f:
                    f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tracked PDF - {os.path.basename(pdf_file)}</title>
    <style>
        body {{ margin: 0; font-family: Arial, sans-serif; }}
        .header {{ background: #f8f9fa; padding: 10px; text-align: center; border-bottom: 1px solid #ddd; }}
        .viewer {{ width: 100%; height: calc(100vh - 60px); border: none; }}
        .tracker {{ display: none; }}
    </style>
</head>
<body>
    <!-- TRACKING PIXEL -->
    <img src="{server_url}/logger.png?pdf={os.path.basename(pdf_file)}" class="tracker" alt="">
    
    <div class="header">
        <strong>📄 {os.path.basename(pdf_file)}</strong> | 
        <span style="color: #666;">🎯 This document is being tracked</span>
    </div>
    
    <!-- PDF EMBED -->
    <embed src="{os.path.basename(pdf_file)}" type="application/pdf" class="viewer">
    
    <script>
        console.log('📊 PDF Wrapper Tracking Active');
        
        // Additional tracking methods
        fetch('{server_url}/logger.png?method=wrapper&pdf={os.path.basename(pdf_file)}').catch(() => {{}});
        
        // Track load time
        window.addEventListener('load', () => {{
            setTimeout(() => {{
                var img = new Image();
                img.src = '{server_url}/logger.png?event=loaded&pdf={os.path.basename(pdf_file)}';
            }}, 2000);
        }});
    </script>
</body>
</html>''')
                print(f"✅ Created wrapper: {os.path.basename(wrapper_file)}")
                
            elif method == "both":
                # Create both HTML and wrapper
                from pdf_to_html_tracker import pdf_to_tracked_html
                html_result = pdf_to_tracked_html(pdf_file, server_url)
                
                wrapper_file = pdf_file.replace('.pdf', '_wrapper.html')
                with open(wrapper_file, 'w', encoding='utf-8') as f:
                    f.write(f'''<!DOCTYPE html>
<html><head><title>Tracked PDF</title><style>
body{{margin:0;font-family:Arial,sans-serif;}}
.header{{background:#f8f9fa;padding:10px;text-align:center;border-bottom:1px solid #ddd;}}
.viewer{{width:100%;height:calc(100vh - 60px);border:none;}}
</style></head><body>
<img src="{server_url}/logger.png?pdf={os.path.basename(pdf_file)}" style="display:none;" alt="">
<div class="header"><strong>{os.path.basename(pdf_file)}</strong> | <span style="color:#666;">🎯 Tracked</span></div>
<embed src="{os.path.basename(pdf_file)}" type="application/pdf" class="viewer">
<script>fetch('{server_url}/logger.png?method=wrapper&pdf={os.path.basename(pdf_file)}').catch(()=>{{}});</script>
</body></html>''')
                
                if html_result:
                    print(f"✅ Created HTML: {os.path.basename(html_result)}")
                print(f"✅ Created wrapper: {os.path.basename(wrapper_file)}")
                
            processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {pdf_file}: {e}")
            continue
    
    print("=" * 60)
    print(f"✅ Batch processing complete!")
    print(f"📊 Processed: {processed}/{len(pdf_files)} files")
    print(f"🎯 All files now have tracking capabilities")
    print(f"\n📋 Next steps:")
    print(f"1. Make sure tracker server is running: py tracker.py")
    print(f"2. Share the HTML files instead of original PDFs")
    print(f"3. Monitor logs.txt for tracking data")

def main():
    parser = argparse.ArgumentParser(description="Batch process PDFs with tracking")
    parser.add_argument("-f", "--folder", default=".", help="Folder containing PDF files (default: current)")
    parser.add_argument("-s", "--server", default="http://localhost:5000", help="Tracker server URL")
    parser.add_argument("-m", "--method", choices=["html", "wrapper", "both"], default="html",
                       help="Tracking method: html (convert), wrapper (embed), both (default: html)")
    
    args = parser.parse_args()
    
    # Validate folder
    if not os.path.exists(args.folder):
        print(f"❌ Folder not found: {args.folder}")
        return
    
    # Process PDFs
    batch_track_pdfs(args.folder, args.server, args.method)

if __name__ == "__main__":
    main()
