<template>
  <div class="layout-container">
    <el-container>
      <!-- 头部导航 -->
      <el-header class="header">
        <div class="header-left">
          <h2>测试平台</h2>
        </div>
        <div class="header-right">
          <span class="welcome-text">欢迎, {{ userInfo.username }}</span>
          <el-tag :type="userInfo.role === 'admin' ? 'danger' : 'primary'">
            {{ userInfo.role === 'admin' ? '管理员' : '普通用户' }}
          </el-tag>
          <el-button @click="logout" size="small">退出登录</el-button>
        </div>
      </el-header>
      
      <!-- 侧边栏 -->
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu
            :default-active="activeMenu"
            class="menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="dashboard">
              <el-icon><House /></el-icon>
              <span>首页</span>
            </el-menu-item>
            <el-menu-item index="testcase">
              <el-icon><Document /></el-icon>
              <span>测试用例</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <!-- 主内容区 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { House, Document } from '@element-plus/icons-vue'
import request from '@/utils/request'

export default {
  name: 'Layout',
  components: {
    House,
    Document
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    
    // 根据当前路由设置活跃菜单
    const activeMenu = computed(() => {
      const path = route.path
      if (path === '/dashboard') return 'dashboard'
      if (path === '/testcase') return 'testcase'
      return 'dashboard'
    })
    
    const handleMenuSelect = (index) => {
      if (index === 'dashboard') {
        router.push('/dashboard')
      } else if (index === 'testcase') {
        router.push('/testcase')
      }
    }
    
    const logout = async () => {
      try {
        await ElMessageBox.confirm('确认退出登录？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await request.post('/logout')
        localStorage.removeItem('user')
        ElMessage.success('退出登录成功')
        router.push('/login')
      } catch {}
    }
    
    return {
      userInfo,
      activeMenu,
      handleMenuSelect,
      logout
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #409EFF;
  color: white;
  padding: 0 20px;
}

.header-left h2 {
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  font-size: 14px;
}

.sidebar {
  background-color: #f5f7fa;
}

.menu {
  border-right: none;
  height: 100%;
}

.main-content {
  background-color: #f0f2f5;
}
</style>