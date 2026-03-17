// Hôtel des Quatre Roses – main.js

// Auto-uppercase reference input
document.addEventListener('DOMContentLoaded', () => {
  const refInput = document.querySelector('input[name="reference"]');
  if (refInput) {
    refInput.addEventListener('input', () => {
      refInput.value = refInput.value.toUpperCase();
    });
  }

  // Auto-dismiss flash messages after 4s (fallback if Alpine.js is not loaded)
  const flashContainer = document.querySelector('[x-data*="show"]');
  if (!flashContainer && document.querySelector('.flash-message')) {
    setTimeout(() => {
      document.querySelectorAll('.flash-message').forEach(el => {
        el.style.transition = 'opacity 0.5s';
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 500);
      });
    }, 4000);
  }
});
