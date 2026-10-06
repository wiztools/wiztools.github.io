document.querySelectorAll('[data-pdf-carousel]').forEach((carousel) => {
  if (carousel.dataset.ready) return;
  carousel.dataset.ready = 'true';
  const track = carousel.querySelector('.pdf-carousel-track');
  const slides = [...track.children];
  const previous = carousel.querySelector('[data-prev]');
  const next = carousel.querySelector('[data-next]');
  const counter = carousel.querySelector('[data-counter]');
  const fullscreen = carousel.querySelector('[data-fullscreen]');
  let current = 0;
  let destination = null;
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
    destination = Math.max(0, Math.min(slides.length - 1, (destination ?? current) + direction));
    const target = slides[destination];
    track.scrollTo({
      left: track.scrollLeft + target.getBoundingClientRect().left - track.getBoundingClientRect().left,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth',
    });
  };
  previous.hidden = next.hidden = false;
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  if (document.fullscreenEnabled) {
    fullscreen.hidden = false;
    fullscreen.addEventListener('click', async () => {
      try {
        if (document.fullscreenElement === carousel) await document.exitFullscreen();
        else {
          slides.forEach((slide) => { slide.querySelector('img').loading = 'eager'; });
          await carousel.requestFullscreen();
        }
      } catch {
        counter.textContent = 'Full screen is unavailable. Try opening the original PDF.';
      }
    });
    document.addEventListener('fullscreenchange', () => {
      const active = document.fullscreenElement === carousel;
      fullscreen.setAttribute('aria-label', active ? 'Exit full screen' : 'Full screen');
      fullscreen.setAttribute('aria-pressed', String(active));
      if (active) track.focus({ preventScroll: true });
      else fullscreen.focus({ preventScroll: true });
    });
  }
  carousel.addEventListener('keydown', (event) => {
    if (event.target !== track && event.target !== previous && event.target !== next && event.target !== fullscreen) return;
    if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
    event.preventDefault();
    move(event.key === 'ArrowRight' ? 1 : -1);
  });
  track.addEventListener('scroll', () => {
    if (!scheduled) { scheduled = true; requestAnimationFrame(update); }
  }, { passive: true });
  track.addEventListener('scrollend', () => { destination = null; update(); });
  ['pointerdown', 'wheel', 'touchstart'].forEach((event) => {
    track.addEventListener(event, () => { destination = null; }, { passive: true });
  });
  new ResizeObserver(update).observe(track);
  update();
});
