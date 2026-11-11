<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">AirPort</div>
      <nav class="menu">
        <router-link to="/flights">Табло рейсов</router-link>
        <router-link to="/airlines">Авиакомпании</router-link>
        <router-link to="/airports">Аэропорты</router-link>
        <router-link to="/aircrafts">Самолеты</router-link>
        <router-link to="/runways">ВПП</router-link>
      </nav>
      <button @click="logout" class="logout-btn">Выйти</button>
    </aside>
    <main class="main-content">
      <header class="topbar">
        <div class="topbar-title">Справочники</div>
        <div class="user-profile"><div class="avatar">A</div><span>Администратор</span></div>
      </header>
      <div class="content">
        <div class="header-action">
          <div><h1 class="page-title">Взлетно-посадочные полосы</h1><p class="subtitle">Инфраструктура и занятость</p></div>
        </div>
        <div v-if="loading" class="loading">Загрузка...</div>
        <div v-else class="board-container">
          <table class="board-table">
            <thead>
              <tr><th>Аэропорт (ID)</th><th>Название</th><th>Длина (м)</th><th>Статус</th><th>Текущий рейс</th></tr>
            </thead>
            <tbody>
              <tr v-for="rw in runways" :key="rw.id">
                <td><span class="gate-badge">{{ rw.airport_full_name }}</span></td>
                <td><b>{{ rw.name }}</b></td>
                <td>{{ rw.length_m }}</td>
                <td>
                  <span :class="rw.is_active ? 'status scheduled' : 'status cancelled'">{{ rw.is_active ? 'Свободна' : 'Закрыта' }}</span>
                </td>
                <td>
                  <span v-if="rw.active_flight" class="status delayed">✈️ {{ rw.active_flight }}</span>
                  <span v-else style="color: #94a3b8;">Нет рейсов</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
const runways = ref([]); const loading = ref(true); const router = useRouter(); const token = localStorage.getItem('access_token');
const fetchRunways = async () => {
  try { const res = await axios.get('http://127.0.0.1:8080/api/runways/', { headers: { Authorization: `Bearer ${token}` } }); runways.value = res.data; } 
  catch (err) { if (err.response?.status === 401) router.push('/'); } finally { loading.value = false; }
};
const logout = () => { localStorage.removeItem('access_token'); router.push('/'); };
onMounted(() => { fetchRunways(); });
</script>

<style scoped>
.topbar-title { font-size: 16px; font-weight: 600; color: #64748b; text-transform: uppercase; }
.user-profile { display: flex; align-items: center; gap: 12px; font-weight: 600; color: #2b3a28; }
.avatar { width: 36px; height: 36px; background: #e67e22; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.subtitle { color: #64748b; margin: 5px 0 0 0; font-size: 15px; }
.gate-badge { background: #f0f4f3; padding: 4px 10px; font-weight: 700; border: 1px solid #e2e8f0; color: #2b3a28;}
.status { padding: 6px 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; border: 1px solid transparent;}
.status.scheduled { background: #e9f5db; color: #4a5d23; border-color: #c2d6a4; }
.status.cancelled { background: #ffebee; color: #c62828; border-color: #ef9a9a; }
.status.delayed { background: #fff3e0; color: #e67e22; border-color: #ffcc80; }
.loading { text-align: center; padding: 50px; color: #64748b; }
</style>