// Simuler le changement de couleur RGB
const colorSlider      = document.getElementById('colorSlider');
const colorDisplay     = document.getElementById('colorDisplay');
const rValue           = document.getElementById('rValue');
const gValue           = document.getElementById('gValue');
const bValue           = document.getElementById('bValue');
const sendColorBtn     = document.getElementById('sendColorBtn');
const selectAllBtn     = document.getElementById('selectAllBtn');
const resetBtn         = document.getElementById('resetBtn');
const rgbErrorMessage  = document.getElementById('rgbErrorMessage');
const startBtn         = document.getElementById('startBtn');
const stopBtn          = document.getElementById('stopBtn');
const errElem          = document.getElementById('actionError');
const lastUpdateElement= document.getElementById('lastUpdate');
let currentAction = null;

const SERVER_IP = "http://192.168.137.202:5000";
console.log("JS actif, IP serveur :", SERVER_IP);


// Fonction pour mettre à jour la couleur affichée
function updateColor() {
    const red   = parseInt(rValue.value);
    const green = parseInt(gValue.value);
    const blue  = parseInt(bValue.value);
    colorDisplay.style.backgroundColor = `rgb(${red}, ${green}, ${blue})`;
}

// Définition des points de contrôle du dégradé
const stops = [
{ pos: 0/6, color: [255,   0,   0] }, // red
{ pos: 1/6, color: [255, 255,   0] }, // yellow
{ pos: 2/6, color: [  0, 255,   0] }, // lime
{ pos: 3/6, color: [  0, 255, 255] }, // cyan
{ pos: 4/6, color: [  0,   0, 255] }, // blue
{ pos: 5/6, color: [255,   0, 255] }, // magenta
{ pos: 6/6, color: [255,   0,   0] }  // red
];

// Interpolation linéaire entre deux composantes
function lerp(a, b, t) {
    return Math.round(a + (b - a) * t);
}

colorSlider.addEventListener('input', function() {
    const t = this.value / this.max;      // de 0 à 1
    // trouve le segment [i, i+1] tel que stops[i].pos ≤ t ≤ stops[i+1].pos
    let i = stops.findIndex((s, j) => t >= s.pos && t <= stops[j+1]?.pos);
    if (i === -1) i = stops.length - 2;    // garde le dernier segment par défaut

    const start = stops[i];
    const end   = stops[i+1];
    // paramètre local dans le segment
    const localT = (t - start.pos) / (end.pos - start.pos);

    // calcule RGB
    const r = lerp(start.color[0], end.color[0], localT);
    const g = lerp(start.color[1], end.color[1], localT);
    const b = lerp(start.color[2], end.color[2], localT);

    // mise à jour des inputs et de la couleur
    rValue.value = r;
    gValue.value = g;
    bValue.value = b;
    updateColor();
});


// Événements pour les champs de saisie RGB
[rValue, gValue, bValue].forEach(input => {
    input.addEventListener('input', function() {
        if (this.value === '')            this.value = 0;
        if (parseInt(this.value) < 0)     this.value = 0;
        if (parseInt(this.value) > 255)   this.value = 255;
        updateColor();
    });
});

// Simuler l'activation des boutons d'action
const actionButtons = document.querySelectorAll('.action-btn');
actionButtons.forEach(button => {
    button.addEventListener('click', () => {
        actionButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        currentAction = button.dataset.action; // 👈 nouvelle ligne importante
    });
});


// Simuler le compteur de dernière mise à jour
let seconds = 3;
let updateTimer;
function updateLastUpdateTime() {
    seconds++;
    if (seconds >= 60) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        lastUpdateElement.textContent = `${minutes}m ${remainingSeconds}s`;
    } else {
        lastUpdateElement.textContent = `Dernière mise à jour il y a ${seconds} secondes...`;

    }
}
updateTimer = setInterval(updateLastUpdateTime, 1000);

// Gestion des LEDs du robot
const robotLeds     = document.querySelectorAll('.robot-round:not(.robot-switch), .robot-square:not(.robot-switch)');
const robotSwitches = document.querySelectorAll('.robot-switch');

// Sélection/désélection des LEDs
robotLeds.forEach(led => {
    led.addEventListener('click', function() {
        this.classList.toggle('selected');
    });
});


// Interrupteurs noir/blanc
robotSwitches.forEach(switchBtn => {
    switchBtn.addEventListener('click', function() {
        if (this.style.backgroundColor === 'white' || this.style.backgroundColor === 'rgb(255, 255, 255)') {
            this.style.backgroundColor = '#000';
        } else {
            this.style.backgroundColor = 'white';
        }
    });
});

// Sélectionner toutes les LEDs
selectAllBtn.addEventListener('click', function() {
    robotLeds.forEach(led => led.classList.add('selected'));
});

// Réinitialiser la sélection des LEDs
resetBtn.addEventListener('click', function() {
    robotLeds.forEach(led => led.classList.remove('selected'));
});

// Vérifier si les valeurs RGB sont valides pour les LEDs RGB spéciales
function isValidRgbForSpecialLeds(r, g, b) {
    return (r === 0 || r === 255) &&
    (g === 0 || g === 255) &&
    (b === 0 || b === 255);
}

// Appliquer la couleur sélectionnée aux LEDs sélectionnées
sendColorBtn.addEventListener('click', function() {
    const red           = parseInt(rValue.value);
    const green         = parseInt(gValue.value);
    const blue          = parseInt(bValue.value);
    const selectedColor = `rgb(${red}, ${green}, ${blue})`;
    const selectedRgbLeds = document.querySelectorAll('.robot-round[data-led-type="rgb"].selected');

    if (selectedRgbLeds.length > 0 && !isValidRgbForSpecialLeds(red, green, blue)) {
        rgbErrorMessage.textContent =
        "Saisie incompatible avec la sélection. Utilisez uniquement 0 ou 255 pour R, G et B.";
        return;
    } else {
        rgbErrorMessage.textContent = "";
    }

    // Appliquer la couleur aux LEDs sélectionnées
    const selectedLeds = document.querySelectorAll('.robot-round.selected, .robot-square.selected');
    selectedLeds.forEach(led => {
        led.style.backgroundColor = selectedColor;
    });
});

// ----------------------------------------------------------------------------
// Déclarations nécessaires pour Start/Stop
// ----------------------------------------------------------------------------
let actionStarted = false;

// Affichage / masquage des erreurs
function showError(msg) {
    errElem.textContent = msg;
    errElem.classList.remove('hidden');
}
function clearError() {
    errElem.textContent = '';
    errElem.classList.add('hidden');
}

// ----------------------------------------------------------------------------
// Gestion du clic START
// ----------------------------------------------------------------------------
startBtn.addEventListener('click', () => {
    if (!currentAction) return;

    clearError();

    if (currentAction === "line") {
    console.log('Démarrage : Suivi de ligne');
    fetch(`${SERVER_IP}/start_line`, { method: 'POST' });
    actionStarted = true;
    return;
}

if (currentAction === "obstacle") {
    console.log('Démarrage : Évitement d\'obstacle');
    fetch(`${SERVER_IP}/start_obstacle`, { method: 'POST' });
    actionStarted = true;
    return;
}

if (currentAction === "labyrinthe") {
    console.log('Démarrage : Labyrinthe');
    fetch(`${SERVER_IP}/start_labyrinthe`, { method: 'POST' });
    actionStarted = true;
    return;
}

if (currentAction === "complet") {
    console.log('Démarrage : Mode Complet');
    fetch(`${SERVER_IP}/start_complet`, { method: 'POST' });
    actionStarted = true;
    return;
}

if (currentAction === "light") {
    console.log('Démarrage : Light Tracking');
    fetch(`${SERVER_IP}/start_light`, { method: 'POST' });
    actionStarted = true;
    return;
}

if (currentAction === "voice-control") {
    console.log('Démarrage : Contrôle vocal');
    fetch(`${SERVER_IP}/start_voice`, { method: 'POST' });
    actionStarted = true;
    return;
}

    // Autres actions ici...
    actionStarted = true;
    console.log(`Démarrage de l'action "${currentAction}"`);
});

// ----------------------------------------------------------------------------
// Gestion du clic STOP
// ----------------------------------------------------------------------------
stopBtn.addEventListener('click', () => {
    clearError();
    if (!currentAction) {
        showError("Veuillez lancer une action avant d'appuyer sur Stop.");
        return;
    }


    if (currentAction === "line") {
    console.log('Arrêt : Suivi de ligne');
    fetch(`${SERVER_IP}/stop_line`, { method: 'POST' });
}
if (currentAction === "obstacle") {
    console.log('Arrêt : Évitement d\'obstacle');
    fetch(`${SERVER_IP}/stop_obstacle`, { method: 'POST' });
}
if (currentAction === "labyrinthe") {
    console.log('Arrêt : Labyrinthe');
    fetch(`${SERVER_IP}/stop_labyrinthe`, { method: 'POST' });
}
if (currentAction === "complet") {
    console.log('Arrêt : Complet');
    fetch(`${SERVER_IP}/stop_complet`, { method: 'POST' });
}
if (currentAction === "light") {
    console.log('Arrêt : Light Tracking');
    fetch(`${SERVER_IP}/stop_light`, { method: 'POST' });
}
if (currentAction === "voice-control") {
    console.log('Arrêt : Contrôle vocal');
    fetch(`${SERVER_IP}/stop_voice`, { method: 'POST' });
}



    console.log("Arrêt de l'action :", currentAction);

    // autre action : arrêt standard
    if (!actionStarted) {
        showError("Veuillez lancer une action avant d'appuyer sur Stop.");
        return;
    }
    actionStarted = false;


    if (updateTimer) clearInterval(updateTimer);
    updateTimer = setInterval(updateLastUpdateTime, 1000);
});


// mouvement

const directionButtons = document.querySelectorAll('.direction-btn');
const speedSlider = document.getElementById('motorSpeed');
const wheelAngleElem = document.getElementById("wheelAngle");

directionButtons.forEach(button => {
    const direction = button.dataset.direction;

    button.addEventListener('mousedown', () => {
        const speed = parseInt(speedSlider.value);
        console.log('Direction pressée:', direction, 'Vitesse:', speed);
        fetch(`${SERVER_IP}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ direction: direction, speed: speed })
        })
       .then(response => response.json())
        .then(data => {
            console.log('Réponse serveur (start):', data);
            if (data.angle_roues !== undefined && wheelAngleElem) {
    wheelAngleElem.textContent = `${data.angle_roues}°`;
}

        })
        .catch(error => console.error('Erreur fetch:', error));
    });

    button.addEventListener('mouseup', () => {
        console.log('Arrêt du mouvement');
        fetch(`${SERVER_IP}/move`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ direction: 'center' })
        })
        .then(response => response.text())
        .then(data => console.log('Réponse serveur (stop):', data))
        .catch(error => console.error('Erreur fetch:', error));
    });

    
});

// --- Contrôle clavier directionnel avec effet visuel --- //

const pressedKeys = new Set();

document.addEventListener("keydown", (event) => {
    const key = event.key.toLowerCase();
    if (!["z", "q", "s", "d"].includes(key)) return;

    if (pressedKeys.has(key)) return;
    pressedKeys.add(key);
    updateMovementFromKeys();
});

document.addEventListener("keyup", (event) => {
    const key = event.key.toLowerCase();
    if (pressedKeys.has(key)) {
        pressedKeys.delete(key);
        updateMovementFromKeys();
    }
});

function updateMovementFromKeys() {
    if (pressedKeys.size === 0) {
        fetch(`${SERVER_IP}/move`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ direction: "center", speed: parseInt(speedSlider.value) })
        });
        return;
    }

    let direction = null;
    if (pressedKeys.has("z") && pressedKeys.has("q")) direction = "up_left";
    else if (pressedKeys.has("z") && pressedKeys.has("d")) direction = "up_right";
    else if (pressedKeys.has("z")) direction = "up";
    else if (pressedKeys.has("s")) direction = "down";
    else if (pressedKeys.has("q")) direction = "left";
    else if (pressedKeys.has("d")) direction = "right";

    if (direction) {
        fetch(`${SERVER_IP}/move`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ direction, speed: parseInt(speedSlider.value) })
        })
        .then(res => res.json())
        .then(data => {
            if (data.angle_roues !== undefined) {
                const wheelElem = document.getElementById("wheelAngle");
                if (wheelElem) wheelElem.textContent = `${data.angle_roues}°`;
            }
        })
        .catch(console.error);
    }
}

// -----------------------------------------------------------------------------
// Gestion des boutons de la tête avec incrément répété
// -----------------------------------------------------------------------------

let holdTimeout = null;
let holdInterval = null;

const headButtons = document.querySelectorAll('.head-btn');
const angleInfoElems = document.querySelectorAll('.angle-info span');
const angleHorizontalElem = angleInfoElems[3];
const angleVerticalElem = angleInfoElems[5];

headButtons.forEach(button => {
    const head = button.dataset.head;

    button.addEventListener('mousedown', () => {
        console.log('head pressée:', head);

        // Premier envoi immédiat
        fetch(`${SERVER_IP}/head`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ head: head })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Réponse serveur (start):', data);
            angleHorizontalElem.textContent = `${data.angle_horizontal}°`;
            angleVerticalElem.textContent = `${data.angle_vertical}°`;
        })
        .catch(error => console.error('Erreur fetch:', error));

        // Démarre un délai avant la répétition
        holdTimeout = setTimeout(() => {
            holdInterval = setInterval(() => {
                console.log('head répétée:', head);
                fetch(`${SERVER_IP}/head`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ head: head })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Réponse serveur (repeat):', data);
                    angleHorizontalElem.textContent = `${data.angle_horizontal}°`;
                    angleVerticalElem.textContent = `${data.angle_vertical}°`;
                })
                .catch(error => console.error('Erreur fetch:', error));
            }, 500); // Incrément toutes les 500 ms après le délai
        }, 600); // Délai avant de commencer la répétition
    });

    button.addEventListener('mouseup', () => {
        console.log('Arrêt de l’incrémentation');
        clearTimeout(holdTimeout);
        clearInterval(holdInterval);
        holdTimeout = null;
        holdInterval = null;
    });

    button.addEventListener('mouseleave', () => {
        clearTimeout(holdTimeout);
        clearInterval(holdInterval);
        holdTimeout = null;
        holdInterval = null;
    });
});

// --- Contrôle clavier pour la tête avec flèches et effet visuel --- //

const headKeyMap = {
    'arrowup': 'up',
    'arrowleft': 'left',
    'arrowdown': 'down',
    'arrowright': 'right',
    'enter': 'center'
};

function getHeadButton(direction) {
    return document.querySelector(`.head-btn[data-head="${direction}"]`);
}

document.addEventListener('keydown', function(event) {
    const key = event.key.toLowerCase();
    const direction = headKeyMap[key];
    if (!direction) return;

    const btn = getHeadButton(direction);
    if (btn?.classList.contains('active')) return; // éviter les doubles appels

    fetch(`${SERVER_IP}/head`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ head: direction })
    })
    .then(response => response.json())
    .then(data => {
        console.log(`Tête direction ${direction}`, data);
        angleHorizontalElem.textContent = `${data.angle_horizontal}°`;
        angleVerticalElem.textContent = `${data.angle_vertical}°`;
    })
    .catch(error => console.error('Erreur fetch head:', error));

    if (btn) btn.classList.add('active');
});

document.addEventListener('keyup', function(event) {
    const key = event.key.toLowerCase();
    const direction = headKeyMap[key];
    if (!direction) return;

    const btn = getHeadButton(direction);
    if (btn) btn.classList.remove('active');
});


// -----------------------------------------------------------------------------
// Couleur
// -----------------------------------------------------------------------------

sendColorBtn.addEventListener('click', function() {
    const red   = parseInt(rValue.value);
    const green = parseInt(gValue.value);
    const blue  = parseInt(bValue.value);

    const selectedElements = Array.from(document.querySelectorAll('.robot-round.selected, .robot-square.selected'));

    if (selectedElements.length === 0) {
        rgbErrorMessage.textContent = "Veuillez sélectionner au moins une LED.";
        return;
    }

    rgbErrorMessage.textContent = "";

    // Séparer LEDs normales et spéciales
    const normalLeds = [];
    const specialLeds = [];

    selectedElements.forEach(led => {
        const id = parseInt(led.dataset.ledId);
        if (id === 14 || id === 15) {
            specialLeds.push(id);
        } else {
            normalLeds.push(id);
        }
    });

    if (specialLeds.length > 0 && !isValidRgbForSpecialLeds(red, green, blue)) {
        rgbErrorMessage.textContent =
            "Saisie incompatible avec les LEDs spéciales. Utilisez uniquement 0 ou 255 pour R, G et B.";
        return;
    } else {
        rgbErrorMessage.textContent = "";
    }

    // LEDs normales : envoie sur /set_leds
    if (normalLeds.length > 0) {
        fetch(`${SERVER_IP}/set_leds`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                leds: normalLeds,
                color: { r: red, g: green, b: blue }
            })
        })
        .then(response => response.text())
        .then(data => console.log('Réponse serveur (normales):', data))
        .catch(error => console.error('Erreur fetch:', error));
    }

    // LEDs spéciales : envoie sur /set_front_leds
    if (specialLeds.length > 0) {
        setSpecialFrontLeds(red, green, blue, specialLeds);
    }
});

// Fonction qui envoie la requête pour les LEDs spéciales
function setSpecialFrontLeds(r, g, b, leds) {
    fetch(`${SERVER_IP}/set_front_leds`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            r: r,
            g: g,
            b: b,
            leds: leds
        })
    })
    .then(response => response.text())
    .then(data => console.log('Réponse serveur (spéciales):', data))
    .catch(error => console.error('Erreur fetch (spéciales):', error));
}

// Rafraîchissement temps réel des infos système

function updateSystemInfoUI(info) {
    const infoElements = document.querySelectorAll('.panel-content.space-y-4.text-sm > div');
    const keys = ["cpu_temp", "gpu_temp", "cpu_use", "ram_use", "battery"];

    keys.forEach((key, i) => {
        const valueSpan = infoElements[i].querySelector('span:last-child');
        const bar       = infoElements[i].querySelector('.status-indicator');

        if (valueSpan && bar) {
            const value = info[key] || "--";
            const unit = (key.includes("temp") ? "°C" : "%");
            valueSpan.textContent = value + unit;

            // Met à jour la largeur du bargraph
            const percentage = parseFloat(value) || 0;
            bar.style.width = percentage + "%";

            // Couleur selon le niveau
            if (percentage > 80) bar.style.backgroundColor = "#e94560"; // rouge
            else if (percentage > 60) bar.style.backgroundColor = "#f59e0b"; // orange
            else bar.style.backgroundColor = "#10b981"; // vert
        }
    });
}

function fetchSystemInfo() {
    fetch(`${SERVER_IP}/system_info`)
        .then(response => response.json())
        .then(data => updateSystemInfoUI(data))
        .catch(error => console.error("Erreur récupération infos système :", error));
}


// Gestion webcam ON/OFF par bouton unique
const webcamBtn = document.querySelector('button[data-action="webcam"]');
let webcamRunning = false;

webcamBtn.addEventListener('click', () => {
    const webcamImg = document.getElementById("webcamStream");
    const overlay = document.getElementById("webcamOverlay");
    const placeholder = document.getElementById("webcamPlaceholder");

if (!webcamRunning) {
    // Lancer webcam
    webcamImg.src = `${SERVER_IP}/video_feed`;
    webcamImg.classList.remove("hidden");
    overlay.classList.remove("hidden");
    placeholder.classList.add("hidden");
    lastUpdateElement.classList.add("hidden");

    webcamBtn.textContent = "OFF";
    webcamBtn.classList.remove("off");
    webcamBtn.classList.add("on");
    webcamRunning = true;
    seconds = 0;
} else {
    // Arrêter webcam
    webcamImg.src = `${SERVER_IP}/snapshot`;
    overlay.classList.add("hidden");
    placeholder.classList.add("hidden");
    lastUpdateElement.classList.remove("hidden");

    webcamBtn.textContent = "ON";
    webcamBtn.classList.remove("on");
    webcamBtn.classList.add("off");
    webcamRunning = false;
    seconds = 0;
}

});


let isScanning = false;
const toggleScanBtn = document.getElementById("toggle-scan-btn");
const radarPlotDiv = document.getElementById("radar-plot");
let scanInterval;

toggleScanBtn.addEventListener("click", () => {
  isScanning = !isScanning;

if (isScanning) {
    toggleScanBtn.textContent = "OFF";
    toggleScanBtn.classList.remove("off");
    toggleScanBtn.classList.add("on");
    startScanLoop();
} else {
    toggleScanBtn.textContent = "ON";
    toggleScanBtn.classList.remove("on");
    toggleScanBtn.classList.add("off");
    stopScanLoop();
}
});

function startScanLoop() {
  fetchAndPlotScan(); // premier affichage
  scanInterval = setInterval(fetchAndPlotScan, 2000); // toutes les 2s
}

function stopScanLoop() {
  clearInterval(scanInterval);
  Plotly.purge('radar-plot');

  const scanText = document.getElementById('scan-off-text');
  scanText.style.removeProperty("display"); // Enlève tout style inline qui cache
  scanText.style.display = 'flex';          // Forcer affichage
  scanText.textContent = 'Scanner OFF';        // Remet le texte
}



function fetchAndPlotScan() {
      document.getElementById('scan-off-text').style.display = 'none';


  fetch(`${SERVER_IP}/scan`)
    .then(resp => resp.json())
    .then(data => {
      const trace = {
        type: 'scatterpolar',
        r: data.rs,
        theta: data.thetas,
        mode: 'markers',
        marker: { color: 'red', size: 8 }
      };
      const layout = {
        polar: {
          radialaxis: { range: [0, 50], showgrid: true },
          angularaxis: { direction: "clockwise", rotation: 90 }
        },
        showlegend: false,
        margin: { t: 20, b: 20, l: 20, r: 20 }
      };
      Plotly.newPlot(radarPlotDiv, [trace], layout, { responsive: true });
    })
    .catch(err => console.error("Erreur scan :", err));
}


// Appel toutes les 5 secondes
setInterval(fetchSystemInfo, 5000);
fetchSystemInfo(); // appel initial

const webControlStopBtn  = document.getElementById("webControlStopBtn");

webControlStopBtn.addEventListener("click", () => {
    fetch(`${SERVER_IP}/stop_web_control`, { method: "POST" })
        .then(() => console.log("web_control.py arrêté"))
        .catch(err => console.error("Erreur arrêt Web Control :", err));
});




