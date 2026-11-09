<template>
  <div class="layout">
    <!-- Меню -->
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

    <!-- Контент -->
    <main class="main-content">
      <header class="topbar">
        <div class="topbar-title">Управление рейсами</div>
        <div class="user-profile">
          <div class="avatar">A</div>
          <span>Администратор</span>
        </div>
      </header>

      <div class="content">
        <div class="header-action">
          <div>
            <h1 class="page-title">Онлайн-табло</h1>
            <p class="subtitle">Все актуальные рейсы аэропорта</p>
          </div>
          <button class="add-btn" @click="openCreateModal">+ Добавить рейс</button>
        </div>

        <!-- БЛОК СТАТИСТИКИ -->
        <div class="stats-grid" v-if="!loading">
          <div class="stat-card">
            <span class="stat-label">Всего рейсов</span>
            <span class="stat-value">{{ stats.total }}</span>
          </div>
          <div class="stat-card scheduled">
            <span class="stat-label">По расписанию</span>
            <span class="stat-value">{{ stats.scheduled }}</span>
          </div>
          <div class="stat-card delayed">
            <span class="stat-label">Задержано</span>
            <span class="stat-value">{{ stats.delayed }}</span>
          </div>
          <div class="stat-card cancelled">
            <span class="stat-label">Отменено</span>
            <span class="stat-value">{{ stats.cancelled }}</span>
          </div>
        </div>
        
        <div v-if="loading" class="loading">Загрузка данных...</div>
        
        <div v-else class="board-container">
          <table class="board-table">
            <thead>
              <tr>
                <th>Время</th>
                <th>Рейс</th>
                <th>Маршрут</th>
                <th>Авиакомпания</th>
                <th>Гейт</th>
                <th>Статус</th>
                <th style="text-align: right;">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="flight in flights" :key="flight.id">
                <td><span class="time-badge">{{ formatTime(flight.departure_time) }}</span></td>
                <td><b>{{ flight.flight_number }}</b></td>
                <td>{{ flight.origin_city }} <span class="arrow">➔</span> {{ flight.destination_city }}</td>
                <td>{{ flight.airline_name }}</td>
                <td><span class="gate-badge">{{ flight.gate || '-' }}</span></td>
                <td>
                  <span class="status" :class="flight.status">{{ translateStatus(flight.status) }}</span>
                </td>
                <td class="actions-cell">
                  <button class="action-btn edit" @click="openEditModal(flight)" title="Редактировать">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/></svg>
                  </button>
                  <button class="action-btn delete" @click="deleteFlight(flight.id)" title="Удалить">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/><path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Модальное окно (Форма) -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Редактировать рейс' : 'Новый рейс' }}</h2>
          <button class="close-modal" @click="closeModal">×</button>
        </div>
        
        <form @submit.prevent="saveFlight" class="flight-form">
          <div class="form-grid">
            <div class="form-group">
              <label>Номер рейса</label>
              <input type="text" v-model="form.flight_number" required placeholder="SU1234" />
            </div>
            <div class="form-group">
              <label>Гейт</label>
              <input type="text" v-model="form.gate" placeholder="A1" />
            </div>

            <div class="form-group">
              <label>Авиакомпания</label>
              <select v-model="form.airline" required>
                <option value="" disabled>Выберите...</option>
                <option v-for="a in lookups.airlines" :key="a.id" :value="a.id">{{ a.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Самолет</label>
              <select v-model="form.aircraft" required>
                <option value="" disabled>Выберите...</option>
                <option v-for="ac in lookups.aircrafts" :key="ac.id" :value="ac.id">{{ ac.model }} ({{ ac.tail_number }})</option>
              </select>
            </div>

            <div class="form-group">
              <label>Откуда</label>
              <select v-model="form.origin" required>
                <option value="" disabled>Выберите...</option>
                <option v-for="ap in lookups.airports" :key="ap.id" :value="ap.id">{{ ap.city }} ({{ ap.iata_code }})</option>
              </select>
            </div>
            <div class="form-group">
              <label>Куда</label>
              <select v-model="form.destination" required>
                <option value="" disabled>Выберите...</option>
                <option v-for="ap in lookups.airports" :key="ap.id" :value="ap.id">{{ ap.city }} ({{ ap.iata_code }})</option>
              </select>
            </div>

            <div class="form-group">
              <label>Время вылета</label>
              <input type="datetime-local" v-model="form.departure_time" required />
            </div>
            <div class="form-group">
              <label>Время прилета</label>
              <input type="datetime-local" v-model="form.arrival_time" required />
            </div>

            <div class="form-group">
              <label>Полоса вылета</label>
              <select v-model="form.departure_runway">
                <option :value="null">Не назначена</option>
                <option v-for="r in lookups.runways" :key="r.id" :value="r.id">{{ r.airport_iata }} - {{ r.name }}</option>
              </select>
            </div>
            <div class="form-group">
              <label>Полоса прилета</label>
              <select v-model="form.arrival_runway">
                <option :value="null">Не назначена</option>
                <option v-for="r in lookups.runways" :key="r.id" :value="r.id">{{ r.airport_iata }} - {{ r.name }}</option>
              </select>
            </div>

            <div class="form-group full-width">
              <label>Статус рейса</label>
              <select v-model="form.status" required>
                <option value="scheduled">По расписанию</option>
                <option value="delayed">Задержан</option>
                <option value="boarding">Посадка</option>
                <option value="departed">Вылетел</option>
                <option value="arrived">Прибыл</option>
                <option value="cancelled">Отменен</option>
              </select>
            </div>
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">Отмена</button>
            <button type="submit" class="save-btn" :disabled="saving">
              {{ saving ? 'Сохранение...' : 'Сохранить' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue'; // Добавили computed
import { useRouter } from 'vue-router';
import axios from 'axios';

const flights = ref([]);
const loading = ref(true);
const router = useRouter();
const token = localStorage.getItem('access_token');
const apiUrl = 'http://127.0.0.1:8080/api';

// ВЫЧИСЛЯЕМАЯ СТАТИСТИКА (пересчитывается автоматически при изменении flights)
const stats = computed(() => {
  const list = flights.value;
  return {
    total: list.length,
    scheduled: list.filter(f => f.status === 'scheduled').length,
    delayed: list.filter(f => f.status === 'delayed').length,
    cancelled: list.filter(f => f.status === 'cancelled').length
  };
});

const lookups = reactive({ airlines: [], aircrafts: [], airports: [], runways: [] });
const showModal = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const currentId = ref(null);

const form = reactive({
  flight_number: '', airline: '', aircraft: '', origin: '', destination: '',
  departure_time: '', arrival_time: '', status: 'scheduled', gate: '',
  departure_runway: null, arrival_runway: null
});

const fetchData = async () => {
  try {
    loading.value = true;
    const config = { headers: { Authorization: `Bearer ${token}` } };
    
    const [fRes, aRes, acRes, apRes, rRes] = await Promise.all([
      axios.get(`${apiUrl}/flights/`, config),
      axios.get(`${apiUrl}/airlines/`, config),
      axios.get(`${apiUrl}/aircrafts/`, config),
      axios.get(`${apiUrl}/airports/`, config),
      axios.get(`${apiUrl}/runways/`, config)
    ]);

    flights.value = fRes.data.sort((a, b) => new Date(a.departure_time) - new Date(b.departure_time));
    lookups.airlines = aRes.data;
    lookups.aircrafts = acRes.data;
    lookups.airports = apRes.data;
    lookups.runways = rRes.data.map(r => {
       const airport = apRes.data.find(a => a.id === r.airport);
       return { ...r, airport_iata: airport ? airport.iata_code : '???' };
    });
  } catch (err) {
    if (err.response?.status === 401) router.push('/');
  } finally {
    loading.value = false;
  }
};

const openCreateModal = () => {
  isEditing.value = false;
  currentId.value = null;
  Object.assign(form, {
    flight_number: '', airline: '', aircraft: '', origin: '', destination: '',
    departure_time: '', arrival_time: '', status: 'scheduled', gate: '',
    departure_runway: null, arrival_runway: null
  });
  showModal.value = true;
};

const openEditModal = (flight) => {
  isEditing.value = true;
  currentId.value = flight.id;
  Object.assign(form, {
    flight_number: flight.flight_number,
    airline: flight.airline,
    aircraft: flight.aircraft,
    origin: flight.origin,
    destination: flight.destination,
    departure_time: flight.departure_time.slice(0, 16), 
    arrival_time: flight.arrival_time.slice(0, 16),
    status: flight.status,
    gate: flight.gate || '',
    departure_runway: flight.departure_runway,
    arrival_runway: flight.arrival_runway
  });
  showModal.value = true;
};

const closeModal = () => { showModal.value = false; };

const saveFlight = async () => {
  saving.value = true;
  const config = { headers: { Authorization: `Bearer ${token}` } };
  
  // Копируем форму, чтобы не менять её в интерфейсе
  const payload = { ...form };
  
  // Если в дате нет секунд, Django может ругаться. Добавляем ":00", если их нет.
  if (payload.departure_time && payload.departure_time.length === 16) payload.departure_time += ':00';
  if (payload.arrival_time && payload.arrival_time.length === 16) payload.arrival_time += ':00';

  try {
    if (isEditing.value) { 
      await axios.patch(`${apiUrl}/flights/${currentId.value}/`, payload, config); 
    } else { 
      await axios.post(`${apiUrl}/flights/`, payload, config); 
    }
    closeModal(); 
    await fetchData();
  } catch (err) { 
    console.error("Ошибка от Django:", err.response?.data); 
    alert('Ошибка при сохранении. Проверьте консоль (F12).'); 
  } finally { 
    saving.value = false; 
  }
};

const deleteFlight = async (id) => {
  if (!confirm('Удалить этот рейс?')) return;
  try {
    const config = { headers: { Authorization: `Bearer ${token}` } };
    await axios.delete(`${apiUrl}/flights/${id}/`, config);
    await fetchData();
  } catch (err) { alert('Ошибка при удалении'); }
};

const formatTime = (isoString) => {
  return new Date(isoString).toLocaleTimeString('ru-RU', {hour: '2-digit', minute:'2-digit'});
};

const translateStatus = (status) => {
  const map = { 'scheduled': 'По расписанию', 'delayed': 'Задержан', 'boarding': 'Посадка', 'departed': 'Вылетел', 'arrived': 'Прибыл', 'cancelled': 'Отменен' };
  return map[status] || status;
};

const logout = () => {
  localStorage.removeItem('access_token');
  router.push('/');
};

onMounted(() => { fetchData(); });
</script>

<style scoped>
/* Шапка контента */
.topbar-title { font-size: 16px; font-weight: 600; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px;}
.user-profile { display: flex; align-items: center; gap: 12px; font-weight: 600; color: #0b3d2e; }
.avatar { 
  width: 36px; height: 36px; background: #e67e22; color: white; 
  border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; 
}

.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.subtitle { color: #7f8c8d; margin: 5px 0 0 0; font-size: 15px; }

/* --- БЛОК СТАТИСТИКИ --- */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  padding: 20px 25px;
  border: 1px solid #e1e8ed;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 5px rgba(0,0,0,0.02);
}

.stat-label {
  font-size: 13px;
  color: #7f8c8d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 32px;
  font-weight: 800;
  color: #0b3d2e; /* По умолчанию темно-зеленый */
}

/* Цвета для разных карточек */
.stat-card.scheduled .stat-value { color: #1e8449; } /* Зеленый */
.stat-card.delayed .stat-value { color: #e65100; }   /* Оранжевый */
.stat-card.cancelled .stat-value { color: #c62828; } /* Красный */

/* Кнопка добавления */
.add-btn { 
  background: #1e5631; color: white; border: none; padding: 12px 24px; 
  border-radius: 0; /* Убрали скругление для строгости */
  font-weight: 600; font-size: 14px; cursor: pointer; 
  transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px;
}
.add-btn:hover { background: #0b3d2e; }

/* Бейджи в таблице */
.time-badge { font-weight: 700; color: #0b3d2e; font-size: 15px; }
.gate-badge { background: #f0f4f3; padding: 4px 10px; font-weight: 600; font-size: 13px; border: 1px solid #e1e8ed;}
.arrow { color: #bdc3c7; margin: 0 5px; font-size: 12px;}

/* Статусы */
.status { padding: 6px 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid transparent;}
.status.scheduled { background: #e3f9ec; color: #1e8449; border-color: #a5d6a7; }
.status.delayed { background: #fff3e0; color: #e65100; border-color: #ffcc80; }
.status.boarding { background: #fdebd0; color: #d35400; border-color: #f5cba7; }
.status.departed { background: #e8f5e9; color: #2e7d32; border-color: #a5d6a7;}
.status.arrived { background: #0b3d2e; color: white; }
.status.cancelled { background: #ffebee; color: #c62828; border-color: #ef9a9a; }

/* Кнопки действий */
.actions-cell { display: flex; justify-content: flex-end; gap: 8px; }
.action-btn { 
  background: #ffffff; border: 1px solid #e1e8ed; 
  width: 32px; height: 32px; display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s ease; color: #7f8c8d;
}
.action-btn svg { width: 14px; height: 14px; }
.action-btn.edit:hover { background: #f0f4f3; border-color: #1e5631; color: #1e5631; }
.action-btn.delete:hover { background: #ffebee; border-color: #c62828; color: #c62828; }

/* Модальное окно */
.modal-overlay { 
  position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
  background: rgba(43, 58, 40, 0.7); 
  backdrop-filter: blur(3px); /* Легкое размытие фона */
  display: flex; justify-content: center; align-items: center; z-index: 1000; 
}

.modal-content { 
  background: white; width: 100%; max-width: 750px; 
  box-shadow: 0 25px 50px rgba(0,0,0,0.25); max-height: 90vh; overflow-y: auto; 
  border: 1px solid #e2e8f0;
}

.modal-header { 
  padding: 25px 30px; border-bottom: 1px solid #e2e8f0; 
  display: flex; justify-content: space-between; align-items: center; 
  background: #f8fafc;
}

/* Оранжевая полоска у заголовка */
.modal-header h2 { 
  margin: 0; color: #2b3a28; font-size: 22px; font-weight: 700; 
  border-left: 5px solid #e67e22; 
  padding-left: 15px;
}

.close-modal { 
  background: #ffffff; border: 1px solid #e2e8f0; width: 32px; height: 32px;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; color: #94a3b8; cursor: pointer; transition: 0.2s;
}
.close-modal:hover { color: #c62828; border-color: #c62828; background: #ffebee; }

.flight-form { padding: 30px; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-group { display: flex; flex-direction: column; }
.form-group.full-width { grid-column: span 2; }

.form-group label { 
  font-size: 12px; font-weight: 700; color: #64748b; 
  margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; 
}

/* Поля ввода */
.form-group input, .form-group select { 
  padding: 12px 15px; border: 1px solid #cbd5e1; font-size: 14px; 
  background: #ffffff; transition: 0.2s; border-radius: 0; 
  font-family: 'Inter', sans-serif; color: #1e293b;
}

/* Подсветка оранжевым при клике */
.form-group input:focus, .form-group select:focus { 
  border-color: #e67e22; 
  outline: none; 
  box-shadow: 0 0 0 3px rgba(230, 126, 34, 0.15); 
}

.modal-actions { 
  display: flex; justify-content: flex-end; gap: 15px; 
  margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; 
}

/* Кнопка ОТМЕНА (прозрачная с рамкой) */
.cancel-btn { 
  background: transparent; color: #64748b; 
  border: 1px solid #cbd5e1; padding: 12px 25px; 
  cursor: pointer; font-weight: 600; transition: 0.2s;
  font-family: 'Inter', sans-serif;
}
.cancel-btn:hover { background: #f1f5f9; color: #1e293b; }

/* Кнопка СОХРАНИТЬ (Оранжевая) */
.save-btn { 
  background: #e67e22; color: white; border: 1px solid #e67e22; 
  padding: 12px 30px; cursor: pointer; font-weight: 700; 
  transition: 0.2s; font-family: 'Inter', sans-serif;
}
.save-btn:hover { background: #d35400; border-color: #d35400; }
.save-btn:disabled { background: #cbd5e1; border-color: #cbd5e1; cursor: not-allowed; }
</style>