# Chrome Extension Installation Guide

## Quick Install (No Icons Needed)

1. **Download the extension folder** to your computer
2. **Open Chrome** and go to `chrome://extensions/`
3. **Enable Developer Mode** (toggle in top right)
4. **Click "Load unpacked"** and select the `chrome-extension` folder
5. **Ignore icon warnings** - the extension will work fine without them

## If you want icons (optional):

### Method 1: Use the Icon Generator
1. Open `generate-icons.html` in your browser
2. Click "Generate Icons" then "Download All Icons"
3. Save the downloaded PNG files in the `chrome-extension` folder
4. Reload the extension in Chrome

### Method 2: Create Simple Icons
Create these files in the `chrome-extension` folder:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels) 
- `icon128.png` (128x128 pixels)

You can use any image editor or even MS Paint to create simple blue squares with "LB" text.

## Testing the Extension

1. **Pin the extension** to your Chrome toolbar
2. **Go to Gmail** (mail.google.com)
3. **Open any email**
4. **Click the extension icon** - you should see the popup
5. **Look for the "⚖️ Capture for Billing" button** in Gmail

## Troubleshooting

- **Extension not loading**: Make sure you selected the correct folder
- **No capture button in Gmail**: Refresh the Gmail page
- **Server connection failed**: Make sure your server is running at http://127.0.0.1:8000
- **Icon errors**: You can ignore these - the extension works without icons
\`\`\`

Let me also create a simplified popup that works without icons:
