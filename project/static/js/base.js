let close_button = document.getElementById('close-btn');
close_button.addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("window-notification").style.display = "none";
});