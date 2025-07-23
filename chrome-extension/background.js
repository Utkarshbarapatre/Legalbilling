// Background service worker for Legal Billing Email Summarizer
console.log("Legal Billing Email Summarizer background script loaded")

// Declare chrome variable
const chrome = window.chrome

// Install event
chrome.runtime.onInstalled.addListener((details) => {
  console.log("Extension installed:", details.reason)

  // Set default settings
  chrome.storage.sync
    .set({
      serverUrl: "http://127.0.0.1:8000",
      autoCaptureEnabled: false,
    })
    .then(() => {
      console.log("Default settings initialized")
    })
    .catch((error) => {
      console.error("Error setting default settings:", error)
    })
})

// Handle messages from content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Message received:", request)

  if (request.action === "captureEmail") {
    handleEmailCapture(request.data)
      .then((result) => {
        sendResponse({ success: true, result })
      })
      .catch((error) => {
        console.error("Error handling email capture:", error)
        sendResponse({ success: false, error: error.message })
      })

    // Return true to indicate we'll send a response asynchronously
    return true
  }

  if (request.action === "testConnection") {
    testServerConnection()
      .then((result) => {
        sendResponse(result)
      })
      .catch((error) => {
        sendResponse({ success: false, error: error.message })
      })

    return true
  }
})

// Handle email capture
async function handleEmailCapture(emailData) {
  try {
    const settings = await chrome.storage.sync.get(["serverUrl"])
    const serverUrl = settings.serverUrl || "http://127.0.0.1:8000"

    console.log("Capturing email to server:", serverUrl)

    const response = await fetch(`${serverUrl}/api/extension/capture-email`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(emailData),
    })

    if (!response.ok) {
      throw new Error(`Server responded with status: ${response.status}`)
    }

    const result = await response.json()
    console.log("Email captured successfully:", result)

    return result
  } catch (error) {
    console.error("Error capturing email:", error)
    throw error
  }
}

// Test server connection
async function testServerConnection() {
  try {
    const settings = await chrome.storage.sync.get(["serverUrl"])
    const serverUrl = settings.serverUrl || "http://127.0.0.1:8000"

    const response = await fetch(`${serverUrl}/health`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (response.ok) {
      const data = await response.json()
      return { success: true, data }
    } else {
      throw new Error(`Server responded with status: ${response.status}`)
    }
  } catch (error) {
    console.error("Server connection test failed:", error)
    return { success: false, error: error.message }
  }
}

// Handle extension startup
chrome.runtime.onStartup.addListener(() => {
  console.log("Extension started")
})

// Handle browser action click (if no popup is defined)
chrome.action.onClicked.addListener((tab) => {
  console.log("Extension icon clicked on tab:", tab.url)

  // If we're on Gmail, try to inject content script
  if (tab.url && tab.url.includes("mail.google.com")) {
    chrome.scripting
      .executeScript({
        target: { tabId: tab.id },
        files: ["content.js"],
      })
      .catch((error) => {
        console.error("Error injecting content script:", error)
      })
  }
})

// Keep service worker alive
let keepAliveInterval

function keepAlive() {
  keepAliveInterval = setInterval(() => {
    chrome.runtime.getPlatformInfo(() => {
      // This is just to keep the service worker active
    })
  }, 20000) // Every 20 seconds
}

function stopKeepAlive() {
  if (keepAliveInterval) {
    clearInterval(keepAliveInterval)
    keepAliveInterval = null
  }
}

// Start keep alive when service worker starts
keepAlive()

// Clean up on suspend
chrome.runtime.onSuspend.addListener(() => {
  console.log("Service worker suspending")
  stopKeepAlive()
})
