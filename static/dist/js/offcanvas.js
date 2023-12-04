;(function () {
  // --------
  // offcanvas
  // --------
  const offcanvas = new bootstrap.Offcanvas(document.getElementById("offcanvas"))
  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the offcanvas
    if (e.detail.target.id == "offcanvas") {
      offcanvas.show()
    }
  })
  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the offcanvas
    if (e.detail.target.id == "offcanvas" && !e.detail.xhr.response) {
      offcanvas.hide()
      e.detail.shouldSwap = false
    }
  })
  // Remove dialog content after hiding
  htmx.on("hidden.bs.offcanvas", () => {
    document.getElementById("offcanvas").innerHTML = ""
  })
})()
