document.getElementById('avatar-input').addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        const file = this.files[0];
        const formData = new FormData();
        formData.append('avatar', file);
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        fetch(window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const avatarImg = document.querySelector('.avatar-img, #avatar-preview');
                if (avatarImg) {
                    avatarImg.src = data.avatar_url + '?t=' + new Date().getTime();
                }
            }
        })
        .catch(error => console.error('Error:', error));
    }
});