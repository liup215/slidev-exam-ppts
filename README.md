# Slidev Exam PPTs

在线考试考纲幻灯片展示网站

## 技术栈
- [Slidev](https://sli.dev/) - 基于 Vue + Markdown 的幻灯片工具
- Vite - 构建工具
- GitHub Pages - 静态托管

## 项目结构
```
slidev-exam-ppts/
├── slides/           # 各考纲幻灯片目录
│   ├── cie-9700/     # CIE Biology 9700
│   ├── aqa-7402/     # AQA Biology
│   └── ...
├── pages/            # 主页及相关页面
├── public/           # 静态资源
└── package.json
```

## 开发
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建
npm run build
```

## 部署
自动部署到 GitHub Pages
