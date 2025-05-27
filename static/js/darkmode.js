document.addEventListener('DOMContentLoaded', function() {
    // Get stored theme preference
    const storedTheme = localStorage.getItem('theme');
    
    // Apply stored theme if available, otherwise use system preference
    if (storedTheme) {
        document.documentElement.setAttribute('data-bs-theme', storedTheme);
    } else {
        const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
        document.documentElement.setAttribute('data-bs-theme', prefersDarkMode ? 'dark' : 'light');
    }
    
    // Update toggle button state
    updateThemeToggle();
    
    // Theme toggle functionality
    document.getElementById('theme-toggle').addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Update theme
        document.documentElement.setAttribute('data-bs-theme', newTheme);
        
        // Save preference to localStorage
        localStorage.setItem('theme', newTheme);
        
        // Update toggle button
        updateThemeToggle();
    });
    
    // Function to update the toggle button appearance
    function updateThemeToggle() {
        const currentTheme = document.documentElement.getAttribute('data-bs-theme');
        const themeToggle = document.getElementById('theme-toggle');
        const moonIcon = document.getElementById('moon-icon');
        const sunIcon = document.getElementById('sun-icon');
        
        if (currentTheme === 'dark') {
            moonIcon.classList.add('d-none');
            sunIcon.classList.remove('d-none');
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
        } else {
            sunIcon.classList.add('d-none');
            moonIcon.classList.remove('d-none');
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
        }
    }
});
