# 每日热门新闻 Top 10 (GitHub Pages 静态版)

一个展示权威信源最热门新闻的网站，每日自动刷新。

## 功能特性

- 🔥 每日 Top 10 热门新闻
- 📰 聚合多个权威信源
- 📂 分类筛选（科技、财经、社会）
- 📱 响应式设计，支持移动端
- 🔔 Modal 弹窗查看详情
- 🔄 数据每日自动刷新（GitHub Actions）

## 数据来源

- Hacker News
- GitHub Trending
- 微博热搜
- 36氪
- Product Hunt
- 腾讯新闻
- 华尔街见闻
- V2EX

## 部署到 GitHub Pages

### 1. 推送代码到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### 2. 启用 GitHub Pages

1. 进入你的 GitHub 仓库
2. 点击 **Settings** → **Pages**
3. 在 **Source** 中选择 **Deploy from a branch**
4. 选择 **main** 分支和 **/(root)** 文件夹
5. 点击 **Save**
6. 等待 1-2 分钟，网站将部署完成

### 3. 启用自动刷新（可选）

GitHub Actions 会每天自动抓取新闻数据并更新 JSON 文件：

1. 进入仓库的 **Actions** 标签
2. 如果需要手动触发刷新，点击 **Refresh News Data** → **Run workflow**
3. 每次运行后，Actions 会自动提交更新的数据

## 本地开发

```bash
# 克隆项目
git clone <your-repo-url>
cd hot-news

# 生成本地数据（需要先配置 news_fetcher）
python generate_data.py

# 使用任意静态服务器预览
python -m http.server 8000

# 访问 http://localhost:8000/static/
```

## 项目结构

```
hot-news/
├── static/
│   ├── index.html              # 首页
│   ├── category-tech.html      # 科技分类页
│   ├── category-finance.html   # 财经分类页
│   ├── category-social.html    # 社会分类页
│   ├── css/style.css           # 样式
│   ├── js/main.js              # 交互逻辑
│   └── data/                   # 新闻数据（自动生成）
│       ├── all.json
│       ├── tech.json
│       ├── finance.json
│       └── social.json
├── .github/workflows/
│   └── refresh-news.yml        # GitHub Actions 自动刷新
├── generate_data.py            # 数据生成脚本
├── news_fetcher.py             # 新闻获取封装
├── requirements.txt            # Python 依赖
└── README.md
```

## 许可证

MIT
