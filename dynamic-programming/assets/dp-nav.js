(() => {
  const links = [...document.querySelectorAll('.dp-content-page .sidebar a[href^="#"]')];
  if (!links.length) return;
  const sections = links.map(a => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const setActive = id => links.forEach(a => {
    if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current','true');
    else a.removeAttribute('aria-current');
  });
  const update = () => {
    const y = window.scrollY + 150;
    let current = sections[0];
    for (const section of sections) if (section.offsetTop <= y) current = section;
    if (current) setActive(current.id);
  };
  links.forEach(a => a.addEventListener('click', () => setActive(a.hash.slice(1))));
  window.addEventListener('scroll', update, {passive:true});
  window.addEventListener('resize', update);
  update();
})();