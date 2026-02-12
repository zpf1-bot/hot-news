const CATEGORIES = {
    'all': 'data/all.json',
    'tech': 'data/tech.json',
    'finance': 'data/finance.json',
    'social': 'data/social.json'
};

let currentCategory = 'all';
let allNewsData = null;

async function loadNews(category = 'all') {
    currentCategory = category;
    const newsList = document.getElementById('newsList');
    newsList.innerHTML = '<div class="loading">加载中...</div>';
    
    try {
        const response = await fetch(CATEGORIES[category]);
        const data = await response.json();
        
        document.getElementById('updateTime').textContent = data.updated_at 
            ? `更新时间: ${formatTime(data.updated_at)}` 
            : '';
        
        renderNews(data.news);
    } catch (error) {
        console.error('Error loading news:', error);
        newsList.innerHTML = '<div class="error">加载失败，请稍后重试</div>';
    }
}

function renderNews(news) {
    const newsList = document.getElementById('newsList');
    
    if (!news || news.length === 0) {
        newsList.innerHTML = '<div class="error">暂无新闻数据</div>';
        return;
    }
    
    newsList.innerHTML = news.map((item, index) => `
        <div class="news-card ${item.category || ''}" onclick="openModal(${index})">
            <div class="news-rank">${index + 1}</div>
            <h3 class="news-title">${escapeHtml(item.title)}</h3>
            <div class="news-meta">
                <span>📰 ${item.source}</span>
                <span>🕐 ${formatTime(item.time)}</span>
                <span class="news-heat">🔥 ${formatHeat(item.heat)}</span>
            </div>
        </div>
    `).join('');
}

function openModal(index) {
    const response = fetch(CATEGORIES[currentCategory])
        .then(res => res.json())
        .then(data => {
            const news = data.news[index];
            if (!news) return;
            
            const modal = document.getElementById('newsModal');
            const modalBody = document.getElementById('modalBody');
            
            modalBody.innerHTML = `
                <h2 class="modal-title">${escapeHtml(news.title)}</h2>
                <div class="modal-meta">
                    <span>📰 ${news.source}</span>
                    <span>🕐 ${formatTime(news.time)}</span>
                    <span class="news-heat">🔥 ${formatHeat(news.heat)}</span>
                    <span>📂 ${getCategoryName(news.category)}</span>
                </div>
                <div class="modal-content-text">${escapeHtml(news.content || '暂无详细内容')}</div>
                <a href="${news.url}" target="_blank" class="modal-link">🔗 阅读原文</a>
            `;
            
            modal.classList.add('show');
            document.body.style.overflow = 'hidden';
        });
}

function closeModal() {
    const modal = document.getElementById('newsModal');
    modal.classList.remove('show');
    document.body.style.overflow = '';
}

function formatTime(time) {
    if (!time) return '';
    try {
        const date = new Date(time);
        if (isNaN(date.getTime())) return time;
        return date.toLocaleString('zh-CN', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch {
        return time;
    }
}

function formatHeat(heat) {
    if (!heat) return '0';
    if (heat >= 10000) return (heat / 10000).toFixed(1) + '万';
    if (heat >= 1000) return (heat / 1000).toFixed(1) + 'k';
    return heat.toString();
}

function getCategoryName(category) {
    const names = {
        tech: '科技',
        finance: '财经',
        social: '社会',
        comprehensive: '综合'
    };
    return names[category] || '综合';
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
    const path = window.location.pathname;
    let category = 'all';
    
    if (path.includes('category-tech.html')) category = 'tech';
    else if (path.includes('category-finance.html')) category = 'finance';
    else if (path.includes('category-social.html')) category = 'social';
    
    loadNews(category);
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const cat = item.dataset.category;
            currentCategory = cat;
            loadNews(cat);
            
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            item.classList.add('active');
        });
    });
    
    document.getElementById('newsModal').addEventListener('click', (e) => {
        if (e.target.id === 'newsModal') closeModal();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
});
