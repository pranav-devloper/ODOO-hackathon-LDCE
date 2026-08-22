(function() {
    window.Share = {
        async copyTrip(token) {
            try {
                const res = await App.api(`/api/share/${token}/copy`, { method: 'POST' });
                if (res.success && res.data?.id) {
                    App.toast('Trip copied successfully!');
                    setTimeout(() => {
                        window.location.href = `/trips/${res.data.id}`;
                    }, 1000);
                } else {
                    App.toast(res.error?.message || 'Failed to copy trip', 'error');
                }
            } catch (error) {
                App.toast(error.message, 'error');
            }
        },

        shareToSocial(platform, url, title) {
            const encodedUrl = encodeURIComponent(url);
            const encodedTitle = encodeURIComponent(title);
            let shareUrl = '';

            switch (platform) {
                case 'twitter':
                case 'x':
                    shareUrl = `https://twitter.com/intent/tweet?url=${encodedUrl}&text=${encodedTitle}`;
                    break;
                case 'facebook':
                    shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}`;
                    break;
                case 'whatsapp':
                    shareUrl = `https://api.whatsapp.com/send?text=${encodedTitle} ${encodedUrl}`;
                    break;
                case 'email':
                    shareUrl = `mailto:?subject=${encodedTitle}&body=Check out this trip: ${encodedUrl}`;
                    break;
                default:
                    return;
            }

            window.open(shareUrl, '_blank', 'width=600,height=400');
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        const toggleShareBtn = document.getElementById('toggle-share-btn');
        if (toggleShareBtn) {
            toggleShareBtn.addEventListener('change', async (e) => {
                const tripId = e.target.dataset.tripId;
                if (!tripId) return;
                
                const isEnabled = e.target.checked;
                
                if (isEnabled) {
                    try {
                        const res = await App.api(`/api/trips/${tripId}/share`, { method: 'POST' });
                        if (res.success) {
                            App.toast('Sharing enabled');
                            const urlDisplay = document.getElementById('share-url-display');
                            if (urlDisplay && res.data.share_url) {
                                urlDisplay.value = window.location.origin + res.data.share_url;
                                urlDisplay.closest('.share-link-container')?.classList.remove('hidden');
                            }
                        } else {
                            e.target.checked = false;
                            App.toast('Failed to enable sharing', 'error');
                        }
                    } catch (err) {
                        e.target.checked = false;
                        App.toast(err.message, 'error');
                    }
                } else {
                    if (await App.confirm('Disable sharing? The current link will stop working.')) {
                        try {
                            const res = await App.api(`/api/trips/${tripId}/share`, { method: 'DELETE' });
                            if (res.success) {
                                App.toast('Sharing disabled');
                                document.querySelector('.share-link-container')?.classList.add('hidden');
                            } else {
                                e.target.checked = true;
                            }
                        } catch (err) {
                            e.target.checked = true;
                            App.toast(err.message, 'error');
                        }
                    } else {
                        e.target.checked = true;
                    }
                }
            });
        }
        
        const copyUrlBtn = document.getElementById('copy-url-btn');
        if (copyUrlBtn) {
            copyUrlBtn.addEventListener('click', () => {
                const urlInput = document.getElementById('share-url-display');
                if (urlInput) {
                    urlInput.select();
                    document.execCommand('copy');
                    App.toast('Link copied to clipboard');
                }
            });
        }
    });
})();
