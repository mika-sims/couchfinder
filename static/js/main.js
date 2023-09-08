// Disappear the alert message after 2.5 seconds adding the class animate__fadeOut
function disappearAlertMessage() {
  const messages = document.getElementById("messages");
  if (messages) {
    setTimeout(() => {
      messages.classList.add("animate__fadeOut");
    }, 2500);
  }
}

disappearAlertMessage();
