const activePage = window.location.pathname;
const navLinks = document.querySelectorAll('nav a').forEach(
    link => {
        if (link.href.includes(`${activePage}`)){
            link.classList.add('active');
            console.log(activePage)
        }
    }
);
// console.log(activePage)
