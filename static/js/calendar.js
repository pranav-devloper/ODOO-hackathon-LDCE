(function() {
    window.Calendar = {
        render(containerId, events, startDate, endDate) {
            const container = document.getElementById(containerId);
            if (!container) return;

            // Basic calendar rendering logic
            // In a real app, this would use a library like FullCalendar or build a complex grid
            
            const start = new Date(startDate);
            const end = new Date(endDate);
            
            if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                container.innerHTML = '<div class="text-center text-gray-500 py-10">Invalid trip dates</div>';
                return;
            }

            let html = '<div class="grid grid-cols-7 gap-2 mb-2">';
            const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            days.forEach(day => {
                html += `<div class="text-center text-xs font-semibold text-gray-400 py-2">${day}</div>`;
            });
            html += '</div><div class="grid grid-cols-7 gap-2">';

            // Fill empty days before start
            const startDay = start.getDay();
            for (let i = 0; i < startDay; i++) {
                html += `<div class="calendar-day empty bg-[#1a1915] rounded-xl opacity-50 min-h-[100px]"></div>`;
            }

            // Fill trip days
            let currentDate = new Date(start);
            while (currentDate <= end) {
                const dateStr = currentDate.toISOString().split('T')[0];
                const dayEvents = events.filter(e => e.date === dateStr);
                
                let eventsHtml = '';
                dayEvents.forEach(ev => {
                    const colorMap = {
                        'accommodation': 'border-l-blue-400 bg-blue-400/10',
                        'transport': 'border-l-yellow-400 bg-yellow-400/10',
                        'activity': 'border-l-[#ffb4a2] bg-[#ffb4a2]/10',
                        'meal': 'border-l-green-400 bg-green-400/10'
                    };
                    const colorClass = colorMap[ev.category?.toLowerCase()] || 'border-l-gray-400 bg-gray-400/10';
                    
                    eventsHtml += `
                        <div class="text-xs mb-1 p-1 pl-2 border-l-2 ${colorClass} rounded truncate cursor-pointer hover:opacity-80 transition-opacity" title="${ev.title}">
                            ${ev.start_time ? ev.start_time.substring(0,5) + ' ' : ''}${ev.title}
                        </div>
                    `;
                });

                html += `
                    <div class="calendar-day bg-[#1a1915] rounded-xl p-2 min-h-[100px] border border-[#2b2a26] hover:border-[#42403b] transition-colors relative group">
                        <div class="text-xs text-gray-500 mb-2 font-medium">${currentDate.getDate()}</div>
                        <div class="events-container">
                            ${eventsHtml}
                        </div>
                        <button class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-[#ffb4a2] transition-all" title="Add activity">
                            <span class="material-symbols-outlined text-[16px]">add</span>
                        </button>
                    </div>
                `;
                
                currentDate.setDate(currentDate.getDate() + 1);
            }
            
            html += '</div>';
            container.innerHTML = html;
        }
    };
})();
