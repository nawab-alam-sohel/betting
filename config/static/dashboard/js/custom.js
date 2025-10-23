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
})();
