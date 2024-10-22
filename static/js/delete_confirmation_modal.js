var deleteModal = document.getElementById("deleteModal");

// When the modal is shown, set the user name and form action
deleteModal.addEventListener("show.bs.modal", function (event) {
  var button = event.relatedTarget; // Button that triggered the modal
  var userId = button.getAttribute("data-user-id"); // Extract user ID from data-* attributes
  var userName = button.getAttribute("data-user-name"); // Extract user name
  var url = button.getAttribute("data-url-name"); // Extract user delete URL

  // Update the modal content
  var userNameElement = document.getElementById("user-name");
  userNameElement.textContent = userName;

  // Update the form action to point to the correct delete URL
  var form = document.getElementById("delete-form");
  form.action = url; // Set the action URL directly from the data attribute
});
