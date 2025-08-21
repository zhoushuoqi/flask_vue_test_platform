<template>
  <div class="testcase-content">
    <!-- 添加用例表单 -->
    <el-card class="add-case-card" v-if="userInfo.role === 'admin' || userInfo.role === 'user'">
      <template #header>
        <div class="card-header">
          <span>添加测试用例</span>
          <el-button @click="toggleAddForm" :type="showAddForm ? 'danger' : 'primary'" size="small">
            {{ showAddForm ? '取消' : '添加用例' }}
          </el-button>
        </div>
      </template>
      
      <el-form
        v-show="showAddForm"
        :model="addForm"
        :rules="rules"
        ref="addFormRef"
        label-width="100px"
        @submit.prevent="handleAddCase"
      >
        <el-form-item label="用例标题" prop="title">
          <el-input
            v-model="addForm.title"
            placeholder="请输入测试用例标题"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="用例描述" prop="description">
          <el-input
            v-model="addForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入用例描述"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="测试步骤" prop="steps">
          <el-input
            v-model="addForm.steps"
            type="textarea"
            :rows="4"
            placeholder="请输入测试步骤"
          ></el-input>
        </el-form-item>
        
        <el-form-item label="预期结果" prop="expected_result">
          <el-input
            v-model="addForm.expected_result"
            type="textarea"
            :rows="3"
            placeholder="请输入预期结果"
          ></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            :loading="addLoading"
            @click="handleAddCase"
          >
            提交
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 用例列表 -->
    <el-card class="case-list-card">
      <template #header>
        <div class="card-header">
          <span>测试用例列表 ({{ testcases.length }} 条)</span>
          <el-button @click="loadTestcases" :loading="listLoading" size="small">
            刷新
          </el-button>
        </div>
      </template>
      
      <el-table
        :data="testcases"
        v-loading="listLoading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="60"></el-table-column>
        <el-table-column prop="title" label="标题" min-width="200"></el-table-column>
        <el-table-column prop="description" label="描述" min-width="250" show-overflow-tooltip></el-table-column>
        <el-table-column prop="creator_name" label="创建者" width="100"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button
              size="small"
              @click="viewCase(scope.row)"
            >
              查看
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 查看用例详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="测试用例详情"
      width="60%"
    >
      <div v-if="selectedCase">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="用例ID">{{ selectedCase.id }}</el-descriptions-item>
          <el-descriptions-item label="标题">{{ selectedCase.title }}</el-descriptions-item>
          <el-descriptions-item label="描述">{{ selectedCase.description || '无' }}</el-descriptions-item>
          <el-descriptions-item label="测试步骤">
            <pre style="white-space: pre-wrap; font-family: inherit;">{{ selectedCase.steps || '无' }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="预期结果">
            <pre style="white-space: pre-wrap; font-family: inherit;">{{ selectedCase.expected_result || '无' }}</pre>
          </el-descriptions-item>
          <el-descriptions-item label="创建者">{{ selectedCase.creator_name }}</el-descriptions-item>
          <el-descriptions-item label="创建时间">{{ formatDate(selectedCase.created_at) }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

export default {
  name: 'TestCase',
  setup() {
    const userInfo = ref(JSON.parse(localStorage.getItem('user') || '{}'))
    const testcases = ref([])
    const showAddForm = ref(false)
    const addFormRef = ref()
    const addLoading = ref(false)
    const listLoading = ref(false)
    const showDetailDialog = ref(false)
    const selectedCase = ref(null)
    
    const addForm = reactive({
      title: '',
      description: '',
      steps: '',
      expected_result: ''
    })
    
    const rules = {
      title: [
        { required: true, message: '请输入用例标题', trigger: 'blur' }
      ]
    }
    
    const toggleAddForm = () => {
      showAddForm.value = !showAddForm.value
      if (!showAddForm.value) {
        resetForm()
      }
    }
    
    const resetForm = () => {
      if (addFormRef.value) {
        addFormRef.value.resetFields()
      }
      Object.assign(addForm, {
        title: '',
        description: '',
        steps: '',
        expected_result: ''
      })
    }
    
    const handleAddCase = async () => {
      if (!addFormRef.value) return
      
      await addFormRef.value.validate(async (valid) => {
        if (valid) {
          addLoading.value = true
          try {
            await request.post('/testcase', addForm)
            ElMessage.success('测试用例添加成功')
            resetForm()
            showAddForm.value = false
            await loadTestcases()
          } catch (error) {
            console.error('添加用例失败:', error)
          } finally {
            addLoading.value = false
          }
        }
      })
    }
    
    const loadTestcases = async () => {
      listLoading.value = true
      try {
        console.log('发送GET请求获取测试用例列表')
        const response = await request.get('/testcase')
        console.log('获取用例响应:', response.data)
        testcases.value = response.data.testcases || []
      } catch (error) {
        console.error('加载用例失败:', error)
      } finally {
        listLoading.value = false
      }
    }
    
    const viewCase = (testcase) => {
      selectedCase.value = testcase
      showDetailDialog.value = true
    }
    
    const formatDate = (dateStr) => {
      if (!dateStr) return ''
      return new Date(dateStr).toLocaleString('zh-CN')
    }
    
    onMounted(() => {
      loadTestcases()
    })
    
    return {
      userInfo,
      testcases,
      showAddForm,
      addForm,
      rules,
      addFormRef,
      addLoading,
      listLoading,
      showDetailDialog,
      selectedCase,
      toggleAddForm,
      resetForm,
      handleAddCase,
      loadTestcases,
      viewCase,
      formatDate
    }
  }
}
</script>

<style scoped>
.testcase-content {
  padding: 0;
}

.add-case-card {
  margin-bottom: 20px;
}

.case-list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>