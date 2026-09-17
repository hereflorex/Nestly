const themeButton = document.getElementById('themeBtn');
const savedTheme = localStorage.getItem('nestly-theme') || 'dark';

function applyTheme(theme) {
    document.documentElement.dataset.theme = theme;
    if (themeButton) themeButton.textContent = theme === 'light' ? '☀' : '☾';
}

applyTheme(savedTheme);

if (themeButton) {
    themeButton.addEventListener('click', () => {
        const nextTheme = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
        applyTheme(nextTheme);
        localStorage.setItem('nestly-theme', nextTheme);
    });
}
