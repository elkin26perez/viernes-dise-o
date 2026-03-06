// ══════════════════════════════════════════
// SITM — Sistema Integrado de Transporte Masivo
// app.js
// ══════════════════════════════════════════

// ── ESTADO GLOBAL ──
const state = {
  totalPassengers: 1842,
  onboard: 187,
  evasions: 34,
  activeBuses: 7,
  evasionValue: 34 * 2900,
};

const routes = [
  { num: 'R-01', name: 'Terminal — Cabecera',        stops: 12, buses: 2, km: 18.4, freq: '8 min',  active: true  },
  { num: 'R-02', name: 'Centro — Norte Industrial',  stops: 9,  buses: 2, km: 14.2, freq: '10 min', active: true  },
  { num: 'R-03', name: 'Sur — Universidad',          stops: 11, buses: 2, km: 16.8, freq: '12 min', active: true  },
  { num: 'R-04', name: 'Circular Centro',            stops: 8,  buses: 1, km: 10.5, freq: '15 min', active: false },
];

const fleet = [
  { id: 'BUS-001', route: 'R-01', status: 'active', pass: 52, cap: 80, evas: 2, stop: 'Cabecera'    },
  { id: 'BUS-002', route: 'R-01', status: 'active', pass: 38, cap: 80, evas: 0, stop: 'Estadio'     },
  { id: 'BUS-003', route: 'R-02', status: 'active', pass: 71, cap: 80, evas: 5, stop: 'Industrial'  },
  { id: 'BUS-004', route: 'R-02', status: 'alert',  pass: 66, cap: 80, evas: 8, stop: 'Plaza Mayor' },
  { id: 'BUS-005', route: 'R-03', status: 'active', pass: 23, cap: 80, evas: 1, stop: 'Universidad' },
  { id: 'BUS-006', route: 'R-03', status: 'active', pass: 44, cap: 80, evas: 3, stop: 'Hospital'    },
  { id: 'BUS-007', route: 'R-04', status: 'active', pass: 31, cap: 80, evas: 2, stop: 'Centro'      },
  { id: 'BUS-008', route: '—',    status: 'idle',   pass: 0,  cap: 80, evas: 0, stop: 'Patio Taller'},
];

const sensors = [
  { id: 'KNX-01', bus: 'BUS-001', status: 'online',  counts: 52 },
  { id: 'KNX-02', bus: 'BUS-002', status: 'online',  counts: 38 },
  { id: 'KNX-03', bus: 'BUS-003', status: 'online',  counts: 71 },
  { id: 'KNX-04', bus: 'BUS-004', status: 'alert',   counts: 66 },
  { id: 'KNX-05', bus: 'BUS-005', status: 'online',  counts: 23 },
  { id: 'KNX-06', bus: 'BUS-006', status: 'online',  counts: 44 },
  { id: 'KNX-07', bus: 'BUS-007', status: 'online',  counts: 31 },
  { id: 'KNX-08', bus: 'BUS-008', status: 'offline', counts: 0  },
];

const alerts = [
  { type: 'danger', icon: '🚨', title: 'Alta tasa de evasión — BUS-004',   desc: '8 evasiones detectadas en última hora. Ruta R-02 sector Plaza Mayor',           time: 'hace 5 min'  },
  { type: 'warn',   icon: '⚠️', title: 'Sensor KNX-04 — Señal inestable',  desc: 'Pérdidas de señal intermitentes. Verificar conexión 4G del equipo',              time: 'hace 12 min' },
  { type: 'danger', icon: '👥', title: 'Sobrecapacidad — BUS-003',          desc: '71 pasajeros (89% ocupación). Considerar enviar refuerzo en ruta R-02',           time: 'hace 18 min' },
];

const hourlyData = [
  { hour: '06', entries: 42,  evasions: 1 },
  { hour: '07', entries: 118, evasions: 4 },
  { hour: '08', entries: 221, evasions: 8 },
  { hour: '09', entries: 189, evasions: 6 },
  { hour: '10', entries: 134, evasions: 3 },
  { hour: '11', entries: 98,  evasions: 2 },
  { hour: '12', entries: 167, evasions: 5 },
  { hour: '13', entries: 143, evasions: 4 },
  { hour: '14', entries: 112, evasions: 3 },
  { hour: '15', entries: 87,  evasions: 2 },
];

const feedEvents = [
  { type: 'entry',   icon: '↑',  msg: '<strong>BUS-003</strong> — Entrada detectada en parada <strong>Industrial</strong>', time: 'ahora'      },
  { type: 'evasion', icon: '⛔', msg: '<strong>BUS-004</strong> — Intento de evasión detectado · Sensor KNX-04',           time: 'hace 1 min' },
  { type: 'exit',    icon: '↓',  msg: '<strong>BUS-001</strong> — Salida registrada en <strong>Cabecera</strong>',          time: 'hace 2 min' },
  { type: 'entry',   icon: '↑',  msg: '<strong>BUS-007</strong> — 4 entradas consecutivas · Centro',                       time: 'hace 3 min' },
  { type: 'info',    icon: 'ℹ',  msg: '<strong>BUS-006</strong> — Partió de Hospital hacia siguiente parada',               time: 'hace 4 min' },
  { type: 'entry',   icon: '↑',  msg: '<strong>BUS-002</strong> — Entrada detectada · Estadio',                             time: 'hace 5 min' },
  { type: 'evasion', icon: '⛔', msg: '<strong>BUS-003</strong> — Evasión confirmada · Pérdida: $2.900',                   time: 'hace 6 min' },
];

// ══════════════════════════════════════════
// RELOJ EN TIEMPO REAL
// ══════════════════════════════════════════
function updateClock() {
  const now = new Date();
  const time = now.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  const date = now.toLocaleDateString('es-CO', { weekday: 'short', day: 'numeric', month: 'short' });
  document.getElementById('live-clock').textContent = `${time} · ${date}`;
}
setInterval(updateClock, 1000);
updateClock();

// ══════════════════════════════════════════
// NAVEGACIÓN
// ══════════════════════════════════════════
function showPage(id, el) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  document.getElementById('page-' + id).classList.add('active');
  if (el) el.classList.add('active');

  const titles = {
    dashboard: 'Dashboard en Tiempo Real',
    rutas:     'Gestión de Rutas y Buses',
    sensores:  'Sensores Kinect — Monitoreo',
    alertas:   'Centro de Alertas',
  };
  document.getElementById('page-title').textContent = titles[id] || id;
}

// ══════════════════════════════════════════
// RENDER — ESTADÍSTICAS
// ══════════════════════════════════════════
function animateCount(el, target) {
  let current = 0;
  const step = Math.max(1, Math.floor(target / 40));
  const interval = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString('es-CO');
    if (current >= target) clearInterval(interval);
  }, 30);
}

function renderStats() {
  animateCount(document.getElementById('stat-total'),    state.totalPassengers);
  animateCount(document.getElementById('stat-onboard'),  state.onboard);
  animateCount(document.getElementById('stat-evasion'),  state.evasions);

  const cards = document.querySelectorAll('.stat-card');
  cards[2].querySelector('.stat-delta').textContent =
    '▼ COP $' + state.evasionValue.toLocaleString('es-CO');
}

// ══════════════════════════════════════════
// RENDER — GRÁFICO DE BARRAS POR HORA
// ══════════════════════════════════════════
function renderHourlyChart() {
  const chart = document.getElementById('hourly-chart');
  const maxVal = Math.max(...hourlyData.map(d => d.entries));
  chart.innerHTML = '';

  hourlyData.forEach((d, i) => {
    const entryH  = Math.floor((d.entries  / maxVal) * 100);
    const evasH   = Math.floor((d.evasions / maxVal) * 100) + 4;

    const wrap = document.createElement('div');
    wrap.className = 'bar-wrap';
    wrap.innerHTML = `
      <div style="display:flex;align-items:flex-end;gap:2px;height:110px">
        <div class="bar bar-entry"
             style="height:0;width:14px;transition-delay:${i * 40}ms"
             data-h="${entryH}"></div>
        <div class="bar bar-evasion"
             style="height:0;width:8px;transition-delay:${i * 40 + 20}ms"
             data-h="${evasH}"></div>
      </div>
      <div class="bar-label">${d.hour}h</div>
    `;
    chart.appendChild(wrap);
  });

  // Animar barras con pequeño delay
  setTimeout(() => {
    chart.querySelectorAll('.bar').forEach(b => {
      b.style.height = b.dataset.h + 'px';
    });
  }, 100);
}

// ══════════════════════════════════════════
// RENDER — FEED DE EVENTOS EN VIVO
// ══════════════════════════════════════════
function renderFeed() {
  const feed = document.getElementById('live-feed');
  feed.innerHTML = '';
  feedEvents.forEach(e => {
    const div = document.createElement('div');
    div.className = `feed-item ${e.type}`;
    div.innerHTML = `
      <span class="feed-icon">${e.icon}</span>
      <span class="feed-msg">${e.msg}</span>
      <span class="feed-time">${e.time}</span>
    `;
    feed.appendChild(div);
  });
}

// ══════════════════════════════════════════
// RENDER — TABLA DE FLOTA
// ══════════════════════════════════════════
function renderFleet() {
  const tbody = document.getElementById('fleet-tbody');
  tbody.innerHTML = '';

  fleet.forEach(b => {
    const occ = Math.round((b.pass / b.cap) * 100);
    const occClass = occ > 80 ? 'occ-high' : occ > 60 ? 'occ-mid' : 'occ-low';

    const statusMap = {
      active: `<span class="status-pill status-active"><span class="status-dot-sm"></span>Activo</span>`,
      idle:   `<span class="status-pill status-idle"><span class="status-dot-sm"></span>En patio</span>`,
      alert:  `<span class="status-pill status-alert"><span class="status-dot-sm"></span>⚠ Alerta</span>`,
    };

    const evasColor  = b.evas > 3 ? 'var(--danger)' : 'var(--muted)';
    const evasWeight = b.evas > 3 ? '700' : '400';

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><span class="bus-id">${b.id}</span></td>
      <td><span class="route-tag">${b.route}</span></td>
      <td>${statusMap[b.status]}</td>
      <td>
        <span style="font-family:'Syne',sans-serif;font-weight:700">${b.pass}</span>
        <span style="color:var(--muted);font-size:10px"> / ${b.cap}</span>
      </td>
      <td>
        <div class="occ-bar">
          <div class="occ-track">
            <div class="occ-fill ${occClass}" style="width:${occ}%"></div>
          </div>
          <span class="occ-num">${occ}%</span>
        </div>
      </td>
      <td><span style="color:${evasColor};font-weight:${evasWeight}">${b.evas}</span></td>
      <td style="color:var(--muted)">${b.stop}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ══════════════════════════════════════════
// RENDER — RUTAS
// ══════════════════════════════════════════
function renderRoutes() {
  const list = document.getElementById('rutas-list');
  list.innerHTML = '';

  routes.forEach(r => {
    const div = document.createElement('div');
    div.className = 'route-card';
    div.innerHTML = `
      <div class="route-header">
        <div class="route-number" style="background:${r.active ? 'var(--accent)' : 'var(--muted)'}">
          ${r.num.replace('R-', '')}
        </div>
        <div class="route-info">
          <h3>${r.name}</h3>
          <p>${r.num} · ${r.active ? '● Activa' : '○ Inactiva'} · ${r.freq} de frecuencia</p>
        </div>
        <div style="margin-left:auto">
          <button class="btn btn-ghost"
                  style="font-size:11px;padding:6px 12px"
                  onclick="toggleRoute('${r.num}')">
            ${r.active ? 'Suspender' : 'Activar'}
          </button>
        </div>
      </div>
      <div class="route-stats">
        <div class="route-stat">
          <div class="route-stat-val">${r.stops}</div>
          <div class="route-stat-lbl">Paradas</div>
        </div>
        <div class="route-stat">
          <div class="route-stat-val">${r.buses}</div>
          <div class="route-stat-lbl">Buses</div>
        </div>
        <div class="route-stat">
          <div class="route-stat-val">${r.km}</div>
          <div class="route-stat-lbl">Km</div>
        </div>
        <div class="route-stat">
          <div class="route-stat-val">${r.freq}</div>
          <div class="route-stat-lbl">Frecuencia</div>
        </div>
      </div>
    `;
    list.appendChild(div);
  });
}

function toggleRoute(num) {
  const r = routes.find(x => x.num === num);
  if (r) {
    r.active = !r.active;
    renderRoutes();
  }
}

// ══════════════════════════════════════════
// RENDER — SENSORES
// ══════════════════════════════════════════
function renderSensors() {
  const grid = document.getElementById('sensor-grid');
  grid.innerHTML = '';

  sensors.forEach(s => {
    const statusColor = {
      online:  'var(--accent2)',
      alert:   'var(--warn)',
      offline: 'var(--danger)',
    }[s.status];

    const statusLabel = {
      online:  '● En línea',
      alert:   '⚠ Alerta',
      offline: '○ Fuera de línea',
    }[s.status];

    const div = document.createElement('div');
    div.className = 'sensor-card';
    div.innerHTML = `
      <div class="sensor-id">${s.id}</div>
      <div class="sensor-icon">📡</div>
      <div style="font-size:10px;color:var(--muted);margin-bottom:4px">${s.bus}</div>
      <div class="sensor-status" style="color:${statusColor}">${statusLabel}</div>
      <div class="sensor-count">${s.counts}</div>
      <div style="font-size:9px;color:var(--muted)">pasajeros</div>
    `;
    grid.appendChild(div);
  });

  // Feed de sensores
  const feed = document.getElementById('sensor-feed');
  feed.innerHTML = '';
  feedEvents.slice(0, 5).forEach(e => {
    const div = document.createElement('div');
    div.className = `feed-item ${e.type}`;
    div.innerHTML = `
      <span class="feed-icon">${e.icon}</span>
      <span class="feed-msg">${e.msg}</span>
      <span class="feed-time">${e.time}</span>
    `;
    feed.appendChild(div);
  });
}

// ══════════════════════════════════════════
// RENDER — ALERTAS
// ══════════════════════════════════════════
function renderAlerts() {
  const list = document.getElementById('alerts-list');
  list.innerHTML = '';

  if (alerts.length === 0) {
    list.innerHTML = `
      <div style="text-align:center;color:var(--muted);padding:40px;font-size:13px">
        ✅ No hay alertas activas
      </div>`;
    return;
  }

  alerts.forEach((a, i) => {
    const div = document.createElement('div');
    div.className = `alert-item ${a.type === 'warn' ? 'warn' : ''}`;
    div.innerHTML = `
      <span class="alert-icon">${a.icon}</span>
      <div class="alert-text">
        <strong>${a.title}</strong>
        <span>${a.desc}</span>
      </div>
      <span class="alert-time">${a.time}</span>
      <button class="btn btn-ghost"
              style="font-size:10px;padding:4px 10px;margin-left:8px"
              onclick="resolveAlert(${i})">
        Resolver
      </button>
    `;
    list.appendChild(div);
  });
}

function resolveAlert(i) {
  alerts.splice(i, 1);
  const badge = document.getElementById('alert-count');
  badge.textContent = alerts.length;
  if (alerts.length === 0) badge.style.display = 'none';
  renderAlerts();
}

function clearAlerts() {
  alerts.length = 0;
  document.getElementById('alert-count').style.display = 'none';
  renderAlerts();
}

// ══════════════════════════════════════════
// MODALES
// ══════════════════════════════════════════
function openModal(id) {
  document.getElementById(id).classList.add('open');
}

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

// Cerrar modal al hacer clic fuera
document.querySelectorAll('.modal-overlay').forEach(m => {
  m.addEventListener('click', e => {
    if (e.target === m) m.classList.remove('open');
  });
});

function addRoute() {
  const num   = document.getElementById('new-route-num').value.trim();
  const name  = document.getElementById('new-route-name').value.trim();
  const stops = parseInt(document.getElementById('new-route-stops').value) || 8;
  const buses = parseInt(document.getElementById('new-route-buses').value) || 1;

  if (!num || !name) {
    alert('Por favor completa los campos requeridos');
    return;
  }

  routes.push({
    num, name, stops, buses,
    km:   (stops * 1.5).toFixed(1),
    freq: '15 min',
    active: true,
  });

  closeModal('modal-ruta');
  renderRoutes();
}

function addSensor() {
  const id  = document.getElementById('new-sensor-id').value.trim();
  const bus = document.getElementById('new-sensor-bus').value;

  if (!id) {
    alert('Ingresa un ID para el sensor');
    return;
  }

  sensors.push({ id, bus, status: 'online', counts: 0 });
  closeModal('modal-sensor');
  renderSensors();
}

// ══════════════════════════════════════════
// SIMULACIÓN EN TIEMPO REAL
// ══════════════════════════════════════════
function simulateLiveData() {
  const busIdx = Math.floor(Math.random() * 7);
  const b = fleet[busIdx];
  if (!b || b.status === 'idle') return;

  const rand = Math.random();
  let newEvent;

  if (rand < 0.65) {
    // Entrada de pasajero
    b.pass = Math.min(b.pass + Math.floor(Math.random() * 3 + 1), b.cap);
    state.totalPassengers += 1;
    state.onboard = fleet.reduce((s, x) => s + x.pass, 0);
    newEvent = { type: 'entry', icon: '↑', msg: `<strong>${b.id}</strong> — Entrada detectada · ${b.stop}`, time: 'ahora' };

  } else if (rand < 0.85) {
    // Salida de pasajero
    b.pass = Math.max(b.pass - Math.floor(Math.random() * 4 + 1), 0);
    state.onboard = fleet.reduce((s, x) => s + x.pass, 0);
    newEvent = { type: 'exit', icon: '↓', msg: `<strong>${b.id}</strong> — Salida registrada · ${b.stop}`, time: 'ahora' };

  } else {
    // Evasión detectada
    b.evas += 1;
    state.evasions += 1;
    state.evasionValue += 2900;
    newEvent = { type: 'evasion', icon: '⛔', msg: `<strong>${b.id}</strong> — ⚠ Evasión detectada · Pérdida: $2.900`, time: 'ahora' };
  }

  // Actualizar timestamps del feed
  feedEvents.unshift(newEvent);
  if (feedEvents.length > 12) feedEvents.pop();
  feedEvents.forEach((e, i) => {
    if (i > 0) e.time = `hace ${i} min`;
  });

  // Sincronizar sensor correspondiente
  sensors[busIdx].counts = b.pass;

  // Re-renderizar todo
  renderStats();
  renderFleet();
  renderFeed();
  renderSensors();
}

// ══════════════════════════════════════════
// INICIALIZACIÓN
// ══════════════════════════════════════════
renderStats();
renderHourlyChart();
renderFeed();
renderFleet();
renderRoutes();
renderSensors();
renderAlerts();

// Simulación en vivo cada 2.5 segundos
setInterval(simulateLiveData, 2500);