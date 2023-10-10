function pictureOverlay() {
  let updateImgBtn = document.querySelector(".update-img-btn");
  let profileImgContainer = document.querySelector(
    ".profile-picture_update-page-container"
  );
  let profilePicture = document.querySelector(".profile-picture_update-page");
  let imageUploadInput = document.querySelector("#id_profile_picture");

  profileImgContainer.addEventListener("mouseenter", function () {
    updateImgBtn.classList.remove("opacity-0");
    updateImgBtn.classList.add("opacity-100");
    updateImgBtn.style.transition = "opacity 0.3s, visibility 0s 0.3s";
    profilePicture.style.opacity = "0.5";
    profilePicture.style.transition = "opacity 0.3s";
  });

  profileImgContainer.addEventListener("mouseleave", function () {
    updateImgBtn.classList.remove("opacity-100");
    updateImgBtn.classList.add("opacity-0");
    updateImgBtn.style.transition = "opacity 0.3s, visibility 0s";
    profilePicture.style.opacity = "1";
    profilePicture.style.transition = "opacity 0.3s, visibility 0s";
  });

  // Handle image upload using AJAX
  imageUploadInput.addEventListener("change", function () {
    const formData = new FormData();
    formData.append("profile_picture", imageUploadInput.files[0]);

    fetch("{% url 'profiles:upload_image' %}", {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": "{{ csrf_token }}",
      },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.image_url) {
          // Update the image source
          profilePicture.src = data.image_url;
        } else {
          console.error("Image upload failed:", data.error);
        }
      })
      .catch((error) => {
        console.error("Image upload error:", error);
      });
  });
}
window.addEventListener("DOMContentLoaded", pictureOverlay);
