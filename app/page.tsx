"use client"

import { useEffect } from "react"
import data from "../static/app"

export default function HomePage() {
  useEffect(() => {
    // Initialize the app when component mounts
    if (typeof window !== "undefined") {
      // Create app instance
      const app = new data.LegalBillingApp()

      // Make checkExtensionStatus available globally
      window.checkExtensionStatus = data.checkExtensionStatus
    }
  }, [])

  return (
    <div>
      <div className="container">
        <header className="header">
          <h1>
            <i className="fas fa-gavel"></i> Legal Billing Email Summarizer
          </h1>
          <p>Automatically fetch Gmail emails, generate AI summaries, and sync with Clio</p>
          <div className="header-actions">
            <button id="chrome-extension-help" className="btn btn-secondary btn-small">
              <i className="fas fa-puzzle-piece"></i> Chrome Extension
            </button>
            <button id="bulk-actions" className="btn btn-secondary btn-small">
              <i className="fas fa-tasks"></i> Bulk Actions
            </button>
          </div>
        </header>

        <div className="status-bar">
          <div className="status-item">
            <span className="status-label">Gmail:</span>
            <span id="gmail-status" className="status-value disconnected">
              Disconnected
            </span>
          </div>
          <div className="status-item">
            <span className="status-label">Clio:</span>
            <span id="clio-status" className="status-value disconnected">
              Disconnected
            </span>
          </div>
          <div className="status-item">
            <span className="status-label">Emails:</span>
            <span id="email-count" className="status-value">
              0
            </span>
          </div>
          <div className="status-item">
            <span className="status-label">Summaries:</span>
            <span id="summary-count" className="status-value">
              0
            </span>
          </div>
          <div className="status-item">
            <span className="status-label">Selected:</span>
            <span id="selected-count" className="status-value">
              0
            </span>
          </div>
        </div>

        <div className="action-panel">
          <div className="action-group">
            <h3>1. Connect Services</h3>
            <button id="connect-gmail" className="btn btn-primary">
              <i className="fab fa-google"></i> Connect Gmail
            </button>
            <button id="connect-clio" className="btn btn-primary">
              <i className="fas fa-link"></i> Connect Clio
            </button>
            <button id="test-clio" className="btn btn-secondary btn-small">
              <i className="fas fa-vial"></i> Test Clio
            </button>
          </div>

          <div className="action-group">
            <h3>2. Email Management</h3>
            <button id="fetch-emails" className="btn btn-secondary">
              <i className="fas fa-envelope"></i> Fetch Emails
            </button>
            <button id="select-all-emails" className="btn btn-secondary btn-small">
              <i className="fas fa-check-square"></i> Select All
            </button>
            <button id="clear-selection" className="btn btn-secondary btn-small">
              <i className="fas fa-square"></i> Clear Selection
            </button>
          </div>

          <div className="action-group">
            <h3>3. AI Processing</h3>
            <button id="generate-summaries" className="btn btn-secondary">
              <i className="fas fa-robot"></i> Generate Summaries
            </button>
            <button id="generate-selected" className="btn btn-secondary btn-small">
              <i className="fas fa-magic"></i> Generate Selected
            </button>
          </div>

          <div className="action-group">
            <h3>4. Export to Clio</h3>
            <button id="push-to-clio" className="btn btn-success">
              <i className="fas fa-upload"></i> Push All to Clio
            </button>
            <button id="push-selected" className="btn btn-success btn-small">
              <i className="fas fa-arrow-up"></i> Push Selected
            </button>
          </div>
        </div>

        <div className="content-area">
          <div className="tabs">
            <button className="tab-button active" data-tab="emails">
              <i className="fas fa-envelope"></i> Emails (<span id="emails-tab-count">0</span>)
            </button>
            <button className="tab-button" data-tab="summaries">
              <i className="fas fa-file-alt"></i> Summaries (<span id="summaries-tab-count">0</span>)
            </button>
            <button className="tab-button" data-tab="extension">
              <i className="fas fa-puzzle-piece"></i> Chrome Extension
            </button>
          </div>

          <div id="emails-tab" className="tab-content active">
            <div className="section-header">
              <h3>Email Management</h3>
              <div className="filters">
                <select id="days-filter">
                  <option value="7">Last 7 days</option>
                  <option value="14">Last 14 days</option>
                  <option value="30">Last 30 days</option>
                </select>
                <select id="email-filter">
                  <option value="all">All Emails</option>
                  <option value="unsummarized">Needs Summary</option>
                  <option value="summarized">Has Summary</option>
                  <option value="unpushed">Not Pushed to Clio</option>
                </select>
                <input type="text" id="search-emails" placeholder="Search emails..." />
              </div>
            </div>
            <div id="emails-list" className="items-list">
              <div className="empty-state">
                <i className="fas fa-envelope-open"></i>
                <p>No emails fetched yet. Click "Fetch Emails" to get started.</p>
              </div>
            </div>
          </div>

          <div id="summaries-tab" className="tab-content">
            <div className="section-header">
              <h3>Generated Summaries</h3>
              <div className="filters">
                <select id="summary-filter">
                  <option value="all">All Summaries</option>
                  <option value="unpushed">Not Pushed to Clio</option>
                  <option value="pushed">Pushed to Clio</option>
                </select>
                <input type="text" id="search-summaries" placeholder="Search summaries..." />
              </div>
            </div>
            <div id="summaries-list" className="items-list">
              <div className="empty-state">
                <i className="fas fa-file-alt"></i>
                <p>No summaries generated yet. Fetch emails and generate summaries first.</p>
              </div>
            </div>
          </div>

          <div id="extension-tab" className="tab-content">
            <div className="extension-guide">
              <h3>
                <i className="fas fa-puzzle-piece"></i> Chrome Extension Setup
              </h3>

              <div className="guide-section">
                <h4>1. Install Extension</h4>
                <ol>
                  <li>
                    Open Chrome and go to <code>chrome://extensions/</code>
                  </li>
                  <li>Enable "Developer mode" (top right toggle)</li>
                  <li>
                    Click "Load unpacked" and select the <code>chrome-extension</code> folder
                  </li>
                  <li>Pin the extension to your toolbar</li>
                </ol>
              </div>

              <div className="guide-section">
                <h4>2. Extension Features</h4>
                <ul>
                  <li>
                    <strong>Auto-capture:</strong> Automatically capture sent emails
                  </li>
                  <li>
                    <strong>Manual capture:</strong> Click the capture button in Gmail
                  </li>
                  <li>
                    <strong>Quick summaries:</strong> Generate summaries from the extension
                  </li>
                  <li>
                    <strong>Dashboard access:</strong> Quick link to this dashboard
                  </li>
                </ul>
              </div>

              <div className="guide-section">
                <h4>3. Extension Status</h4>
                <div id="extension-status" className="status-check">
                  <button onClick={() => window.checkExtensionStatus?.()} className="btn btn-secondary">
                    <i className="fas fa-sync"></i> Check Extension Status
                  </button>
                  <div id="extension-result"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Loading overlay */}
        <div id="loading-overlay" className="loading-overlay hidden">
          <div className="loading-spinner">
            <i className="fas fa-spinner fa-spin"></i>
            <p id="loading-message">Processing...</p>
          </div>
        </div>

        {/* Chrome Extension Help Modal */}
        <div id="extension-modal" className="modal hidden">
          <div className="modal-content">
            <div className="modal-header">
              <h3>
                <i className="fas fa-puzzle-piece"></i> Chrome Extension Guide
              </h3>
              <button id="close-extension-modal" className="close-btn">
                &times;
              </button>
            </div>
            <div className="modal-body">
              <div className="extension-steps">
                <div className="step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <h4>Download Extension Files</h4>
                    <p>
                      The Chrome extension files are in the <code>chrome-extension</code> folder of your project.
                    </p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <h4>Load in Chrome</h4>
                    <p>
                      Go to <code>chrome://extensions/</code>, enable Developer mode, and click "Load unpacked".
                    </p>
                  </div>
                </div>
                <div className="step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <h4>Use in Gmail</h4>
                    <p>Open Gmail and you'll see a "Capture for Billing" button. Click it to capture emails!</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Edit Summary Modal */}
        <div id="edit-modal" className="modal hidden">
          <div className="modal-content">
            <div className="modal-header">
              <h3>Edit Summary</h3>
              <button id="close-modal" className="close-btn">
                &times;
              </button>
            </div>
            <div className="modal-body">
              <div className="form-group">
                <label htmlFor="edit-hours">Billing Hours:</label>
                <input type="number" id="edit-hours" step="0.25" min="0" max="24" />
              </div>
              <div className="form-group">
                <label htmlFor="edit-description">Billing Description:</label>
                <textarea id="edit-description" rows={4}></textarea>
              </div>
              <div className="form-group">
                <label htmlFor="edit-summary">Full Summary:</label>
                <textarea id="edit-summary" rows={6}></textarea>
              </div>
            </div>
            <div className="modal-footer">
              <button id="save-summary" className="btn btn-primary">
                Save Changes
              </button>
              <button id="cancel-edit" className="btn btn-secondary">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Include Font Awesome and styles */}
      <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />
      <style jsx>{`
        @import url('/static/styles.css');
      `}</style>
    </div>
  )
}
