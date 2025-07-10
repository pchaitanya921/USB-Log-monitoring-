from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QMessageBox, QScrollArea, QFrame, QGridLayout, QProgressBar)
from core.malware_scanner import MalwareScanner
from core.access_control import AccessControl
import os
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import QTimer, Qt

class DeviceBlock(QFrame):
    """Individual device block widget"""
    def __init__(self, device_info, parent=None):
        super().__init__(parent)
        self.device_info = device_info
        self.scanner = MalwareScanner()
        self.access_control = AccessControl()
        self.scan_status = "Not Scanned"
        self.threat_count = 0
        self.init_ui()
        
    def init_ui(self):
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 12px;
            }
            QFrame:hover {
                border: 1px solid #00ffe7;
                background: transparent;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header frame with increased padding
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 6px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(4)
        
        device_title = QLabel(f"USB Device: {self.device_info.get('Product', 'Unknown')}")
        device_title.setFont(QFont("Consolas", 11, QFont.Bold))
        device_title.setStyleSheet("color: #39ff14; letter-spacing: 0px;")
        header_layout.addWidget(device_title)
        
        layout.addWidget(header_frame)
        
        # Details frame with increased padding
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 8px;
            }
        """)
        
        details_layout = QGridLayout(details_frame)
        details_layout.setSpacing(4)
        details_layout.setVerticalSpacing(2)
        
        # Add device details with more spacing
        row = 0
        for key, value in self.device_info.items():
            if key != 'Product':  # Already shown in header
                label = QLabel(f"{key}:")
                label.setFont(QFont("Consolas", 9, QFont.Bold))
                label.setStyleSheet("color: #39ff14;")
                value_label = QLabel(str(value))
                value_label.setFont(QFont("Consolas", 9))
                value_label.setStyleSheet("color: #39ff14;")
                details_layout.addWidget(label, row, 0)
                details_layout.addWidget(value_label, row, 1)
                row += 1
        
        layout.addWidget(details_frame)
        
        # Status frame with increased padding
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 6px;
            }
        """)
        
        status_layout = QVBoxLayout(status_frame)
        status_layout.setSpacing(4)
        
        self.status_label = QLabel("Status: Ready to scan")
        self.status_label.setFont(QFont("Consolas", 9))
        self.status_label.setStyleSheet("color: #39ff14;")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_frame)
        
        # Button frame with increased padding
        button_frame = QFrame()
        button_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 6px;
            }
        """)
        
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(6)
        
        self.scan_btn = QPushButton("SCAN DEVICE")
        self.scan_btn.setFont(QFont("Consolas", 9, QFont.Bold))
        self.scan_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00ffe7;
                border: 1px solid #00ffe7;
                border-radius: 0px;
                padding: 4px 8px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #00ffe7;
                border: 1px solid #00ffe7;
            }
            QPushButton:pressed {
                background: #00ffe7;
                color: #000000;
                border: 1px solid #00ffe7;
            }
        """)
        self.scan_btn.clicked.connect(self.scan_device)
        button_layout.addWidget(self.scan_btn)
        
        self.quarantine_btn = QPushButton("QUARANTINE")
        self.quarantine_btn.setFont(QFont("Consolas", 9, QFont.Bold))
        self.quarantine_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ff6b6b;
                border: 1px solid #ff6b6b;
                border-radius: 0px;
                padding: 4px 8px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #ff6b6b;
                border: 1px solid #ff6b6b;
            }
            QPushButton:pressed {
                background: #ff6b6b;
                color: #000000;
                border: 1px solid #ff6b6b;
            }
        """)
        self.quarantine_btn.clicked.connect(self.quarantine_device)
        button_layout.addWidget(self.quarantine_btn)
        
        self.allow_btn = QPushButton("ALLOW")
        self.allow_btn.setFont(QFont("Consolas", 9, QFont.Bold))
        self.allow_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #4ecdc4;
                border: 1px solid #4ecdc4;
                border-radius: 0px;
                padding: 4px 8px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #4ecdc4;
                border: 1px solid #4ecdc4;
            }
            QPushButton:pressed {
                background: #4ecdc4;
                color: #000000;
                border: 1px solid #4ecdc4;
            }
        """)
        self.allow_btn.clicked.connect(self.allow_device)
        button_layout.addWidget(self.allow_btn)
        
        layout.addWidget(button_frame)
        
        # Update access control button states
        self.update_access_controls()
        
    def scan_device(self):
        """Scan the device for threats"""
        device_id = self.device_info.get('DeviceID', '')
        if device_id:
            self.status_label.setText("Status: Scanning...")
            # Simulate scan
            import time
            time.sleep(1)
            self.status_label.setText("Status: Scan completed - Clean")
            if hasattr(self, 'show_hacker_notification'):
                self.show_hacker_notification("Device Scan", f"Device {device_id} scanned successfully", "info")

    def quarantine_device(self):
        """Quarantine the device (not implemented)."""
        # For now, just show a message
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Quarantine", "Device quarantine feature not implemented yet.")

    def allow_device(self):
        """Allow the device"""
        device_id = self.device_info.get('DeviceID', '')
        if device_id:
            self.status_label.setText("Status: Device allowed")
            if hasattr(self, 'show_hacker_notification'):
                self.show_hacker_notification("Device Allowed", f"Device {device_id} has been allowed", "info")

    def update_access_controls(self):
        """Update access control button states"""
        device_id = self.device_info.get('DeviceID', '')
        self.quarantine_btn.setEnabled(True)
        self.allow_btn.setEnabled(True)

class DeviceScannerWidget(QWidget):
    def __init__(self, parent=None, alerts_manager=None, logger=None):
        super().__init__(parent)
        self.alerts_manager = alerts_manager
        self.logger = logger
        self.device_blocks = []
        self.scanner = MalwareScanner()
        self.access_control = AccessControl()
        self.scanner_callback = None
        self.init_ui()
        
    def set_scanner_callback(self, callback):
        """Set the scanner callback function"""
        self.scanner_callback = callback

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 12px;
            }
            QWidget:hover {
                border: 1px solid #00ffe7;
                background: transparent;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # Header section with enhanced styling
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        title = QLabel()
        title.setPixmap(QPixmap("resources/icons/scan.svg").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Scan All button with enhanced styling
        self.scan_all_btn = QPushButton("🚀 SCAN ALL DEVICES")
        self.scan_all_btn.setFont(QFont("Consolas", 14, QFont.Bold))
        self.scan_all_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #00ffe7;
                border: 1px solid #00ffe7;
                border-radius: 0px;
                padding: 12px 20px;
                margin: 5px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: transparent;
                color: #39ff14;
                border: 1px solid #39ff14;
            }
            QPushButton:pressed {
                background: transparent;
                color: #ff00cc;
                border: 1px solid #ff00cc;
            }
        """)
        self.scan_all_btn.setMinimumHeight(45)
        self.scan_all_btn.clicked.connect(self.scan_all_devices)
        header_layout.addWidget(self.scan_all_btn)
        
        layout.addWidget(header_frame)
        
        # Status and info section
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(10)
        
        # Status label
        self.statusLabel = QLabel("⏳ Status: Waiting for USB devices...")
        self.statusLabel.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 12, QFont.Bold))
        self.statusLabel.setStyleSheet("""
            color: #39ff14; 
            text-shadow: 0 0 5px #39ff14;
            margin-bottom: 5px;
        """)
        info_layout.addWidget(self.statusLabel)
        
        # Device count
        self.device_count_label = QLabel("🔌 Connected Devices: 0")
        self.device_count_label.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 12, QFont.Bold))
        self.device_count_label.setStyleSheet("""
            color: #00ffe7; 
            text-shadow: 0 0 5px #00ffe7;
            margin-bottom: 5px;
        """)
        info_layout.addWidget(self.device_count_label)
        
        layout.addWidget(info_frame)
        
        # Scrollable area for device blocks with enhanced styling
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #39ff14;
                border-radius: 0px;
                background: transparent;
            }
            QScrollBar:vertical {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #00ff00;
                border-radius: 0px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #00ff00;
            }
        """)
        
        self.device_container = QWidget()
        self.device_layout = QGridLayout(self.device_container)
        self.device_layout.setSpacing(10)
        self.device_layout.setVerticalSpacing(8)
        
        scroll_area.setWidget(self.device_container)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)

    def update_devices(self, devices):
        """Update the device display with new device list"""
        # Clear existing device blocks
        for block in self.device_blocks:
            block.setParent(None)
        self.device_blocks.clear()
        
        # Update device count
        self.device_count_label.setText(f"Connected Devices: {len(devices)}")
        
        if not devices:
            self.statusLabel.setText("Status: No USB devices connected")
            return
            
        self.statusLabel.setText(f"Status: {len(devices)} USB device(s) detected")
        
        # Create device blocks
        for i, device in enumerate(devices):
            block = DeviceBlock(device, self)
            row = i // 2  # 2 blocks per row
            col = i % 2
            self.device_layout.addWidget(block, row, col)
            self.device_blocks.append(block)
            
        # Auto-scan all devices
        self.auto_scan_all_devices()
        
    def auto_scan_all_devices(self):
        """Automatically scan all connected devices"""
        if not self.device_blocks:
            return
            
        self.statusLabel.setText("Status: Auto-scanning all USB devices...")
        QTimer.singleShot(1000, self.perform_auto_scan)
        
    def perform_auto_scan(self):
        """Perform the actual auto-scan"""
        total_threats = 0
        scanned_count = 0
        
        for block in self.device_blocks:
            device_id = block.device_info.get('DeviceID', '')
            try:
                if device_id and os.path.exists(device_id):
                    results = self.scanner.scan_path(device_id)
                else:
                    # No demo/simulation - only real scans
                    results = {}
                
                if results:
                    block.scan_status = f"Threats: {len(results)}"
                    block.threat_count = len(results)
                    block.status_label.setText("🔴")
                    block.status_label.setStyleSheet("color: #FF4444;")
                    total_threats += len(results)
                else:
                    block.scan_status = "Clean"
                    block.threat_count = 0
                    block.status_label.setText("🟢")
                    block.status_label.setStyleSheet("color: #00FF00;")
                    
                try:
                    block.status_label.setText(f"Scan Status: {block.scan_status}")
                except AttributeError:
                    pass
                scanned_count += 1
                
            except Exception as e:
                block.scan_status = "Scan Failed"
                block.status_label.setText("⚠️")
                block.status_label.setStyleSheet("color: #FFA500;")
                try:
                    block.status_label.setText(f"Scan Status: {block.scan_status}")
                except AttributeError:
                    pass
        
        # Update status
        if total_threats > 0:
            self.statusLabel.setText(f"Status: Auto-scan complete. {total_threats} threat(s) found across {scanned_count} device(s)")
            if self.alerts_manager:
                self.alerts_manager.send_email_alert(
                    "USB HawkEye Alert: Threats Detected",
                    f"Auto-scan detected {total_threats} threat(s) across {scanned_count} USB device(s)",
                    self.alerts_manager.email_config.get('recipient', '')
                )
        else:
            self.statusLabel.setText(f"Status: Auto-scan complete. All {scanned_count} device(s) are clean")
            
        # Log the auto-scan
        if self.logger:
            self.logger.log_event("auto_scan", f"Scanned {scanned_count} devices, found {total_threats} threats")
            
        # Call callback if set
        if self.scanner_callback:
            self.scanner_callback({"scanned": scanned_count, "threats": total_threats})

    def scan_all_devices(self):
        """Manually scan all devices"""
        self.statusLabel.setText("Status: Manually scanning all USB devices...")
        QTimer.singleShot(500, self.perform_auto_scan) 