document.addEventListener("DOMContentLoaded", () => {

    const categories = document.querySelectorAll(".category");

    categories.forEach(category => {

        category.addEventListener("click", () => {

            categories.forEach(item => {
                item.classList.remove("active");
            });

            category.classList.add("active");

        });

    });


    const addButtons = document.querySelectorAll(".add-button");

    addButtons.forEach(button => {

        button.addEventListener("click", () => {

            button.textContent = "✓";

            setTimeout(() => {
                button.textContent = "+";
            }, 800);

        });

    });

});