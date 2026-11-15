<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">AirPort LED</div>
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
        <div class="topbar-title">Информация о рейсе</div>
        <div class="user-profile"><div class="avatar">A</div><span>Администратор</span></div>
      </header>

      <div class="content">
        <div class="header-action">
          <button class="back-btn" @click="$router.push('/flights')">← Назад к табло</button>
        </div>

        <div v-if="loading" class="loading">Загрузка данных...</div>
        <div v-else-if="error" class="error-msg">{{ error }}</div>
        
        <div v-else class="ticket-card">
          <div class="ticket-header">
            <h1>{{ flight.flight_number }}</h1>
            <span class="status" :class="flight.status">{{ translateStatus(flight.status) }}</span>
          </div>

          <div class="route-info">
            <div class="city-block">
              <span class="time">{{ formatTime(flight.departure_time) }}</span>
              <span class="city">{{ flight.origin_city }}</span>
              <span class="code">{{ flight.origin_iata }}</span>
            </div>
            
            <!-- ВМЕСТО САМОЛЕТИКА ТЕПЕРЬ ВРЕМЯ В ПУТИ -->
            <div class="flight-duration">
              <span class="duration-label">В пути</span>
              <span class="duration-time">{{ calculateDuration(flight.departure_time, flight.arrival_time) }}</span>
            </div>
            
            <div class="city-block">
              <span class="time">{{ formatTime(flight.arrival_time) }}</span>
              <span class="city">{{ flight.destination_city }}</span>
              <span class="code">{{ flight.destination_iata }}</span>
            </div>
          </div>

          <div class="details-grid">
            <div class="detail-item">
              <span class="label">Авиакомпания</span>
              <span class="value">{{ flight.airline_name }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Самолет</span>
              <span class="value">{{ flight.aircraft_model }} ({{ flight.aircraft_tail }})</span>
            </div>
            <div class="detail-item">
              <span class="label">Гейт</span>
              <span class="value gate-badge">{{ flight.gate || 'Не назначен' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Терминал</span>
              <span class="value">{{ flight.terminal || '1' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Полоса вылета</span>
              <span class="value">{{ flight.departure_runway_name || 'Не назначена' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">Полоса прилета</span>
              <span class="value">{{ flight.arrival_runway_name || 'Не назначена' }}</span>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const flight = ref(null);
const loading = ref(true);
const error = ref('');
const token = localStorage.getItem('access_token');

const fetchFlight = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8080/api/flights/${route.params.id}/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    flight.value = res.data;
  } catch (err) {
    error.value = 'Рейс не найден или ошибка соединения.';
  } finally {
    loading.value = false;
  }
};

const formatTime = (isoString) => new Date(isoString).toLocaleTimeString('ru-RU', {hour: '2-digit', minute:'2-digit'});
const translateStatus = (status) => { const map = { 'scheduled': 'По расписанию', 'delayed': 'Задержан', 'boarding': 'Посадка', 'departed': 'Вылетел', 'arrived': 'Прибыл', 'cancelled': 'Отменен' }; return map[status] || status; };

// ФУНКЦИЯ ВЫЧИСЛЕНИЯ ВРЕМЕНИ В ПУТИ
const calculateDuration = (dep, arr) => {
  const start = new Date(dep);
  const end = new Date(arr);
  const diffMs = end - start;
  
  if (diffMs <= 0) return '0 ч 0 мин';
  
  const diffHrs = Math.floor(diffMs / 3600000);
  const diffMins = Math.floor((diffMs % 3600000) / 60000);
  
  if (diffHrs > 0) {
    return `${diffHrs} ч ${diffMins} мин`;
  } else {
    return `${diffMins} мин`;
  }
};

const logout = () => { localStorage.removeItem('access_token'); router.push('/'); };

onMounted(() => { fetchFlight(); });
</script>

<style scoped>
.back-btn { background: none; border: 1px solid #cbd5e1; padding: 8px 15px; cursor: pointer; color: #64748b; font-weight: 600; transition: 0.2s; }
.back-btn:hover { background: #f1f5f9; color: #1e293b; }
.ticket-card { background: white; max-width: 800px; margin: 0 auto; border: 1px solid #e2e8f0; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
.ticket-header { display: flex; justify-content: space-between; align-items: center; padding: 25px 30px; border-bottom: 1px dashed #cbd5e1; background: #f8fafc; }
.ticket-header h1 { margin: 0; color: #2b3a28; font-size: 32px; }
.route-info { display: flex; justify-content: space-between; align-items: center; padding: 40px 30px; border-bottom: 1px solid #e2e8f0; }
.city-block { display: flex; flex-direction: column; align-items: center; width: 120px; }
.city-block .time { font-size: 36px; font-weight: 800; color: #2b3a28; }
.city-block .city { font-size: 16px; font-weight: 600; color: #1e293b; margin-top: 5px; }
.city-block .code { font-size: 14px; color: #64748b; }

/* НОВЫЕ СТИЛИ ДЛЯ ВРЕМЕНИ В ПУТИ */
.flight-duration { display: flex; flex-direction: column; align-items: center; justify-content: center; }
.duration-label { font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.5px; }
.duration-time { font-size: 18px; font-weight: 700; color: #2b3a28; margin-top: 5px; background: #f8fafc; padding: 4px 12px; border-radius: 4px; border: 1px solid #e2e8f0; }

.details-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; padding: 30px; }
.detail-item { display: flex; flex-direction: column; }
.detail-item .label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; margin-bottom: 5px; }
.detail-item .value { font-size: 16px; font-weight: 500; color: #1e293b; }
.status { padding: 8px 15px; font-size: 13px; font-weight: 700; text-transform: uppercase; border: 1px solid transparent;}
.status.scheduled { background: #e9f5db; color: #4a5d23; border-color: #c2d6a4; }
.status.delayed { background: #fff3e0; color: #e67e22; border-color: #ffcc80; }
.status.boarding { background: #fdebd0; color: #d35400; border-color: #f5cba7; }
.status.departed { background: #e9f5db; color: #4a5d23; border-color: #c2d6a4;}
.status.arrived { background: #2b3a28; color: white; }
.status.cancelled { background: #ffebee; color: #c62828; border-color: #ef9a9a; }
</style>