function setDarkMode() {
    // I have no idea what the first variable is/does
    var isDark = document.body.classList.toggle('darkmode');
    var themeBtn = document.getElementById('theme-btn');

    if(isDark) {
        themeBtn.className = 'btn btn-light'
        themeBtn.innerHTML = 'Light Mode'
    }
    else {
        themeBtn.className = 'btn btn-dark'
        themeBtn.innerHTML = 'Dark Mode'
    }
}