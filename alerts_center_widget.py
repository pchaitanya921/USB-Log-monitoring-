from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QDateEdit, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from core.alerts import AlertsManager
from datetime import datetime
import pandas as pd
import os

class AlertsCenterWidget(QWidget):
    def __init__(self, parent=None, alerts_manager=None):
        super().__init__(parent)
        self.alerts_manager = alerts_manager or AlertsManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #101010; color: #39ff14;")
        title = QLabel("Alerts History")
        title.setFont(QFont("Consolas", 14, QFont.Bold))
        title.setStyleSheet("color: #39ff14;")
        layout.addWidget(title)
        # Search and filter bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search alerts...")
        self.search_input.textChanged.connect(self.refresh_alerts)
        search_layout.addWidget(self.search_input)
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.addItems(["email", "sms"])
        self.type_filter.currentIndexChanged.connect(self.refresh_alerts)
        search_layout.addWidget(self.type_filter)
        self.from_date_filter = QDateEdit()
        self.from_date_filter.setCalendarPopup(True)
        self.from_date_filter.setDate(QDate.currentDate())
        self.from_date_filter.dateChanged.connect(self.refresh_alerts)
        search_layout.addWidget(QLabel("From:"))
        search_layout.addWidget(self.from_date_filter)
        self.to_date_filter = QDateEdit()
        self.to_date_filter.setCalendarPopup(True)
        self.to_date_filter.setDate(QDate.currentDate())
        self.to_date_filter.dateChanged.connect(self.refresh_alerts)
        search_layout.addWidget(QLabel("To:"))
        search_layout.addWidget(self.to_date_filter)
        layout.addLayout(search_layout)
        self.alerts_list = QListWidget()
        self.alerts_list.setFont(QFont("Consolas", 10))
        self.alerts_list.setStyleSheet("background-color: #181818; color: #39ff14; border: 2px solid #39ff14;")
        layout.addWidget(self.alerts_list)
        # Export buttons
        btn_layout = QHBoxLayout()
        self.export_json_btn = QPushButton("Export JSON")
        self.export_json_btn.clicked.connect(lambda: self.export_alerts('json'))
        btn_layout.addWidget(self.export_json_btn)
        self.export_excel_btn = QPushButton("Export Excel")
        self.export_excel_btn.clicked.connect(lambda: self.export_alerts('excel'))
        btn_layout.addWidget(self.export_excel_btn)
        self.export_pdf_btn = QPushButton("Export PDF")
        self.export_pdf_btn.clicked.connect(lambda: self.export_alerts('pdf'))
        btn_layout.addWidget(self.export_pdf_btn)
        layout.addLayout(btn_layout)
        # Test alert form
        form_layout = QHBoxLayout()
        self.type_box = QComboBox()
        self.type_box.addItems(["Email", "SMS"])
        form_layout.addWidget(self.type_box)
        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("Recipient (email or phone)")
        form_layout.addWidget(self.recipient_input)
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Message")
        form_layout.addWidget(self.message_input)
        self.send_btn = QPushButton("Send Test Alert")
        self.send_btn.clicked.connect(self.send_test_alert)
        form_layout.addWidget(self.send_btn)
        layout.addLayout(form_layout)
        self.setLayout(layout)
        self.refresh_alerts()

    def get_filtered_alerts(self):
        keyword = self.search_input.text().strip().lower() if hasattr(self, 'search_input') else ''
        selected_type = self.type_filter.currentText() if hasattr(self, 'type_filter') else 'All Types'
        from_date = self.from_date_filter.date().toPyDate() if hasattr(self, 'from_date_filter') else None
        to_date = self.to_date_filter.date().toPyDate() if hasattr(self, 'to_date_filter') else None
        filtered = []
        for alert in self.alerts_manager.get_history():
            status = "OK" if 'error' not in alert else f"ERROR: {alert['error']}"
            msg = f"[{alert['type'].upper()}] To: {alert['to']} | {alert.get('subject', '')} | {alert['message']} | {status} | {alert.get('timestamp', '')}"
            alert_type = alert.get('type', '')
            alert_time = alert.get('timestamp', '')
            alert_date = None
            if alert_time:
                try:
                    alert_date = datetime.strptime(alert_time.split()[0], "%Y-%m-%d").date()
                except Exception:
                    alert_date = None
            if selected_type != "All Types" and alert_type != selected_type:
                continue
            if from_date and alert_date and alert_date < from_date:
                continue
            if to_date and alert_date and alert_date > to_date:
                continue
            if not keyword or keyword in msg.lower():
                filtered.append(alert)
        return filtered

    def refresh_alerts(self):
        self.alerts_list.clear()
        for alert in self.get_filtered_alerts():
            status = "OK" if 'error' not in alert else f"ERROR: {alert['error']}"
            msg = f"[{alert['type'].upper()}] To: {alert['to']} | {alert.get('subject', '')} | {alert['message']} | {status} | {alert.get('timestamp', '')}"
            self.alerts_list.addItem(msg)

    def export_alerts(self, fmt):
        alerts = self.get_filtered_alerts()
        filename, _ = QFileDialog.getSaveFileName(self, f"Export Alerts as {fmt.upper()}", os.getcwd(), f"*.{fmt}")
        if not filename:
            return
        base = os.path.splitext(filename)[0]
        if fmt == 'json':
            pd.DataFrame(alerts).to_json(f'{base}.json', orient='records', indent=2)
        elif fmt == 'excel':
            pd.DataFrame(alerts).to_excel(f'{base}.xlsx', index=False)

    def send_test_alert(self):
        alert_type = self.type_box.currentText().lower()
        recipient = self.recipient_input.text().strip()
        message = self.message_input.text().strip()
        if alert_type == 'email':
            self.alerts_manager.send_email_alert("Test Alert", message, recipient)
        else:
            self.alerts_manager.send_sms_alert(message, recipient)
        self.refresh_alerts() 