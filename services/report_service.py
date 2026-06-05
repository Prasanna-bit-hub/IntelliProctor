from database.database import (
    get_connection
)


class ReportService:

    def generate_report(self):

        conn = get_connection()

        alerts = conn.execute(
            '''
            SELECT *
            FROM alerts
            '''
        ).fetchall()

        conn.close()

        total_alerts = len(alerts)

        high = 0

        medium = 0

        low = 0

        breakdown = {}

        # COUNT ALERTS

        for alert in alerts:

            severity = alert['severity']

            alert_type = alert['alert_type']

            # SEVERITY COUNT

            if severity == 'HIGH':

                high += 1

            elif severity == 'MEDIUM':

                medium += 1

            elif severity == 'LOW':

                low += 1

            # ALERT BREAKDOWN

            if alert_type not in breakdown:

                breakdown[alert_type] = 0

            breakdown[alert_type] += 1

        # INTEGRITY SCORE

        integrity_score = max(
            0,
            100 - (
                high * 10 +
                medium * 5 +
                low * 2
            )
        )

        # STATUS

        if integrity_score >= 90:

            status = 'CLEAN'

        elif integrity_score >= 70:

            status = 'REVIEW'

        else:

            status = 'FLAGGED'

        return {

            'total_alerts': total_alerts,

            'integrity_score': integrity_score,

            'status': status,

            'breakdown': breakdown
        }