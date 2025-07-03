// ScrollReveal Animations
ScrollReveal().reveal('.hero-content', { delay: 300, duration: 1000 });
ScrollReveal().reveal('.feature-card', { interval: 200, duration: 1000 });
ScrollReveal().reveal('.step', { interval: 200, duration: 1000 });
ScrollReveal().reveal('.cta', { delay: 300, duration: 1000 });

// Hover Effects for Cards
const featureCards = document.querySelectorAll('.feature-card');
const steps = document.querySelectorAll('.step');

featureCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px)';
        card.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.2)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
    });
});

steps.forEach(step => {
    step.addEventListener('mouseenter', () => {
        step.style.transform = 'translateY(-10px)';
        step.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.2)';
    });

    step.addEventListener('mouseleave', () => {
        step.style.transform = 'translateY(0)';
        step.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
    });
});