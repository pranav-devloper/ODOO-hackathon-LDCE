(function() {
    window.Budget = {
        async deleteExpense(id, elementRef) {
            if (await App.confirm('Delete this expense?')) {
                try {
                    const res = await App.api(`/api/expenses/${id}`, { method: 'DELETE' });
                    if (res.success) {
                        App.toast('Expense deleted');
                        if (elementRef) {
                            const row = elementRef.closest('tr') || elementRef.closest('.expense-item');
                            if (row) {
                                row.remove();
                                // Typically, trigger a reload or chart update here
                                setTimeout(() => window.location.reload(), 500);
                            }
                        }
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                }
            }
        },
        
        initCharts(chartData) {
            // chartData: { categories: { name: amount }, daily: { date: amount } }
            if (typeof Chart === 'undefined') {
                console.warn('Chart.js not loaded');
                return;
            }

            const colors = ['#ffb4a2', '#c7c2ea', '#ecc15a', '#e4775c', '#a48b85'];

            const categoryCanvas = document.getElementById('category-chart');
            if (categoryCanvas && chartData.categories) {
                new Chart(categoryCanvas, {
                    type: 'doughnut',
                    data: {
                        labels: Object.keys(chartData.categories),
                        datasets: [{
                            data: Object.values(chartData.categories),
                            backgroundColor: colors,
                            borderWidth: 0
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: { position: 'right', labels: { color: '#e6e2db' } }
                        }
                    }
                });
            }

            const dailyCanvas = document.getElementById('daily-chart');
            if (dailyCanvas && chartData.daily) {
                new Chart(dailyCanvas, {
                    type: 'bar',
                    data: {
                        labels: Object.keys(chartData.daily).map(d => App.formatDate(d)),
                        datasets: [{
                            label: 'Daily Spend',
                            data: Object.values(chartData.daily),
                            backgroundColor: '#ffb4a2',
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: { grid: { color: '#2b2a26' }, ticks: { color: '#908e89' } },
                            x: { grid: { display: false }, ticks: { color: '#908e89' } }
                        },
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }
        }
    };

    document.addEventListener('DOMContentLoaded', () => {
        const addExpenseForm = document.getElementById('add-expense-form');
        if (addExpenseForm) {
            addExpenseForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const tripId = addExpenseForm.dataset.tripId;
                if (!tripId) return;

                const btn = addExpenseForm.querySelector('button[type="submit"]');
                const formData = new FormData(addExpenseForm);
                const data = Object.fromEntries(formData.entries());
                
                // Convert amount to number
                data.amount = parseFloat(data.amount);

                App.setButtonLoading(btn, true, 'ADDING...');

                try {
                    const res = await App.api(`/api/trips/${tripId}/expenses`, {
                        method: 'POST',
                        body: data
                    });

                    if (res.success) {
                        App.toast('Expense added!');
                        setTimeout(() => window.location.reload(), 500);
                    } else {
                        App.toast(res.error?.message || 'Failed to add expense', 'error');
                    }
                } catch (error) {
                    App.toast(error.message, 'error');
                } finally {
                    App.setButtonLoading(btn, false, 'ADD EXPENSE');
                }
            });
        }
    });
})();
