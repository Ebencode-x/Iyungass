(function () {
  'use strict';

  /* ---------------------------------------------------------
     Mobile navigation toggle
  --------------------------------------------------------- */
  var header = document.querySelector('.site-header');
  var navToggle = document.getElementById('nav-toggle');

  if (navToggle && header) {
    navToggle.addEventListener('click', function () {
      var isOpen = header.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }

  /* Close mobile nav after a link is chosen */
  var navLinks = document.querySelectorAll('.nav-link, .header-actions .btn');
  navLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      if (header && header.classList.contains('is-open')) {
        header.classList.remove('is-open');
        if (navToggle) {
          navToggle.setAttribute('aria-expanded', 'false');
        }
      }
    });
  });

  /* ---------------------------------------------------------
     Smooth scrolling for in-page anchor links
  --------------------------------------------------------- */
  var anchorLinks = document.querySelectorAll('a[href^="#"]');

  anchorLinks.forEach(function (link) {
    link.addEventListener('click', function (event) {
      var targetId = link.getAttribute('href');

      if (!targetId || targetId === '#') {
        return;
      }

      var target = document.querySelector(targetId);

      if (target) {
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
      }
    });
  });

  /* ---------------------------------------------------------
     Dynamic copyright year
  --------------------------------------------------------- */
  var yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  /* ---------------------------------------------------------
     Admission status modal
  --------------------------------------------------------- */
  var checkStatusLink = document.getElementById('check-status');
  var modalOverlay = document.getElementById('modal-overlay');
  var modalClose = document.getElementById('modal-close');

  function openModal() {
    if (modalOverlay) {
      modalOverlay.classList.add('is-open');
      document.body.style.overflow = 'hidden';
      if (modalClose) {
        modalClose.focus();
      }
    }
  }

  function closeModal() {
    if (modalOverlay) {
      modalOverlay.classList.remove('is-open');
      document.body.style.overflow = '';
      if (checkStatusLink) {
        checkStatusLink.focus();
      }
    }
  }

  if (checkStatusLink) {
    checkStatusLink.addEventListener('click', function (event) {
      event.preventDefault();
      openModal();
    });
  }

  if (modalClose) {
    modalClose.addEventListener('click', closeModal);
  }

  if (modalOverlay) {
    modalOverlay.addEventListener('click', function (event) {
      if (event.target === modalOverlay) {
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && modalOverlay && modalOverlay.classList.contains('is-open')) {
      closeModal();
    }
  });
})();
