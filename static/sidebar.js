document.addEventListener("DOMContentLoaded", function () {
    const sidebar = document.querySelector(".main-sidebar");
    const menuButton = document.querySelector(".menu-toggle");

    if (menuButton) {
        menuButton.addEventListener("click", function () {
            sidebar.classList.toggle("active");
        });

        // Close sidebar when clicking outside (mobile)
        document.addEventListener("click", function (event) {
            if (!sidebar.contains(event.target) && !menuButton.contains(event.target)) {
                sidebar.classList.remove("active");
            }
        });
    }
});
