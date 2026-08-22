(function() {
    window.Itinerary = {
        async removeActivity(activityId, elementRef) {
            if (await App.confirm('Remove this activity from your itinerary?')) {
                try {
                    const res = await App.api(`/api/itinerary/${activityId}`, { method: 'DELETE' });
                    if (res.success) {
                        App.toast('Activity removed');
                        if (elementRef) {
                            const item = elementRef.closest('.itinerary-item');
                            if (item) {
                                item.style.opacity = '0';
                                setTimeout(() => item.remove(), 300);
                            }
                        }
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                }
            }
        },

        async addActivity(tripId, tripStopId, activityId, date, startTime, endTime) {
            try {
                const res = await App.api(`/api/trips/${tripId}/itinerary`, {
                    method: 'POST',
                    body: {
                        trip_stop_id: tripStopId,
                        activity_id: activityId,
                        date: date,
                        start_time: startTime,
                        end_time: endTime
                    }
                });
                
                if (res.success) {
                    App.toast('Activity added to itinerary');
                    window.location.reload(); // Quick refresh to show new state
                }
            } catch (error) {
                App.toast(error.message, 'error');
            }
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        // Drag and drop for stops
        const stopsList = document.getElementById('stops-list');
        if (stopsList) {
            initDragAndDrop(stopsList, 'trip-stop', async (newOrder) => {
                const tripId = stopsList.dataset.tripId;
                if (!tripId) return;
                try {
                    await App.api(`/api/trips/${tripId}/stops/reorder`, {
                        method: 'PATCH',
                        body: { order: newOrder }
                    });
                    App.toast('Stops reordered');
                } catch (error) {
                    App.toast('Failed to reorder stops: ' + error.message, 'error');
                }
            });
        }

        // Drag and drop for activities within a day
        const dayContainers = document.querySelectorAll('.itinerary-day-container');
        dayContainers.forEach(container => {
            initDragAndDrop(container, 'itinerary-item', async (newOrder) => {
                const tripId = container.dataset.tripId;
                if (!tripId) return;
                try {
                    await App.api(`/api/trips/${tripId}/itinerary/reorder`, {
                        method: 'PATCH',
                        body: { order: newOrder }
                    });
                    App.toast('Activities reordered');
                } catch (error) {
                    App.toast('Failed to reorder activities: ' + error.message, 'error');
                }
            });
        });

        function initDragAndDrop(container, itemClass, onReorder) {
            let draggedItem = null;

            container.addEventListener('dragstart', (e) => {
                if (e.target.classList.contains(itemClass)) {
                    draggedItem = e.target;
                    setTimeout(() => e.target.classList.add('opacity-50', 'bg-gray-800'), 0);
                }
            });

            container.addEventListener('dragend', (e) => {
                if (e.target.classList.contains(itemClass)) {
                    e.target.classList.remove('opacity-50', 'bg-gray-800');
                    draggedItem = null;
                    
                    // Collect new order
                    const items = [...container.querySelectorAll(`.${itemClass}`)];
                    const newOrder = items.map(item => item.dataset.id);
                    if (onReorder) onReorder(newOrder);
                }
            });

            container.addEventListener('dragover', (e) => {
                e.preventDefault();
                if (!draggedItem) return;
                
                const afterElement = getDragAfterElement(container, e.clientY, itemClass);
                if (afterElement == null) {
                    container.appendChild(draggedItem);
                } else {
                    container.insertBefore(draggedItem, afterElement);
                }
            });
        }

        function getDragAfterElement(container, y, itemClass) {
            const draggableElements = [...container.querySelectorAll(`.${itemClass}:not(.opacity-50)`)];

            return draggableElements.reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;
                if (offset < 0 && offset > closest.offset) {
                    return { offset: offset, element: child };
                } else {
                    return closest;
                }
            }, { offset: Number.NEGATIVE_INFINITY }).element;
        }
    });
})();
