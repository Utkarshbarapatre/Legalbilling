"use client"

import { useEffect } from "react"

export default function SyntheticV0PageForDeployment() {
  useEffect(() => {
    // Redirect to the main application
    window.location.href = "/static/index.html"
  }, [])

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1>Legal Billing Email Summarizer</h1>
        <p>Redirecting to application...</p>
        <p>
          If not redirected, <a href="/static/index.html">click here</a>
        </p>
      </div>
    </div>
  )
}
