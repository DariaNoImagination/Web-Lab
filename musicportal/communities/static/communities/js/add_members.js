document.querySelectorAll('.community-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const scrollY = window.scrollY;
        const formData = new FormData(form);
        const btn = form.querySelector('button');
        const card = form.closest('.community-card');
        const membersElement = card ? card.querySelector('.members-count') : null;

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
                btn.innerHTML = '⭐ В сообществе';
                if (membersElement && data.members_count !== undefined) {
                    membersElement.innerHTML = `<strong>👥 Участников:</strong> ${data.members_count}`;
                }
            } else if (data.status === 'removed') {
                btn.classList.remove('active');
                btn.innerHTML = '⭐ Вступить';
                if (membersElement && data.members_count !== undefined) {
                    membersElement.innerHTML = `<strong>👥 Участников:</strong> ${data.members_count}`;
                }
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