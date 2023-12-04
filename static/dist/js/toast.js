;(function () {
  const toastElement = document.getElementById("toast")
  const toastBody = document.getElementById("toast-body")
  const toast = new bootstrap.Toast(toastElement, { delay: 2000 })

  htmx.on("showMessage", (e) => {
    toastBody.innerText = e.detail.value
    toast.show()
  })

  // --------
  // Tooltips
  // --------
  // Instantiate all tooltips
  // document.querySelectorAll('[data-bs-toggle="tooltip"]')
  //   .forEach(tooltip => {
  //     new bootstrap.Tooltip(tooltip)
  // })
  // 初始化提示框
  // var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  // var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  //   return new bootstrap.Tooltip(tooltipTriggerEl)
  // }) 

})()