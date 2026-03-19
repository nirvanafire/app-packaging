<template>
  <div class="dashboard">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="nav-brand">
        <span class="logo">🏠</span>
        <span>控制台</span>
      </div>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/dashboard">控制台</router-link>
        <span class="user-info">
          {{ authStore.username }}
          <span class="badge">{{ authStore.user?.roles?.join(', ') }}</span>
        </span>
        <button @click="handleLogout" class="btn-logout">退出</button>
      </div>
    </nav>

    <!-- 主要内容 -->
    <main class="main-content">
      <div class="container">
        <!-- 欢迎卡片 -->
        <div class="welcome-card">
          <h2>欢迎回来，{{ authStore.username }}！</h2>
          <p>您已登录系统，可以访问以下功能</p>
        </div>

        <!-- 功能卡片 -->
        <div class="cards-grid">
          <div class="card">
            <h3>👤 个人信息</h3>
            <div class="info-list">
              <div class="info-item">
                <span class="label">用户名</span>
                <span class="value">{{ authStore.user?.username }}</span>
              </div>
              <div class="info-item">
                <span class="label">邮箱</span>
                <span class="value">{{ authStore.user?.email }}</span>
              </div>
              <div class="info-item">
                <span class="label">角色</span>
                <span class="value roles">{{ authStore.user?.roles?.join(', ') }}</span>
              </div>
            </div>
          </div>

          <div class="card">
            <h3>🔐 权限说明</h3>
            <div class="permission-list">
              <div class="permission-item" :class="{ active: authStore.hasRole('user') }">
                <span class="perm-icon">{{ authStore.hasRole('user') ? '✅' : '❌' }}</span>
                <span>用户权限</span>
              </div>
              <div class="permission-item" :class="{ active: authStore.hasRole('editor') }">
                <span class="perm-icon">{{ authStore.hasRole('editor') ? '✅' : '❌' }}</span>
                <span>编辑权限</span>
              </div>
              <div class="permission-item" :class="{ active: authStore.hasRole('admin') }">
                <span class="perm-icon">{{ authStore.hasRole('admin') ? '✅' : '❌' }}</span>
                <span>管理员权限</span>
              </div>
            </div>
          </div>

          <div class="card">
            <h3>📊 系统状态</h3>
            <div class="status-info">
              <div class="status-item">
                <span class="dot green"></span>
                <span>服务运行正常</span>
              </div>
              <div class="status-item">
                <span class="label">版本</span>
                <span class="value">v1.0.0</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 管理员面板 -->
        <div v-if="authStore.hasRole('admin')" class="admin-panel">
          <h3>👑 管理员面板</h3>
          <button @click="fetchUsers" class="admin-btn">查看所有用户</button>
          
          <div v-if="users.length" class="users-table">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>用户名</th>
                  <th>邮箱</th>
                  <th>角色</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.roles.join(', ') }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const users = ref([])

async function handleLogout() {
  await authStore.logout()
  router.push('/')
}

async function fetchUsers() {
  try {
    const response = await fetch('/auth/users')
    if (response.ok) {
      const data = await response.json()
      users.value = data.users
    }
  } catch (error) {
    console.error('获取用户列表失败:', error)
  }
}
</script>

<style scoped>
.dashboard {
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

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
}

/* 主要内容 */
.main-content {
  flex: 1;
  background: #f5f5f5;
  padding: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.welcome-card h2 {
  color: #333;
  margin-bottom: 8px;
}

.welcome-card p {
  color: #666;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h3 {
  color: #333;
  margin-bottom: 20px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.info-item .label {
  color: #666;
}

.info-item .value {
  font-weight: 500;
  color: #333;
}

.info-item .value.roles {
  color: #667eea;
}

.permission-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.permission-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  border-radius: 6px;
}

.permission-item.active {
  background: #e8f5e9;
}

.perm-icon {
  font-size: 18px;
}

.status-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot.green {
  background: #4caf50;
}

/* 管理员面板 */
.admin-panel {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.admin-panel h3 {
  color: #f44336;
  margin-bottom: 20px;
}

.admin-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  margin-bottom: 20px;
}

.users-table {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background: #f5f5f5;
  font-weight: 600;
  color: #333;
}
</style>
