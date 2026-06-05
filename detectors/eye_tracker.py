class EyeTracker:

    def get_gaze(

        self,

        frame,

        landmarks
    ):

        # SIMPLE DEMO VERSION

        left_eye = (
            landmarks.landmark[33]
        )

        right_eye = (
            landmarks.landmark[263]
        )

        nose = (
            landmarks.landmark[1]
        )

        # LOOK LEFT

        if nose.x < left_eye.x:

            return 'LEFT'

        # LOOK RIGHT

        if nose.x > right_eye.x:

            return 'RIGHT'

        # LOOK DOWN

        if nose.y > 0.55:

            return 'DOWN'

        return 'CENTER'