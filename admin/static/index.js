let menuicn = document.querySelector(".menuicn");
let nav = document.querySelector(".navcontainer");

menuicn.addEventListener("click", () => {
	nav.classList.toggle("navclose");
})

const options = document.querySelectorAll('.option1');

options.forEach(option => {
    option.addEventListener('click', function() {
        options.forEach(opt => opt.classList.remove('active'));
        this.classList.add('active');
    });
});

