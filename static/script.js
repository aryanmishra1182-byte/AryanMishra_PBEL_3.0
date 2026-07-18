document.addEventListener("DOMContentLoaded", () => {

    /* ==========================
       MULTI STEP WIZARD
    ========================== */

    const steps = document.querySelectorAll(".form-step");
    const nextBtns = document.querySelectorAll(".next-btn");
    const prevBtns = document.querySelectorAll(".prev-btn");
    const progressBar = document.querySelector(".progress-bar");

    let currentStep = 0;

    function showStep(index) {

        steps.forEach((step) => {

            step.classList.remove("active");

        });

        steps[index].classList.add("active");

        if (progressBar) {

            const progress = ((index + 1) / steps.length) * 100;
            progressBar.style.width = progress + "%";

        }

        window.scrollTo({

            top: document.getElementById("predict").offsetTop - 70,
            behavior: "smooth"

        });

    }

    nextBtns.forEach((btn) => {

        btn.addEventListener("click", () => {

            const inputs = steps[currentStep].querySelectorAll("input, select");

            let valid = true;

            inputs.forEach((input) => {

                if (!input.checkValidity()) {

                    valid = false;
                    input.reportValidity();

                }

            });

            if (!valid) return;

            if (currentStep < steps.length - 1) {

                currentStep++;
                showStep(currentStep);

            }

        });

    });

    prevBtns.forEach((btn) => {

        btn.addEventListener("click", () => {

            if (currentStep > 0) {

                currentStep--;
                showStep(currentStep);

            }

        });

    });

    showStep(currentStep);

    /* ==========================
       LOADER
    ========================== */

    const form = document.querySelector("form");
    const loader = document.getElementById("loader");

    if (form && loader) {

        form.addEventListener("submit", () => {

            loader.style.display = "flex";

        });

    }

    /* ==========================
       COUNT UP ANIMATION
    ========================== */

    const statNumbers = document.querySelectorAll(".stat-card h2");

    statNumbers.forEach((counter) => {

        const originalText = counter.innerText;

        const target = parseInt(originalText.replace(/\D/g, ""));

        if (isNaN(target)) return;

        let count = 0;

        const speed = Math.max(10, target / 70);

        const updateCounter = () => {

            count += speed;

            if (count >= target) {

                counter.innerText = originalText;

            } else {

                let suffix = "";

                if (originalText.includes("%")) suffix = "%";
                if (originalText.includes("+")) suffix = "+";

                counter.innerText = Math.floor(count) + suffix;

                requestAnimationFrame(updateCounter);

            }

        };

        updateCounter();

    });

    /* ==========================
       TYPING EFFECT
    ========================== */

    const typing = document.getElementById("typing-text");

    if (typing) {

        const words = [

            "Using Machine Learning",
            "With Artificial Intelligence",
            "With Data Science",
            "Using Predictive Analytics"

        ];

        let wordIndex = 0;
        let charIndex = 0;
        let deleting = false;

        function typeEffect() {

            const currentWord = words[wordIndex];

            if (!deleting) {

                typing.textContent = currentWord.substring(0, charIndex++);

                if (charIndex > currentWord.length) {

                    deleting = true;

                    setTimeout(typeEffect, 1500);

                    return;

                }

            } else {

                typing.textContent = currentWord.substring(0, charIndex--);

                if (charIndex < 0) {

                    deleting = false;
                    wordIndex = (wordIndex + 1) % words.length;

                }

            }

            setTimeout(typeEffect, deleting ? 45 : 90);

        }

        typeEffect();

    }

    /* ==========================
       SMOOTH NAVBAR LINKS
    ========================== */

    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {

        anchor.addEventListener("click", function (e) {

            const target = document.querySelector(this.getAttribute("href"));

            if (!target) return;

            e.preventDefault();

            window.scrollTo({

                top: target.offsetTop - 70,
                behavior: "smooth"

            });

        });

    });

    /* ==========================
       SCORE CIRCLE ANIMATION
    ========================== */

    const circle = document.querySelector(".progress-circle");

    if (circle) {

        const percent = parseFloat(circle.style.getPropertyValue("--percent"));

        circle.style.strokeDashoffset = 565;

        setTimeout(() => {

            circle.style.strokeDashoffset =
                565 - (565 * percent) / 100;

        }, 500);

    }

    /* ==========================
       FADE IN ON SCROLL
    ========================== */

    const observer = new IntersectionObserver(

        (entries) => {

            entries.forEach((entry) => {

                if (entry.isIntersecting) {

                    entry.target.classList.add("show");

                }

            });

        },

        {

            threshold: 0.15

        }

    );

    document.querySelectorAll(".glass-card, .stat-card").forEach((card) => {

        card.classList.add("hidden");

        observer.observe(card);

    });

});