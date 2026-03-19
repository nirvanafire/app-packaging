import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  
  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.roles?.includes('admin') || false)
  const username = computed(() => user.value?.username || '')
  
  async function login(username, password) {
    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      
      const data = await response.json()
      
      if (response.ok) {
        user.value = data.user
        localStorage.setItem('user', JSON.stringify(data.user))
        return { success: true }
      } else {
        return { success: false, error: data.error }
      }
    } catch (error) {
      return { success: false, error: '网络错误' }
    }
  }
  
  async function logout() {
    try {
      await fetch('/auth/logout', { method: 'POST' })
    } catch (e) {
      // ignore
    }
    
    user.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }
  
  async function checkAuth() {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
        
        // 验证会话是否有效
        const response = await fetch('/auth/profile')
        if (!response.ok) {
          user.value = null
          localStorage.removeItem('user')
        }
      } catch (e) {
        user.value = null
        localStorage.removeItem('user')
      }
    }
  }
  
  function hasRole(role) {
    return user.value?.roles?.includes(role) || false
  }
  
  return {
    user,
    token,
    isAuthenticated,
    isAdmin,
    username,
    login,
    logout,
    checkAuth,
    hasRole
  }
})
