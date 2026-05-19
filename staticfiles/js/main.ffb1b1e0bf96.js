function initParticles() {
  const canvas = document.getElementById("hero-canvas");
  if (!canvas || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return;
  }

  const ctx = canvas.getContext("2d");
  let particles = [];
  let animationFrame;

  function resize() {
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    createParticles();
  }

  function createParticles() {
    const count = window.innerWidth < 720 ? 24 : 42;
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * canvas.offsetWidth,
      y: Math.random() * canvas.offsetHeight,
      radius: Math.random() * 2.4 + 0.8,
      vx: (Math.random() - 0.5) * 0.28,
      vy: (Math.random() - 0.5) * 0.28,
      alpha: Math.random() * 0.32 + 0.08,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.offsetWidth, canvas.offsetHeight);

    particles.forEach((particle) => {
      particle.x += particle.vx;
      particle.y += particle.vy;

      if (particle.x < 0 || particle.x > canvas.offsetWidth) {
        particle.vx *= -1;
      }
      if (particle.y < 0 || particle.y > canvas.offsetHeight) {
        particle.vy *= -1;
      }

      ctx.beginPath();
      ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(92, 186, 255, ${particle.alpha})`;
      ctx.fill();
    });

    for (let i = 0; i < particles.length; i += 1) {
      for (let j = i + 1; j < particles.length; j += 1) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.hypot(dx, dy);

        if (distance < 120) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(90, 167, 255, ${0.12 * (1 - distance / 120)})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    animationFrame = window.requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener("resize", resize);
  draw();

  window.addEventListener("beforeunload", () => {
    if (animationFrame) {
      window.cancelAnimationFrame(animationFrame);
    }
  });
}

function initNavbar() {
  const navbar = document.querySelector(".navbar");
  const menu = document.getElementById("mobile-menu");
  const backdrop = document.querySelector("[data-menu-backdrop]");
  const openButton = document.querySelector("[data-menu-toggle]");
  const closeButton = document.querySelector("[data-menu-close]");

  if (navbar) {
    window.addEventListener("scroll", () => {
      navbar.classList.toggle("scrolled", window.scrollY > 8);
    });
  }

  if (!menu || !backdrop || !openButton) {
    return;
  }

  const setMenuState = (open) => {
    menu.classList.toggle("open", open);
    backdrop.classList.toggle("open", open);
    document.body.classList.toggle("menu-open", open);
    menu.setAttribute("aria-hidden", String(!open));
    openButton.setAttribute("aria-expanded", String(open));
  };

  openButton.addEventListener("click", () => setMenuState(true));

  if (closeButton) {
    closeButton.addEventListener("click", () => setMenuState(false));
  }

  backdrop.addEventListener("click", () => setMenuState(false));

  menu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => setMenuState(false));
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setMenuState(false);
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      setMenuState(false);
    }
  });
}

function initDashboardMenu() {
  const sidebar = document.querySelector("[data-dashboard-sidebar]");
  const backdrop = document.querySelector("[data-dashboard-backdrop]");
  const toggle = document.querySelector("[data-dashboard-toggle]");

  if (!sidebar || !backdrop || !toggle) {
    return;
  }

  const setSidebarState = (open) => {
    sidebar.classList.toggle("open", open);
    backdrop.classList.toggle("open", open);
    document.body.classList.toggle("dashboard-nav-open", open);
    toggle.setAttribute("aria-expanded", String(open));
  };

  toggle.addEventListener("click", () => {
    setSidebarState(!sidebar.classList.contains("open"));
  });

  backdrop.addEventListener("click", () => setSidebarState(false));

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      setSidebarState(false);
    }
  });

  window.addEventListener("resize", () => {
    if (window.innerWidth > 920) {
      setSidebarState(false);
    }
  });
}

function initReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!items.length) {
    return;
  }

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    items.forEach((item) => item.classList.add("visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.16 }
  );

  items.forEach((item) => observer.observe(item));
}

function initCountdowns() {
  document.querySelectorAll("[data-countdown]").forEach((element) => {
    const target = new Date(element.dataset.countdown).getTime();
    if (Number.isNaN(target)) {
      return;
    }

    const render = () => {
      const diff = target - Date.now();

      if (diff <= 0) {
        element.innerHTML = '<span class="text-gradient">Event started</span>';
        return false;
      }

      const days = Math.floor(diff / 86400000);
      const hours = Math.floor((diff % 86400000) / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);

      element.innerHTML = `
        <div class="countdown-unit"><span class="num">${String(days).padStart(2, "0")}</span><span class="lbl">Days</span></div>
        <div class="countdown-unit"><span class="num">${String(hours).padStart(2, "0")}</span><span class="lbl">Hrs</span></div>
        <div class="countdown-unit"><span class="num">${String(minutes).padStart(2, "0")}</span><span class="lbl">Min</span></div>
        <div class="countdown-unit"><span class="num">${String(seconds).padStart(2, "0")}</span><span class="lbl">Sec</span></div>
      `;

      return true;
    };

    if (!render()) {
      return;
    }

    const timer = window.setInterval(() => {
      if (!render()) {
        window.clearInterval(timer);
      }
    }, 1000);
  });
}

function initLightbox() {
  const lightbox = document.getElementById("lightbox");
  if (!lightbox) {
    return;
  }

  const image = lightbox.querySelector("img");
  const closeButton = lightbox.querySelector(".lightbox-close");

  const closeLightbox = () => {
    lightbox.classList.remove("active");
    document.body.classList.remove("lightbox-open");
    image.removeAttribute("src");
  };

  document.querySelectorAll(".gallery-item[data-src]").forEach((item) => {
    item.addEventListener("click", () => {
      image.src = item.dataset.src;
      lightbox.classList.add("active");
      document.body.classList.add("lightbox-open");
    });
  });

  if (closeButton) {
    closeButton.addEventListener("click", closeLightbox);
  }

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });

  window.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeLightbox();
    }
  });
}

function initAlerts() {
  document.querySelectorAll(".alert").forEach((alert) => {
    const closeButton = alert.querySelector(".alert-close");

    const removeAlert = () => {
      alert.style.opacity = "0";
      window.setTimeout(() => {
        if (alert.parentElement) {
          alert.remove();
        }
      }, 220);
    };

    if (closeButton) {
      closeButton.addEventListener("click", removeAlert);
    }

    window.setTimeout(removeAlert, 5000);
  });
}

function initPasswordStrength() {
  const password = document.getElementById("id_password");
  const bar = document.getElementById("pwd-strength");
  const label = document.getElementById("pwd-strength-label");

  if (!password || !bar || !label) {
    return;
  }

  password.addEventListener("input", () => {
    const value = password.value;
    let score = 0;

    if (value.length >= 6) score += 1;
    if (/[A-Z]/.test(value)) score += 1;
    if (/[0-9]/.test(value)) score += 1;
    if (/[^a-zA-Z0-9]/.test(value)) score += 1;

    const widths = ["0%", "25%", "50%", "75%", "100%"];
    const colors = ["#ff7a7a", "#ff9f6e", "#ffc46b", "#9fe3a8"];
    const labels = ["", "Weak", "Fair", "Good", "Strong"];

    bar.style.width = widths[score];
    bar.style.background = colors[Math.max(score - 1, 0)] || "transparent";
    label.textContent = labels[score];
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initParticles();
  initNavbar();
  initDashboardMenu();
  initReveal();
  initCountdowns();
  initLightbox();
  initAlerts();
  initPasswordStrength();
});
