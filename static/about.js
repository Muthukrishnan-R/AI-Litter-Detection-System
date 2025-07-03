// Add hover effects to sections
const sections = document.querySelectorAll('.about-section');

sections.forEach(section => {
  section.addEventListener('mouseenter', () => {
    section.style.transform = 'translateY(-10px)';
    section.style.boxShadow = '0 8px 25px rgba(0, 0, 0, 0.2)';
  });

  section.addEventListener('mouseleave', () => {
    section.style.transform = 'translateY(0)';
    section.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
  });
});