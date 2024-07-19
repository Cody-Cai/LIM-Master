;(function () {
  const modal = new bootstrap.Modal(document.getElementById("modal"));
  const txtElement = document.getElementById("txtmodal");
  if (txtElement) {
    txtmodal = new bootstrap.Modal(txtElement);
  }

  htmx.on("htmx:afterSwap", (e) => {
    // Response targeting #dialog => show the modal
    if (e.detail.target.id == "dialog") {
      modal.show()
    }
    if (e.detail.target.id == "txtdialog") {
      txtmodal.show()
    }
  })
  
  htmx.on("htmx:beforeSwap", (e) => {
    // Empty response targeting #dialog => hide the modal
    if (e.detail.target.id == "dialog" && !e.detail.xhr.response) {
      modal.hide()
      e.detail.shouldSwap = false
    }
    if (e.detail.target.id == "txtdialog" && !e.detail.xhr.response) {
      txtmodal.hide()
      e.detail.shouldSwap = false
    }
  })

  // Remove dialog content after hiding
  htmx.on("hidden.bs.modal", () => {
    document.getElementById("dialog").innerHTML = ""
  })

  if (txtmodal) {  
    // Remove dialog content after hiding
    htmx.on("hidden.bs.modal", () => {
      document.getElementById("txtdialog").innerHTML = ""
    })
  }
  
})()
