function clicked_img(img,fp){
          console.log(img.src);

          var top=document.getElementById('top')

          top.src = img.src;

          top.hidden=false;


          if (img.naturalWidth<screen.width*0.6 && img.naturalHeight<screen.height*0.6) {

            top.width=img.naturalWidth;
            top.height=img.naturalHeight;

          } else {

            top.width=screen.width*0.6;
            top.height=img.naturalHeight/img.naturalWidth*top.width;

          }

          document.getElementById('close').hidden = false;
 }


function do_close(){
  document.getElementById('top').hidden=true;
  document.getElementById('close').hidden=true;
}

document.addEventListener("DOMContentLoaded", function () {
  const deleteButtons = document.querySelectorAll(".delete-btn");

  deleteButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const path = button.getAttribute("data-path");

      // Send a request to the server to delete the photo
      fetch(`/delete-photo?path=${path}`, {
        method: "DELETE",
      })
        .then(response => {
          if (response.ok) {
            // If the response is successful, remove the photo container from the DOM
            const photoContainer = button.closest(".photo-container");
            photoContainer.remove();
          } else {
            console.error("Failed to delete photo");
          }
        })
        .catch(error => console.error("Error:", error));
    });
  });
});

function clicked_img(img) {
  document.getElementById("top").src = img.src;
  document.getElementById("top").hidden = false;
  document.getElementById("close").hidden = false;
  document.querySelector(".overlay").style.display = "flex";
}

function do_close() {
  document.getElementById("top").hidden = true;
  document.getElementById("close").hidden = true;
  document.querySelector(".overlay").style.display = "none";
}
