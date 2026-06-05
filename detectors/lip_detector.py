import math


class LipDetector:

    def get_distance(self, p1, p2):

        return math.sqrt(

            (p2.x - p1.x) ** 2 +

            (p2.y - p1.y) ** 2
        )

    def detect_talking(

        self,

        landmarks
    ):

        try:

            upper_lip = (
                landmarks.landmark[13]
            )

            lower_lip = (
                landmarks.landmark[14]
            )

            mouth_distance = (
                self.get_distance(
                    upper_lip,
                    lower_lip
                )
            )

            if mouth_distance > 0.02:

                return True

            return False

        except Exception as e:

            print(
                "LIP DETECTOR ERROR:",
                e
            )

            return False