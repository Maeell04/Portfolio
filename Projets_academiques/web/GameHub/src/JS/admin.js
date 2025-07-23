(function(){
  const prev = document.getElementById('user-prev');
  const next = document.getElementById('user-next');
  const rows = Array.from(document.querySelectorAll('#user-table tbody tr'));
  let start = 0, perPage = 5;
  function render() {
    rows.forEach((r,i)=> r.style.display = (i>=start && i<start+perPage)?'':'none');
  }
  prev.addEventListener('click', ()=>{ start = Math.max(0, start - perPage); render(); });
  next.addEventListener('click', ()=>{ if(start + perPage < rows.length){ start += perPage; render(); }});
  render();
})();

document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.querySelector('.games-carousel');
  const prevBtn  = document.getElementById('games-prev');
  const nextBtn  = document.getElementById('games-next');

  const scrollAmount = document.querySelector('.games-wrapper').offsetWidth;

  nextBtn.addEventListener('click', () => {
    carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
  });
  prevBtn.addEventListener('click', () => {
    carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
  });
});