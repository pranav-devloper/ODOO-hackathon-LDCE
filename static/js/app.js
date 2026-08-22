// GlobeTrotter App Core
const App = {
    // API Helper - makes fetch requests with proper headers and error handling
    async api(url, options = {}) {
        const defaults = {
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin'  // Include cookies
        };
        const config = { ...defaults, ...options };
        if (config.body && typeof config.body === 'object') {
            config.body = JSON.stringify(config.body);
        }
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error?.message || data.detail || 'Request failed');
            }
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // Toast notifications
    toast(message, type = 'success', duration = 3000) {
        // type: success, error, warning, info
        const container = document.getElementById('toast-container');
        if (!container) return;
        const toast = document.createElement('div');
        // Style based on type with proper Tailwind-compatible classes
        const colors = {
            success: 'border-l-4 border-l-green-400',
            error: 'border-l-4 border-l-red-400',
            warning: 'border-l-4 border-l-yellow-400',
            info: 'border-l-4 border-l-blue-400'
        };
        const icons = {
            success: 'check_circle',
            error: 'error',
            warning: 'warning',
            info: 'info'
        };
        toast.className = `flex items-center gap-3 px-6 py-4 rounded-xl shadow-xl ${colors[type]} bg-[#2b2a26] text-[#e6e2db] transform translate-x-full opacity-0 transition-all duration-300`;
        toast.innerHTML = `
            <span class="material-symbols-outlined text-lg">${icons[type]}</span>
            <span class="text-sm font-medium">${message}</span>
        `;
        container.appendChild(toast);
        // Animate in
        requestAnimationFrame(() => {
            toast.style.transform = 'translateX(0)';
            toast.style.opacity = '1';
        });
        // Auto remove
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    },

    // Format currency (Indian Rupees)
    formatCurrency(amount) {
        return '₹' + Number(amount).toLocaleString('en-IN');
    },

    // Format date
    formatDate(dateStr) {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    },

    // Loading button state
    setButtonLoading(btn, loading, originalText) {
        if (loading) {
            btn.dataset.originalText = btn.textContent;
            btn.textContent = 'LOADING...';
            btn.disabled = true;
            btn.style.opacity = '0.7';
        } else {
            btn.textContent = originalText || btn.dataset.originalText || 'Submit';
            btn.disabled = false;
            btn.style.opacity = '1';
        }
    },

    // Confirm dialog
    async confirm(message) {
        return window.confirm(message);
    },

    // Debounce utility
    debounce(func, wait) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    },

    // Mobile menu toggle
    initMobileMenu() {
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');
        if (btn && menu) {
            btn.addEventListener('click', () => {
                menu.classList.toggle('hidden');
            });
        }
    }
};

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    App.initMobileMenu();
});

// Make globally available
window.App = App;
