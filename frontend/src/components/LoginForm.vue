<template>
  <div class="login-container">
    <div class="login-card">
      <h1 class="login-title">iqOption Trading Login</h1>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <!-- Email Input -->
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="Enter your iqOption email"
            class="form-input"
            :disabled="isLoading"
            required
          />
        </div>

        <!-- Password Input -->
        <div class="form-group">
          <label for="password" class="form-label">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Enter your password"
            class="form-input"
            :disabled="isLoading"
            required
            minlength="6"
          />
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
          <span class="error-icon">⚠</span>
          {{ errorMessage }}
        </div>

        <!-- Loading Indicator -->
        <div v-if="isLoading" class="loading-indicator">
          <span class="spinner"></span>
          Authenticating...
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="btn-login"
          :disabled="isLoading || !email || !password"
        >
          {{ isLoading ? 'Signing In...' : 'Sign In' }}
        </button>
      </form>

      <!-- Info Footer -->
      <div class="login-footer">
        <p>Use your iqOption broker credentials to log in</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginForm',
  props: {
    apiUrl: {
      type: String,
      default: 'http://localhost:5000'
    }
  },
  data() {
    return {
      email: '',
      password: '',
      isLoading: false,
      errorMessage: ''
    };
  },
  methods: {
    async handleLogin() {
      // Clear previous error
      this.errorMessage = '';

      // Validate form
      if (!this.email || !this.password) {
        this.errorMessage = 'Please enter both email and password';
        return;
      }

      if (this.password.length < 6) {
        this.errorMessage = 'Password must be at least 6 characters';
        return;
      }

      this.isLoading = true;

      try {
        const response = await fetch(`${this.apiUrl}/api/broker/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.errorMessage = data.error || 'Login failed';
          this.isLoading = false;
          return;
        }

        // Emit login event with session data
        this.$emit('login', {
          sessionId: data.sessionId,
          email: this.email,
          mode: data.mode
        });

        // Store session in localStorage
        localStorage.setItem('sessionId', data.sessionId);
        localStorage.setItem('userEmail', this.email);
        localStorage.setItem('tradingMode', data.mode);
      } catch (error) {
        this.errorMessage = `Connection error: ${error.message}`;
      } finally {
        this.isLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 40px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  text-align: center;
  color: #333;
  font-size: 28px;
  margin-bottom: 30px;
  font-weight: 700;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-weight: 600;
  color: #333;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  padding: 12px 15px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  transition: all 0.3s ease;
  font-family: inherit;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  background-color: #f8f9ff;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 15px;
  background-color: #fee;
  color: #c33;
  border-radius: 8px;
  font-size: 14px;
  border-left: 4px solid #c33;
}

.error-icon {
  font-size: 18px;
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  background-color: #f0f4ff;
  border-radius: 8px;
  color: #667eea;
  font-size: 14px;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid #e0e0e0;
  border-top: 2px solid #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-login {
  padding: 12px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

.btn-login:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #e0e0e0;
  color: #666;
  font-size: 13px;
}

.login-footer p {
  margin: 0;
}

/* Dark mode support */
.dark-mode .login-card {
  background: #1e1e1e;
  color: #fff;
}

.dark-mode .login-title {
  color: #fff;
}

.dark-mode .form-label {
  color: #e0e0e0;
}

.dark-mode .form-input {
  background: #2d2d2d;
  color: #fff;
  border-color: #444;
}

.dark-mode .form-input:focus {
  border-color: #667eea;
  background-color: #1a1a1a;
}

.dark-mode .login-footer {
  border-top-color: #444;
  color: #999;
}
</style>
