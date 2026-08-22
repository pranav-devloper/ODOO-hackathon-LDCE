(function() {
    document.addEventListener('DOMContentLoaded', () => {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) return;

        // Parallax scroll effect
        const parallaxElements = document.querySelectorAll('.parallax-layer');
        if (parallaxElements.length > 0) {
            let ticking = false;
            
            window.addEventListener('scroll', () => {
                if (!ticking) {
                    window.requestAnimationFrame(() => {
                        const scrolled = window.scrollY;
                        parallaxElements.forEach(el => {
                            const speed = parseFloat(el.dataset.speed || '0.5');
                            const yPos = -(scrolled * speed);
                            el.style.transform = `translate3d(0, ${yPos}px, 0)`;
                        });
                        ticking = false;
                    });
                    ticking = true;
                }
            }, { passive: true });
        }

        // Fade in up elements via Intersection Observer
        const fadeElements = document.querySelectorAll('.fade-in-up');
        if (fadeElements.length > 0) {
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            const observer = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            fadeElements.forEach(el => {
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
                observer.observe(el);
            });
        }

        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
        
        // Optional: Bird animation logic
        const birds = document.querySelectorAll('.bird-anim');
        birds.forEach(bird => {
            // Randomize starting positions and animation delays
            const randomY = Math.random() * 20;
            const delay = Math.random() * 5;
            bird.style.top = `${randomY}%`;
            bird.style.animationDelay = `${delay}s`;
        });
    });
})();
