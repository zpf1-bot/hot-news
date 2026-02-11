let currentCategory = 'all';

async function loadNews(category = 'all') {
    currentCategory = category;
    const newsList = document.getElementById('newsList');
    newsList.innerHTML = '<div class="loading">加载中...</div>';
    
    try {
        const url = category === 'all' ? '/api/news' : `/api/news?category=${category}`;
        const response = await fetch(url);
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

async function openModal(index) {
    const response = await fetch(`/api/news/${index}`);
    const news = await response.json();
    
    if (news.error) {
        alert('无法获取新闻详情');
        return;
    }
    
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
}

function closeModal() {
    const modal = document.getElementById('newsModal');
    modal.classList.remove('show');
    document.body.style.overflow = '';
}

async function refreshNews() {
    const btn = document.querySelector('.refresh-btn');
    btn.classList.add('loading');
    btn.textContent = '刷新中...';
    
    try {
        const response = await fetch('/api/refresh', { method: 'POST' });
        const data = await response.json();
        
        if (data.success) {
            await loadNews(currentCategory);
            btn.textContent = '✅ 已刷新';
        } else {
            alert('刷新失败: ' + (data.error || '未知错误'));
        }
    } catch (error) {
        console.error('Error refreshing news:', error);
        alert('刷新失败，请稍后重试');
    }
    
    setTimeout(() => {
        btn.classList.remove('loading');
        btn.textContent = '🔄 刷新';
    }, 2000);
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
    loadNews('all');
    
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const category = item.dataset.category;
            window.location.href = category === 'all' ? '/' : `/category/${category}`;
        });
    });
    
    document.getElementById('newsModal').addEventListener('click', (e) => {
        if (e.target.id === 'newsModal') closeModal();
    });
    
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeModal();
    });
});
