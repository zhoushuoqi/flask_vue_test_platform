<template>
  <div class="dashboard-content">
    <el-card class="welcome-card">
      <h3>欢迎使用测试平台</h3>
      <p>这是一个简单的测试用例管理平台，您可以：</p>
      <ul>
        <li>创建和管理测试用例</li>
        <li>查看测试用例列表</li>
        <li>按照权限进行操作</li>
      </ul>
      
      <div class="stats">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-number">{{ stats.totalCases }}</div>
                <div class="stat-label">总用例数</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-number">{{ stats.myCases }}</div>
                <div class="stat-label">我的用例</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card class="stat-card">
              <div class="stat-item">
                <div class="stat-number">{{ userInfo.role === 'admin' ? '管理员' : '用户' }}</div>
                <div class="stat-label">当前角色</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import request from '@/utils/request'

export default {
  name: 'Dashboard',
  setup() {
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const stats = reactive({
      totalCases: 0,
      myCases: 0
    })
    
    const loadStats = async () => {
      try {
        console.log('Dashboard加载统计信息')
        const response = await request.get('/testcase')
        console.log('统计信息响应:', response.data)
        const testcases = response.data.testcases
        stats.totalCases = testcases.length
        stats.myCases = testcases.filter(tc => tc.created_by === userInfo.value.id).length
      } catch (error) {
        console.error('加载统计信息失败:', error)
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      userInfo,
      stats
    }
  }
}
</script>

<style scoped>
.dashboard-content {
  padding: 0;
}

.welcome-card {
  margin-bottom: 20px;
}

.welcome-card h3 {
  margin-top: 0;
  color: #333;
}

.welcome-card ul {
  color: #666;
}

.stats {
  margin-top: 30px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  padding: 10px;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}
</style>