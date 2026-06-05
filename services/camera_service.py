import cv2
import threading
import time

from detectors.face_detector import FaceDetector
from detectors.eye_tracker import EyeTracker
from detectors.head_pose import HeadPoseEstimator
from detectors.person_detector import PersonDetector
from detectors.cheating_detector import CheatingDetector
from detectors.lip_detector import LipDetector


class CameraService:

    def __init__(

        self,

        alert_service,

        audio_service
    ):

        # CAMERA

        self.capture = cv2.VideoCapture(0)

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            640
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            480
        )

        self.capture.set(
            cv2.CAP_PROP_FPS,
            30
        )

        # SERVICES

        self.alert_service = (
            alert_service
        )

        self.audio_service = (
            audio_service
        )

        # DETECTORS

        self.face_detector = (
            FaceDetector()
        )

        self.eye_tracker = (
            EyeTracker()
        )

        self.head_pose = (
            HeadPoseEstimator()
        )

        self.person_detector = (
            PersonDetector()
        )

        self.cheating_detector = (
            CheatingDetector()
        )

        self.lip_detector = (
            LipDetector()
        )

        # STATES

        self.running = False

        self.frame = None

        self.last_alert_time = 0

    # =====================================
    # START CAMERA
    # =====================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.capture = cv2.VideoCapture(0)

        threading.Thread(

            target=self.update_frames,

            daemon=True

        ).start()

        print("CAMERA STARTED")

        # AUDIO START

        if hasattr(
            self.audio_service,
            'start'
        ):

            self.audio_service.start()

    # =====================================
    # STOP CAMERA
    # =====================================

    def stop(self):

        self.running = False

        if hasattr(
            self.audio_service,
            'stop'
        ):

            self.audio_service.stop()

        self.capture.release()

        print("CAMERA STOPPED")

    # =====================================
    # UPDATE FRAMES
    # =====================================

    def update_frames(self):

        while self.running:

            try:

                success, frame = (
                    self.capture.read()
                )

                if not success:

                    print(
                        "FRAME READ FAILED"
                    )

                    time.sleep(1)

                    continue

                # MIRROR CAMERA

                frame = cv2.flip(
                    frame,
                    1
                )

                # DEFAULT VALUES

                face_count = 0

                gaze = 'CENTER'

                yaw = 0

                pitch = 0

                talking = False

                persons = 0

                phones = 0

                audio_detected = False

                faces = []

                # =====================================
                # FACE DETECTION
                # =====================================

                try:

                    faces = (
                        self.face_detector.detect(
                            frame
                        )
                    )

                    face_count = len(faces)

                except Exception as e:

                    print(
                        "FACE ERROR:",
                        e
                    )

                # =====================================
                # DRAW FACE LANDMARKS
                # =====================================

                try:

                    for face_landmarks in faces:

                        h, w, _ = frame.shape

                        for landmark in face_landmarks.landmark:

                            x = int(
                                landmark.x * w
                            )

                            y = int(
                                landmark.y * h
                            )

                            cv2.circle(

                                frame,

                                (x, y),

                                1,

                                (0, 255, 0),

                                -1
                            )

                except Exception as e:

                    print(
                        "LANDMARK ERROR:",
                        e
                    )

                # =====================================
                # PERSON + PHONE DETECTION
                # =====================================

                try:

                    detections = (
                        self.person_detector.detect(
                            frame
                        )
                    )

                    persons = (
                        detections['persons']
                    )

                    phones = (
                        detections['phones']
                    )

                except Exception as e:

                    print(
                        "YOLO ERROR:",
                        e
                    )

                # =====================================
                # FACE ANALYSIS
                # =====================================

                if face_count > 0:

                    landmarks = faces[0]

                    # GAZE

                    try:

                        gaze = (
                            self.eye_tracker.get_gaze(

                                frame,

                                landmarks
                            )
                        )

                    except Exception as e:

                        print(
                            "GAZE ERROR:",
                            e
                        )

                    # HEAD POSE

                    try:

                        yaw, pitch, roll = (

                            self.head_pose.get_pose(

                                frame,

                                landmarks
                            )
                        )

                    except Exception as e:

                        print(
                            "POSE ERROR:",
                            e
                        )

                    # LIP MOVEMENT

                    try:

                        talking = (

                            self.lip_detector.detect_talking(

                                landmarks
                            )
                        )

                    except Exception as e:

                        print(
                            "LIP ERROR:",
                            e
                        )

                # =====================================
                # AUDIO DETECTION
                # =====================================

                try:

                    if hasattr(
                        self.audio_service,
                        'detected'
                    ):

                        audio_detected = (
                            self.audio_service.detected
                        )

                except Exception as e:

                    print(
                        "AUDIO ERROR:",
                        e
                    )

                # =====================================
                # CHEATING ANALYSIS
                # =====================================

                try:

                    alerts = (

                        self.cheating_detector.analyze(

                            face_count,

                            gaze,

                            yaw,

                            pitch,

                            persons,

                            phones,

                            audio_detected,

                            talking
                        )
                    )

                except Exception as e:

                    print(
                        "ANALYSIS ERROR:",
                        e
                    )

                    alerts = []

                # =====================================
                # DRAW STATS
                # =====================================

                cv2.putText(

                    frame,

                    f'Faces: {face_count}',

                    (20, 40),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 255, 0),

                    2
                )

                cv2.putText(

                    frame,

                    f'Persons: {persons}',

                    (20, 80),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (255, 255, 0),

                    2
                )

                cv2.putText(

                    frame,

                    f'Phones: {phones}',

                    (20, 120),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 0, 255),

                    2
                )

                cv2.putText(

                    frame,

                    f'Gaze: {gaze}',

                    (20, 160),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (255, 0, 255),

                    2
                )

                cv2.putText(

                    frame,

                    f'Talking: {talking}',

                    (20, 200),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.8,

                    (0, 255, 255),

                    2
                )

                # =====================================
                # ALERTS
                # =====================================

                current_time = time.time()

                for i, alert in enumerate(alerts):

                    cv2.putText(

                        frame,

                        alert['type'],

                        (20, 260 + (i * 40)),

                        cv2.FONT_HERSHEY_SIMPLEX,

                        0.9,

                        (0, 0, 255),

                        3
                    )

                    # PREVENT SPAM

                    if (
                        current_time -
                        self.last_alert_time
                    ) > 3:

                        self.alert_service.save_alert(

                            frame,

                            alert['type'],

                            alert['severity']
                        )

                        self.last_alert_time = (
                            current_time
                        )

                # FINAL FRAME

                self.frame = frame

                time.sleep(0.03)

            except Exception as e:

                print(
                    "CAMERA ERROR:",
                    e
                )

                time.sleep(1)

    # =====================================
    # GET FRAME
    # =====================================

    def get_frame(self):

        return self.frame