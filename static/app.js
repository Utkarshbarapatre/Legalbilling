class LegalBillingApp {
  constructor() {
    this.selectedEmails = new Set()
    this.allEmails = []
    this.allSummaries = []
    this.init()
    this.bindEvents()
    this.checkConnectionStatus()
  }

  init() {
    this.loadingOverlay = document.getElementById("loading-overlay")
    this.loadingMessage = document.getElementById("loading-message")

    // Status elements
    this.gmailStatus = document.getElementById("gmail-status")
    this.clioStatus = document.getElementById("clio-status")
    this.emailCount = document.getElementById("email-count")
    this.summaryCount = document.getElementById("summary-count")
    this.selectedCount = document.getElementById("selected-count")

    // Lists
    this.emailsList = document.getElementById("emails-list")
    this.summariesList = document.getElementById("summaries-list")

    // Modals
    this.editModal = document.getElementById("edit-modal")
    this.extensionModal = document.getElementById("extension-modal")
    this.currentEditId = null

    console.log("Advanced Legal Billing App initialized")
  }

  bindEvents() {
    // Tab switching
    document.querySelectorAll(".tab-button").forEach((button) => {
      button.addEventListener("click", (e) => {
        this.switchTab(e.target.closest(".tab-button").dataset.tab)
      })
    })

    // Action buttons
    document.getElementById("connect-gmail").addEventListener("click", () => this.connectGmail())
    document.getElementById("connect-clio").addEventListener("click", () => this.connectClio())
    document.getElementById("test-clio").addEventListener("click", () => this.testClio())
    document.getElementById("fetch-emails").addEventListener("click", () => this.fetchEmails())
    document.getElementById("generate-summaries").addEventListener("click", () => this.generateSummaries())
    document.getElementById("generate-selected").addEventListener("click", () => this.generateSelectedSummaries())
    document.getElementById("push-to-clio").addEventListener("click", () => this.pushToClio())
    document.getElementById("push-selected").addEventListener("click", () => this.pushSelectedToClio())

    // Selection buttons
    document.getElementById("select-all-emails").addEventListener("click", () => this.selectAllEmails())
    document.getElementById("clear-selection").addEventListener("click", () => this.clearSelection())

    // Chrome extension
    document.getElementById("chrome-extension-help").addEventListener("click", () => this.showExtensionModal())
    document.getElementById("close-extension-modal").addEventListener("click", () => this.hideExtensionModal())

    // Modal events
    document.getElementById("close-modal").addEventListener("click", () => this.closeModal())
    document.getElementById("cancel-edit").addEventListener("click", () => this.closeModal())
    document.getElementById("save-summary").addEventListener("click", () => this.saveSummary())

    // Filters
    document.getElementById("days-filter").addEventListener("change", () => this.fetchEmails())
    document.getElementById("email-filter").addEventListener("change", () => this.filterEmails())
    document.getElementById("summary-filter").addEventListener("change", () => this.filterSummaries())
    document.getElementById("search-emails").addEventListener("input", () => this.searchEmails())
    document.getElementById("search-summaries").addEventListener("input", () => this.searchSummaries())
  }

  switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll(".tab-button").forEach((btn) => btn.classList.remove("active"))
    document.querySelector(`[data-tab="${tabName}"]`).classList.add("active")

    // Update tab content
    document.querySelectorAll(".tab-content").forEach((content) => content.classList.remove("active"))
    document.getElementById(`${tabName}-tab`).classList.add("active")

    // Load data for specific tabs
    if (tabName === "summaries") {
      this.loadSummaries()
    } else if (tabName === "emails") {
      this.loadStoredEmails()
    }
  }

  showLoading(message = "Processing...") {
    this.loadingMessage.textContent = message
    this.loadingOverlay.classList.remove("hidden")
  }

  hideLoading() {
    this.loadingOverlay.classList.add("hidden")
  }

  showExtensionModal() {
    this.extensionModal.classList.remove("hidden")
  }

  hideExtensionModal() {
    this.extensionModal.classList.add("hidden")
  }

  async checkConnectionStatus() {
    // Check URL parameters for connection status
    const urlParams = new URLSearchParams(window.location.search)
    if (urlParams.get("clio_connected") === "true") {
      this.clioStatus.textContent = "Connected"
      this.clioStatus.className = "status-value connected"
      console.log("Clio connection successful")
      window.history.replaceState({}, document.title, window.location.pathname)
    }

    // Load counts
    await this.updateCounts()
  }

  async updateCounts() {
    try {
      const emailsResponse = await fetch("/api/gmail/emails/stored")
      const emailsData = await emailsResponse.json()
      const emailCount = emailsData.emails?.length || 0
      this.emailCount.textContent = emailCount
      document.getElementById("emails-tab-count").textContent = emailCount

      const summariesResponse = await fetch("/api/summarizer/summaries")
      const summariesData = await summariesResponse.json()
      const summaryCount = summariesData.summaries?.length || 0
      this.summaryCount.textContent = summaryCount
      document.getElementById("summaries-tab-count").textContent = summaryCount

      this.selectedCount.textContent = this.selectedEmails.size
    } catch (error) {
      console.error("Error updating counts:", error)
    }
  }

  async connectGmail() {
    this.showLoading("Connecting to Gmail...")
    console.log("Initiating Gmail connection")

    try {
      const response = await fetch("/api/gmail/authenticate", {
        method: "POST",
      })

      const data = await response.json()

      if (data.success) {
        this.gmailStatus.textContent = "Connected"
        this.gmailStatus.className = "status-value connected"
        console.log("Gmail connected successfully")
      } else {
        throw new Error(data.message || "Gmail connection failed")
      }
    } catch (error) {
      console.error(`Gmail connection error: ${error.message}`)
      alert("Gmail connection failed. Please check your credentials.")
    } finally {
      this.hideLoading()
    }
  }

  async connectClio() {
    this.showLoading("Redirecting to Clio...")
    console.log("Initiating Clio connection")

    try {
      const response = await fetch("/api/clio/auth")
      const data = await response.json()

      if (data.auth_url) {
        window.location.href = data.auth_url
      } else {
        throw new Error("Failed to get Clio auth URL")
      }
    } catch (error) {
      console.error(`Clio connection error: ${error.message}`)
      alert("Clio connection failed. Please try again.")
      this.hideLoading()
    }
  }

  async testClio() {
    this.showLoading("Testing Clio connection...")

    try {
      const response = await fetch("/api/clio/test")
      const data = await response.json()

      if (data.connected) {
        alert(`Clio test successful!\nUser: ${data.user?.name || "Unknown"}\nMessage: ${data.message}`)
        this.clioStatus.textContent = "Connected"
        this.clioStatus.className = "status-value connected"
      } else {
        alert(`Clio test failed: ${data.message}`)
      }
    } catch (error) {
      console.error("Clio test error:", error)
      alert("Clio test failed. Please check your connection.")
    } finally {
      this.hideLoading()
    }
  }

  async fetchEmails() {
    const daysBack = document.getElementById("days-filter").value
    this.showLoading("Fetching emails from Gmail...")
    console.log(`Fetching emails from last ${daysBack} days`)

    try {
      const response = await fetch(`/api/gmail/emails?days_back=${daysBack}&max_results=100`)
      const data = await response.json()

      if (data.success) {
        console.log(`Fetched ${data.emails_fetched} emails (${data.new_emails} new)`)
        this.allEmails = data.emails || []
        this.displayEmails(this.allEmails)
        this.updateCounts()
      } else {
        throw new Error("Failed to fetch emails")
      }
    } catch (error) {
      console.error(`Email fetch error: ${error.message}`)
      alert("Failed to fetch emails. Please check your Gmail connection.")
    } finally {
      this.hideLoading()
    }
  }

  async loadStoredEmails() {
    try {
      const response = await fetch("/api/gmail/emails/stored")
      const data = await response.json()
      this.allEmails = data.emails || []
      this.displayEmails(this.allEmails)
    } catch (error) {
      console.error("Error loading stored emails:", error)
    }
  }

  displayEmails(emails) {
    if (!emails || emails.length === 0) {
      this.emailsList.innerHTML = `
        <div class="empty-state">
          <i class="fas fa-envelope-open"></i>
          <p>No emails found for the selected criteria.</p>
        </div>
      `
      return
    }

    this.emailsList.innerHTML = emails
      .map((email, index) => {
        const emailId = email.id || index
        const isSelected = this.selectedEmails.has(emailId)
        return `
          <div class="email-item ${isSelected ? "selected" : ""}" data-email-id="${emailId}">
            <input type="checkbox" class="item-checkbox" ${isSelected ? "checked" : ""} 
                   onchange="app.toggleEmailSelection('${emailId}')">
            <div class="item-header">
              <div>
                <div class="item-title">${this.escapeHtml(email.subject || "No Subject")}</div>
                <div class="item-meta">
                  From: ${this.escapeHtml(email.sender || "Unknown")} | 
                  To: ${this.escapeHtml(email.recipient || "Unknown")} | 
                  ${email.date_sent ? new Date(email.date_sent).toLocaleString() : "Unknown date"}
                </div>
              </div>
            </div>
            <div class="item-content">
              ${this.truncateText(this.escapeHtml(email.body || ""), 200)}
            </div>
            <div class="item-actions">
              <button class="btn btn-small btn-secondary" onclick="app.generateSingleSummary('${emailId}')">
                <i class="fas fa-magic"></i> Generate Summary
              </button>
              ${
                email.summary
                  ? `
                <button class="btn btn-small btn-success" onclick="app.viewSummary('${emailId}')">
                  <i class="fas fa-eye"></i> View Summary
                </button>
              `
                  : ""
              }
            </div>
          </div>
        `
      })
      .join("")
  }

  toggleEmailSelection(emailId) {
    if (this.selectedEmails.has(emailId)) {
      this.selectedEmails.delete(emailId)
    } else {
      this.selectedEmails.add(emailId)
    }

    // Update visual state
    const emailItem = document.querySelector(`[data-email-id="${emailId}"]`)
    if (emailItem) {
      emailItem.classList.toggle("selected", this.selectedEmails.has(emailId))
    }

    this.updateCounts()
  }

  selectAllEmails() {
    this.allEmails.forEach((email, index) => {
      this.selectedEmails.add(email.id || index)
    })
    this.displayEmails(this.allEmails)
    this.updateCounts()
  }

  clearSelection() {
    this.selectedEmails.clear()
    this.displayEmails(this.allEmails)
    this.updateCounts()
  }

  filterEmails() {
    const filter = document.getElementById("email-filter").value
    let filteredEmails = [...this.allEmails]

    switch (filter) {
      case "unsummarized":
        filteredEmails = this.allEmails.filter((email) => !email.summary)
        break
      case "summarized":
        filteredEmails = this.allEmails.filter((email) => email.summary)
        break
      case "unpushed":
        filteredEmails = this.allEmails.filter((email) => !email.pushed_to_clio)
        break
    }

    this.displayEmails(filteredEmails)
  }

  searchEmails() {
    const searchTerm = document.getElementById("search-emails").value.toLowerCase()
    if (!searchTerm) {
      this.filterEmails()
      return
    }

    const filteredEmails = this.allEmails.filter(
      (email) =>
        (email.subject || "").toLowerCase().includes(searchTerm) ||
        (email.sender || "").toLowerCase().includes(searchTerm) ||
        (email.body || "").toLowerCase().includes(searchTerm),
    )

    this.displayEmails(filteredEmails)
  }

  async generateSummaries() {
    this.showLoading("Generating AI summaries for all emails...")
    console.log("Starting AI summary generation for all emails")

    try {
      const response = await fetch("/api/summarizer/generate", {
        method: "POST",
      })

      const data = await response.json()

      if (data.success) {
        console.log(`Generated ${data.summaries_generated} summaries`)
        if (data.errors && data.errors.length > 0) {
          console.warn("Some errors occurred:", data.errors)
        }
        alert(`Generated ${data.summaries_generated} summaries successfully!`)
        this.updateCounts()
        this.loadStoredEmails()
      } else {
        throw new Error("Failed to generate summaries")
      }
    } catch (error) {
      console.error(`Summary generation error: ${error.message}`)
      alert("Failed to generate summaries. Please try again.")
    } finally {
      this.hideLoading()
    }
  }

  async generateSelectedSummaries() {
    if (this.selectedEmails.size === 0) {
      alert("Please select emails first")
      return
    }

    this.showLoading(`Generating summaries for ${this.selectedEmails.size} selected emails...`)
    await this.generateSummaries()
  }

  async generateSingleSummary(emailId) {
    this.showLoading("Generating summary for this email...")

    try {
      const response = await fetch("/api/summarizer/generate", {
        method: "POST",
      })

      const data = await response.json()

      if (data.success) {
        alert("Summary generated successfully!")
        this.loadStoredEmails()
      } else {
        throw new Error("Failed to generate summary")
      }
    } catch (error) {
      console.error("Error generating single summary:", error)
      alert("Failed to generate summary. Please try again.")
    } finally {
      this.hideLoading()
    }
  }

  async loadSummaries() {
    try {
      const response = await fetch("/api/summarizer/summaries")
      const data = await response.json()
      this.allSummaries = data.summaries || []
      this.displaySummaries(this.allSummaries)
    } catch (error) {
      console.error(`Error loading summaries: ${error.message}`)
    }
  }

  displaySummaries(summaries) {
    if (!summaries || summaries.length === 0) {
      this.summariesList.innerHTML = `
        <div class="empty-state">
          <i class="fas fa-file-alt"></i>
          <p>No summaries generated yet.</p>
        </div>
      `
      return
    }

    this.summariesList.innerHTML = summaries
      .map(
        (summary) => `
        <div class="summary-item">
          <div class="item-header">
            <div>
              <div class="item-title">${this.escapeHtml(summary.subject || "No Subject")}</div>
              <div class="item-meta">
                ${summary.date_sent ? new Date(summary.date_sent).toLocaleString() : "Unknown date"} | 
                Clio: ${summary.pushed_to_clio ? "✅ Pushed" : "❌ Not pushed"}
              </div>
            </div>
            <div class="item-actions">
              <button class="btn btn-small btn-secondary" onclick="app.editSummary(${summary.id})">
                <i class="fas fa-edit"></i> Edit
              </button>
              ${
                !summary.pushed_to_clio
                  ? `
                <button class="btn btn-small btn-success" onclick="app.pushSingleToClio(${summary.id})">
                  <i class="fas fa-upload"></i> Push to Clio
                </button>
              `
                  : ""
              }
            </div>
          </div>
          <div class="billing-info">
            <div class="billing-hours">⏱️ Hours: ${summary.billing_hours || "0.25"}</div>
            <div><strong>Description:</strong> ${this.escapeHtml(summary.billing_description || "")}</div>
          </div>
          <div class="item-content">
            <strong>Summary:</strong><br>
            ${this.escapeHtml(summary.summary || "")}
          </div>
        </div>
      `,
      )
      .join("")
  }

  filterSummaries() {
    const filter = document.getElementById("summary-filter").value
    let filteredSummaries = [...this.allSummaries]

    switch (filter) {
      case "unpushed":
        filteredSummaries = this.allSummaries.filter((summary) => !summary.pushed_to_clio)
        break
      case "pushed":
        filteredSummaries = this.allSummaries.filter((summary) => summary.pushed_to_clio)
        break
    }

    this.displaySummaries(filteredSummaries)
  }

  searchSummaries() {
    const searchTerm = document.getElementById("search-summaries").value.toLowerCase()
    if (!searchTerm) {
      this.filterSummaries()
      return
    }

    const filteredSummaries = this.allSummaries.filter(
      (summary) =>
        (summary.subject || "").toLowerCase().includes(searchTerm) ||
        (summary.summary || "").toLowerCase().includes(searchTerm) ||
        (summary.billing_description || "").toLowerCase().includes(searchTerm),
    )

    this.displaySummaries(filteredSummaries)
  }

  editSummary(summaryId) {
    const summary = this.allSummaries.find((s) => s.id === summaryId)
    if (summary) {
      this.currentEditId = summaryId
      document.getElementById("edit-hours").value = summary.billing_hours || "0.25"
      document.getElementById("edit-description").value = summary.billing_description || ""
      document.getElementById("edit-summary").value = summary.summary || ""
      this.editModal.classList.remove("hidden")
    }
  }

  closeModal() {
    this.editModal.classList.add("hidden")
    this.currentEditId = null
  }

  async saveSummary() {
    if (!this.currentEditId) return

    const summaryData = {
      billing_hours: document.getElementById("edit-hours").value,
      billing_description: document.getElementById("edit-description").value,
      summary: document.getElementById("edit-summary").value,
    }

    try {
      const response = await fetch(`/api/summarizer/summaries/${this.currentEditId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(summaryData),
      })

      const data = await response.json()

      if (data.success) {
        console.log("Summary updated successfully")
        this.closeModal()
        this.loadSummaries()
      } else {
        throw new Error("Failed to update summary")
      }
    } catch (error) {
      console.error(`Error updating summary: ${error.message}`)
      alert("Failed to update summary. Please try again.")
    }
  }

  async pushToClio() {
    this.showLoading("Pushing all summaries to Clio...")
    console.log("Starting Clio push for all summaries")

    try {
      const response = await fetch("/api/clio/push-entries", {
        method: "POST",
      })

      const data = await response.json()

      if (data.success) {
        console.log(`Pushed ${data.pushed_count} entries to Clio`)
        if (data.errors && data.errors.length > 0) {
          console.warn("Some errors occurred:", data.errors)
        }
        alert(`Successfully pushed ${data.pushed_count} entries to Clio!`)
        this.loadSummaries()
      } else {
        throw new Error("Failed to push to Clio")
      }
    } catch (error) {
      console.error(`Clio push error: ${error.message}`)
      alert("Failed to push to Clio. Please check your connection and try the test button first.")
    } finally {
      this.hideLoading()
    }
  }

  async pushSelectedToClio() {
    if (this.selectedEmails.size === 0) {
      alert("Please select emails first")
      return
    }

    await this.pushToClio()
  }

  async pushSingleToClio(summaryId) {
    this.showLoading("Pushing summary to Clio...")

    try {
      const response = await fetch("/api/clio/push-entries", {
        method: "POST",
      })

      const data = await response.json()

      if (data.success) {
        alert("Summary pushed to Clio successfully!")
        this.loadSummaries()
      } else {
        throw new Error("Failed to push to Clio")
      }
    } catch (error) {
      console.error("Error pushing single summary:", error)
      alert("Failed to push to Clio. Please try again.")
    } finally {
      this.hideLoading()
    }
  }

  escapeHtml(text) {
    if (!text) return ""
    const div = document.createElement("div")
    div.textContent = text
    return div.innerHTML
  }

  truncateText(text, maxLength) {
    if (!text || text.length <= maxLength) return text
    return text.substring(0, maxLength) + "..."
  }
}

// Extension status check function
function checkExtensionStatus() {
  const result = document.getElementById("extension-result")
  result.innerHTML = "<p>Checking extension status...</p>"

  setTimeout(() => {
    result.innerHTML = `
      <div class="guide-section">
        <h4>Extension Status</h4>
        <p>✅ Dashboard is running and ready</p>
        <p>📧 Server URL: ${window.location.origin}</p>
        <p>🔗 Make sure your extension points to this URL</p>
      </div>
    `
  }, 1000)
}

// Initialize the application
const app = new LegalBillingApp()

// Export the app class for Next.js import
const data = {
  LegalBillingApp,
  checkExtensionStatus,
}

export default data
