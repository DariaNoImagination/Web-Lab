document.querySelectorAll('.favorite-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const scrollY = window.scrollY;
        const formData = new FormData(form);
        const btn = form.querySelector('button');

        btn.disabled = true;
        const originalText = btn.innerHTML;
        btn.innerHTML = '⏳';

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            const data = await response.json();

            if (data.status === 'added') {
                btn.classList.add('active');
                btn.innerHTML = '❤️ В избранном';
            } else {
                btn.classList.remove('active');
                btn.innerHTML = '🤍 В избранное';
            }

            window.scrollTo(0, scrollY);

        } catch (error) {
            console.error('Error:', error);
            btn.innerHTML = originalText;
        } finally {
            btn.disabled = false;
        }
    });
});
