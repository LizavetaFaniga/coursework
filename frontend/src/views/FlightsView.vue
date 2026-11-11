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
        <div class="topbar-title">Управление рейсами</div>
        <div class="user-profile"><div class="avatar">A</div><span>Администратор</span></div>
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
          <div class="stat-card" :class="{ active: filters.status === '' }" @click="setFilter('')">
            <span class="stat-label">Всего рейсов</span>
            <span class="stat-value">{{ stats.total }}</span>
          </div>
          <div class="stat-card scheduled" :class="{ active: filters.status === 'scheduled' }" @click="setFilter('scheduled')">
            <span class="stat-label">По расписанию</span>
            <span class="stat-value">{{ stats.scheduled }}</span>
          </div>
          <div class="stat-card delayed" :class="{ active: filters.status === 'delayed' }" @click="setFilter('delayed')">
            <span class="stat-label">Задержано</span>
            <span class="stat-value">{{ stats.delayed }}</span>
          </div>
          <div class="stat-card cancelled" :class="{ active: filters.status === 'cancelled' }" @click="setFilter('cancelled')">
            <span class="stat-label">Отменено</span>
            <span class="stat-value">{{ stats.cancelled }}</span>
          </div>
        </div>

        <!-- ПАНЕЛЬ ПОИСКА И ФИЛЬТРАЦИИ -->
        <div class="filters-panel">
          <div class="search-box">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#64748b" viewBox="0 0 16 16"><path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/></svg>
            <input 
              type="text" 
              v-model="filters.search" 
              @input="debounceFetch"
              placeholder="Поиск по номеру рейса или городу..." 
            />
          </div>
          <div class="filter-box">
            <select v-model="filters.status" @change="fetchData">
              <option value="">Все статусы</option>
              <option value="scheduled">По расписанию</option>
              <option value="delayed">Задержан</option>
              <option value="boarding">Посадка</option>
              <option value="departed">Вылетел</option>
              <option value="arrived">Прибыл</option>
              <option value="cancelled">Отменен</option>
            </select>
          </div>
          <div class="filter-box">
            <select v-model="filters.airline" @change="fetchData">
              <option value="">Все авиакомпании</option>
              <option v-for="a in lookups.airlines" :key="a.id" :value="a.id">{{ a.name }}</option>
            </select>
          </div>
          <div class="filter-box">
            <select v-model="filters.ordering" @change="fetchData">
              <option value="departure_time">Сначала ранние</option>
              <option value="-departure_time">Сначала поздние</option>
              <option value="flight_number">По номеру рейса</option>
            </select>
          </div>
        </div>
        
        <div v-if="loading" class="loading">Загрузка данных...</div>
        
        <div v-else class="board-container">
          <table class="board-table">
            <thead>
              <tr>
                <th>Время</th><th>Рейс</th><th>Маршрут</th><th>Авиакомпания</th><th>Гейт</th><th>Статус</th><th style="text-align: right;">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="flight in flights" :key="flight.id">
                <td><span class="time-badge">{{ formatTime(flight.departure_time) }}</span></td>
                <td><b>{{ flight.flight_number }}</b></td>
                <td>{{ flight.origin_city }} <span class="arrow">➔</span> {{ flight.destination_city }}</td>
                <td>{{ flight.airline_name }}</td>
                <td><span class="gate-badge">{{ flight.gate || '-' }}</span></td>
                <td><span class="status" :class="flight.status">{{ translateStatus(flight.status) }}</span></td>
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

    <!-- МОДАЛЬНОЕ ОКНО -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ isEditing ? 'Редактировать рейс' : 'Новый рейс' }}</h2>
          <button class="close-modal" @click="closeModal">×</button>
        </div>
        
        <form @submit.prevent="saveFlight" class="flight-form">
          <div class="form-grid">
            <div class="form-group"><label>Номер рейса</label><input type="text" v-model="form.flight_number" required /></div>
            <div class="form-group"><label>Гейт</label><input type="text" v-model="form.gate" /></div>

            <div class="form-group"><label>Авиакомпания</label><select v-model="form.airline" required><option value="" disabled>Выберите...</option><option v-for="a in lookups.airlines" :key="a.id" :value="a.id">{{ a.name }}</option></select></div>
            <div class="form-group"><label>Самолет</label><select v-model="form.aircraft" required><option value="" disabled>Выберите...</option><option v-for="ac in lookups.aircrafts" :key="ac.id" :value="ac.id">{{ ac.model }} ({{ ac.tail_number }})</option></select></div>

            <div class="form-group"><label>Откуда</label><select v-model="form.origin" required><option value="" disabled>Выберите...</option><option v-for="ap in lookups.airports" :key="ap.id" :value="ap.id">{{ ap.city }} ({{ ap.iata_code }})</option></select></div>
            <div class="form-group"><label>Куда</label><select v-model="form.destination" required><option value="" disabled>Выберите...</option><option v-for="ap in lookups.airports" :key="ap.id" :value="ap.id">{{ ap.city }} ({{ ap.iata_code }})</option></select></div>

            <div class="form-group"><label>Время вылета</label><input type="datetime-local" v-model="form.departure_time" required /></div>
            <div class="form-group"><label>Время прилета</label><input type="datetime-local" v-model="form.arrival_time" required /></div>

            <!-- Полоса вылета -->
            <div class="form-group">
              <label>Полоса вылета</label>
              <select v-model="form.departure_runway">
                <option :value="null">Не назначена</option>
                <option 
                  v-for="r in lookups.runways.filter(rw => rw.airport === form.origin)" 
                  :key="r.id" :value="r.id"
                  :disabled="r.status_text !== 'СВОБОДНА'" 
                  :style="r.status_text !== 'СВОБОДНА' ? 'color: #c62828;' : 'color: #1e293b;'"
                >
                  {{ r.name }} [{{ r.status_text }}]
                </option>
              </select>
            </div>

            <!-- Полоса прилета -->
            <div class="form-group">
              <label>Полоса прилета</label>
              <select v-model="form.arrival_runway">
                <option :value="null">Не назначена</option>
                <option 
                  v-for="r in lookups.runways.filter(rw => rw.airport === form.destination)" 
                  :key="r.id" :value="r.id"
                  :disabled="r.status_text !== 'СВОБОДНА'"
                  :style="r.status_text !== 'СВОБОДНА' ? 'color: #c62828;' : 'color: #1e293b;'"
                >
                  {{ r.name }} [{{ r.status_text }}]
                </option>
              </select>
            </div>

            <div class="form-group full-width"><label>Статус рейса</label><select v-model="form.status" required><option value="scheduled">По расписанию</option><option value="delayed">Задержан</option><option value="boarding">Посадка</option><option value="departed">Вылетел</option><option value="arrived">Прибыл</option><option value="cancelled">Отменен</option></select></div>
          </div>

          <!-- Блок вывода ошибки валидации -->
          <div v-if="modalError" class="validation-error">
            ⚠️ {{ modalError }}
          </div>

          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">Отмена</button>
            <button type="submit" class="save-btn" :disabled="saving">{{ saving ? 'Сохранение...' : 'Сохранить' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const flights = ref([]);
const loading = ref(true);
const router = useRouter();
const token = localStorage.getItem('access_token');
const apiUrl = 'http://127.0.0.1:8080/api';

const filters = reactive({ search: '', status: '', airline: '', ordering: 'departure_time' });
let debounceTimer = null;

const stats = computed(() => {
  const list = flights.value;
  return { total: list.length, scheduled: list.filter(f => f.status === 'scheduled').length, delayed: list.filter(f => f.status === 'delayed').length, cancelled: list.filter(f => f.status === 'cancelled').length };
});

const lookups = reactive({ airlines: [], aircrafts: [], airports: [], runways: [] });
const showModal = ref(false);
const isEditing = ref(false);
const saving = ref(false);
const currentId = ref(null);
const modalError = ref('');

const form = reactive({ flight_number: '', airline: '', aircraft: '', origin: '', destination: '', departure_time: '', arrival_time: '', status: 'scheduled', gate: '', departure_runway: null, arrival_runway: null });

const fetchData = async () => {
  try {
    loading.value = true;
    const config = { headers: { Authorization: `Bearer ${token}` } };
    
    let flightUrl = `${apiUrl}/flights/?`;
    if (filters.search) flightUrl += `search=${filters.search}&`;
    if (filters.status) flightUrl += `status=${filters.status}&`;
    if (filters.airline) flightUrl += `airline=${filters.airline}&`;
    if (filters.ordering) flightUrl += `ordering=${filters.ordering}&`;

    const [fRes, aRes, acRes, apRes, rRes] = await Promise.all([
      axios.get(flightUrl, config), 
      axios.get(`${apiUrl}/airlines/`, config), 
      axios.get(`${apiUrl}/aircrafts/`, config), 
      axios.get(`${apiUrl}/airports/`, config), 
      axios.get(`${apiUrl}/runways/`, config)
    ]);
    
    flights.value = fRes.data.sort((a, b) => new Date(a.departure_time) - new Date(b.departure_time));
    lookups.airlines = aRes.data; lookups.aircrafts = acRes.data; lookups.airports = apRes.data;
    lookups.runways = rRes.data; 
  } catch (err) { 
    if (err.response?.status === 401) router.push('/'); 
  } finally { 
    loading.value = false; 
  }
};

const debounceFetch = () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => { fetchData(); }, 500);
};

const setFilter = (status) => {
  filters.status = status;
  fetchData();
};

const openCreateModal = () => { 
  isEditing.value = false; currentId.value = null; modalError.value = '';
  Object.assign(form, { flight_number: '', airline: '', aircraft: '', origin: '', destination: '', departure_time: '', arrival_time: '', status: 'scheduled', gate: '', departure_runway: null, arrival_runway: null }); 
  showModal.value = true; 
};

const openEditModal = (flight) => { 
  isEditing.value = true; currentId.value = flight.id; modalError.value = '';
  Object.assign(form, { flight_number: flight.flight_number, airline: flight.airline, aircraft: flight.aircraft, origin: flight.origin, destination: flight.destination, departure_time: flight.departure_time.slice(0, 16), arrival_time: flight.arrival_time.slice(0, 16), status: flight.status, gate: flight.gate || '', departure_runway: flight.departure_runway, arrival_runway: flight.arrival_runway }); 
  showModal.value = true; 
};

const closeModal = () => { showModal.value = false; };

const saveFlight = async () => {
  saving.value = true;
  modalError.value = '';
  
  const payload = { ...form };
  if (payload.departure_time && payload.departure_time.length === 16) payload.departure_time += ':00';
  if (payload.arrival_time && payload.arrival_time.length === 16) payload.arrival_time += ':00';

  const config = { headers: { Authorization: `Bearer ${token}` } };
  try {
    if (isEditing.value) { await axios.patch(`${apiUrl}/flights/${currentId.value}/`, payload, config); } 
    else { await axios.post(`${apiUrl}/flights/`, payload, config); }
    closeModal(); await fetchData();
  } catch (err) { 
    console.error(err.response?.data);
    if (err.response && err.response.data) {
      const errors = err.response.data;
      let errorMessages = [];
      for (const key in errors) {
        errorMessages.push(errors[key].join(' '));
      }
      modalError.value = errorMessages.join(' | ');
    } else {
      modalError.value = 'Произошла неизвестная ошибка при сохранении.';
    }
  } finally { saving.value = false; }
};

const deleteFlight = async (id) => {
  if (!confirm('Удалить этот рейс?')) return;
  try { await axios.delete(`${apiUrl}/flights/${id}/`, { headers: { Authorization: `Bearer ${token}` } }); await fetchData(); } catch (err) { alert('Ошибка при удалении'); }
};

const formatTime = (isoString) => new Date(isoString).toLocaleTimeString('ru-RU', {hour: '2-digit', minute:'2-digit'});
const translateStatus = (status) => { const map = { 'scheduled': 'По расписанию', 'delayed': 'Задержан', 'boarding': 'Посадка', 'departed': 'Вылетел', 'arrived': 'Прибыл', 'cancelled': 'Отменен' }; return map[status] || status; };
const logout = () => { localStorage.removeItem('access_token'); router.push('/'); };
onMounted(() => { fetchData(); });
</script>

<style scoped>
.topbar-title { font-size: 16px; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 1px;}
.user-profile { display: flex; align-items: center; gap: 12px; font-weight: 600; color: #2b3a28; }
.avatar { width: 36px; height: 36px; background: #e67e22; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; }
.header-action { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 30px; }
.subtitle { color: #64748b; margin: 5px 0 0 0; font-size: 15px; }

.add-btn { background: #2b3a28; color: white; border: none; padding: 12px 24px; border-radius: 0; font-weight: 600; font-size: 14px; cursor: pointer; transition: 0.2s; text-transform: uppercase; letter-spacing: 0.5px;}
.add-btn:hover { background: #1e2b1c; }

/* СТИЛИ ДЛЯ СТАТИСТИКИ */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.stat-card { background: white; padding: 20px 25px; border: 1px solid #e2e8f0; display: flex; flex-direction: column; box-shadow: 0 1px 3px rgba(0,0,0,0.02); cursor: pointer; transition: all 0.2s ease; border-bottom: 3px solid transparent; }
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.stat-card.active { background: #f8fafc; border-bottom: 3px solid #2b3a28; }
.stat-label { font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px; }
.stat-value { font-size: 32px; font-weight: 800; color: #2b3a28; }
.stat-card.scheduled .stat-value { color: #4a5d23; } 
.stat-card.delayed .stat-value { color: #e67e22; } 
.stat-card.cancelled .stat-value { color: #c62828; } 

/* СТИЛИ ДЛЯ ФИЛЬТРОВ */
.filters-panel { display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px; background: white; padding: 15px; border: 1px solid #e2e8f0; }
.search-box { flex-grow: 1; min-width: 250px; display: flex; align-items: center; border: 1px solid #cbd5e1; padding: 0 15px; background: #f8fafc; }
.search-box svg { margin-right: 10px; }
.search-box input { border: none; background: transparent; padding: 12px 0; width: 100%; font-size: 14px; outline: none; font-family: 'Inter', sans-serif; }
.filter-box select { padding: 12px 15px; border: 1px solid #cbd5e1; background: #f8fafc; font-size: 14px; outline: none; font-family: 'Inter', sans-serif; cursor: pointer; min-width: 180px; height: 100%; }

.time-badge { font-weight: 700; color: #2b3a28; font-size: 15px; }
.gate-badge { background: #f0f4f3; padding: 4px 10px; font-weight: 600; font-size: 13px; border: 1px solid #e2e8f0; color: #2b3a28;}
.arrow { color: #cbd5e1; margin: 0 5px; font-size: 12px;}

.status { padding: 6px 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid transparent;}
.status.scheduled { background: #e9f5db; color: #4a5d23; border-color: #c2d6a4; }
.status.delayed { background: #fff3e0; color: #e67e22; border-color: #ffcc80; }
.status.boarding { background: #fdebd0; color: #d35400; border-color: #f5cba7; }
.status.departed { background: #e9f5db; color: #4a5d23; border-color: #c2d6a4;}
.status.arrived { background: #2b3a28; color: white; }
.status.cancelled { background: #ffebee; color: #c62828; border-color: #ef9a9a; }

.actions-cell { display: flex; justify-content: flex-end; gap: 8px; }
.action-btn { background: #ffffff; border: 1px solid #e2e8f0; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s ease; color: #64748b; }
.action-btn svg { width: 14px; height: 14px; }
.action-btn.edit:hover { background: #e9f5db; border-color: #4a5d23; color: #4a5d23; }
.action-btn.delete:hover { background: #ffebee; border-color: #c62828; color: #c62828; }

/* СТИЛИ ДЛЯ МОДАЛЬНОГО ОКНА */
.modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(43, 58, 40, 0.7); display: flex; justify-content: center; align-items: center; z-index: 1000; }
.modal-content { background: white; width: 100%; max-width: 750px; box-shadow: 0 20px 40px rgba(0,0,0,0.2); max-height: 90vh; overflow-y: auto; }
.modal-header { padding: 25px 30px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; }
.modal-header h2 { margin: 0; color: #2b3a28; font-size: 22px; font-weight: 700; }
.close-modal { background: none; border: none; font-size: 28px; color: #94a3b8; cursor: pointer; }
.close-modal:hover { color: #c62828; }
.flight-form { padding: 30px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.form-group { display: flex; flex-direction: column; }
.form-group.full-width { grid-column: span 2; }
.form-group label { font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }
.form-group input, .form-group select { padding: 12px 15px; border: 1px solid #cbd5e1; font-size: 14px; background: #f8fafc; transition: 0.2s; border-radius: 0; font-family: 'Inter', sans-serif;}
.form-group input:focus, .form-group select:focus { border-color: #2b3a28; outline: none; background: white; }
.modal-actions { display: flex; justify-content: flex-end; gap: 15px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; }
.cancel-btn { background: #f1f5f9; color: #64748b; border: none; padding: 12px 25px; cursor: pointer; font-weight: 600; }
.cancel-btn:hover { background: #e2e8f0; }
.save-btn { background: #2b3a28; color: white; border: none; padding: 12px 30px; cursor: pointer; font-weight: 700; }
.save-btn:hover { background: #1e2b1c; }
.loading { text-align: center; padding: 50px; font-size: 16px; color: #64748b; }

/* Стили для ошибки валидации */
.validation-error { background: #fef2f2; color: #dc2626; border: 1px solid #f87171; padding: 12px 15px; margin-top: 20px; font-size: 14px; font-weight: 500; line-height: 1.4; }
</style>