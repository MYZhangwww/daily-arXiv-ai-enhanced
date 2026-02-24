/**
 * 今日推荐页面脚本 / Today's Recommendations Page Script
 * 展示发送到飞书的精选论文
 */

let recommendedData = [];
let allDates = [];
let currentSelectedDate = null;
let currentViewMode = 'grid';
let currentFilterMode = 'all';
let currentDisplayedPapers = [];

// 配置 API 端点
const API_BASE = dataSource.baseUrl || './data';
const API_ENDPOINTS = {
    recommended: `${API_BASE}/recommended_papers.jsonl`,
};

/**
 * 初始化页面
 */
document.addEventListener('DOMContentLoaded', () => {
    fetchGitHubStats();
    initEventListeners();
    loadRecommendedPapers();
});

/**
 * 初始化事件监听
 */
function initEventListeners() {
    // 视图切换
    document.querySelectorAll('.view-button').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            switchViewMode(btn.dataset.view);
        });
    });

    // 优先级过滤
    document.getElementById('priorityFilter').addEventListener('change', (e) => {
        currentFilterMode = e.target.value;
        renderPapers(currentSelectedDate);
    });

    // 模态框关闭
    document.getElementById('closeModal').addEventListener('click', closeModal);
    document.getElementById('paperModal').addEventListener('click', (e) => {
        if (e.target.id === 'paperModal') closeModal();
    });

    // 回到顶部
    document.getElementById('backToTop').addEventListener('click', scrollToTop);
    window.addEventListener('scroll', toggleBackToTopButton);
}

/**
 * 加载推荐论文数据
 */
async function loadRecommendedPapers() {
    try {
        const response = await fetch(API_ENDPOINTS.recommended);
        if (!response.ok) throw new Error('Failed to fetch recommended papers');
        
        const text = await response.text();
        recommendedData = text
            .split('\n')
            .filter(line => line.trim())
            .map(line => {
                try {
                    return JSON.parse(line);
                } catch (e) {
                    console.error('Error parsing line:', line);
                    return null;
                }
            })
            .filter(item => item !== null);

        // 按推荐日期分组
        groupByDate();
        
        // 更新统计信息
        updateStatistics();
        
        // 渲染日期按钮
        renderDateButtons();
        
        // 选择最新的日期
        if (allDates.length > 0) {
            selectDate(allDates[0]);
        }

    } catch (error) {
        console.error('Error loading recommended papers:', error);
        showEmptyState('Failed to load recommended papers');
    }
}

/**
 * 按日期分组数据
 */
function groupByDate() {
    const dateMap = {};

    recommendedData.forEach(paper => {
        const date = paper.recommended_date || 'Unknown';
        if (!dateMap[date]) {
            dateMap[date] = [];
        }
        dateMap[date].push(paper);
    });

    // 按日期倒序排列
    allDates = Object.keys(dateMap).sort().reverse();
}

/**
 * 更新统计信息
 */
function updateStatistics() {
    const stats = {
        total: recommendedData.length,
        priority: recommendedData.filter(p => p.is_priority).length,
        dates: allDates.length
    };

    document.getElementById('totalRecommended').textContent = stats.total;
    document.getElementById('priorityPapers').textContent = stats.priority;
    document.getElementById('recommendedDates').textContent = stats.dates;
}

/**
 * 渲染日期按钮
 */
function renderDateButtons() {
    const container = document.getElementById('dateButtons');
    container.innerHTML = '';

    allDates.forEach(date => {
        const count = recommendedData.filter(p => p.recommended_date === date).length;
        const btn = document.createElement('button');
        btn.className = 'date-button';
        btn.textContent = `${date} <span class="count">${count}</span>`;
        btn.innerHTML = `${date} <span class="count">${count}</span>`;
        btn.addEventListener('click', () => selectDate(date));
        container.appendChild(btn);
    });
}

/**
 * 选择日期
 */
function selectDate(date) {
    currentSelectedDate = date;

    // 更新活跃日期按钮
    document.querySelectorAll('.date-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.textContent.startsWith(date)) {
            btn.classList.add('active');
        }
    });

    // 更新标题
    const count = recommendedData.filter(p => p.recommended_date === date).length;
    document.getElementById('sectionTitle').textContent = `${date} - ${count} 篇推荐论文 / ${count} Recommended Papers`;

    // 渲染论文
    renderPapers(date);
}

/**
 * 渲染论文列表
 */
function renderPapers(date) {
    const container = document.getElementById('papersContainer');

    if (!date) {
        showEmptyState('No papers found');
        return;
    }

    // 过滤论文
    let papers = recommendedData.filter(p => p.recommended_date === date);

    // 应用优先级过滤
    if (currentFilterMode === 'priority') {
        papers = papers.filter(p => p.is_priority);
    } else if (currentFilterMode === 'normal') {
        papers = papers.filter(p => !p.is_priority);
    }

    currentDisplayedPapers = papers;

    if (papers.length === 0) {
        showEmptyState('No papers found for this filter');
        return;
    }

    // 按优先级排序（优先级优先）
    papers.sort((a, b) => {
        if (a.is_priority && !b.is_priority) return -1;
        if (!a.is_priority && b.is_priority) return 1;
        return 0;
    });

    // 渲染论文卡片
    container.innerHTML = papers.map((paper, idx) => createPaperCard(paper, idx)).join('');

    // 添加事件监听
    container.querySelectorAll('.recommended-paper-card').forEach((card, idx) => {
        card.addEventListener('click', () => showPaperModal(papers[idx]));
    });
}

/**
 * 创建论文卡片 HTML
 */
function createPaperCard(paper, idx) {
    const priorityClass = paper.is_priority ? 'priority-paper' : '';
    const priorityBadge = paper.is_priority ? '<div class="priority-badge">⭐ 优先级</div>' : '';
    
    const date = paper.recommended_date ? new Date(paper.recommended_date).toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    }) : 'Unknown';

    const authors = paper.authors || 'N/A';
    const title = paper.title || 'N/A';
    const category = paper.category || 'N/A';
    const summary = paper.tldr || paper.summary || 'No summary available';

    return `
        <div class="recommended-paper-card ${priorityClass} paper-card-enter">
            ${priorityBadge}
            <div class="paper-meta">
                <span class="meta-item date">📅 ${date}</span>
                <span class="meta-item category">📁 ${category}</span>
                ${paper.is_priority ? '<span class="meta-item priority">⭐ Priority</span>' : ''}
            </div>
            <h3 class="paper-title">${escapeHtml(title)}</h3>
            <p class="paper-authors">✍️ ${escapeHtml(authors)}</p>
            <p class="paper-summary">${escapeHtml(summary.substring(0, 200))}${summary.length > 200 ? '...' : ''}</p>
            <div class="paper-actions">
                <button class="paper-action-btn" onclick="event.stopPropagation()">📖 详情</button>
                <a href="${paper.url || '#'}" target="_blank" class="paper-action-btn primary" onclick="event.stopPropagation()">🔗 arXiv</a>
            </div>
        </div>
    `;
}

/**
 * 显示论文详情模态框
 */
function showPaperModal(paper) {
    const modal = document.getElementById('paperModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');

    title.textContent = paper.title || 'Paper Details';

    const html = `
        <div class="paper-details">
            <div class="detail-section">
                <h3 class="detail-title">标题 / Title</h3>
                <p class="detail-content">${escapeHtml(paper.title || 'N/A')}</p>
            </div>

            <div class="detail-section">
                <h3 class="detail-title">作者 / Authors</h3>
                <p class="detail-content">${escapeHtml(paper.authors || 'N/A')}</p>
            </div>

            <div class="detail-section">
                <h3 class="detail-title">分类 / Category</h3>
                <p class="detail-content">${escapeHtml(paper.category || 'N/A')}</p>
            </div>

            <div class="detail-section">
                <h3 class="detail-title">ID / ArXiv ID</h3>
                <p class="detail-content">${escapeHtml(paper.id || 'N/A')}</p>
            </div>

            <div class="detail-section">
                <h3 class="detail-title">推荐日期 / Recommendation Date</h3>
                <p class="detail-content">${paper.recommended_date || 'N/A'}</p>
            </div>

            <div class="detail-section">
                <h3 class="detail-title">优先级 / Priority</h3>
                <p class="detail-content">${paper.is_priority ? '⭐ 优先级论文 / Priority Paper' : '普通论文 / Normal Paper'}</p>
            </div>

            ${paper.tldr ? `
                <div class="detail-section">
                    <h3 class="detail-title">AI 总结 / AI Summary</h3>
                    <p class="detail-content">${escapeHtml(paper.tldr)}</p>
                </div>
            ` : ''}

            ${paper.summary ? `
                <div class="detail-section">
                    <h3 class="detail-title">摘要 / Abstract</h3>
                    <p class="detail-content">${escapeHtml(paper.summary)}</p>
                </div>
            ` : ''}
        </div>
    `;

    body.innerHTML = html;

    // 更新链接
    document.getElementById('paperLink').href = paper.url || '#';
    document.getElementById('pdfLink').href = paper.url ? paper.url.replace('/abs/', '/pdf/') + '.pdf' : '#';

    modal.style.display = 'flex';
}

/**
 * 关闭模态框
 */
function closeModal() {
    document.getElementById('paperModal').style.display = 'none';
}

/**
 * 切换视图模式
 */
function switchViewMode(mode) {
    currentViewMode = mode;
    const container = document.getElementById('papersContainer');

    // 更新按钮状态
    document.querySelectorAll('.view-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.view === mode) {
            btn.classList.add('active');
        }
    });

    // 更新容器类名
    if (mode === 'list') {
        container.classList.add('list-view');
    } else {
        container.classList.remove('list-view');
    }
}

/**
 * 显示空状态
 */
function showEmptyState(message) {
    const container = document.getElementById('papersContainer');
    container.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">📭</div>
            <h3 class="empty-state-title">暂无数据 / No Data</h3>
            <p class="empty-state-text">${message}</p>
        </div>
    `;
}

/**
 * HTML 转义
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * 滚动到顶部
 */
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

/**
 * 切换回到顶部按钮
 */
function toggleBackToTopButton() {
    const btn = document.getElementById('backToTop');
    if (window.pageYOffset > 300) {
        btn.style.display = 'flex';
    } else {
        btn.style.display = 'none';
    }
}

/**
 * 获取 GitHub 统计
 */
async function fetchGitHubStats() {
    try {
        const response = await fetch('https://api.github.com/repos/dw-dengwei/daily-arXiv-ai-enhanced');
        const data = await response.json();
        document.getElementById('starCount').textContent = data.stargazers_count;
        document.getElementById('forkCount').textContent = data.forks_count;
    } catch (error) {
        console.error('Failed to fetch GitHub stats:', error);
        document.getElementById('starCount').textContent = '?';
        document.getElementById('forkCount').textContent = '?';
    }
}
