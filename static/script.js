// // Wait for the DOM to be fully loaded
// document.addEventListener("DOMContentLoaded", function () {
//     // Get all the like and dislike buttons by their data-recipe-id
//     const likeButtons = document.querySelectorAll(".like i[data-recipe-id]");
//     const dislikeButtons = document.querySelectorAll(".dislike i[data-recipe-id]");
  
//     // Add click event listeners to the like buttons
//     likeButtons.forEach((likeButton) => {
//       likeButton.addEventListener("click", function () {
//         // Get the data-recipe-id from the clicked button
//         const recipeId = this.getAttribute("data-recipe-id");

  
//         // Find the corresponding dislike button and change its color to black
//         const correspondingDislikeButton = document.querySelector(
//           `.dislike i[data-recipe-id="${recipeId}"]`
//         );
//         if (correspondingDislikeButton) {
//           correspondingDislikeButton.classList.toggle = "black";
//         }
  
//         // Change the color of the clicked like button to red
//         this.classList.toggle = "red";
//       });
//     });
  
//     // Add click event listeners to the dislike buttons
//     dislikeButtons.forEach((dislikeButton) => {
//       dislikeButton.addEventListener("click", function () {
//         // Get the data-recipe-id from the clicked button
//         const recipeId = this.getAttribute("data-recipe-id");
  
//         // Find the corresponding like button and change its color to black
//         const correspondingLikeButton = document.querySelector(
//           `.like i[data-recipe-id="${recipeId}"]`
//         );
//         if (correspondingLikeButton) {
//           correspondingLikeButton.classList.toggle = "black";
//         }
  
//         // Change the color of the clicked dislike button to red
//         this.classList.toggle = "red";
//       });
//     });
//   });
//   js file
// Toggle the 'red' class when the link is clicked
$('.up').on('click', function() {
    $(this).addClass('red');

  });
  
  // You can do the same for the 'down' link if needed
  $('.down').on('click', function() {
    $(this).addClass('red');
  });
  

