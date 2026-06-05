
from flask import (
    Flask,
    render_template,
    jsonify,
    Response,
    send_file,
    request
)

from flask_socketio import SocketIO

from database.database import (
    initialize_database,
    get_connection
)

from services.alert_service import AlertService
from services.audio_service import AudioService
from services.camera_service import CameraService
from services.report_service import ReportService
from services.pdf_service import PDFService

import cv2


# =====================================
# FLASK APP
# =====================================

app = Flask(__name__)

app.config['SECRET_KEY'] = 'intelliproctor'


# =====================================
# SOCKET IO
# =====================================

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading'
)


# =====================================
# DATABASE
# =====================================

initialize_database()


# =====================================
# SERVICES
# =====================================

alert_service = AlertService(
    socketio
)

audio_service = AudioService()

camera_service = CameraService(
    alert_service,
    audio_service
)

report_service = ReportService()

pdf_service = PDFService()


# =====================================
# HOME PAGE
# =====================================

@app.route('/')
def index():

    return render_template(
        'index.html'
    )


# =====================================
# ADMIN PAGE
# =====================================

@app.route('/admin')
def admin():

    return render_template(
        'admin_dashboard.html'
    )


# =====================================
# ALERT PAGE
# =====================================

@app.route('/alerts_page')
def alerts_page():

    return render_template(
        'alerts.html'
    )

# =====================================
# RESET ALERTS
# =====================================

@app.route('/reset_alerts', methods=['POST'])
def reset_alerts():

    conn = get_connection()

    conn.execute(
        'DELETE FROM alerts'
    )

    conn.commit()

    conn.close()

    return jsonify({
        'status': 'alerts reset'
    })

# =====================================
# REPORT PAGE
# =====================================

@app.route('/report')
def report():

    report_data = (
        report_service.generate_report()
    )

    return render_template(
        'report.html',
        report=report_data
    )


# =====================================
# START MONITORING
# =====================================

@app.route('/start', methods=['POST'])
def start_monitoring():

    if not camera_service.running:

        camera_service.start()

    return jsonify({
        'status': 'started'
    })


# =====================================
# STOP MONITORING
# =====================================

@app.route('/stop', methods=['POST'])
def stop_monitoring():

    camera_service.stop()

    return jsonify({
        'status': 'stopped'
    })

# FULLSCREEN ALERT

@app.route(
    '/fullscreen_alert',
    methods=['POST']
)
def fullscreen_alert():

    frame = (
        camera_service.get_frame()
    )

    if frame is not None:

        alert_service.save_alert(

            frame,

            'EXITED FULLSCREEN',

            'HIGH'
        )

    return jsonify({

        'status':'alert added'
    })

# =====================================
# TAB SWITCH DETECTION
# =====================================

@app.route('/tab_switch', methods=['POST'])
def tab_switch():

    frame = camera_service.get_frame()

    if frame is not None:

        alert_service.save_alert(

            frame,

            "TAB SWITCH DETECTED",

            "HIGH"
        )

    return jsonify({
        'status': 'success'
    })


# =====================================
# ALERT API
# =====================================

@app.route('/alerts')
def alerts():

    conn = get_connection()

    rows = conn.execute(
        '''
        SELECT *
        FROM alerts
        ORDER BY id DESC
        '''
    ).fetchall()

    conn.close()

    result = []

    for row in rows:

        result.append({

            'id': row['id'],

            'timestamp': row['timestamp'],

            'alert_type': row['alert_type'],

            'severity': row['severity'],

            'snapshot_path': row['snapshot_path']
        })

    return jsonify(result)


# =====================================
# VIDEO STREAM
# =====================================

def generate_frames():

    while True:

        frame = (
            camera_service.get_frame()
        )

        if frame is None:

            continue

        success, buffer = cv2.imencode(
            '.jpg',
            frame,
            [cv2.IMWRITE_JPEG_QUALITY, 90]
        )

        if not success:

            continue

        frame_bytes = buffer.tobytes()

        yield (

            b'--frame\r\n'

            b'Content-Type: image/jpeg\r\n\r\n'

            + frame_bytes +

            b'\r\n'
        )


@app.route('/video_feed')
def video_feed():

    return Response(
        generate_frames(),
        mimetype=(
            'multipart/x-mixed-replace; boundary=frame'
        )
    )


# =====================================
# PDF EXPORT
# =====================================

@app.route('/download_report')
def download_report():

    pdf_path = (
        pdf_service.generate_report()
    )

    return send_file(
        pdf_path,
        as_attachment=True
    )


# =====================================
# MAIN
# =====================================

if __name__ == '__main__':

    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=False
    )