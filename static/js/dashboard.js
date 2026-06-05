const socket = io();

const alertsList =
    document.getElementById(
        'alertsList'
    );

const totalAlerts =
    document.getElementById(
        'totalAlerts'
    );

const highAlerts =
    document.getElementById(
        'highAlerts'
    );

const integrityScore =
    document.getElementById(
        'integrityScore'
    );

const sessionStatus =
    document.getElementById(
        'sessionStatus'
    );


// START BUTTON

document.getElementById(
    'startBtn'
).onclick = async () => {

    await fetch('/start', {
        method:'POST'
    });
};


// STOP BUTTON

document.getElementById(
    'stopBtn'
).onclick = async () => {

    await fetch('/stop', {
        method:'POST'
    });
};

// RESET ALERTS

document.getElementById(
    'resetBtn'
).onclick = async () => {

    await fetch('/reset_alerts', {

        method:'POST'
    });

    // RESET UI

    alertsList.innerHTML = '';

    totalAlerts.innerText = 0;

    highAlerts.innerText = 0;

    integrityScore.innerText = 100;

    sessionStatus.innerText = 'CLEAN';
};


// LOAD EXISTING ALERTS

async function loadAlerts(){

    const response =
        await fetch('/alerts');

    const alerts =
        await response.json();

    alertsList.innerHTML = '';

    let total = 0;
    let high = 0;
    let score = 100;

    alerts.forEach(alert => {

        total++;

        if(alert.severity === 'HIGH'){
            high++;
            score -= 10;
        }

        if(alert.severity === 'MEDIUM'){
            score -= 5;
        }

        if(alert.severity === 'LOW'){
            score -= 2;
        }

        addAlert(alert);

    });

    if(score < 0){
        score = 0;
    }

    totalAlerts.innerText = total;

    highAlerts.innerText = high;

    integrityScore.innerText = score;

    if(score >= 90){

        sessionStatus.innerText =
            'CLEAN';

    }else if(score >= 70){

        sessionStatus.innerText =
            'REVIEW';

    }else{

        sessionStatus.innerText =
            'FLAGGED';
    }
}


// ADD ALERT CARD

function addAlert(alert){

    const div =
        document.createElement('div');

    div.className =
        'alert-item';

    div.innerHTML = `

        <div class="alert-left">

            <div class="alert-type">
                ${alert.alert_type}
            </div>

            <div class="alert-time">
                ${alert.timestamp}
            </div>

        </div>

        <div class="severity ${alert.severity}">
            ${alert.severity}
        </div>

    `;

    alertsList.prepend(div);
}


// LIVE ALERTS

socket.on('new_alert', function(data){

    addAlert(data);

    totalAlerts.innerText =
        parseInt(totalAlerts.innerText) + 1;

    if(data.severity === 'HIGH'){

        highAlerts.innerText =
            parseInt(highAlerts.innerText) + 1;
    }

    let score =
        parseInt(
            integrityScore.innerText
        );

    if(data.severity === 'HIGH'){
        score -= 10;
    }

    if(data.severity === 'MEDIUM'){
        score -= 5;
    }

    if(data.severity === 'LOW'){
        score -= 2;
    }

    if(score < 0){
        score = 0;
    }

    integrityScore.innerText =
        score;

    if(score >= 90){

        sessionStatus.innerText =
            'CLEAN';

    }else if(score >= 70){

        sessionStatus.innerText =
            'REVIEW';

    }else{

        sessionStatus.innerText =
            'FLAGGED';
    }
});

loadAlerts();