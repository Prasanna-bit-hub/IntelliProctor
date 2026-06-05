import os
import cv2
from datetime import datetime

from database.database import (
    get_connection
)


class AlertService:

    def __init__(self, socketio):

        self.socketio = socketio

        os.makedirs(
            'snapshots',
            exist_ok=True
        )

    def save_alert(
        self,
        frame,
        alert_type,
        severity
    ):

        timestamp = datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        filename = datetime.now().strftime(
            '%Y%m%d_%H%M%S.jpg'
        )

        snapshot_path = (
            f'snapshots/{filename}'
        )

        # SAVE IMAGE

        cv2.imwrite(
            snapshot_path,
            frame
        )

        # SAVE DATABASE

        conn = get_connection()

        conn.execute("""

            INSERT INTO alerts (

                timestamp,
                alert_type,
                severity,
                snapshot_path

            )

            VALUES (?, ?, ?, ?)

        """, (

            timestamp,
            alert_type,
            severity,
            snapshot_path

        ))

        conn.commit()

        conn.close()

        # EMIT LIVE EVENT

        self.socketio.emit(

            'new_alert',

            {
                'timestamp': timestamp,

                'alert_type': alert_type,

                'severity': severity,

                'snapshot_path': snapshot_path
            }
        )