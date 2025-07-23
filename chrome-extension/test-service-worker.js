// Simple test to verify service worker functionality
console.log("Service worker test file loaded")

// Declare the chrome variable
const chrome = window.chrome

// Test basic functionality
function testServiceWorker() {
  console.log("Testing service worker...")

  // Test storage
  chrome.storage.sync.set({ test: "value" }, () => {
    console.log("Storage test: SET completed")

    chrome.storage.sync.get(["test"], (result) => {
      console.log("Storage test: GET result:", result)
    })
  })

  // Test runtime
  console.log("Runtime available:", !!chrome.runtime)
  console.log("Extension ID:", chrome.runtime.id)
}

// Run test
testServiceWorker()
