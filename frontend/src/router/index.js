import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import FlightsView from '../views/FlightsView.vue'
import AirlinesView from '../views/AirlinesView.vue'
import AirportsView from '../views/AirportsView.vue'
import AircraftsView from '../views/AircraftsView.vue'
import RunwaysView from '../views/RunwaysView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'login', component: LoginView },
    { path: '/flights', name: 'flights', component: FlightsView, meta: { requiresAuth: true } },
    { path: '/airlines', name: 'airlines', component: AirlinesView, meta: { requiresAuth: true } },
    { path: '/airports', name: 'airports', component: AirportsView, meta: { requiresAuth: true } },
    { path: '/aircrafts', name: 'aircrafts', component: AircraftsView, meta: { requiresAuth: true } },
    { path: '/runways', name: 'runways', component: RunwaysView, meta: { requiresAuth: true } }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !token) {
    next('/'); 
  } else {
    next();
  }
})

export default router