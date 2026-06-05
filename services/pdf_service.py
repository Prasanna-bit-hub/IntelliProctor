from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

from database.database import (
    get_connection
)

import os


class PDFService:

    def generate_report(self):

        os.makedirs(
            'reports',
            exist_ok=True
        )

        file_path = (
            'reports/intelliproctor_report.pdf'
        )

        doc = SimpleDocTemplate(
            file_path,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elements = []

        # TITLE

        title = Paragraph(
            "INTELLIPROCTOR AI REPORT",
            styles['Title']
        )

        elements.append(title)

        elements.append(
            Spacer(1, 20)
        )

        # DATABASE

        conn = get_connection()

        alerts = conn.execute(
            '''
            SELECT *
            FROM alerts
            ORDER BY id DESC
            '''
        ).fetchall()

        conn.close()

        # STATS

        total_alerts = len(alerts)

        integrity_score = max(
            0,
            100 - (total_alerts * 5)
        )

        status = (
            "CLEAN"
            if integrity_score >= 90
            else "FLAGGED"
        )

        stats_data = [

            ['Metric', 'Value'],

            ['Total Alerts', str(total_alerts)],

            ['Integrity Score', str(integrity_score)],

            ['Status', status]

        ]

        stats_table = Table(
            stats_data,
            colWidths=[250, 250]
        )

        stats_table.setStyle(

            TableStyle([

                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.grey
                ),

                (
                    'TEXTCOLOR',
                    (0, 0),
                    (-1, 0),
                    colors.whitesmoke
                ),

                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    'FONTNAME',
                    (0, 0),
                    (-1, 0),
                    'Helvetica-Bold'
                )

            ])
        )

        elements.append(stats_table)

        elements.append(
            Spacer(1, 30)
        )

        # ALERT TABLE

        alert_title = Paragraph(
            "Alert History",
            styles['Heading2']
        )

        elements.append(alert_title)

        elements.append(
            Spacer(1, 10)
        )

        alert_data = [[

            'Time',
            'Alert',
            'Severity'

        ]]

        for alert in alerts:

            alert_data.append([

                alert['timestamp'],

                alert['alert_type'],

                alert['severity']

            ])

        alert_table = Table(
            alert_data,
            colWidths=[180, 250, 100]
        )

        alert_table.setStyle(

            TableStyle([

                (
                    'BACKGROUND',
                    (0, 0),
                    (-1, 0),
                    colors.darkblue
                ),

                (
                    'TEXTCOLOR',
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    'GRID',
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    'FONTNAME',
                    (0, 0),
                    (-1, 0),
                    'Helvetica-Bold'
                )

            ])
        )

        elements.append(alert_table)

        # BUILD PDF

        doc.build(elements)

        return file_path