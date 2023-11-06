// Checks if the navbar is expanded, if so, collapse it
function toggleNavbarCollapse() {
    const navbar = document.querySelector('#navbarResponsive');
    if (navbar.classList.contains('show')) {
      document.querySelector('.navbar-toggler').click();
    }
  }
  