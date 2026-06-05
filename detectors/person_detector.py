from ultralytics import YOLO

from config import YOLO_MODEL_PATH

import cv2


class PersonDetector:

    def __init__(self):

        self.model = YOLO(
            YOLO_MODEL_PATH
        )

    def detect(self, frame):

        # SMALLER FRAME = FASTER AI

        small_frame = cv2.resize(
            frame,
            (320, 240)
        )

        results = self.model(

            small_frame,

            verbose=False,

            conf=0.5

        )

        persons = 0

        phones = 0

        for result in results:

            boxes = result.boxes

            for box in boxes:

                cls = int(
                    box.cls[0]
                )

                # PERSON

                if cls == 0:

                    persons += 1

                # PHONE

                if cls == 67:

                    phones += 1

        return {

            'persons': persons,

            'phones': phones
        }