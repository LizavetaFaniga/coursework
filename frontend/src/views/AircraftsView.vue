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
          <div><h1 class="page-title">Самолеты</h1><p class="subtitle">Парк воздушных судов</p></div>
        </div>
        <div v-if="loading" class="loading">Загрузка...</div>
        <div v-else class="board-container">
          <table class="board-table">
            <thead><tr><th>Бортовой номер</th><th>Модель</th><th>Вместимость</th><th>Авиакомпания</th></tr></thead>
            <tbody>
              <tr v-for="ac in aircrafts" :key="ac.id">
                <td><b>{{ ac.tail_number }}</b></td>
                <td>{{ ac.model }}</td>
                <td>{{ ac.capacity }} мест</td>
                <td><span class="gate-badge">{{ ac.airline_name }}</span></td>
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

const aircrafts = ref([]); 
const loading = ref(true); 
const router = useRouter(); 
const token = localStorage.getItem('access_token');

const fetchAircrafts = async () => {
  try { 
    const res = await axios.get('http://127.0.0.1:8080/api/aircrafts/', { headers: { Authorization: `Bearer ${token}` } }); 
    aircrafts.value = res.data; 
  } catch (err) { 
    if (err.response?.status === 401) router.push('/'); 
  } finally { 
    loading.value = false; 
  }
};

const logout = () => { localStorage.removeItem('access_token'); router.push('/'); };
onMounted(() => { fetchAircrafts(); });
</script>

<style scoped>
.topbar-title { font-size: 16px; font-weight: 600; color: #64748b; text-transform: uppercase; }
.user-profile { display: flex; align-items: center; gap: 12px; font-weight: 600; color: #2b3a28; }
.avatar { width: 36px; height: 36px; background: #e67e22; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.subtitle { color: #64748b; margin: 5px 0 0 0; font-size: 15px; }
.gate-badge { background: #f0f4f3; padding: 4px 10px; font-weight: 700; border: 1px solid #e2e8f0; color: #2b3a28;}
.loading { text-align: center; padding: 50px; color: #64748b; }
</style>