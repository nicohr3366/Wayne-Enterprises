// WAYNETECH — main.js

// NAV scroll effect
window.addEventListener('scroll', () => {
  document.getElementById('mainNav').style.borderBottomColor =
    window.scrollY > 80 ? 'rgba(201,168,76,0.35)' : 'rgba(201,168,76,0.18)';
});

// MODAL
const overlay = document.getElementById('modalOverlay');
const inner   = document.getElementById('modalInner');

function openModal(type, id) {
  const urls = { gadget:`/api/gadget/${id}/`, villain:`/api/villain/${id}/`,
                 division:`/api/division/${id}/`, executive:`/api/executive/${id}/` };
  inner.innerHTML = '<div class="modal-loading">Cargando expediente...</div>';
  overlay.classList.add('open');
  document.body.style.overflow = 'hidden';
  fetch(urls[type]).then(r=>r.json()).then(d=>{
    if (type==='gadget')    inner.innerHTML = gadgetModal(d);
    if (type==='villain')   inner.innerHTML = villainModal(d);
    if (type==='division')  inner.innerHTML = divisionModal(d);
    if (type==='executive') inner.innerHTML = executiveModal(d);
  }).catch(()=>{ inner.innerHTML='<div class="modal-loading">Error al cargar.</div>'; });
}
function closeModal(){ overlay.classList.remove('open'); document.body.style.overflow=''; }
function closeModalOut(e){ if(e.target===overlay) closeModal(); }
document.addEventListener('keydown', e=>{ if(e.key==='Escape') closeModal(); });

function imgOrPh(src, icon='◈'){
  if(src) return `<img src="${src}" alt="" style="width:100%;height:100%;min-height:320px;object-fit:cover;object-position:center top;filter:grayscale(15%) contrast(1.08)">`;
  return `<div class="modal-img-ph"><span class="ph-icon">${icon}</span><span class="ph-lbl">IMAGEN CLASIFICADA</span></div>`;
}

function gadgetModal(d){
  return `<button class="modal-close" onclick="closeModal()">✕</button>
  <div class="modal-top">
    <div class="modal-img"><div class="scan-line"></div>${imgOrPh(d.image,'⚙')}</div>
    <div class="modal-meta">
      <div class="modal-badge">${d.code} · ${d.clearance_level}</div>
      <div class="modal-title">${d.name}</div>
      <div class="modal-sub">${d.classification}</div>
      <table class="mtable">
        <tr><td>CÓDIGO</td><td>${d.code}</td></tr>
        <tr><td>CLASIFICACIÓN</td><td>${d.classification}</td></tr>
        <tr><td>ESTADO</td><td>${d.status}</td></tr>
        <tr><td>AÑO DESARROLLO</td><td>${d.year_developed}</td></tr>
        <tr><td>INCIDENTES RESUELTOS</td><td>${d.threat_neutralized}</td></tr>
        <tr><td>NIVEL DE ACCESO</td><td>${d.clearance_level}</td></tr>
      </table>
    </div>
  </div>
  <div class="modal-body">
    <div class="mbst">DESCRIPCIÓN</div><p class="mdesc">${d.description}</p>
    ${d.specs?`<div class="mbst">ESPECIFICACIONES TÉCNICAS</div><p class="mtext">${d.specs.replace(/\|/g,'<br>')}</p>`:''}
  </div>`;
}

function villainModal(d){
  const tc={'S':'#e74c3c','A':'#e67e22','B':'#f1c40f','C':'#27ae60'};
  const c=tc[d.threat_code]||'#7a8899';
  return `<button class="modal-close" onclick="closeModal()">✕</button>
  <div class="modal-top">
    <div class="modal-img"><div class="scan-line"></div>${imgOrPh(d.image,'☠')}</div>
    <div class="modal-meta">
      <div class="modal-badge" style="color:${c};border-color:${c}60">AMENAZA ${d.threat_code} — ${d.threat_level}</div>
      <div class="modal-title">${d.alias}</div>
      <div class="modal-sub">Identidad: ${d.name}</div>
      <table class="mtable">
        <tr><td>NIVEL DE AMENAZA</td><td style="color:${c}">${d.threat_level}</td></tr>
        <tr><td>ESTADO ACTUAL</td><td>${d.status}</td></tr>
        <tr><td>VECES DETENIDO</td><td>${d.times_detained}x</td></tr>
        ${d.last_detained?`<tr><td>ÚLTIMA DETENCIÓN</td><td>${d.last_detained}</td></tr>`:''}
        ${d.arkham_cell?`<tr><td>CELDA ARKHAM</td><td>${d.arkham_cell}</td></tr>`:''}
      </table>
    </div>
  </div>
  <div class="modal-body">
    <div class="mbst">PERFIL</div><p class="mdesc">${d.description}</p>
    <div class="mbst">CRÍMENES DOCUMENTADOS</div><p class="mtext">${d.crimes}</p>
  </div>`;
}

function divisionModal(d){
  const pc={'Alta — Lanzamiento Inmediato':'#27ae60','Media — Migración Planificada':'#c9a84c','Baja — Evaluación en Curso':'#7a8899'};
  const c=pc[d.cloud_priority]||'#c9a84c';
  return `<button class="modal-close" onclick="closeModal()">✕</button>
  <div class="modal-top">
    <div class="modal-img">${imgOrPh(d.image,'◈')}</div>
    <div class="modal-meta">
      <div class="modal-badge" style="color:${c};border-color:${c}60">PRIORIDAD CLOUD: ${d.cloud_priority}</div>
      <div class="modal-title">${d.name}</div>
      <div class="modal-sub">${d.focus}</div>
      <table class="mtable">
        <tr><td>ENFOQUE</td><td>${d.focus}</td></tr>
        <tr><td>PRIORIDAD CLOUD</td><td style="color:${c}">${d.cloud_priority}</td></tr>
      </table>
    </div>
  </div>
  <div class="modal-body">
    <div class="mbst">DESCRIPCIÓN Y RESPONSABILIDADES</div><p class="mdesc">${d.description}</p>
    <div class="mbst">RELEVANCIA PARA LA MIGRACIÓN A LA NUBE</div><p class="mtext">${d.cloud_relevance}</p>
  </div>`;
}

function executiveModal(d){
  return `<button class="modal-close" onclick="closeModal()">✕</button>
  <div class="modal-top">
    <div class="modal-img"><div class="scan-line"></div>${imgOrPh(d.image,'◉')}</div>
    <div class="modal-meta">
      <div class="modal-badge">${d.level}</div>
      <div class="modal-title">${d.role}</div>
      <div class="modal-sub">${d.full_title}</div>
      <table class="mtable">
        <tr><td>NOMBRE</td><td>${d.name}</td></tr>
        <tr><td>CARGO</td><td>${d.full_title}</td></tr>
        <tr><td>NIVEL</td><td>${d.level}</td></tr>
        <tr><td>ID EMPLEADO</td><td>${d.employee_id}</td></tr>
      </table>
    </div>
  </div>
  <div class="modal-body">
    <div class="mbst">RESPONSABILIDADES ESTRATÉGICAS</div><p class="mdesc">${d.strategic_responsibilities}</p>
    <div class="mbst">ROL EN LA TRANSFORMACIÓN CLOUD</div><p class="mtext">${d.cloud_role}</p>
  </div>`;
}

// Intersection observer - fade in on scroll
const observer = new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.style.opacity='1'; e.target.style.transform='translateY(0)'; }});
}, {threshold:0.06});

document.querySelectorAll('.gcard,.vcard,.div-card,.org-card,.kpi-card,.phase,.cm-card,.ccoe-item').forEach(el=>{
  el.style.opacity='0'; el.style.transform='translateY(16px)';
  el.style.transition='opacity 0.5s ease, transform 0.5s ease, background 0.25s';
  observer.observe(el);
});

// Animate KPI bars when visible
const kpiFills = document.querySelectorAll('.kpi-fill');
const kpiObs = new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting){ e.target.style.width=e.target.dataset.width; kpiObs.unobserve(e.target); }});
},{threshold:0.1});
kpiFills.forEach(el=>{ const w=el.style.width; el.style.width='0'; el.dataset.width=w; kpiObs.observe(el); });
