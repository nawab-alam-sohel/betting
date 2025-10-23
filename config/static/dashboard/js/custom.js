// Inline minimal HTMX-like shim to ensure htmx.ajax exists even if HTMX isn't loaded separately
window.htmx = window.htmx || {
  ajax: function(method, url, options){
    var target = (options && options.target) ? document.querySelector(options.target) : null;
    fetch(url, { method: method || 'GET', credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(function(r){ return r.text(); })
      .then(function(html){ if (target) { target.innerHTML = html; } })
      .catch(function(){ /* silent */ });
  }
};

(function(){
  // When any element with [data-open-modal] is clicked, open modal and HTMX load the target URL
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-open-modal]');
    if(!t) return;
    var url = t.getAttribute('data-url');
    if(!url) return;
    if (window.$) { $('#systemModal').modal('show'); }
    // trigger HTMX request into modal body
    var body = document.getElementById('system-modal-body');
    if (body) { htmx.ajax('GET', url, { target: '#system-modal-body', swap: 'innerHTML' }); }
  });

  // Basic toast helper if SweetAlert2 is available
  window.toast = function(msg, type){
    if (window.Swal) {
      Swal.fire({ toast:true, icon: type||'success', title: msg||'Saved', position:'top-end', timer:2000, showConfirmButton:false });
    }
  }
  
  // Sidebar badges for Payments (Deposits/Withdrawals)
  function addBadgeToSelector(selector, count, color){
    try {
      var a = document.querySelector('aside.main-sidebar ' + selector + ', .main-sidebar ' + selector + ', ' + selector);
      if (!a) return;
      // Remove old badge if exists
      var old = a.querySelector('.jl-badge');
      if (old) old.remove();
      var span = document.createElement('span');
      span.className = 'badge badge-' + (color||'secondary') + ' right jl-badge';
      span.textContent = String(count);
      a.appendChild(span);
    } catch(e) { /* ignore */ }
  }

  function refreshPaymentBadges(){
    fetch('/admin/metrics/payments/', { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (!data) return;
        // Deposits (proxy models under payments app)
        addBadgeToSelector('a[href="/admin/payments/paymentintentpending/"]', data.deposits.pending, 'warning');
        addBadgeToSelector('a[href="/admin/payments/paymentintentcompleted/"]', data.deposits.completed, 'success');
        addBadgeToSelector('a[href="/admin/payments/paymentintentfailed/"]', data.deposits.failed, 'danger');
        addBadgeToSelector('a[href="/admin/payments/paymentintent/"]', data.deposits.all, 'info');
        // Withdrawals (proxy models)
        addBadgeToSelector('a[href="/admin/payments/withdrawalrequestpending/"]', data.withdrawals.pending, 'warning');
        addBadgeToSelector('a[href="/admin/payments/withdrawalrequestapproved/"]', data.withdrawals.approved, 'success');
        addBadgeToSelector('a[href="/admin/payments/withdrawalrequestrejected/"]', data.withdrawals.rejected, 'danger');
        addBadgeToSelector('a[href="/admin/payments/withdrawalrequest/"]', data.withdrawals.all, 'info');
      })
      .catch(function(){ /* ignore */ });
  }

  // Sidebar badges for Notifications (In-App unread, logs total)
  function refreshNotificationBadges(){
    fetch('/admin/metrics/notifications/', { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (!data) return;
        // In-App Notifications unread on the model link
        addBadgeToSelector('a[href="/admin/notifications/inappnotification/"]', data.inapp.unread, 'warning');
        // NotificationLog total on the model link
        addBadgeToSelector('a[href="/admin/notifications/notificationlog/"]', data.logs.all, 'info');
      })
      .catch(function(){ /* ignore */ });
  }

  // Sidebar badges for Users (KYC pending)
  function refreshUserBadges(){
    fetch('/admin/metrics/users/', { credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(function(r){ return r.json(); })
      .then(function(data){
        if (!data) return;
        // KYC pending count on KYCDocument model link
        addBadgeToSelector('a[href="/admin/users/kycdocument/"]', data.kyc && typeof data.kyc.pending === 'number' ? data.kyc.pending : 0, 'warning');
      })
      .catch(function(){ /* ignore */ });
  }

  if (document.body && document.body.classList.contains('app-jazzmin')){
    // initial
    refreshPaymentBadges();
    refreshNotificationBadges();
  refreshUserBadges();
    // refresh on ajax nav changes (Jazzmin uses pushState); fallback to interval
    window.addEventListener('popstate', function(){
      refreshPaymentBadges();
      refreshNotificationBadges();
      refreshUserBadges();
    });
    setInterval(function(){
      refreshPaymentBadges();
      refreshNotificationBadges();
      refreshUserBadges();
    }, 60000);
  }
})();
