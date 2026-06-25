(function() {
  'use strict';

  // ====== Report Registry ======
  var REPORTS = [
    { cat: 'company', file: '东山精密_002384_Serenity分析报告.html', title: '东山精密 (002384)', subtitle: '供应链瓶颈分析' },
    { cat: 'company', file: '永鼎股份_600105_Serenity分析报告.html', title: '永鼎股份 (600105)', subtitle: '供应链瓶颈分析' },
    { cat: 'company', file: '长高电新_Serenity分析报告.html', title: '长高电新 (002452)', subtitle: '供应链瓶颈分析' },
    { cat: 'company', file: '智立方_301312_Serenity分析报告.html', title: '智立方 (301312)', subtitle: '深度分析' },
    { cat: 'company', file: '香农芯创_300475_Serenity分析报告.html', title: '香农芯创 (300475)', subtitle: '深度分析' },
    { cat: 'company', file: '工业富联_601138_Serenity分析报告.html', title: '工业富联 (601138)', subtitle: '深度分析' },
    { cat: 'company', file: '快克智能_603203_Serenity分析报告.html', title: '快克智能 (603203)', subtitle: '深度分析' },
    { cat: 'company', file: '东材科技_601208_Serenity分析报告.html', title: '东材科技 (601208)', subtitle: '高速电子树脂 · AI算力瓶颈' },
    { cat: 'industry', file: 'A股CPO深度调研-20260623.html', title: 'A股CPO深度调研', subtitle: '2026-06-23' },
    { cat: 'industry', file: 'AI服务器深度调研报告.html', title: 'AI 服务器深度调研报告', subtitle: '' },
    { cat: 'industry', file: 'MLCC深度研究报告.html', title: 'MLCC 产业链深度研究报告', subtitle: '' },
    { cat: 'industry', file: '存储芯片深度调研报告.html', title: '存储芯片深度调研报告', subtitle: '2026年6月' }
  ];

  var CATEGORIES = {
    company: { label: '公司深度分析', icon: '📈' },
    industry: { label: '行业深度调研', icon: '🔬' }
  };

  // ====== Detect current page ======
  var pathParts = window.location.pathname.split('/');
  var currentFile = decodeURIComponent(pathParts[pathParts.length - 1]);
  var isIndex = (currentFile === '' || currentFile.toLowerCase() === 'index.html');

  // ====== Inject CSS ======
  var style = document.createElement('style');
  style.textContent = [
    '.sn-nav *,.sn-panel *,.sn-top-btn *{margin:0;padding:0;box-sizing:border-box}',
    '.sn-nav{position:fixed;top:0;left:0;right:0;z-index:9999;height:48px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans SC",sans-serif}',
    '.sn-nav a{color:#58a6ff;text-decoration:none;font-size:14px;transition:color 0.15s}',
    '.sn-nav a:hover{color:#79c0ff}',
    '.sn-nav .sn-brand{color:#f0f6fc;font-weight:600;font-size:15px;display:flex;align-items:center;gap:8px;cursor:pointer}',
    '.sn-nav .sn-brand:hover{color:#f0f6fc;text-decoration:none}',
    '.sn-nav .sn-brand .sn-logo{font-size:18px}',
    '.sn-nav .sn-right{display:flex;align-items:center;gap:12px}',
    '.sn-nav .sn-toggle{background:#21262d;color:#c9d1d9;border:1px solid #30363d;border-radius:6px;padding:5px 14px;cursor:pointer;font-size:13px;font-family:inherit;transition:background 0.15s,border-color 0.15s;display:flex;align-items:center;gap:6px}',
    '.sn-nav .sn-toggle:hover{background:#30363d;border-color:#58a6ff}',
    '.sn-nav .sn-toggle .sn-arrow{font-size:10px;transition:transform 0.2s}',
    '.sn-nav .sn-toggle.open .sn-arrow{transform:rotate(180deg)}',
    '.sn-panel{display:none;position:fixed;top:48px;left:0;right:0;z-index:9998;background:#161b22;border-bottom:1px solid #30363d;max-height:70vh;overflow-y:auto;padding:16px 24px;box-shadow:0 8px 24px rgba(0,0,0,0.5)}',
    '.sn-panel.open{display:block;animation:snFadeIn 0.15s ease}',
    '@keyframes snFadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}',
    '.sn-panel .sn-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}',
    '.sn-panel .sn-group{margin-bottom:4px}',
    '.sn-panel .sn-group-label{color:#8b949e;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px;padding-left:4px;font-weight:600}',
    '.sn-panel .sn-item{display:block;padding:7px 10px;border-radius:6px;font-size:13px;color:#c9d1d9;text-decoration:none;transition:background 0.12s,color 0.12s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}',
    '.sn-panel .sn-item:hover{background:#1c2128;color:#f0f6fc}',
    '.sn-panel .sn-item.active{color:#58a6ff;font-weight:600;background:rgba(88,166,255,0.08)}',
    '.sn-panel .sn-item .sn-badge{font-size:11px;color:#8b949e;font-weight:400;margin-left:4px}',
    '.sn-top-btn{position:fixed;bottom:28px;right:28px;z-index:9997;width:42px;height:42px;border-radius:50%;background:#161b22;border:1px solid #30363d;color:#8b949e;font-size:20px;cursor:pointer;display:none;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(0,0,0,0.4);transition:border-color 0.2s,color 0.2s,transform 0.15s}',
    '.sn-top-btn:hover{border-color:#58a6ff;color:#58a6ff;transform:translateY(-2px)}',
    '.sn-top-btn.visible{display:flex}',
    '.sn-overlay{display:none;position:fixed;inset:0;z-index:9997;background:rgba(0,0,0,0.3)}',
    '.sn-overlay.open{display:block}',
    '@media print{.sn-nav,.sn-panel,.sn-top-btn,.sn-overlay{display:none!important}}',
    '@media(max-width:640px){.sn-nav{padding:0 16px}.sn-panel{padding:12px 16px;max-height:60vh}.sn-panel .sn-grid{grid-template-columns:1fr}.sn-top-btn{bottom:20px;right:20px;width:38px;height:38px}}'
  ].join('');
  document.head.appendChild(style);

  // ====== Inject overlay (for closing panel on outside click) ======
  var overlay = document.createElement('div');
  overlay.className = 'sn-overlay';
  overlay.id = 'snOverlay';
  document.body.appendChild(overlay);

  // ====== Inject nav bar ======
  var brandHTML = isIndex
    ? '<span class="sn-brand"><span class="sn-logo">🔍</span>Serenity 研究报告</span>'
    : '<a class="sn-brand" href="../index.html"><span class="sn-logo">🔍</span>Serenity 研究报告</a>';

  var navHTML = '<div class="sn-nav" id="snNav">'
    + brandHTML
    + '<div class="sn-right">'
    + '<button class="sn-toggle" id="snToggle">📋 所有报告 <span class="sn-arrow">▾</span></button>'
    + '</div></div>';

  document.body.insertAdjacentHTML('afterbegin', navHTML);

  // ====== Inject dropdown panel ======
  var panelHTML = '<div class="sn-panel" id="snPanel"><div class="sn-grid">';

  ['company', 'industry'].forEach(function(cat) {
    panelHTML += '<div class="sn-group"><div class="sn-group-label">' + CATEGORIES[cat].icon + ' ' + CATEGORIES[cat].label + '</div>';
    REPORTS.forEach(function(r) {
      if (r.cat !== cat) return;
      var isActive = (!isIndex && r.file === currentFile);
      var activeClass = isActive ? ' active' : '';
      var link = isIndex ? 'html/' + r.file : encodeURIComponent(r.file);
      panelHTML += '<a class="sn-item' + activeClass + '" href="' + link + '">'
        + '▸ ' + r.title
        + (r.subtitle ? '<span class="sn-badge">· ' + r.subtitle + '</span>' : '')
        + (isActive ? ' ←' : '')
        + '</a>';
    });
    panelHTML += '</div>';
  });

  panelHTML += '</div></div>';
  document.body.insertAdjacentHTML('beforeend', panelHTML);

  // ====== Inject back-to-top button ======
  var topBtn = document.createElement('button');
  topBtn.className = 'sn-top-btn';
  topBtn.id = 'snTop';
  topBtn.innerHTML = '↑';
  topBtn.title = '回到顶部';
  document.body.appendChild(topBtn);

  // ====== Adjust body padding ======
  document.body.style.paddingTop = '52px';

  // ====== Event handlers ======
  var toggle = document.getElementById('snToggle');
  var panel = document.getElementById('snPanel');
  var topBtnEl = document.getElementById('snTop');
  var overlayEl = document.getElementById('snOverlay');

  function openPanel() {
    panel.classList.add('open');
    toggle.classList.add('open');
    overlayEl.classList.add('open');
  }

  function closePanel() {
    panel.classList.remove('open');
    toggle.classList.remove('open');
    overlayEl.classList.remove('open');
  }

  if (toggle) {
    toggle.addEventListener('click', function(e) {
      e.stopPropagation();
      panel.classList.contains('open') ? closePanel() : openPanel();
    });
  }

  if (overlayEl) {
    overlayEl.addEventListener('click', closePanel);
  }

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && panel && panel.classList.contains('open')) {
      closePanel();
    }
  });

  // Scroll: show/hide back-to-top button
  window.addEventListener('scroll', function() {
    if (topBtnEl) {
      topBtnEl.classList.toggle('visible', window.scrollY > 300);
    }
  });

  if (topBtnEl) {
    topBtnEl.addEventListener('click', function() {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
})();
