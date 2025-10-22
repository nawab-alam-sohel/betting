// Load Tailwind (CDN) and Chart.js, then render charts
(function(){
  function loadScript(src){
    return new Promise(function(resolve, reject){
      var s = document.createElement('script');
      s.src = src; s.async = true; s.onload = resolve; s.onerror = reject; document.head.appendChild(s);
    });
  }
  function onReady(fn){ if (document.readyState !== 'loading') fn(); else document.addEventListener('DOMContentLoaded', fn); }

  onReady(async function(){
    try {
      // Tailwind CDN
      await loadScript('https://cdn.tailwindcss.com');
    } catch(e) { /* fail-soft */ }
    try {
      await loadScript('https://cdn.jsdelivr.net/npm/chart.js');
    } catch(e) { console.warn('Chart.js not loaded', e); return; }

    // Place BETLAB badge in sidebar
    try {
      var sidebar = document.querySelector('.main-sidebar');
      if (sidebar && !document.querySelector('.betlab-version')){
        var badge = document.createElement('div');
        badge.className = 'betlab-version';
        badge.innerText = 'BETLAB V4.0';
        sidebar.appendChild(badge);
      }
    } catch(e) {}

    // Fill cards
    var data = window.BETLAB_DASHBOARD_DATA || {cards:{},charts:{}};
    function setText(id, val){ var el = document.getElementById(id); if (el) el.textContent = val; }
    setText('card-total-bettors', data.cards.total_bettors || 0);
    setText('card-active-bettors', data.cards.active_bettors || 0);
    setText('card-upcoming-games', data.cards.upcoming_games || 0);
    setText('card-open-for-betting', data.cards.open_for_betting || 0);
    setText('card-pending-bets', data.cards.pending_bets || 0);
    setText('card-withdraw-requests', data.cards.withdraw_requests || 0);

    // Charts helpers
    function lineChart(ctxId, labels, datasets){
      var el = document.getElementById(ctxId); if(!el || !window.Chart) return;
      new Chart(el.getContext('2d'), {
        type: 'line',
        data: { labels: labels, datasets: datasets },
        options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: true } }, scales: { y: { beginAtZero: true } } }
      });
    }
    function donutChart(ctxId, labels, values, colors){
      var el = document.getElementById(ctxId); if(!el || !window.Chart) return;
      new Chart(el.getContext('2d'), {
        type: 'doughnut',
        data: { labels: labels, datasets: [{ data: values, backgroundColor: colors }] },
        options: { responsive: true, maintainAspectRatio: false, cutout: '60%' }
      });
    }

    // Render line charts
    var dw = data.charts.deposit_withdraw || {labels:[],deposited:[],withdrawn:[]};
    lineChart('chart-deposit-withdraw', dw.labels, [
      { label: 'Deposited', data: dw.deposited, borderColor: '#22c55e', backgroundColor: 'rgba(34,197,94,.2)', tension: .3 },
      { label: 'Withdrawn', data: dw.withdrawn, borderColor: '#ef4444', backgroundColor: 'rgba(239,68,68,.2)', tension: .3 },
    ]);

    var tr = data.charts.transactions || {labels:[],plus:[],minus:[]};
    lineChart('chart-transactions', tr.labels, [
      { label: 'Plus Transactions', data: tr.plus, borderColor: '#3b82f6', backgroundColor: 'rgba(59,130,246,.2)', tension: .3 },
      { label: 'Minus Transactions', data: tr.minus, borderColor: '#f59e0b', backgroundColor: 'rgba(245,158,11,.2)', tension: .3 },
    ]);

    // Donuts
    var lb = data.charts.login_browser || {labels:[],values:[]};
    donutChart('donut-browser', lb.labels, lb.values, ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6']);
    var los = data.charts.login_os || {labels:[],values:[]};
    donutChart('donut-os', los.labels, los.values, ['#8b5cf6','#06b6d4','#ef4444','#f59e0b','#22c55e']);
    var lc = data.charts.login_country || {labels:[],values:[]};
    donutChart('donut-country', lc.labels, lc.values, ['#ef4444','#3b82f6','#22c55e','#f59e0b','#06b6d4']);
  });
})();
