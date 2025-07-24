"use client"

import { useEffect } from "react"

export default function HomePage() {
  useEffect(() => {
    // Redirect to the static HTML page
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
        flexDirection: "column",
      }}
    >
      <h1>Legal Billing Email Summarizer</h1>
      <p>Redirecting to application...</p>
      <p>
        If not redirected automatically, <a href="/static/index.html">click here</a>
      </p>
    </div>
  )
}
