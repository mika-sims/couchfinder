$(document).ready(function () {
  // Function to fetch friendship requests via AJAX from the server
  function fetchFriendshipRequests() {
    $.ajax({
      url: "/profiles/display-friendship-requests/",
      type: "GET",
      dataType: "json",
      success: function (data) {
        // Handle the JSON response
        const friendshipRequests = data.friendship_requests;
        const $notificationMenu = $("#notification-menu");
        const $notificationCount = $("#notification-count");
        $notificationMenu.empty();

        // Check if there are any friendship requests
        if (friendshipRequests.length === 0) {
          // If no requests, hide the notification badge
          $notificationCount.hide();
          $notificationMenu.append(
            $("<li>", {
              class: "dropdown-item small",
              text: "No new notifications",
            })
          );
          return;
        }

        // Loop through friendship requests and append notifications
        friendshipRequests.forEach(function (request) {
          const $notificationItem = $("<li>", {
            class: "dropdown-item",
          });

          // Create a link within the notification item
          const $notificationLink = $("<a>", {
            class: "dropdown-item text-secondary small",
            href: `/profiles/profile/${request.id}`,
          });

          const notificationText = $("<span>", {
            class: "fw-bold",
            text: request.from_user,
          }).appendTo($notificationLink);
          $("<span>", {
            text: " sent you a friend request",
          }).appendTo($notificationLink);

          $notificationItem.append($notificationLink);

          $notificationMenu.append($notificationItem);
        });

        const notificationCount = friendshipRequests.length;
        $notificationCount.text(notificationCount).addClass("small").show();
      },
      error: function (error) {
        // Handle any errors that occur during the AJAX call
        console.error(
          "An error occurred while fetching friendship requests.",
          error
        );
      },
    });
  }

  // Call the fetchFriendshipRequests function when the page loads
  fetchFriendshipRequests();
});
