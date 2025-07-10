from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHBoxLayout, QPushButton, QFileDialog, QLineEdit, QComboBox, QDateEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate
from core.logger import ActivityLogger
import os
from datetime import datetime

class LogsViewerWidget(QWidget):
    def __init__(self, parent=None, logger=None):
        super().__init__(parent)
        self.logger = logger or ActivityLogger()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("background-color: #101010; color: #39ff14;")
        title = QLabel("Threat & Activity Logs")
        title.setFont(QFont("Consolas", 14, QFont.Bold))
        title.setStyleSheet("color: #39ff14;")
        layout.addWidget(title)
        # Search and filter bar
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search logs...")
        self.search_input.textChanged.connect(self.refresh_logs)
        search_layout.addWidget(self.search_input)
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.addItems(["threat", "scan", "usb_event", "unauthorized_access"])
        self.type_filter.currentIndexChanged.connect(self.refresh_logs)
        search_layout.addWidget(self.type_filter)
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setDate(QDate.currentDate())
        self.date_filter.dateChanged.connect(self.refresh_logs)
        search_layout.addWidget(self.date_filter)
        layout.addLayout(search_layout)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Type", "Details"])
        self.table.setFont(QFont("Consolas", 10))
        self.table.setStyleSheet("background-color: #181818; color: #39ff14; border: 2px solid #39ff14;")
        layout.addWidget(self.table)
        # Export buttons
        btn_layout = QHBoxLayout()
        self.export_json_btn = QPushButton("Export JSON")
        self.export_json_btn.clicked.connect(lambda: self.export_logs('json'))
        btn_layout.addWidget(self.export_json_btn)
        self.export_excel_btn = QPushButton("Export Excel")
        self.export_excel_btn.clicked.connect(lambda: self.export_logs('excel'))
        btn_layout.addWidget(self.export_excel_btn)
        self.export_pdf_btn = QPushButton("Export PDF")
        self.export_pdf_btn.clicked.connect(lambda: self.export_logs('pdf'))
        btn_layout.addWidget(self.export_pdf_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.refresh_logs()

    def refresh_logs(self):
        self.table.setRowCount(0)
        keyword = self.search_input.text().strip().lower() if hasattr(self, 'search_input') else ''
        selected_type = self.type_filter.currentText() if hasattr(self, 'type_filter') else 'All Types'
        selected_date = self.date_filter.date().toPyDate() if hasattr(self, 'date_filter') else None
        for entry in self.logger.logs:
            msg = f"{entry.get('type', '')} {entry.get('details', '')}"
            entry_type = entry.get('type', '')
            entry_time = entry.get('timestamp', '')
            entry_date = None
            if entry_time:
                try:
                    entry_date = datetime.strptime(entry_time.split()[0], "%Y-%m-%d").date()
                except Exception:
                    entry_date = None
            if selected_type != "All Types" and entry_type != selected_type:
                continue
            if selected_date and entry_date and entry_date != selected_date:
                continue
            if not keyword or keyword in msg.lower():
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(entry.get('timestamp', ''))))
                self.table.setItem(row, 1, QTableWidgetItem(str(entry.get('type', ''))))
                self.table.setItem(row, 2, QTableWidgetItem(str(entry.get('details', ''))))

    def export_logs(self, fmt):
        filename, _ = QFileDialog.getSaveFileName(self, f"Export Logs as {fmt.upper()}", os.getcwd(), f"*.{fmt}")
        if filename:
            self.logger.export_logs(fmt, filename=os.path.splitext(filename)[0]) 