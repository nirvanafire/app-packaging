<template>
  <div class="home">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-brand">
        <span class="logo">🚀</span>
        <span>PyQt6 Web App</span>
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/dashboard">控制台</router-link>
        <template v-if="authStore.isAuthenticated">
          <span class="user-info">{{ authStore.username }}</span>
          <button @click="handleLogout" class="btn-logout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn-login">登录</router-link>
        </template>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="hero">
        <h1>Vue3 + Flask 全栈应用</h1>
        <p class="subtitle">PyQt6 Web Browser with Modern Frontend</p>
        
        <div class="tech-stack">
          <div class="tech-item">
            <span class="tech-icon">⚡</span>
            <span class="tech-name">Vite</span>
          </div>
          <div class="tech-item">
            <span class="tech-icon">💚</span>
            <span class="tech-name">Vue 3</span>
          </div>
          <div class="tech-item">
            <span class="tech-icon">🐍</span>
            <span class="tech-name">Flask</span>
          </div>
          <div class="tech-item">
            <span class="tech-icon">🔐</span>
            <span class="tech-name">Auth</span>
          </div>
        </div>

        <div class="features">
          <h2>功能特性</h2>
          <div class="feature-grid">
            <div class="feature-card">
              <h3>🔐 用户认证</h3>
              <p>Flask-Login + Flask-Principal 权限管理</p>
            </div>
            <div class="feature-card">
              <h3>⚡ 快速开发</h3>
              <p>Vite HMR 热更新，开发体验极佳</p>
            </div>
            <div class="feature-card">
              <h3>🛡️ 角色权限</h3>
              <p>Admin / Editor / User 三级权限</p>
            </div>
            <div class="feature-card">
              <h3>🎨 现代UI</h3>
              <p>Vue3 Composition API + Pinia</p>
            </div>
          </div>
        </div>

        <div class="api-demo">
          <h2>API 测试</h2>
          <div class="api-buttons">
            <button @click="testApi('status')" class="api-btn">获取状态</button>
            <button @click="testApi('info')" class="api-btn">应用信息</button>
          </div>
          <div v-if="apiResult" class="api-result">
            <pre>{{ apiResult }}</pre>
          </div>
        </div>
      </div>
    </main>

    <!-- 页脚 -->
    <footer class="footer">
      <p>Powered by Vue3 + Vite + Flask</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const apiResult = ref(null)

async function testApi(type) {
  try {
    const response = await fetch(`/api/${type}`)
    const data = await response.json()
    apiResult.value = JSON.stringify(data, null, 2)
  } catch (error) {
    apiResult.value = `Error: ${error.message}`
  }
}

async function handleLogout() {
  await authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏 */
.navbar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 16px 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: 600;
}

.logo {
  font-size: 24px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.3s;
}

.nav-links a:hover {
  opacity: 0.8;
}

.user-info {
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 16px;
  border-radius: 20px;
}

.btn-login, .btn-logout {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.3s;
}

.btn-login:hover, .btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 主要内容 */
.main-content {
  flex: 1;
  background: #f5f5f5;
  padding: 60px 40px;
}

.hero {
  max-width: 1000px;
  margin: 0 auto;
  text-align: center;
}

.hero h1 {
  font-size: 42px;
  color: #333;
  margin-bottom: 16px;
}

.subtitle {
  color: #666;
  font-size: 18px;
  margin-bottom: 40px;
}

/* 技术栈 */
.tech-stack {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 60px;
}

.tech-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.tech-icon {
  font-size: 36px;
}

.tech-name {
  font-weight: 600;
  color: #333;
}

/* 功能卡片 */
.features {
  margin-bottom: 60px;
}

.features h2 {
  color: #333;
  margin-bottom: 24px;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.feature-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: left;
}

.feature-card h3 {
  margin-bottom: 8px;
  color: #333;
}

.feature-card p {
  color: #666;
  font-size: 14px;
}

/* API 测试 */
.api-demo h2 {
  color: #333;
  margin-bottom: 24px;
}

.api-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 24px;
}

.api-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.api-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.api-result {
  background: #263238;
  color: #4fc3f7;
  padding: 20px;
  border-radius: 8px;
  text-align: left;
  max-width: 600px;
  margin: 0 auto;
}

.api-result pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: 'Fira Code', monospace;
}

/* 页脚 */
.footer {
  background: #263238;
  color: #90a4ae;
  text-align: center;
  padding: 20px;
}
</style>
