// ========================================
// Modern Placement Portal - Advanced JS Animations
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== Initialization =====
    initScrollReveal();
    initParallaxEffect();
    initCardAnimations();
    initButtonRipple();
    initCountUpAnimation();
    initTooltips();
    initSmoothScroll();
    initNavbarScroll();
    initFormValidationEffects();
    initChartAnimations();
    
    // ===== Scroll Reveal Animation =====
    function initScrollReveal() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    // Add stagger delay for children
                    const children = entry.target.querySelectorAll('.stagger-item');
                    children.forEach((child, index) => {
                        setTimeout(() => {
                            child.classList.add('revealed');
                        }, index * 100);
                    });
                }
            });
        }, observerOptions);
        
        // Observe cards, stat-cards, and other elements
        document.querySelectorAll('.card, .stat-card, .reveal-on-scroll').forEach(el => {
            el.classList.add('reveal');
            observer.observe(el);
        });
    }
    
    // ===== Parallax Effect on Mouse Move =====
    function initParallaxEffect() {
        document.addEventListener('mousemove', function(e) {
            const cards = document.querySelectorAll('.card, .stat-card');
            const x = e.clientX / window.innerWidth;
            const y = e.clientY / window.innerHeight;
            
            cards.forEach((card, index) => {
                const speed = (index + 1) * 2;
                const xOffset = (x - 0.5) * speed;
                const yOffset = (y - 0.5) * speed;
                
                if (card.classList.contains('parallax-card')) {
                    card.style.transform = `perspective(1000px) rotateY(${xOffset}deg) rotateX(${-yOffset}deg)`;
                }
            });
        });
    }
    
    // ===== Card 3D Tilt Effect =====
    function initCardAnimations() {
        const cards = document.querySelectorAll('.card');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transition = 'transform 0.1s ease';
            });
            
            card.addEventListener('mousemove', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = ((y - centerY) / centerY) * 5;
                const rotateY = ((x - centerX) / centerX) * 5;
                
                this.style.transform = `perspective(1000px) rotateX(${-rotateX}deg) rotateY(${rotateY}deg) translateY(-8px) scale(1.02)`;
            });
            
            card.addEventListener('mouseleave', function() {
                this.style.transition = 'transform 0.3s ease';
                this.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0) scale(1)';
            });
        });
    }
    
    // ===== Advanced Button Ripple Effect =====
    function initButtonRipple() {
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                const ripple = document.createElement('span');
                const rect = this.getBoundingClientRect();
                const size = Math.max(rect.width, rect.height);
                const x = e.clientX - rect.left - size / 2;
                const y = e.clientY - rect.top - size / 2;
                
                ripple.style.width = ripple.style.height = size + 'px';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.classList.add('ripple-effect');
                
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 600);
            });
        });
    }
    
    // ===== Count Up Animation for Stats =====
    function initCountUpAnimation() {
        const statNumbers = document.querySelectorAll('.stat-card h3');
        
        const animateCount = (element) => {
            const target = parseInt(element.innerText);
            if (isNaN(target)) return;
            
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;
            
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    element.innerText = target;
                    clearInterval(timer);
                } else {
                    element.innerText = Math.floor(current);
                }
            }, 16);
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                    entry.target.classList.add('counted');
                    animateCount(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        statNumbers.forEach(num => observer.observe(num));
    }
    
    // ===== Bootstrap Tooltips =====
    function initTooltips() {
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    }
    
    // ===== Smooth Scroll =====
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    // ===== Navbar Scroll Effect =====
    function initNavbarScroll() {
        const navbar = document.querySelector('.navbar');
        let lastScroll = 0;
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }
    
    // ===== Form Input Animation =====
    function initFormValidationEffects() {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('input-focused');
            });
            
            input.addEventListener('blur', function() {
                this.parentElement.classList.remove('input-focused');
                if (this.value) {
                    this.parentElement.classList.add('input-filled');
                } else {
                    this.parentElement.classList.remove('input-filled');
                }
            });
            
            // Add success animation on valid input
            input.addEventListener('input', function() {
                if (this.checkValidity && this.checkValidity()) {
                    this.classList.add('is-valid-animated');
                } else {
                    this.classList.remove('is-valid-animated');
                }
            });
        });
    }
    
    // ===== Chart Animation Enhancement =====
    function initChartAnimations() {
        // Add animation class when charts come into view
        const charts = document.querySelectorAll('canvas');
        
        const chartObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('chart-animate');
                }
            });
        }, { threshold: 0.5 });
        
        charts.forEach(chart => chartObserver.observe(chart));
    }
    
    // ===== Loading Animation =====
    window.addEventListener('load', () => {
        document.body.classList.add('loaded');
        
        // Animate elements on load
        setTimeout(() => {
            document.querySelectorAll('.animate-on-load').forEach((el, index) => {
                setTimeout(() => {
                    el.classList.add('loaded');
                }, index * 100);
            });
        }, 100);
    });
    
    // ===== Floating Action Button (if exists) =====
    const fab = document.querySelector('.fab');
    if (fab) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                fab.classList.add('fab-visible');
            } else {
                fab.classList.remove('fab-visible');
            }
        });
    }
    
});

// ===== Add CSS for Ripple Effect =====
const style = document.createElement('style');
style.textContent = `
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .reveal {
        opacity: 0;
        transform: translateY(30px);
        transition: opacity 0.6s ease, transform 0.6s ease;
    }
    
    .reveal.revealed {
        opacity: 1;
        transform: translateY(0);
    }
    
    .navbar-scrolled {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
    }
    
    .input-focused {
        transform: scale(1.01);
    }
    
    .is-valid-animated {
        animation: successPulse 0.5s ease;
    }
    
    @keyframes successPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .chart-animate canvas {
        animation: chartFadeIn 1s ease-out;
    }
    
    @keyframes chartFadeIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .fab {
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: var(--primary-gradient);
        color: white;
        border: none;
        box-shadow: var(--shadow-lg);
        cursor: pointer;
        transform: scale(0);
        transition: all 0.3s ease;
        z-index: 1000;
    }
    
    .fab.fab-visible {
        transform: scale(1);
    }
    
    .fab:hover {
        transform: scale(1.1);
        box-shadow: var(--shadow-xl);
    }
`;
document.head.appendChild(style);
