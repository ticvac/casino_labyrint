document.addEventListener("DOMContentLoaded", function() {
    const achievementIcons = document.querySelectorAll(".achievement-icon");
    achievementIcons.forEach(icon => {
        icon.addEventListener("click", function() {
            alert("Achievement unlocked: " + this.dataset.text);
        });
    });
});
