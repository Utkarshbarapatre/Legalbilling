# Chrome Extension Setup Guide

## 📦 Installation

### 1. Load Extension in Chrome

1. **Open Chrome Extensions page:**
   - Go to `chrome://extensions/`
   - Or click Menu → More Tools → Extensions

2. **Enable Developer Mode:**
   - Toggle "Developer mode" in the top right

3. **Load Extension:**
   - Click "Load unpacked"
   - Select the `chrome-extension` folder from your project

4. **Pin Extension:**
   - Click the puzzle piece icon in Chrome toolbar
   - Pin "Legal Billing Email Summarizer"

### 2. Configure Extension

1. **Click the extension icon** in Chrome toolbar
2. **Set Server URL:** `http://127.0.0.1:8000`
3. **Enable auto-capture** if desired
4. **Test connection** - should show "Connected"

## 🚀 Usage

### Manual Capture
1. **Open Gmail** in Chrome
2. **Open any email**
3. **Click extension icon** → "Capture Current Email"
4. **Or click the "⚖️ Capture for Billing" button** in Gmail toolbar

### Auto Capture
1. **Enable auto-capture** in extension popup
2. **Send emails normally** - they'll be captured automatically
3. **Check dashboard** to see captured emails

### Generate Summaries
1. **Click extension icon**
2. **Click "Generate Summaries"**
3. **Or use the main dashboard** at `http://127.0.0.1:8000`

## 🔧 Features

### Extension Popup
- **Server connection status**
- **Email/summary statistics**
- **Current email preview**
- **One-click capture**
- **Auto-capture toggle**
- **Quick summary generation**
- **Dashboard access**

### Gmail Integration
- **Capture button** in Gmail toolbar
- **Auto-capture sent emails**
- **Real-time notifications**
- **Seamless email extraction**

### Advanced Features
- **Automatic email parsing**
- **Smart content extraction**
- **Background processing**
- **Offline queue** (coming soon)
- **Bulk operations** (coming soon)

## 🛠️ Troubleshooting

### Extension Not Loading
\`\`\`bash
# Check if all files exist
ls chrome-extension/
# Should show: manifest.json, popup.html, popup.js, content.js, etc.
\`\`\`

### Server Connection Issues
1. **Verify server is running:** `http://127.0.0.1:8000/health`
2. **Check server URL** in extension settings
3. **Ensure CORS is enabled** (already configured)

### Gmail Integration Not Working
1. **Refresh Gmail page**
2. **Check browser console** for errors (F12)
3. **Verify extension permissions**
4. **Try incognito mode** to test

### Auto-Capture Not Working
1. **Enable auto-capture** in extension popup
2. **Send a test email**
3. **Check extension console** for errors
4. **Verify Gmail page is fully loaded**

## 📊 Dashboard Integration

The extension works seamlessly with the main dashboard:

1. **Captured emails** appear in the dashboard
2. **Generate summaries** from either interface
3. **Edit summaries** in the dashboard
4. **Push to Clio** from the dashboard

## 🔒 Privacy & Security

- **No data stored** in extension
- **All data sent** to your local server
- **No external services** contacted
- **Gmail data** processed locally
- **Secure OAuth** for Clio integration

## 🚀 Advanced Usage

### Keyboard Shortcuts (Coming Soon)
- `Ctrl+Shift+C` - Capture current email
- `Ctrl+Shift+S` - Generate summary
- `Ctrl+Shift+D` - Open dashboard

### Bulk Operations (Coming Soon)
- Capture multiple emails at once
- Batch summary generation
- Bulk export to Clio

### Custom Templates (Coming Soon)
- Custom billing descriptions
- Matter-specific templates
- Time estimation rules
