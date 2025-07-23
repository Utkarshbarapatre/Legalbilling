# Chrome Extension Troubleshooting Guide

## Service Worker Registration Failed (Status Code: 151)

This error usually means there's an issue with the background script. Here's how to fix it:

### Step 1: Check Files Exist
Make sure these files exist in the chrome-extension folder:
- ✅ `manifest.json`
- ✅ `background.js`
- ✅ `popup.html`
- ✅ `popup.js`
- ✅ `content.js`
- ✅ `styles.css`

### Step 2: Reload Extension
1. Go to `chrome://extensions/`
2. Find "Legal Billing Email Summarizer"
3. Click the **reload button** (circular arrow icon)
4. Check for any new errors

### Step 3: Check Console
1. Go to `chrome://extensions/`
2. Click "Details" on your extension
3. Click "Inspect views: service worker"
4. Look for errors in the console

### Step 4: Verify Manifest
Make sure your `manifest.json` looks exactly like this:
\`\`\`json
{
  "manifest_version": 3,
  "name": "Legal Billing Email Summarizer",
  "version": "1.0.0",
  "description": "Automatically capture and summarize emails for legal billing",
  "permissions": ["activeTab", "storage", "scripting"],
  "host_permissions": ["https://mail.google.com/*", "http://localhost:8000/*", "http://127.0.0.1:8000/*"],
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["https://mail.google.com/*"],
      "js": ["content.js"],
      "css": ["styles.css"],
      "run_at": "document_end"
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_title": "Legal Billing Summarizer"
  }
}
\`\`\`

### Step 5: Test Background Script
1. Open `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked" and select the folder again
4. If it still fails, check the background.js file

## Common Solutions

### Solution 1: Remove and Reinstall
1. Remove the extension completely
2. Close Chrome
3. Reopen Chrome
4. Go to `chrome://extensions/`
5. Load the extension again

### Solution 2: Check File Permissions
Make sure all files are readable and not corrupted.

### Solution 3: Simplify Background Script
If the background script is too complex, try this minimal version:

\`\`\`javascript
// Minimal background.js
console.log('Background script loaded');

chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed');
});
\`\`\`

### Solution 4: Use Chrome Canary
Sometimes the stable Chrome has issues. Try Chrome Canary or Chrome Dev.

## Testing Steps

1. **Load Extension**: Should load without errors
2. **Check Background**: Service worker should be active
3. **Test Popup**: Click extension icon, popup should open
4. **Test Gmail**: Go to Gmail, content script should inject
5. **Test Capture**: Try capturing an email

## Getting Help

If none of these solutions work:

1. **Check Chrome Version**: Make sure you're using Chrome 88+
2. **Check Console Errors**: Look for specific error messages
3. **Try Incognito Mode**: Test if it works in incognito
4. **Restart Chrome**: Sometimes a restart fixes issues

## Error Codes

- **151**: Service worker registration failed
- **Could not load manifest**: JSON syntax error
- **Could not load icon**: Missing icon files (can be ignored)
- **Permissions error**: Check host_permissions in manifest
