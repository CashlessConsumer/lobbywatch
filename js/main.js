/// LobbyWatch: nav highlight + consultation table filtering
(function(){
  function normPath(p){ return (p.length > 1 && p.charAt(p.length-1) === '/') ? p.slice(0, -1) : p; }
  var path = normPath(location.pathname) || '/';
  document.querySelectorAll('nav > a').forEach(function(a){
    var href = normPath(a.getAttribute('href')) || '/';
    if (href === path) a.classList.add('active'); else a.classList.remove('active');
  });

  // consultation ledger: text filter + chips (regulator / status / comments)
  var mq = document.getElementById('mq');
  var table = document.getElementById('ledger');
  if (!mq || !table) return;
  var rows = Array.prototype.slice.call(table.querySelectorAll('tbody tr'));
  var active = { chip: 'all' };

  function apply(){
    var q = mq.value.trim().toLowerCase();
    var shown = 0;
    rows.forEach(function(tr){
      var hay = tr.getAttribute('data-search') || '';
      var chips = (tr.getAttribute('data-chips') || '').toLowerCase().split(' ');
      var okChip = active.chip === 'all' || chips.indexOf(active.chip) !== -1;
      var okText = !q || hay.indexOf(q) !== -1;
      var show = okChip && okText;
      tr.style.display = show ? '' : 'none';
      if (show) shown++;
    });
    var counter = document.getElementById('count');
    if (counter) counter.textContent = shown + ' of ' + rows.length + ' rows';
  }

  document.querySelectorAll('.chip[data-filter]').forEach(function(chip){
    chip.addEventListener('click', function(){
      document.querySelectorAll('.chip[data-filter]').forEach(function(c){ c.classList.remove('active'); });
      chip.classList.add('active');
      active.chip = chip.getAttribute('data-filter');
      apply();
    });
  });
  mq.addEventListener('input', apply);
})();
