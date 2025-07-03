// Add hover effects to info items
const infoItems = document.querySelectorAll('.info-item');

infoItems.forEach(item => {
  item.addEventListener('mouseenter', () => {
    item.style.transform = 'scale(1.05)';
  });

  item.addEventListener('mouseleave', () => {
    item.style.transform = 'scale(1)';
  });
});

// Add hover effects to form button
const formButton = document.querySelector('.form-button');

formButton.addEventListener('mouseenter', () => {
  formButton.style.transform = 'scale(1.05)';
});

formButton.addEventListener('mouseleave', () => {
  formButton.style.transform = 'scale(1)';
});