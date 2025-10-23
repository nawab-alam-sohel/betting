// Minimal HTMX-like shim for our modal use-case
window.htmx = window.htmx || {
  ajax: function(method, url, options){
    var target = (options && options.target) ? document.querySelector(options.target) : null;
    fetch(url, { method: method || 'GET', credentials: 'same-origin', headers: { 'X-Requested-With': 'XMLHttpRequest' }})
      .then(function(r){ return r.text(); })
      .then(function(html){ if (target) { target.innerHTML = html; } })
      .catch(function(){ /* silent */ });
  }
};
