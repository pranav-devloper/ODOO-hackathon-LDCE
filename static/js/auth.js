(function() {
    document.addEventListener('DOMContentLoaded', () => {
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');
        const forgotPasswordForm = document.getElementById('forgot-password-form');
        
        const showError = (form, message) => {
            let errorDiv = form.querySelector('.auth-error');
            if (!errorDiv) {
                errorDiv = document.createElement('div');
                errorDiv.className = 'auth-error text-red-400 text-sm mb-4 p-3 bg-red-400/10 rounded-lg';
                form.insertBefore(errorDiv, form.firstChild);
            }
            errorDiv.textContent = message;
        };

        const clearError = (form) => {
            const errorDiv = form.querySelector('.auth-error');
            if (errorDiv) {
                errorDiv.remove();
            }
        };

        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                clearError(loginForm);
                const btn = loginForm.querySelector('button[type="submit"]');
                const formData = new FormData(loginForm);
                const data = Object.fromEntries(formData.entries());
                
                App.setButtonLoading(btn, true, 'LOGGING IN...');
                
                try {
                    const response = await App.api('/api/auth/login', {
                        method: 'POST',
                        body: data
                    });
                    
                    if (response.success) {
                        App.toast('Logged in successfully');
                        window.location.href = '/dashboard';
                    } else {
                        showError(loginForm, response.error?.message || 'Login failed');
                    }
                } catch (error) {
                    showError(loginForm, error.message || 'An error occurred during login');
                } finally {
                    App.setButtonLoading(btn, false, 'LOGIN');
                }
            });
        }

        if (signupForm) {
            signupForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                clearError(signupForm);
                
                const formData = new FormData(signupForm);
                const data = Object.fromEntries(formData.entries());
                
                if (data.password !== data.confirm_password) {
                    showError(signupForm, 'Passwords do not match');
                    return;
                }
                
                const btn = signupForm.querySelector('button[type="submit"]');
                App.setButtonLoading(btn, true, 'SIGNING UP...');
                
                try {
                    const response = await App.api('/api/auth/signup', {
                        method: 'POST',
                        body: data
                    });
                    
                    if (response.success) {
                        App.toast('Account created successfully');
                        window.location.href = '/dashboard';
                    } else {
                        showError(signupForm, response.error?.message || 'Signup failed');
                    }
                } catch (error) {
                    showError(signupForm, error.message || 'An error occurred during signup');
                } finally {
                    App.setButtonLoading(btn, false, 'SIGN UP');
                }
            });
        }
        
        if (forgotPasswordForm) {
            forgotPasswordForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                clearError(forgotPasswordForm);
                
                const formData = new FormData(forgotPasswordForm);
                const data = Object.fromEntries(formData.entries());
                
                const btn = forgotPasswordForm.querySelector('button[type="submit"]');
                App.setButtonLoading(btn, true, 'SENDING...');
                
                try {
                    const response = await App.api('/api/auth/forgot-password', {
                        method: 'POST',
                        body: data
                    });
                    
                    if (response.success) {
                        App.toast('Password reset link sent to your email');
                        forgotPasswordForm.reset();
                    } else {
                        showError(forgotPasswordForm, response.error?.message || 'Request failed');
                    }
                } catch (error) {
                    showError(forgotPasswordForm, error.message || 'An error occurred');
                } finally {
                    App.setButtonLoading(btn, false, 'SEND RESET LINK');
                }
            });
        }
    });
})();
