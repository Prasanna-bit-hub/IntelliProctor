class HeadPoseEstimator:

    def get_pose(

        self,

        frame,

        landmarks
    ):

        # IMPORTANT FACE POINTS

        nose = (
            landmarks.landmark[1]
        )

        left_face = (
            landmarks.landmark[234]
        )

        right_face = (
            landmarks.landmark[454]
        )

        forehead = (
            landmarks.landmark[10]
        )

        chin = (
            landmarks.landmark[152]
        )

        # =====================================
        # YAW (LEFT / RIGHT TURN)
        # =====================================

        left_distance = abs(
            nose.x - left_face.x
        )

        right_distance = abs(
            right_face.x - nose.x
        )

        yaw = (
            (left_distance - right_distance)
            * 300
        )

        # =====================================
        # PITCH (UP / DOWN)
        # =====================================

        pitch = (
            (chin.y - forehead.y)
            * 100
        )

        # =====================================
        # ROLL
        # =====================================

        roll = 0

        return yaw, pitch, roll