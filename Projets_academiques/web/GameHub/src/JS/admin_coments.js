document.addEventListener('DOMContentLoaded', () => {
  const prevBtn = document.getElementById('prev-comments');
  const nextBtn = document.getElementById('next-comments');
  const rows = Array.from(document.querySelectorAll('#comments-table tbody tr'));
  const perPage = 5;
  let startIndex = 0;

  function render() {
    rows.forEach((row, idx) => {
      row.style.display = (idx >= startIndex && idx < startIndex + perPage) ? '' : 'none';
    });
  }

  if (!prevBtn || !nextBtn || rows.length === 0) return;

  prevBtn.addEventListener('click', () => {
    startIndex = Math.max(0, startIndex - perPage);
    render();
  });

  nextBtn.addEventListener('click', () => {
    if (startIndex + perPage < rows.length) {
      startIndex += perPage;
      render();
    }
  });

  render();
});
