// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    console.log('Initializing mobile menu...');
    console.log('navToggle:', navToggle);
    console.log('navMenu:', navMenu);
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Toggle clicked');
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            console.log('Menu active:', navMenu.classList.contains('active'));
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (navToggle && navMenu && !navToggle.contains(event.target) && !navMenu.contains(event.target)) {
            navMenu.classList.remove('active');
            navToggle.classList.remove('active');
        }
    });
    
    // Add click handlers for dropdown toggles on mobile
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                e.stopPropagation();
                const dropdown = this.closest('.nav-dropdown');
                dropdown.classList.toggle('active');
            }
        });
    });
    
    // Populate dropdown menus
    console.log('Populating dropdowns...');
    populateStatesDropdown();
    populateCitiesDropdown();
});

// Populate States dropdown
async function populateStatesDropdown() {
    try {
        console.log('Fetching states from API...');
        const response = await fetch('/api/states');
        const states = await response.json();
        console.log('States received:', states);
        
        // Take first 10 states for dropdown
        const statesList = document.querySelector('.states-list');
        console.log('States list element:', statesList);
        if (statesList) {
            const statesHTML = states.slice(0, 10).map(state => `
                <a href="/state/${state}" class="dropdown-item">${state}</a>
            `).join('');
            statesList.innerHTML = statesHTML;
            console.log('States dropdown populated with:', statesHTML);
        } else {
            console.error('States list element not found');
        }
    } catch (error) {
        console.error('Error loading states:', error);
        // Fallback to hardcoded states if API fails
        const fallbackStates = ['California', 'New York', 'Texas', 'Florida', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan'];
        const statesList = document.querySelector('.states-list');
        if (statesList) {
            statesList.innerHTML = fallbackStates.map(state => `
                <a href="/state/${state}" class="dropdown-item">${state}</a>
            `).join('');
            console.log('Used fallback states');
        }
    }
}

// Populate Cities dropdown
async function populateCitiesDropdown() {
    try {
        console.log('Populating cities dropdown...');
        // Use hardcoded top cities
        const topCities = [
            {name: 'New York', state: 'NY'},
            {name: 'Los Angeles', state: 'CA'},
            {name: 'Chicago', state: 'IL'},
            {name: 'Houston', state: 'TX'},
            {name: 'Phoenix', state: 'AZ'},
            {name: 'Philadelphia', state: 'PA'},
            {name: 'San Antonio', state: 'TX'},
            {name: 'San Diego', state: 'CA'},
            {name: 'Dallas', state: 'TX'},
            {name: 'San Jose', state: 'CA'}
        ];
        
        const citiesList = document.querySelector('.cities-list');
        console.log('Cities list element:', citiesList);
        if (citiesList) {
            const citiesHTML = topCities.map(city => `
                <a href="/city/${city.state}/${city.name}" class="dropdown-item">${city.name}, ${city.state}</a>
            `).join('');
            citiesList.innerHTML = citiesHTML;
            console.log('Cities dropdown populated with:', citiesHTML);
        } else {
            console.error('Cities list element not found');
        }
    } catch (error) {
        console.error('Error loading cities:', error);
    }
}

// Simple anchor link handling
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView();
            }
        });
    });
});

// Form validation and submission
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Basic form validation
            const name = this.querySelector('#name').value.trim();
            const email = this.querySelector('#email').value.trim();
            const message = this.querySelector('#message').value.trim();
            
            if (!name || !email || !message) {
                alert('Please fill in all required fields.');
                return;
            }
            
            if (!isValidEmail(email)) {
                alert('Please enter a valid email address.');
                return;
            }
            
            // Simulate form submission
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                alert('Thank you for your message! We will get back to you soon.');
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
});

// Email validation helper
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Simple element visibility
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in class to elements immediately
    const elements = document.querySelectorAll('.feature-card, .state-card, .business-card, .service-card');
    elements.forEach(el => el.classList.add('fade-in'));
});

// Search functionality (if implemented)
function searchBusinesses(query) {
    const searchResults = document.querySelector('.search-results');
    if (!searchResults) return;
    
    // Simulate search
    const businesses = document.querySelectorAll('.business-card');
    businesses.forEach(business => {
        const businessName = business.querySelector('.business-name').textContent.toLowerCase();
        const businessLocation = business.querySelector('.business-location').textContent.toLowerCase();
        
        if (businessName.includes(query.toLowerCase()) || businessLocation.includes(query.toLowerCase())) {
            business.style.display = 'block';
        } else {
            business.style.display = 'none';
        }
    });
}

// State filter functionality
function filterByState(state) {
    if (state === 'all') {
        // Show all businesses
        const businesses = document.querySelectorAll('.business-card');
        businesses.forEach(business => business.style.display = 'block');
    } else {
        // Filter by state
        const businesses = document.querySelectorAll('.business-card');
        businesses.forEach(business => {
            const businessState = business.querySelector('.business-location').textContent;
            if (businessState.includes(state)) {
                business.style.display = 'block';
            } else {
                business.style.display = 'none';
            }
        });
    }
}

// Rating display helper
function displayRating(rating, container) {
    const stars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    let starsHTML = '';
    for (let i = 0; i < 5; i++) {
        if (i < stars) {
            starsHTML += '⭐';
        } else if (i === stars && hasHalfStar) {
            starsHTML += '⭐';
        } else {
            starsHTML += '☆';
        }
    }
    
    container.innerHTML = starsHTML;
}

// Lazy loading for images (if implemented)
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Simple back to top button
document.addEventListener('DOMContentLoaded', function() {
    // Create back to top button
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '↑';
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: var(--primary-color);
        color: white;
        border: none;
        cursor: pointer;
        font-size: 20px;
        z-index: 1000;
    `;
    
    document.body.appendChild(backToTopBtn);
    
    // Scroll to top when clicked
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo(0, 0);
    });
});

// Add CSS for additional mobile styles
const style = document.createElement('style');
style.textContent = `
    
    .contact-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
    
    .about-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .benefits-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
    }
    
    .benefit {
        background-color: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: var(--radius-md);
    }
    
    .services-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }
    
    .service-card {
        background-color: var(--bg-primary);
        padding: 2rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .service-card:hover {
        transform: translateY(-5px);
    }
    
    .service-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .approach-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .approach-item {
        background-color: var(--bg-secondary);
        padding: 2rem;
        border-radius: var(--radius-lg);
    }
    
    .state-header,
    .city-header,
    .about-header,
    .contact-header,
    .privacy-header {
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
        color: white;
        padding: 3rem 0;
        text-align: center;
    }
    
    .state-stats,
    .city-stats {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin-top: 2rem;
    }
    
    .stat {
        text-align: center;
    }
    
    .stat-number {
        display: block;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    .stat-label {
        color: rgba(255, 255, 255, 0.9);
        font-size: 0.875rem;
    }
    
    .cities-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
    }
    
    .city-card {
        background-color: var(--bg-primary);
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        text-align: center;
        transition: transform 0.2s ease;
    }
    
    .city-card:hover {
        transform: translateY(-3px);
    }
    
    .state-info-content,
    .city-info-content {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
    }
    
    .info-card {
        background-color: var(--bg-secondary);
        padding: 2rem;
        border-radius: var(--radius-lg);
    }
    
    .info-card ul {
        list-style: none;
        padding-left: 0;
    }
    
    .info-card li {
        padding: 0.5rem 0;
        border-bottom: 1px solid var(--border-light);
    }
    
    .info-card li:last-child {
        border-bottom: none;
    }
    
    .info-card li:before {
        content: "✓";
        color: var(--success-color);
        font-weight: bold;
        margin-right: 0.5rem;
    }
    
    .navigation {
        padding: 2rem 0;
        background-color: var(--bg-secondary);
    }
    
    .nav-links {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .no-businesses {
        padding: 4rem 0;
        text-align: center;
    }
    
    .no-businesses-content {
        max-width: 600px;
        margin: 0 auto;
    }
    
    .contact-faq {
        margin-top: 2rem;
    }
    
    .faq-item {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background-color: var(--bg-secondary);
        border-radius: var(--radius-md);
    }
    
    .faq-item h4 {
        margin-bottom: 0.5rem;
        color: var(--text-primary);
    }
    
    .faq-item p {
        margin-bottom: 0;
        color: var(--text-secondary);
    }
    
    .privacy-text {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .privacy-text h2 {
        color: var(--text-primary);
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    .privacy-text h3 {
        color: var(--text-primary);
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .privacy-text ul {
        margin-left: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .privacy-text li {
        margin-bottom: 0.5rem;
    }
    
    .privacy-date {
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
`;

document.head.appendChild(style);
