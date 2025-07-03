// Add hover effects to table rows
const tableRows = document.querySelectorAll('.past-detections-table tbody tr');

tableRows.forEach(row => {
  row.addEventListener('mouseenter', () => {
    row.style.backgroundColor = 'rgba(255, 204, 0, 0.1)';
  });

  row.addEventListener('mouseleave', () => {
    row.style.backgroundColor = 'transparent';
  });
});

// Add hover effects to images
const images = document.querySelectorAll('.past-detections-table img');

images.forEach(img => {
  img.addEventListener('mouseenter', () => {
    img.style.transform = 'scale(1.1)';
  });

  img.addEventListener('mouseleave', () => {
    img.style.transform = 'scale(1)';
  });
});