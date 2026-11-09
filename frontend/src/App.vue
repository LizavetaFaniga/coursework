<template>
  <router-view />
</template>

<script setup>
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f4f5f7;
  color: #1e293b;
  -webkit-font-smoothing: antialiased;
}

.layout { display: flex; min-height: 100vh; }

/* --- БОКОВОЕ МЕНЮ (Оливковое) --- */
.sidebar { 
  width: 260px; 
  background: #2b3a28; 
  display: flex; 
  flex-direction: column; 
  z-index: 10;
}

.logo { 
  font-size: 20px; 
  font-weight: 700; 
  padding: 30px 24px; 
  color: #ffffff; 
  letter-spacing: 1px;
  border-bottom: 1px solid #3d5139; 
  text-transform: uppercase;
}

.menu { display: flex; flex-direction: column; padding: 10px 0; flex-grow: 1; }

.menu a { 
  color: #a4b59f; 
  text-decoration: none; 
  padding: 16px 24px; 
  font-size: 15px; 
  font-weight: 500;
  transition: all 0.1s ease; 
  display: flex;
  align-items: center;
  border-left: 4px solid transparent; 
}

.menu a:hover, .menu a.router-link-active { 
  background: #ffffff; 
  color: #2b3a28; 
  font-weight: 600;
}

.menu a.router-link-active { 
  border-left: 4px solid #e67e22; 
  font-weight: 700;
}

.logout-btn { 
  margin: 20px; 
  padding: 12px; 
  background: #e67e22; /* Оранжевый фон */
  color: #ffffff; /* Белый текст */
  border: 1px solid #e67e22; 
  border-radius: 0; 
  cursor: pointer; 
  font-weight: 700; /* Жирный шрифт */
  transition: all 0.2s ease; 
  font-size: 14px;
  text-transform: uppercase;
  font-family: 'Inter', sans-serif;
}

.logout-btn:hover { 
  background: #d35400; /* Темнее при наведении */
  border-color: #d35400;
  color: #ffffff; 
}

/* --- ОСНОВНАЯ ЧАСТЬ --- */
.main-content { flex-grow: 1; display: flex; flex-direction: column; overflow: hidden; }
.topbar { background: white; padding: 0 40px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; height: 72px; }
.content { padding: 40px; max-width: 1400px; margin: 0 auto; width: 100%; box-sizing: border-box; }
.board-container { background: white; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05); overflow: hidden; }
.board-table { width: 100%; border-collapse: collapse; font-size: 14px; }
.board-table th { background: #f8fafc; color: #64748b; padding: 16px 24px; text-align: left; font-weight: 600; border-bottom: 1px solid #e2e8f0; text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
.board-table td { padding: 18px 24px; border-bottom: 1px solid #e2e8f0; color: #1e293b; vertical-align: middle; font-weight: 500; }
.board-table tr:hover { background: #f8fafc; }
.board-table tr:last-child td { border-bottom: none; }
</style>