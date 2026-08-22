(function() {
    window.AppMap = {
        init(containerId, stops) {
            if (typeof L === 'undefined') {
                console.warn('Leaflet.js not loaded. Falling back.');
                this.renderFallback(containerId, stops);
                return;
            }

            const container = document.getElementById(containerId);
            if (!container) return;
            
            // Empty container if re-initializing
            container.innerHTML = '';

            try {
                const map = L.map(containerId, {
                    zoomControl: false // Add custom position if needed
                });

                // Add dark theme tiles
                L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
                    subdomains: 'abcd',
                    maxZoom: 19
                }).addTo(map);

                L.control.zoom({ position: 'topright' }).addTo(map);

                if (!stops || stops.length === 0) {
                    map.setView([20, 0], 2); // default world view
                    return map;
                }

                const latLngs = [];
                const customIcon = L.divIcon({
                    className: 'custom-map-marker',
                    html: `<div style="background-color: #ffb4a2; width: 12px; height: 12px; border-radius: 50%; border: 2px solid #141310; box-shadow: 0 0 5px rgba(255,180,162,0.5);"></div>`,
                    iconSize: [12, 12],
                    iconAnchor: [6, 6]
                });

                stops.forEach((stop, index) => {
                    if (stop.latitude && stop.longitude) {
                        const latLng = [stop.latitude, stop.longitude];
                        latLngs.push(latLng);
                        
                        const marker = L.marker(latLng, { icon: customIcon }).addTo(map);
                        
                        const popupContent = `
                            <div class="text-[#141310] p-2 min-w-[150px]">
                                <h3 class="font-bold text-sm mb-1">${stop.title || stop.name}</h3>
                                ${stop.date ? `<p class="text-xs text-gray-600">${App.formatDate(stop.date)}</p>` : ''}
                            </div>
                        `;
                        marker.bindPopup(popupContent);
                        
                        marker.on('click', () => {
                            // Can trigger external events here
                            console.log('Clicked stop:', stop.id);
                        });
                    }
                });

                // Draw route line
                if (latLngs.length > 1) {
                    L.polyline(latLngs, {
                        color: '#ffb4a2',
                        weight: 2,
                        opacity: 0.6,
                        dashArray: '5, 10',
                        lineJoin: 'round'
                    }).addTo(map);
                }

                // Fit bounds
                if (latLngs.length > 0) {
                    const bounds = L.latLngBounds(latLngs);
                    map.fitBounds(bounds, { padding: [50, 50] });
                }

                return map;
            } catch (err) {
                console.error("Map initialization failed", err);
                this.renderFallback(containerId, stops);
            }
        },
        
        renderFallback(containerId, stops) {
            const container = document.getElementById(containerId);
            if (!container) return;
            
            if (!stops || stops.length === 0) {
                container.innerHTML = '<div class="h-full flex items-center justify-center text-gray-500">No locations to display</div>';
                return;
            }
            
            let html = '<div class="h-full bg-[#1a1915] p-6 overflow-y-auto"><h3 class="text-xl text-[#e6e2db] mb-4">Route</h3><ul class="space-y-4">';
            stops.forEach((stop, i) => {
                html += `
                    <li class="flex items-start gap-3">
                        <div class="mt-1 w-6 h-6 rounded-full bg-[#2b2a26] flex items-center justify-center text-xs text-[#ffb4a2] border border-[#ffb4a2]/30 flex-shrink-0">${i+1}</div>
                        <div>
                            <div class="font-medium text-[#e6e2db]">${stop.title || stop.name}</div>
                            ${stop.country ? `<div class="text-xs text-gray-400">${stop.country}</div>` : ''}
                        </div>
                    </li>
                `;
            });
            html += '</ul></div>';
            container.innerHTML = html;
        }
    };
})();
