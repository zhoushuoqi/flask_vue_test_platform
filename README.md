# 测试平台使用说明

## 项目简介

这是一个基于Vue 3 + Flask的简单测试用例管理平台，支持用户登录、权限管理和测试用例的增加、查看功能。

## 技术栈

**前端**
- Vue 3 + Composition API
- Element Plus UI组件库
- Vue Router 4
- Axios

**后端**
- Flask 2.3.3
- MySQL数据库
- Flask Session认证

## 功能特性

- ✅ 用户登录/退出
- ✅ 权限管理（管理员/普通用户）
- ✅ 测试用例管理（增加、查看、列表）
- ✅ 统一导航栏布局
- ✅ 响应式界面设计

## 项目结构

```
vortex_fe/
├── backend/                 # Flask后端
│   ├── app.py              # 后端主应用
│   ├── requirements.txt    # Python依赖
│   └── database.sql        # 数据库初始化脚本
├── src/                    # Vue前端源码
│   ├── components/
│   │   └── Layout.vue      # 统一布局组件
│   ├── views/
│   │   ├── Login.vue       # 登录页面
│   │   ├── Dashboard.vue   # 首页仪表板
│   │   └── TestCase.vue    # 测试用例管理
│   ├── router/
│   │   └── index.js        # 路由配置
│   ├── utils/
│   │   └── request.js      # HTTP请求封装
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── public/
│   └── index.html
└── package.json
```

## 安装与运行

### 环境要求

- Node.js 16+
- Python 3.8+
- MySQL 5.7+

### 1. 数据库设置

1. 创建MySQL数据库：
```sql
CREATE DATABASE vortex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 导入数据库脚本：
```bash
mysql -u root -p vortex < backend/database.sql
```

### 2. 后端启动

1. 进入后端目录：
```bash
cd backend
```

2. 安装Python依赖：
```bash
pip install -r requirements.txt
```

3. 修改数据库配置（如需要）：
编辑 `app.py` 文件中的 `DB_CONFIG` 部分：
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',        # 修改为你的MySQL密码
    'database': 'vortex'
}
```

4. 启动Flask服务：
```bash
python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 3. 前端启动

1. 安装依赖：
```bash
npm install
```

2. 启动开发服务器：
```bash
npm run serve
```

前端应用将在 `http://localhost:8080` 启动

## 使用指南

### 登录系统

访问 `http://localhost:8080` 会自动跳转到登录页面。

**预设账号：**
- **管理员账号**：`admin` / `admin123`
- **普通用户账号**：`user` / `user123`

### 主要功能

#### 1. 首页仪表板
- 显示测试用例统计信息
- 显示当前用户角色
- 快速导航到其他功能模块

#### 2. 测试用例管理
- **添加用例**：点击"添加用例"按钮，填写用例信息
  - 用例标题（必填）
  - 用例描述
  - 测试步骤
  - 预期结果
- **查看用例列表**：显示所有测试用例的列表
- **查看详情**：点击"查看"按钮查看用例完整信息

#### 3. 用户权限
- **管理员**：可以查看所有功能，具有完整权限
- **普通用户**：可以添加和查看测试用例

### 导航栏功能

- **首页**：返回仪表板
- **测试用例**：进入测试用例管理页面
- **用户信息**：显示当前登录用户和角色
- **退出登录**：安全退出系统

## API接口说明

### 认证相关
- `POST /api/login` - 用户登录
- `POST /api/logout` - 用户退出
- `GET /api/user/info` - 获取当前用户信息

### 测试用例相关
- `POST /api/testcase` - 添加测试用例
- `GET /api/testcase` - 获取测试用例列表

## 数据库表结构

### users 用户表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键ID |
| username | VARCHAR(50) | 用户名 |
| password | VARCHAR(64) | 密码哈希值 |
| role | ENUM | 用户角色(admin/user) |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### test_cases 测试用例表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INT | 主键ID |
| title | VARCHAR(200) | 用例标题 |
| description | TEXT | 用例描述 |
| steps | TEXT | 测试步骤 |
| expected_result | TEXT | 预期结果 |
| created_by | INT | 创建者ID |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

## 开发说明

### 前端开发
- 使用Vue 3 Composition API
- Element Plus作为UI组件库
- 所有页面都使用统一的Layout布局
- 使用session进行身份认证

### 后端开发
- 使用Flask轻量级框架
- Session-based认证，无需JWT token
- CORS支持跨域请求
- 简单的权限控制装饰器

### 扩展功能建议

1. **用户管理**：添加用户增删改查功能
2. **测试用例分类**：支持用例分组和标签
3. **测试执行**：支持用例执行和结果记录
4. **报表统计**：测试用例执行统计报告
5. **角色权限**：更细粒度的权限控制

## 故障排除

### 常见问题

1. **登录后立即跳转回登录页**
   - 检查后端服务是否正常运行
   - 确认数据库连接配置正确
   - 查看浏览器控制台是否有错误信息

2. **测试用例列表为空**
   - 确认数据库表已正确创建
   - 检查用户是否有权限查看用例
   - 查看后端日志是否有数据库错误

3. **跨域问题**
   - 确认后端CORS配置正确
   - 检查前端请求地址是否正确

### 日志查看

- **前端日志**：打开浏览器开发者工具的Console选项卡
- **后端日志**：查看运行Flask应用的终端输出
- **网络请求**：在浏览器Network选项卡查看API请求状态


## 许可证

MIT License