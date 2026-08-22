(function() {
    window.Destinations = {
        async toggleSave(destinationId, btnRef) {
            const isSaved = btnRef.dataset.saved === 'true';
            const method = isSaved ? 'DELETE' : 'POST';
            
            try {
                const res = await App.api(`/api/destinations/${destinationId}/save`, { method });
                if (res.success) {
                    btnRef.dataset.saved = (!isSaved).toString();
                    const icon = btnRef.querySelector('.material-symbols-outlined');
                    if (icon) {
                        icon.style.fontVariationSettings = !isSaved ? "'FILL' 1" : "'FILL' 0";
                        icon.classList.toggle('text-[#ffb4a2]', !isSaved);
                        icon.classList.toggle('text-gray-400', isSaved);
                    }
                    App.toast(isSaved ? 'Removed from saved' : 'Destination saved!');
                }
            } catch (error) {
                App.toast(error.message, 'error');
            }
        },

        async addToTrip(destinationId, tripId) {
            try {
                const res = await App.api(`/api/trips/${tripId}/stops`, {
                    method: 'POST',
                    body: { destination_id: destinationId }
                });
                
                if (res.success) {
                    App.toast('Added to trip successfully!');
                }
            } catch (error) {
                App.toast(error.message, 'error');
            }
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        const searchInput = document.getElementById('destination-search');
        if (searchInput) {
            const performSearch = App.debounce(async (query) => {
                try {
                    const url = new URL('/api/destinations', window.location.origin);
                    if (query) url.searchParams.set('q', query);
                    
                    const countryFilter = document.getElementById('country-filter')?.value;
                    const regionFilter = document.getElementById('region-filter')?.value;
                    
                    if (countryFilter) url.searchParams.set('country', countryFilter);
                    if (regionFilter) url.searchParams.set('region', regionFilter);

                    const res = await App.api(url);
                    if (res.success) {
                        renderDestinations(res.data.destinations || []);
                    }
                } catch (error) {
                    console.error('Search failed', error);
                }
            }, 300);

            searchInput.addEventListener('input', (e) => performSearch(e.target.value));
            
            document.getElementById('country-filter')?.addEventListener('change', () => performSearch(searchInput.value));
            document.getElementById('region-filter')?.addEventListener('change', () => performSearch(searchInput.value));
        }
        
        function renderDestinations(destinations) {
            const container = document.getElementById('destinations-grid');
            if (!container) return;
            
            if (destinations.length === 0) {
                container.innerHTML = '<div class="col-span-full text-center text-gray-500 py-10">No destinations found matching your criteria.</div>';
                return;
            }
            
            // Re-render HTML logic would go here depending on the exact card structure
            // Example stub:
            // container.innerHTML = destinations.map(d => `<div class="card">...</div>`).join('');
        }
    });
})();
