# 每日热门新闻 Top 10

一个展示权威信源最热门新闻的网站，每日自动刷新。

## 功能特性

- 🔥 每日 Top 10 热门新闻
- 📰 聚合多个权威信源
- 📂 分类筛选（科技、财经、社会）
- 📱 响应式设计，支持移动端
- 🔔 Modal 弹窗查看详情
- ⏰ 每日自动刷新

## 数据来源

- Hacker News
- GitHub Trending
- 微博热搜
- 36氪
- Product Hunt
- 腾讯新闻
- 华尔街见闻
- V2EX

## 本地开发

```bash
# 克隆项目
git clone <your-repo-url>
cd hot-news-site

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 访问 http://localhost:5000
```

## Render 部署

### 1. 推送到 GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

### 2. 连接 Render

1. 登录 [Render](https://render.com)
2. 点击 **New +** → **Web Service**
3. 选择你的 GitHub 仓库
4. 配置：
   - **Name**: hot-news-api
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Python Version**: 3.10

5. 点击 **Create Web Service**

### 3. 创建定时任务

1. 点击 **New +** → **Cron Job**
2. 配置：
   - **Name**: hot-news-cron
   - **Environment**: Python
   - **Schedule**: `0 0 * * *` (每天凌晨0点)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python cron_job.py`
   - **Python Version**: 3.10

3. 点击 **Create Cron Job**

## 项目结构

```
hot-news-site/
├── app.py              # Flask 主应用
├── cron_job.py         # 定时刷新脚本
├── news_fetcher.py     # 新闻获取封装
├── requirements.txt    # Python 依赖
├── render.yaml         # Render 部署配置
├── static/
│   ├── index.html      # 首页
│   ├── css/style.css   # 样式
│   └── js/main.js      # 交互逻辑
├── templates/
│   └── category.html   # 分类页
└── data/
    └── news_cache.json # 新闻缓存
```

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页 |
| `/category/<name>` | GET | 分类页 |
| `/api/news` | GET | 获取 Top 10 新闻 |
| `/api/news?category=tech` | GET | 获取分类新闻 |
| `/api/news/<id>` | GET | 获取新闻详情 |
| `/api/refresh` | POST | 手动刷新新闻 |

## 自定义

### 修改分类

编辑 `app.py` 中的 `CATEGORIES` 字典：

```python
CATEGORIES = {
    'tech': ['AI', 'LLM', 'GPT', 'GitHub'],
    'finance': ['股票', '加密货币'],
    'social': ['微博', '腾讯'],
    'custom': ['你的关键词']
}
```

### 修改刷新时间

编辑 `render.yaml` 中的 cron 表达式：

```yaml
schedule: "0 6 * * *"  # 每天早上6点
```

## 许可证

MIT
