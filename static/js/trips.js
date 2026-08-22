(function() {
    window.Trips = {
        async deleteTrip(id, elementRef) {
            if (await App.confirm('Are you sure you want to delete this trip? This action cannot be undone.')) {
                try {
                    const res = await App.api(`/api/trips/${id}`, { method: 'DELETE' });
                    if (res.success) {
                        App.toast('Trip deleted successfully');
                        if (elementRef) {
                            const card = elementRef.closest('.trip-card');
                            if (card) {
                                card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                                card.style.opacity = '0';
                                card.style.transform = 'scale(0.9)';
                                setTimeout(() => card.remove(), 300);
                            }
                        } else {
                            window.location.reload();
                        }
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                }
            }
        },
        
        async shareTrip(id) {
            try {
                const res = await App.api(`/api/trips/${id}/share`, { method: 'POST' });
                if (res.success && res.data?.share_url) {
                    // Show modal or toast with link
                    const url = window.location.origin + res.data.share_url;
                    try {
                        await navigator.clipboard.writeText(url);
                        App.toast('Share link copied to clipboard!');
                    } catch(err) {
                        prompt('Share URL:', url);
                    }
                }
            } catch (error) {
                App.toast(error.message, 'error');
            }
        },
        
        async disableShare(id) {
            if (await App.confirm('Are you sure you want to disable sharing for this trip?')) {
                try {
                    const res = await App.api(`/api/trips/${id}/share`, { method: 'DELETE' });
                    if (res.success) {
                        App.toast('Sharing disabled for this trip');
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                }
            }
        },
        
        copyShareUrl(url) {
            const fullUrl = url.startsWith('http') ? url : window.location.origin + url;
            navigator.clipboard.writeText(fullUrl)
                .then(() => App.toast('Copied to clipboard!'))
                .catch(err => {
                    prompt('Share URL:', fullUrl);
                });
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        // Handle filter tabs if present
        const filterTabs = document.querySelectorAll('.trip-filter-tab');
        if (filterTabs.length > 0) {
            filterTabs.forEach(tab => {
                tab.addEventListener('click', (e) => {
                    const filter = e.target.dataset.filter;
                    const url = new URL(window.location);
                    if (filter) {
                        url.searchParams.set('status', filter);
                    } else {
                        url.searchParams.delete('status');
                    }
                    window.location.href = url.toString();
                });
            });
        }

        // Trip Creation Form
        const createForm = document.getElementById('create-trip-form');
        if (createForm) {
            createForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const btn = createForm.querySelector('button[type="submit"]');
                const formData = new FormData(createForm);
                const data = Object.fromEntries(formData.entries());
                
                App.setButtonLoading(btn, true, 'CREATING...');
                
                try {
                    const res = await App.api('/api/trips', {
                        method: 'POST',
                        body: data
                    });
                    
                    if (res.success) {
                        App.toast('Trip created successfully!');
                        window.location.href = `/trips/${res.data.id}`;
                    } else {
                        App.toast(res.error?.message || 'Failed to create trip', 'error');
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                } finally {
                    App.setButtonLoading(btn, false, 'CREATE TRIP');
                }
            });
        }
        
        // Trip Edit Form
        const editForm = document.getElementById('edit-trip-form');
        if (editForm) {
            editForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const tripId = editForm.dataset.tripId;
                if (!tripId) return;
                
                const btn = editForm.querySelector('button[type="submit"]');
                const formData = new FormData(editForm);
                const data = Object.fromEntries(formData.entries());
                
                App.setButtonLoading(btn, true, 'SAVING...');
                
                try {
                    const res = await App.api(`/api/trips/${tripId}`, {
                        method: 'PATCH',
                        body: data
                    });
                    
                    if (res.success) {
                        App.toast('Trip updated successfully!');
                        setTimeout(() => window.location.reload(), 500);
                    } else {
                        App.toast(res.error?.message || 'Failed to update trip', 'error');
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                } finally {
                    App.setButtonLoading(btn, false, 'SAVE CHANGES');
                }
            });
        }
    });
})();
