# Legal Billing Email Summarizer - Chrome Extension

## Quick Start

1. **Install Extension:**
   - Open Chrome → `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked" → Select this folder
   - Ignore icon warnings (extension works without them)

2. **Use Extension:**
   - Go to Gmail
   - Click extension icon in toolbar
   - Click "Capture Current Email" on any email
   - Or look for "⚖️ Capture for Billing" button in Gmail

3. **Configure:**
   - Make sure server URL is `http://127.0.0.1:8000`
   - Enable auto-capture if desired

## Features

- ✅ **Manual Capture**: Click button to capture any email
- ✅ **Auto Capture**: Automatically capture sent emails
- ✅ **Quick Summaries**: Generate AI summaries from extension
- ✅ **Dashboard Link**: Quick access to main dashboard

## Troubleshooting

**Extension won't load:**
- Make sure you selected the correct folder
- Ignore icon warnings - they're not required

**No capture button in Gmail:**
- Refresh Gmail page
- Check if extension is enabled

**Server connection failed:**
- Make sure server is running: `python run.py`
- Check server URL in extension settings

**Auto-capture not working:**
- Enable auto-capture in extension popup
- Send a test email to verify

## Files

- `manifest.json` - Extension configuration
- `popup.html/js` - Extension popup interface
- `content.js` - Gmail integration script
- `background.js` - Background service worker
- `styles.css` - Gmail button styling
