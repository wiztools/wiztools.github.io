document.querySelectorAll('[data-pdf-carousel]').forEach((carousel) => {
  if (carousel.dataset.ready) return;
  carousel.dataset.ready = 'true';
  const track = carousel.querySelector('.pdf-carousel-track');
  const slides = [...track.children];
  const previous = carousel.querySelector('[data-prev]');
  const next = carousel.querySelector('[data-next]');
  const counter = carousel.querySelector('[data-counter]');
  let current = 0;
  let scheduled = false;
  const update = () => {
    scheduled = false;
    const left = track.getBoundingClientRect().left;
    current = slides.reduce((nearest, slide, index) =>
      Math.abs(slide.getBoundingClientRect().left - left) <
      Math.abs(slides[nearest].getBoundingClientRect().left - left) ? index : nearest, 0);
    counter.textContent = `${current + 1} / ${slides.length}`;
    previous.disabled = current === 0;
    next.disabled = current === slides.length - 1;
  };
  const move = (direction) => {
    const target = slides[Math.max(0, Math.min(slides.length - 1, current + direction))];
    track.scrollBy({
      left: target.getBoundingClientRect().left - track.getBoundingClientRect().left,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
    });
  };
  previous.hidden = next.hidden = false;
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  track.addEventListener('keydown', (event) => {
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    move(event.key === 'ArrowRight' ? 1 : -1);
  });
  track.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, { passive: true });
  new ResizeObserver(update).observe(track);
  update();
});
