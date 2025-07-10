from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, 
                             QComboBox, QPushButton, QHBoxLayout, QLabel, QFrame, 
                             QHeaderView, QMessageBox, QToolTip)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from core.access_control import AccessControl
import sys


class AccessControlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.access_control = AccessControl()
        self.devices = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("background: transparent; color: #39ff14;")
        
        # Header with status information
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: rgba(10, 10, 10, 0.3);
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 6px;
                margin-bottom: 4px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("USB ACCESS CONTROL - THREAT-BASED SECURITY")
        title.setFont(QFont("Consolas", 12, QFont.Bold))
        title.setStyleSheet("color: #00ff00; letter-spacing: 0px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Auto-block threats • Read-only for new devices • Manual control available")
        subtitle.setFont(QFont("Consolas", 9))
        subtitle.setStyleSheet("color: #00ff00; text-align: center;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Status summary
        self.status_label = QLabel("Status: Monitoring USB devices...")
        self.status_label.setFont(QFont("Consolas", 10))
        self.status_label.setStyleSheet("color: #00ff00; padding: 4px;")
        layout.addWidget(self.status_label)
        
        # Enhanced table with more columns
        self.table = QTableWidget(0, 10)
        self.table.setFont(QFont("Consolas", 9))
        self.table.setStyleSheet("""
            QTableWidget {
                background: rgba(10, 10, 10, 0.3);
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                gridline-color: rgba(26, 26, 26, 0.5);
                selection-background-color: rgba(26, 26, 26, 0.7);
                selection-color: #00ff00;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid rgba(26, 26, 26, 0.3);
            }
            QTableWidget::item:hover {
                background: rgba(26, 26, 26, 0.5);
            }
            QHeaderView::section {
                background: rgba(26, 26, 26, 0.7);
                color: #00ff00;
                border: 1px solid #00ff00;
                padding: 6px;
                font-weight: bold;
                font-family: 'Consolas', monospace;
            }
        """)
        
        # Set column headers
        headers = ["Device ID", "Model", "Vendor", "Serial", "Size", "Status", "Permission", "Actions", "Whitelist", "Blacklist"]
        self.table.setHorizontalHeaderLabels(headers)
        
        # Set column widths
        self.table.setColumnWidth(0, 150)  # Device ID
        self.table.setColumnWidth(1, 120)  # Model
        self.table.setColumnWidth(2, 100)  # Vendor
        self.table.setColumnWidth(3, 120)  # Serial
        self.table.setColumnWidth(4, 80)   # Size
        self.table.setColumnWidth(5, 100)  # Status
        self.table.setColumnWidth(6, 100)  # Permission
        self.table.setColumnWidth(7, 200)  # Actions
        self.table.setColumnWidth(8, 80)   # Whitelist
        self.table.setColumnWidth(9, 80)   # Blacklist
        
        # Enable sorting
        self.table.setSortingEnabled(True)
        
        layout.addWidget(self.table)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("REFRESH STATUS")
        refresh_btn.setFont(QFont("Consolas", 10, QFont.Bold))
        refresh_btn.setStyleSheet("""
            QPushButton {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 8px 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #00ff00;
            }
            QPushButton:pressed {
                background: #00ff00;
                color: #000000;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_device_status)
        button_layout.addWidget(refresh_btn)
        
        auto_scan_btn = QPushButton("AUTO SCAN ALL")
        auto_scan_btn.setFont(QFont("Consolas", 10, QFont.Bold))
        auto_scan_btn.setStyleSheet("""
            QPushButton {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 8px 16px;
                font-weight: normal;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #00ff00;
            }
            QPushButton:pressed {
                background: #00ff00;
                color: #000000;
            }
        """)
        auto_scan_btn.clicked.connect(self.auto_scan_all_devices)
        button_layout.addWidget(auto_scan_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def update_devices(self, devices):
        self.devices = devices
        self.table.setRowCount(0)
        
        for device in devices:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            device_id = device.get('DeviceID', '')
            
            # Basic device info
            self.table.setItem(row, 0, QTableWidgetItem(str(device_id)))
            self.table.setItem(row, 1, QTableWidgetItem(str(device.get('Model', ''))))
            self.table.setItem(row, 2, QTableWidgetItem(str(device.get('Vendor', ''))))
            self.table.setItem(row, 3, QTableWidgetItem(str(device.get('Serial', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(str(device.get('Size', ''))))
            
            # Device status
            status = self.get_device_status_text(device_id)
            status_item = QTableWidgetItem(status)
            self.color_status_item(status_item, device_id)
            self.table.setItem(row, 5, status_item)
            
            # Permission dropdown
            perm_box = QComboBox()
            perm_box.addItems(["Read-Only", "Full Access", "Block"])
            current_perm = self.access_control.get_permission(device_id)
            perm_map = {"read-only": 0, "full": 1, "block": 2}
            perm_box.setCurrentIndex(perm_map.get(current_perm, 0))
            perm_box.currentIndexChanged.connect(lambda idx, r=row: self.handle_permission_change(r))
            self.table.setCellWidget(row, 6, perm_box)
            
            # Action buttons
            action_frame = QFrame()
            action_layout = QHBoxLayout(action_frame)
            action_layout.setContentsMargins(2, 2, 2, 2)
            action_layout.setSpacing(2)
            
            scan_btn = QPushButton("SCAN")
            scan_btn.setFont(QFont("Consolas", 8))
            scan_btn.setStyleSheet("""
                QPushButton {
                    background: #1a1a1a;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    padding: 4px 8px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background: #0f0f0f;
                }
            """)
            scan_btn.clicked.connect(lambda checked, r=row: self.scan_device(r))
            action_layout.addWidget(scan_btn)
            
            clean_btn = QPushButton("CLEAN")
            clean_btn.setFont(QFont("Consolas", 8))
            clean_btn.setStyleSheet("""
                QPushButton {
                    background: #1a1a1a;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    padding: 4px 8px;
                    font-weight: normal;
                }
                QPushButton:hover {
                    background: #0f0f0f;
                }
            """)
            clean_btn.clicked.connect(lambda checked, r=row: self.mark_device_clean(r))
            action_layout.addWidget(clean_btn)
            
            self.table.setCellWidget(row, 7, action_frame)
            
            # Whitelist button
            wl_btn = QPushButton("WHITELIST" if not self.access_control.is_whitelisted(device_id) else "✓")
            wl_btn.setCheckable(True)
            wl_btn.setChecked(self.access_control.is_whitelisted(device_id))
            wl_btn.setFont(QFont("Consolas", 8))
            wl_btn.setStyleSheet("""
                QPushButton {
                    background: #1a1a1a;
                    color: #00ff00;
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    padding: 4px 8px;
                    font-weight: normal;
                }
                QPushButton:checked {
                    background: #00ff00;
                    color: #000000;
                }
                QPushButton:hover {
                    background: #0f0f0f;
                }
            """)
            wl_btn.clicked.connect(lambda checked, r=row: self.handle_whitelist(r))
            self.table.setCellWidget(row, 8, wl_btn)
            
            # Blacklist button
            bl_btn = QPushButton("BLOCK" if not self.access_control.is_blacklisted(device_id) else "✗")
            bl_btn.setCheckable(True)
            bl_btn.setChecked(self.access_control.is_blacklisted(device_id))
            bl_btn.setFont(QFont("Consolas", 8))
            bl_btn.setStyleSheet("""
                QPushButton {
                    background: #1a1a1a;
                    color: #ff0000;
                    border: 1px solid #ff0000;
                    border-radius: 0px;
                    padding: 4px 8px;
                    font-weight: normal;
                }
                QPushButton:checked {
                    background: #ff0000;
                    color: #ffffff;
                }
                QPushButton:hover {
                    background: #0f0f0f;
                }
            """)
            bl_btn.clicked.connect(lambda checked, r=row: self.handle_blacklist(r))
            self.table.setCellWidget(row, 9, bl_btn)
        
        self.update_status_summary()

    def get_device_status_text(self, device_id):
        """Get human-readable device status."""
        if device_id in self.access_control.threat_devices:
            return "THREAT"
        elif device_id in self.access_control.clean_devices:
            return "CLEAN"
        elif device_id in self.access_control.new_devices:
            return "NEW"
        elif device_id in self.access_control.whitelist:
            return "TRUSTED"
        elif device_id in self.access_control.blacklist:
            return "BLOCKED"
        else:
            return "UNKNOWN"

    def color_status_item(self, item, device_id):
        """Color the status item based on device status."""
        if device_id in self.access_control.threat_devices:
            item.setBackground(QColor(255, 0, 0, 100))  # Red for threats
        elif device_id in self.access_control.clean_devices:
            item.setBackground(QColor(0, 255, 0, 100))  # Green for clean
        elif device_id in self.access_control.whitelist:
            item.setBackground(QColor(0, 255, 255, 100))  # Cyan for trusted
        elif device_id in self.access_control.blacklist:
            item.setBackground(QColor(255, 0, 0, 150))  # Dark red for blocked
        elif device_id in self.access_control.new_devices:
            item.setBackground(QColor(255, 255, 0, 100))  # Yellow for new

    def handle_permission_change(self, row):
        item = self.table.item(row, 0)
        perm_box = self.table.cellWidget(row, 6)
        if item is None or perm_box is None:
            return
        device_id = item.text()
        permission = perm_box.currentText().lower().replace(' ', '-')
        self.access_control.set_permission(device_id, permission)
        self.update_status_summary()

    def handle_whitelist(self, row):
        item = self.table.item(row, 0)
        wl_btn = self.table.cellWidget(row, 8)
        if item is None or wl_btn is None:
            return
        device_id = item.text()
        if wl_btn.isChecked():
            self.access_control.add_to_whitelist(device_id)
            wl_btn.setText("✓")
        else:
            self.access_control.whitelist.discard(device_id)
            wl_btn.setText("WHITELIST")
        self.update_status_summary()

    def handle_blacklist(self, row):
        item = self.table.item(row, 0)
        bl_btn = self.table.cellWidget(row, 9)
        if item is None or bl_btn is None:
            return
        device_id = item.text()
        if bl_btn.isChecked():
            self.access_control.add_to_blacklist(device_id)
            bl_btn.setText("✗")
        else:
            self.access_control.blacklist.discard(device_id)
            bl_btn.setText("BLOCK")
        self.update_status_summary()

    def scan_device(self, row):
        """Scan a specific device for threats."""
        item = self.table.item(row, 0)
        if item is None:
            return
        device_id = item.text()
        
        # Simulate scanning (in real implementation, this would call the malware scanner)
        self.status_label.setText(f"Scanning device {device_id}...")
        
        # For demo purposes, randomly mark as threat or clean
        import random
        if random.random() < 0.2:  # 20% chance of threat
            self.access_control.mark_device_threat(device_id)
            QMessageBox.warning(self, "Threat Detected", f"Threats found in {device_id}. Device has been blocked.")
        else:
            self.access_control.mark_device_clean(device_id)
            QMessageBox.information(self, "Scan Complete", f"{device_id} is clean. Access granted.")
        
        self.update_devices(self.devices)  # Refresh the table

    def mark_device_clean(self, row):
        """Manually mark device as clean."""
        item = self.table.item(row, 0)
        if item is None:
            return
        device_id = item.text()
        self.access_control.mark_device_clean(device_id)
        QMessageBox.information(self, "Device Clean", f"{device_id} marked as clean.")
        self.update_devices(self.devices)

    def refresh_device_status(self):
        """Refresh the status of all devices."""
        self.update_devices(self.devices)
        self.status_label.setText("Device status refreshed.")

    def auto_scan_all_devices(self):
        """Automatically scan all connected devices."""
        if not self.devices:
            QMessageBox.information(self, "No Devices", "No USB devices connected.")
            return
        
        self.status_label.setText("Auto-scanning all devices...")
        
        for device in self.devices:
            device_id = device.get('DeviceID', '')
            if device_id:
                # Add as new device if not seen before
                if device_id not in self.access_control.permissions:
                    self.access_control.add_new_device(device_id)
        
        self.update_devices(self.devices)
        self.status_label.setText("Auto-scan complete. New devices set to read-only.")

    def update_status_summary(self):
        """Update the status summary label."""
        total = len(self.devices)
        threats = len([d for d in self.devices if d.get('DeviceID', '') in self.access_control.threat_devices])
        clean = len([d for d in self.devices if d.get('DeviceID', '') in self.access_control.clean_devices])
        new = len([d for d in self.devices if d.get('DeviceID', '') in self.access_control.new_devices])
        blocked = len([d for d in self.devices if d.get('DeviceID', '') in self.access_control.blacklist])
        
        summary = f"Status: {total} devices | {threats} threats | {clean} clean | {new} new | {blocked} blocked"
        self.status_label.setText(summary)

 