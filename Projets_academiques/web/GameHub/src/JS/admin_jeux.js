document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.games-wrapper');
    const prevBtn = document.getElementById('games-prev');
    const nextBtn = document.getElementById('games-next');
  
    if (!wrapper || !prevBtn || !nextBtn) return;
  
    const scrollAmount = wrapper.offsetWidth;
  
    nextBtn.addEventListener('click', () => {
      wrapper.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
  
    prevBtn.addEventListener('click', () => {
      wrapper.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
  });
  