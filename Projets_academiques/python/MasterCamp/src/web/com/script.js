// Adresse de ton robot / serveur Flask
const serverIP   = '192.168.1.42';
const serverPort = '5000';
const baseURL    = `http://${serverIP}:${serverPort}`;
const mjpegURL   = `${baseURL}/camera`;
const stopURL    = `${baseURL}/stop_program`;

// variables de sélection
let selectedRow   = null;
let selectedColor = null;
let rowValue      = null;
let colorValue    = null;
let running       = false;
let logTimer      = null;

// références DOM
const actionBtn         = document.getElementById('actionBtn');
const stopBtn           = document.getElementById('stopProgramBtn');
const infoBox           = document.getElementById('selectionInfo');
const cameraPlaceholder = document.getElementById('cameraPlaceholder');
const cameraStream      = document.getElementById('cameraStream');
const cameraStatus      = document.getElementById('cameraStatus');
const rangebtns         = document.querySelectorAll('.rangebtn');
const boxbtns           = document.querySelectorAll('.boxbtn');
const terminalOutput    = document.getElementById('terminalOutput');

// active/désactive le bouton Chercher
function updateActionBtn() {
  actionBtn.disabled = !(selectedRow && selectedColor) && !running;
}

// met à jour la div “Sélection actuelle”
function updateInfoBox() {
  infoBox.innerHTML = `
    Sélection actuelle :<br/>
    <strong>Rangée :</strong> ${rowValue || '—'} &nbsp;&nbsp;
    <strong>Couleur :</strong> ${colorValue || '—'}
  `;
}

// Démarrer le polling des logs
function startLogPolling() {
  terminalOutput.textContent = '';
  logTimer = setInterval(() => {
    fetch(`${baseURL}/get_logs`)
      .then(res => res.json())
      .then(lines => {
        terminalOutput.textContent = lines.join('\n');
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
      })
      .catch(() => {});
  }, 500);
}

// Arrêter le polling des logs
function stopLogPolling() {
  if (logTimer) {
    clearInterval(logTimer);
    logTimer = null;
  }
}

// choix de rangée (bloqué si running)
rangebtns.forEach(btn => btn.addEventListener('click', () => {
  if (running) return;
  rangebtns.forEach(b => b.classList.remove('selected-row'));
  btn.classList.add('selected-row');
  selectedRow = btn.dataset.value;
  updateActionBtn();
}));

// choix de couleur (bloqué si running)
boxbtns.forEach(btn => btn.addEventListener('click', () => {
  if (running) return;
  boxbtns.forEach(b => b.classList.remove('selected-box'));
  btn.classList.add('selected-box');
  selectedColor = btn.dataset.value;
  updateActionBtn();
}));

// clic sur Chercher / Arrêter
actionBtn.addEventListener('click', () => {
  if (!running) {
    // --- DÉMARRAGE ---
    running    = true;
    rowValue   = selectedRow;
    colorValue = selectedColor;

    // 1) Envoi des valeurs au robot
    fetch(`${baseURL}/set_search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ row: rowValue, color: colorValue })
    })
    .then(res => res.json())
    .then(json => console.log('Search config envoyée:', json))
    .catch(err => console.error('Erreur envoi set_search:', err));

    // 2) Lancement du flux MJPEG
    cameraStream.src = mjpegURL;
    cameraStream.classList.remove('hidden');
    cameraPlaceholder.classList.add('hidden');
    cameraStatus.classList.remove('hidden');

    // 3) Démarrer le polling des logs
    startLogPolling();

    // 4) Affichage des infos et bascule du bouton
    updateInfoBox();
    infoBox.classList.remove('hidden');
    actionBtn.textContent = 'Arrêter';
    actionBtn.classList.replace('bg-green-300','bg-red-600');
    actionBtn.classList.replace('hover:bg-green-400','hover:bg-red-700');
    actionBtn.disabled = false;
  } else {
    // --- ARRÊT ---
    stopProgram();
  }
});

// fonction d’arrêt
function stopProgram() {
  running = false;

  // coupe le flux MJPEG
  cameraStream.src = '';
  cameraStream.classList.add('hidden');
  cameraStatus.classList.add('hidden');
  cameraPlaceholder.classList.remove('hidden');

  // arrêter le polling des logs
  stopLogPolling();

  // cacher infos & réinit sélections
  infoBox.classList.add('hidden');
  rangebtns.forEach(b => b.classList.remove('selected-row'));
  boxbtns.forEach(b => b.classList.remove('selected-box'));
  selectedRow   = null;
  selectedColor = null;
  rowValue      = null;
  colorValue    = null;

  // remettre le bouton en mode Chercher
  actionBtn.textContent = 'Chercher';
  actionBtn.classList.replace('bg-red-600','bg-green-300');
  actionBtn.classList.replace('hover:bg-red-700','hover:bg-green-400');
  updateActionBtn();
}

// bouton fixe “Arrêter le programme”
stopBtn.addEventListener('click', () => {
  if (running) {
    // appeler l’endpoint stop_program
    fetch(stopURL, { method: 'POST' })
      .then(res => res.json())
      .then(json => console.log('Programme stoppé:', json))
      .catch(err => console.error('Erreur stop_program:', err));
    stopProgram();
  }
});

// initialisation
updateActionBtn();
