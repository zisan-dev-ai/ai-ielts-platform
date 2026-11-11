/* AI IELTS App Core JS */
document.addEventListener('DOMContentLoaded', () => {
  console.log('AI IELTS Application initialized.');

  // Dark / Light Theme Toggle
  const themeToggleBtn = document.getElementById('theme-toggle');
  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.body.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.body.setAttribute('data-theme', newTheme);
      localStorage.setItem('ielts_theme', newTheme);
    });

    const savedTheme = localStorage.getItem('ielts_theme');
    if (savedTheme) {
      document.body.setAttribute('data-theme', savedTheme);
    }
  }
});
