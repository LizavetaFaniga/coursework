<template>
  <div class="login-layout">
    
    <!-- Левая панель с брендингом и картинкой -->
    <div class="brand-panel">
      <div class="brand-content">
        <h1>AirPort<br>Management</h1>
        <p>Единая система управления расписанием и ресурсами международного аэропорта.</p>
      </div>
    </div>

    <!-- Правая панель с формой -->
    <div class="form-panel">
      <div class="form-wrapper">
        <div class="form-header">
          <h2>Вход для администратора</h2>
          <p>Пожалуйста, авторизуйтесь для доступа к панели управления</p>
        </div>
        
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label>Логин</label>
            <input type="text" v-model="username" required placeholder="Введите ваш логин" />
          </div>
          
          <div class="form-group">
            <label>Пароль</label>
            <input type="password" v-model="password" required placeholder="Введите пароль" />
          </div>
          
          <button type="submit" :disabled="loading">
            {{ loading ? 'Авторизация...' : 'Войти в систему' }}
          </button>
          
          <p v-if="error" class="error">{{ error }}</p>
        </form>
        
        <div class="form-footer">
          <p>© 2024 Система управления аэропортом</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);
const router = useRouter();

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    const response = await axios.post('http://127.0.0.1:8080/api/token/', {
      username: username.value,
      password: password.value
    });
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    router.push('/flights');
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'Неверный логин или пароль';
    } else {
      error.value = 'Ошибка соединения с сервером. Проверьте, запущен ли бэкенд.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* Общий каркас */
.login-layout {
  display: flex;
  min-height: 100vh;
  background: #f4f5f7;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Левая панель (ТОТ САМЫЙ НЕЙТРАЛЬНЫЙ СЕРЫЙ) */
.brand-panel {
  display: none; 
  width: 45%;
  /* Чистый серый цвет без синевы */
  background: linear-gradient(135deg, rgba(60, 60, 60, 0.65), rgba(80, 80, 80, 0.75)), 
              url('/airport.png') center/cover no-repeat;
  padding: 60px;
  flex-direction: column;
  justify-content: flex-end;
  color: white;
}

@media (min-width: 900px) {
  .brand-panel { display: flex; } 
}

.brand-content h1 {
  font-size: 42px;
  font-weight: 800;
  margin: 0 0 20px 0;
  line-height: 1.2;
  letter-spacing: 1px;
}

.brand-content p {
  font-size: 18px;
  color: #dddddd; /* Светло-серый текст */
  line-height: 1.6;
  max-width: 400px;
  margin: 0;
}

/* Правая панель */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

/* Белая карточка */
.form-wrapper {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  padding: 45px; 
  border: 1px solid #e2e8f0; 
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05); 
}

.form-header {
  margin-bottom: 35px;
  text-align: center; 
}

.form-header h2 {
  margin: 0 0 10px 0;
  color: #2b3a28; /* Оливковый */
  font-size: 26px;
  font-weight: 700;
}

.form-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
  line-height: 1.4;
}

/* Поля ввода */
.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #1e293b;
  font-weight: 600;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

input {
  width: 100%;
  padding: 14px 16px;
  box-sizing: border-box;
  border: 1px solid #cbd5e1;
  font-size: 15px;
  color: #1e293b;
  transition: all 0.3s ease;
  background: #f8fafc;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

input:focus {
  border-color: #2b3a28;
  background: #ffffff;
  outline: none;
}

/* ОЛИВКОВАЯ КНОПКА */
button {
  width: 100%;
  padding: 16px;
  background: #2b3a28; /* Оливковый */
  color: white;
  border: none;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s ease;
  margin-top: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

button:hover {
  background: #1e2b1c;
}

button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
}

/* Ошибка и футер */
.error {
  color: #c62828;
  margin-top: 15px;
  font-size: 14px;
  text-align: center;
  font-weight: 500;
  background: #ffebee;
  padding: 10px;
}

.form-footer {
  margin-top: 40px;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}
</style>