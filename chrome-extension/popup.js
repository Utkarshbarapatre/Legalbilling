// Legal Billing Popup Script
console.log("Popup script loaded")

// Declare chrome variable
const chrome = window.chrome

class LegalBillingPopup {
  constructor() {
    this.serverUrl = "http://127.0.0.1:8000"
    this.init()
  }

  async init() {
    try {
      // Load settings
      const settings = await chrome.storage.sync.get(["serverUrl", "autoCaptureEnabled"])
      if (settings.serverUrl) {
        this.serverUrl = settings.serverUrl
        const serverUrlInput = document.getElementById("server-url")
        if (serverUrlInput) {
          serverUrlInput.value = settings.serverUrl
        }
      }

      // Bind events
      this.bindEvents()

      // Check server status
      await this.checkServerStatus()

      // Load stats
      await this.loadStats()

      // Check current email
      await this.checkCurrentEmail()
    } catch (error) {
      console.error("Error initializing popup:", error)
    }
  }

  bindEvents() {
    // Capture email button
    const captureBtn = document.getElementById("capture-email")
    if (captureBtn) {
      captureBtn.addEventListener("click", () => this.captureCurrentEmail())
    }

    // Auto-capture toggle
    const autoCaptureBtn = document.getElementById("auto-capture")
    if (autoCaptureBtn) {
      autoCaptureBtn.addEventListener("click", () => this.toggleAutoCapture())
    }

    // Generate summaries
    const generateBtn = document.getElementById("generate-summaries")
    if (generateBtn) {
      generateBtn.addEventListener("click", () => this.generateSummaries())
    }

    // Open dashboard
    const dashboardBtn = document.getElementById("open-dashboard")
    if (dashboardBtn) {
      dashboardBtn.addEventListener("click", () => this.openDashboard())
    }

    // Settings
    const serverUrlInput = document.getElementById("server-url")
    if (serverUrlInput) {
      serverUrlInput.addEventListener("change", (e) => {
        this.serverUrl = e.target.value
        chrome.storage.sync.set({ serverUrl: this.serverUrl })
      })
    }

    const autoCaptureCheckbox = document.getElementById("auto-capture-sent")
    if (autoCaptureCheckbox) {
      autoCaptureCheckbox.addEventListener("change", (e) => {
        chrome.storage.sync.set({ autoCaptureEnabled: e.target.checked })
      })
    }
  }

  async checkServerStatus() {
    try {
      const response = await fetch(`${this.serverUrl}/health`)
      const statusElement = document.getElementById("server-status")
      const textElement = document.getElementById("server-text")

      if (response.ok) {
        if (statusElement) statusElement.className = "status-dot connected"
        if (textElement) textElement.textContent = "Connected"
      } else {
        throw new Error("Server not responding")
      }
    } catch (error) {
      console.error("Server status check failed:", error)
      const statusElement = document.getElementById("server-status")
      const textElement = document.getElementById("server-text")

      if (statusElement) statusElement.className = "status-dot disconnected"
      if (textElement) textElement.textContent = "Disconnected"
    }
  }

  async loadStats() {
    try {
      const [emailsResponse, summariesResponse] = await Promise.all([
        fetch(`${this.serverUrl}/api/gmail/emails/stored`),
        fetch(`${this.serverUrl}/api/summarizer/summaries`),
      ])

      if (emailsResponse.ok) {
        const emailsData = await emailsResponse.json()
        const emailsElement = document.getElementById("emails-captured")
        if (emailsElement) {
          emailsElement.textContent = emailsData.emails?.length || 0
        }
      }

      if (summariesResponse.ok) {
        const summariesData = await summariesResponse.json()
        const summariesElement = document.getElementById("summaries-generated")
        if (summariesElement) {
          summariesElement.textContent = summariesData.summaries?.length || 0
        }
      }
    } catch (error) {
      console.error("Error loading stats:", error)
    }
  }

  async checkCurrentEmail() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
      if (tab.url && tab.url.includes("mail.google.com")) {
        const results = await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          function: this.getCurrentEmailInfo,
        })

        if (results[0]?.result) {
          const emailInfo = results[0].result
          const currentEmailDiv = document.getElementById("current-email")
          const subjectElement = document.getElementById("current-subject")

          if (currentEmailDiv && subjectElement) {
            currentEmailDiv.style.display = "block"
            subjectElement.textContent = emailInfo.subject || "No subject"
          }
        }
      }
    } catch (error) {
      console.error("Error checking current email:", error)
    }
  }

  getCurrentEmailInfo() {
    // This function runs in the Gmail tab context
    const subjectElement = document.querySelector("[data-thread-perm-id] h2, .hP")
    return {
      subject: subjectElement?.textContent || "Unknown",
      url: window.location.href,
    }
  }

  async captureCurrentEmail() {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
      if (!tab.url || !tab.url.includes("mail.google.com")) {
        alert("Please navigate to Gmail first")
        return
      }

      // Execute content script to capture email
      const results = await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        function: this.extractEmailData,
      })

      if (results[0]?.result) {
        const emailData = results[0].result

        // Send to server via background script
        const response = await chrome.runtime.sendMessage({
          action: "captureEmail",
          data: emailData,
        })

        if (response.success) {
          alert("Email captured successfully!")
          await this.loadStats()
        } else {
          throw new Error(response.error || "Failed to capture email")
        }
      }
    } catch (error) {
      console.error("Error capturing email:", error)
      alert("Failed to capture email: " + error.message)
    }
  }

  extractEmailData() {
    // This function runs in the Gmail tab context
    try {
      // Extract email data from Gmail interface
      const subject = document.querySelector("[data-thread-perm-id] h2, .hP")?.textContent || ""
      const sender = document.querySelector(".go .g2")?.textContent || ""
      const recipient = document.querySelector(".hb .g2")?.textContent || ""
      const body = document.querySelector(".ii.gt .a3s")?.textContent || ""
      const dateElement = document.querySelector(".g3")

      return {
        subject,
        sender,
        recipient,
        body,
        date_sent: dateElement?.getAttribute("title") || new Date().toISOString(),
        url: window.location.href,
        captured_at: new Date().toISOString(),
      }
    } catch (error) {
      console.error("Error extracting email data:", error)
      return null
    }
  }

  async toggleAutoCapture() {
    const settings = await chrome.storage.sync.get(["autoCaptureEnabled"])
    const newState = !settings.autoCaptureEnabled

    await chrome.storage.sync.set({ autoCaptureEnabled: newState })

    const button = document.getElementById("auto-capture")
    if (button) {
      button.textContent = newState ? "🔄 Auto-Capture ON" : "🔄 Auto-Capture OFF"
      button.className = newState ? "btn btn-success" : "btn btn-secondary"
    }
  }

  async generateSummaries() {
    try {
      const response = await fetch(`${this.serverUrl}/api/summarizer/generate`, {
        method: "POST",
      })

      if (response.ok) {
        const data = await response.json()
        alert(`Generated ${data.summaries_generated} summaries!`)
        await this.loadStats()
      } else {
        throw new Error("Failed to generate summaries")
      }
    } catch (error) {
      console.error("Error generating summaries:", error)
      alert("Failed to generate summaries: " + error.message)
    }
  }

  openDashboard() {
    chrome.tabs.create({ url: this.serverUrl })
  }
}

// Initialize popup when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM loaded, initializing popup")
  new LegalBillingPopup()
})
