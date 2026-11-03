(function () {
  var SRC = 'https://hearths-of-the-glen.onrender.com';

  document.querySelectorAll('.game-embed').forEach(function (box) {
    var button = box.querySelector('.game-start');
    if (!button) return;

    button.addEventListener('click', function () {
      if (box.querySelector('iframe')) return;
      var iframe = document.createElement('iframe');
      iframe.src = SRC;
      iframe.title = button.getAttribute('data-game-title') || '';
      iframe.setAttribute('allow', 'fullscreen');
      iframe.setAttribute('allowfullscreen', '');
      box.classList.add('is-playing');
      box.replaceChildren(iframe);
    });
  });
})();
