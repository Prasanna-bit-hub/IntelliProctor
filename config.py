import os

YOLO_MODEL_PATH = "yolov8n.pt"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_PATH = os.path.join(BASE_DIR, 'intelliproctor.db')

SNAPSHOT_DIR = os.path.join(BASE_DIR, 'snapshots')

LOG_DIR = os.path.join(BASE_DIR, 'logs')

MODEL_PATH = os.path.join(BASE_DIR, 'models', 'yolov8n.pt')

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 30

AUDIO_THRESHOLD = 0.04

NO_FACE_SECONDS = 3
LOOK_AWAY_SECONDS = 2

SECRET_KEY = 'intelliproctor-secret'