# Vue3 + Vite 前端

基于 Vue3 + Vite + Pinia + Vue Router 的现代前端应用。

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器 (带 HMR)
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

## 目录结构

```
frontend/
├── src/
│   ├── assets/        # 静态资源
│   ├── components/    # Vue 组件
│   ├── router/        # Vue Router 配置
│   ├── stores/        # Pinia 状态管理
│   ├── views/         # 页面视图
│   ├── App.vue        # 根组件
│   └── main.js        # 入口文件
├── index.html         # HTML 模板
├── vite.config.js     # Vite 配置
└── package.json
```

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue 状态管理
- **Vue Router 4** - Vue.js 官方路由

## 开发模式

开发时 Vite 运行在 `http://localhost:5173`，自动代理 API 请求到 Flask 后端 `http://127.0.0.1:5000`。

## 生产构建

构建后输出到 `src/web/static/dist/`，由 Flask 提供静态文件服务。
