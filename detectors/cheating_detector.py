class CheatingDetector:

    def analyze(

        self,

        face_count,

        gaze,

        yaw,

        pitch,

        persons,

        phones,

        audio_detected,

        talking=False
    ):

        alerts = []

        # =====================================
        # NO FACE
        # =====================================

        if face_count == 0:

            alerts.append({

                'type': 'NO FACE',

                'severity': 'HIGH'
            })

        # =====================================
        # MULTIPLE PERSONS
        # =====================================

        if persons > 1:

            alerts.append({

                'type': 'MULTIPLE PERSONS',

                'severity': 'HIGH'
            })

        # =====================================
        # PHONE DETECTION
        # =====================================

        if phones > 0:

            alerts.append({

                'type': 'MOBILE PHONE DETECTED',

                'severity': 'HIGH'
            })

        # =====================================
        # EYE GAZE
        # =====================================

        if gaze in ['LEFT', 'RIGHT']:

            alerts.append({

                'type': 'LOOKING AWAY',

                'severity': 'MEDIUM'
            })

        if gaze == 'DOWN':

            alerts.append({

                'type': 'LOOKING DOWN',

                'severity': 'MEDIUM'
            })

        # =====================================
        # HEAD TURN DETECTION
        # =====================================

        if yaw > 15:

            alerts.append({

                'type': 'HEAD TURN RIGHT',

                'severity': 'MEDIUM'
            })

        if yaw < -15:

            alerts.append({

                'type': 'HEAD TURN LEFT',

                'severity': 'MEDIUM'
            })

        # =====================================
        # HEAD DOWN
        # =====================================

        if pitch > 35:

            alerts.append({

                'type': 'HEAD DOWN',

                'severity': 'MEDIUM'
            })

        # =====================================
        # TALKING DETECTION
        # =====================================

        if talking:

            alerts.append({

                'type': 'TALKING DETECTED',

                'severity': 'LOW'
            })

        # =====================================
        # AUDIO DETECTION
        # =====================================

        if audio_detected:

            alerts.append({

                'type': 'SUSPICIOUS AUDIO',

                'severity': 'LOW'
            })

        return alerts