// Declare the chrome variable to fix the lint error
const chrome = window.chrome

class GmailCapture {
  constructor() {
    this.init()
  }

  async init() {
    // Check if auto-capture is enabled
    const settings = await chrome.storage.sync.get(["autoCaptureEnabled", "serverUrl"])

    if (settings.autoCaptureEnabled) {
      this.setupAutoCapture()
    }

    this.addCaptureButton()
  }

  setupAutoCapture() {
    // Monitor for sent emails
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === "childList") {
          // Check for sent email confirmation
          const sentConfirmation = document.querySelector('[data-message-text*="sent"], .aH')
          if (sentConfirmation && !sentConfirmation.dataset.captured) {
            sentConfirmation.dataset.captured = "true"
            this.autoCaptureSentEmail()
          }
        }
      })
    })

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    })
  }

  addCaptureButton() {
    // Add capture button to Gmail interface
    const toolbar = document.querySelector(".ar9.T-I-J3.J-J5-Ji")
    if (toolbar && !document.getElementById("legal-billing-capture")) {
      const button = document.createElement("div")
      button.id = "legal-billing-capture"
      button.className = "T-I J-J5-Ji T-I-KE L3"
      button.innerHTML = "⚖️ Capture for Billing"
      button.style.cssText = `
                background: #3b82f6;
                color: white;
                margin-left: 10px;
                cursor: pointer;
                padding: 8px 12px;
                border-radius: 4px;
                font-size: 12px;
            `

      button.addEventListener("click", () => this.captureCurrentEmail())
      toolbar.appendChild(button)
    }
  }

  async captureCurrentEmail() {
    try {
      const emailData = this.extractEmailData()
      if (!emailData) {
        alert("Could not extract email data")
        return
      }

      const settings = await chrome.storage.sync.get(["serverUrl"])
      const serverUrl = settings.serverUrl || "http://127.0.0.1:8000"

      const response = await fetch(`${serverUrl}/api/extension/capture-email`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(emailData),
      })

      if (response.ok) {
        this.showNotification("Email captured for billing!", "success")
      } else {
        throw new Error("Server error")
      }
    } catch (error) {
      console.error("Capture error:", error)
      this.showNotification("Failed to capture email", "error")
    }
  }

  extractEmailData() {
    try {
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
        source: "chrome_extension",
      }
    } catch (error) {
      console.error("Error extracting email data:", error)
      return null
    }
  }

  showNotification(message, type = "info") {
    const notification = document.createElement("div")
    notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            background: ${type === "success" ? "#10b981" : "#ef4444"};
        `
    notification.textContent = message

    document.body.appendChild(notification)

    setTimeout(() => {
      notification.remove()
    }, 3000)
  }

  async autoCaptureSentEmail() {
    // Wait a moment for the email to be fully sent
    setTimeout(() => {
      this.captureCurrentEmail()
    }, 2000)
  }
}

// Initialize when Gmail loads
if (window.location.hostname === "mail.google.com") {
  new GmailCapture()
}
