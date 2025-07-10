import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QListWidget, QHBoxLayout, QFrame, QSystemTrayIcon, QMenu, QAction, QPushButton, QTableWidget, QTableWidgetItem, QGridLayout, QScrollArea, QStackedWidget
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt
from ui.device_scanner_widget import DeviceScannerWidget
from core.usb_monitor import USBMonitor
from ui.access_control_widget import AccessControlWidget
from ui.alerts_center_widget import AlertsCenterWidget
from ui.logs_viewer_widget import LogsViewerWidget
from core.alerts import AlertsManager
from core.logger import ActivityLogger
from ui.settings_widget import SettingsWidget
import json
import os

from ui.notification_popup import NotificationManager
from ui.animated_background import CyberpunkHackerBackground

class MainDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB HawkEye")
        self.setGeometry(100, 100, 1200, 800)
        # Set app logo
        logo_path = "resources/usb_hawkeye_logo.svg"
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        self.set_dark_theme()
        # Add cyberpunk hacker background
        self.cyberpunk_background = CyberpunkHackerBackground(self)
        self.cyberpunk_background.lower()  # Ensure it's behind all widgets
        self.cyberpunk_background.setGeometry(self.rect())
        self.activity_log = []
        self.threat_count = 0
        self.alerts_manager = AlertsManager()
        self.logger = ActivityLogger()
        self.user_role = None
        self.tray_icon = None
        # Initialize notification manager
        self.notification_manager = NotificationManager(self)
        # Stat tracking
        self.connected_devices_count = 0
        self.total_devices_set = set()
        self.total_scans_count = 0
        self.last_scan_str = "-"

        # Initialize UI first but keep it hidden
        self.init_ui()
        
        # Create stacked widget to switch between login and main interface
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create and add login widget
        from ui.login_dialog import LoginWidget
        self.login_widget = LoginWidget(self.stacked_widget)
        self.login_widget.login_successful.connect(self.on_login_successful)
        self.stacked_widget.addWidget(self.login_widget)
        
        # Add main interface (initially hidden)
        self.main_interface = QWidget()
        main_layout = QVBoxLayout(self.main_interface)
        main_layout.addWidget(self.tabs)
        self.stacked_widget.addWidget(self.main_interface)
        
        # Show login screen first
        self.stacked_widget.setCurrentWidget(self.login_widget)
        
        # Show the main window
        self.show()
        self.raise_()
        self.activateWindow()
        
        # Initialize other components
        self.init_usb_monitor()
        self.init_tray()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(10, 10, 10))
        palette.setColor(QPalette.WindowText, QColor(0, 255, 0))  # green
        palette.setColor(QPalette.Base, QColor(26, 26, 26))
        palette.setColor(QPalette.AlternateBase, QColor(15, 15, 15))
        palette.setColor(QPalette.ToolTipBase, QColor(10, 10, 10))
        palette.setColor(QPalette.ToolTipText, QColor(0, 255, 0))
        palette.setColor(QPalette.Text, QColor(0, 255, 0))  # green
        palette.setColor(QPalette.Button, QColor(26, 26, 26))
        palette.setColor(QPalette.ButtonText, QColor(0, 255, 0))
        palette.setColor(QPalette.BrightText, QColor(0, 255, 0))  # green
        palette.setColor(QPalette.Highlight, QColor(0, 255, 0))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
        self.setPalette(palette)

    def on_login_successful(self, username, role):
        """Handle successful login"""
        self.username = username
        self.user_role = role
        # Get email from login widget
        self.user_email = getattr(self.login_widget, 'email', None)
        # Switch to main interface
        self.stacked_widget.setCurrentWidget(self.main_interface)
        # Update settings widget with user info
        self.settings_widget.update_user_info(username, role, self.user_email)

    def init_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #00ff00;
                background: #0a0a0a;
                border-radius: 0px;
            }
            QTabBar::tab {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-bottom: none;
                border-radius: 0px;
                padding: 8px 16px;
                margin-right: 2px;
                font-family: 'Consolas', monospace;
                font-weight: normal;
                font-size: 10px;
                letter-spacing: 0px;
                text-transform: none;
            }
            QTabBar::tab:selected {
                background: #00ff00;
                color: #000000;
                border: 1px solid #00ff00;
            }
            QTabBar::tab:hover {
                background: #1f1f1f;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
        """)
        
        self.dashboard_tab = self.create_dashboard_tab()
        self.tabs.addTab(self.dashboard_tab, "DASHBOARD")
        self.device_scanner = DeviceScannerWidget(alerts_manager=self.alerts_manager, logger=self.logger)
        self.device_scanner.set_scanner_callback(self.on_scan_result)
        self.tabs.addTab(self.device_scanner, "DEVICE SCANNER")
        self.access_control_widget = AccessControlWidget()
        self.tabs.addTab(self.access_control_widget, "ACCESS CONTROL")
        self.alerts_center_widget = AlertsCenterWidget(alerts_manager=self.alerts_manager)
        self.tabs.addTab(self.alerts_center_widget, "ALERTS CENTER")
        self.logs_viewer_widget = LogsViewerWidget(logger=self.logger)
        self.tabs.addTab(self.logs_viewer_widget, "LOGS VIEWER")
        self.settings_widget = SettingsWidget(username=getattr(self, 'username', None), role=getattr(self, 'user_role', None), logout_callback=self.handle_logout, scan_callback=self.trigger_scan)
        self.tabs.addTab(self.settings_widget, "SETTINGS")
        # Always enable all tabs for testing
        self.tabs.setTabEnabled(self.tabs.indexOf(self.access_control_widget), True)
        self.tabs.setTabEnabled(self.tabs.indexOf(self.settings_widget), True)
        self.tabs.setTabEnabled(self.tabs.indexOf(self.logs_viewer_widget), True)

    def create_dashboard_tab(self):
        # Create the main dashboard widget and layout as before
        content_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Header with cyberpunk title
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: rgba(10, 10, 10, 0.3);
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 6px;
                margin-bottom: 2px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("USB HAWKEYE - CYBERPUNK SECURITY DASHBOARD")
        title.setFont(QFont("Consolas", 14, QFont.Bold))
        title.setStyleSheet("""
            color: #00ff00; 
            letter-spacing: 0px;
            margin: 1px 0;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Real-time USB Device Monitoring & Threat Detection")
        subtitle.setFont(QFont("Consolas", 10))
        subtitle.setStyleSheet("color: #00ff00; text-align: center; margin: 1px 0;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
        # Stat cards row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(8)
        self.stat_cards = []
        stat_info = [
            ("CONNECTED DEVICES", "0", "resources/icons/usb.svg"),
            ("TOTAL DEVICES", "0", "resources/icons/user.svg"),
            ("TOTAL SCANS", "0", "resources/icons/scan.svg"),
            ("LAST SCAN", "-", "resources/icons/alert.svg")
        ]
        for label, value, icon_path in stat_info:
            card_outer = QFrame()
            card_outer.setStyleSheet("""
                QFrame {
                    background: rgba(10, 10, 10, 0.3);
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    min-width: 180px;
                    min-height: 80px;
                    margin: 0 1px;
                }
                QFrame:hover {
                    border: 1px solid #00ff00;
                    background: rgba(10, 10, 10, 0.5);
                }
            """)
            card_outer_layout = QVBoxLayout(card_outer)
            card_outer_layout.setContentsMargins(8, 8, 8, 8)
            card_outer_layout.setSpacing(4)
            
            # Icon and label
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            card_outer_layout.addWidget(icon_label)
            
            # Label block
            label_frame = QFrame()
            label_frame.setStyleSheet("""
                QFrame {
                    background: rgba(10, 10, 10, 0.3);
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    min-height: 18px;
                }
            """)
            label_layout = QVBoxLayout(label_frame)
            label_layout.setContentsMargins(4, 2, 4, 2)
            card_label = QLabel(label)
            card_label.setFont(QFont("Consolas", 9, QFont.Bold))
            card_label.setStyleSheet("color: #00ff00; letter-spacing: 0px; text-align: center;")
            card_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label_layout.addWidget(card_label)
            card_outer_layout.addWidget(label_frame)
            
            # Value block
            value_frame = QFrame()
            value_frame.setStyleSheet("""
                QFrame {
                    background: rgba(10, 10, 10, 0.3);
                    border: 1px solid #00ff00;
                    border-radius: 0px;
                    min-height: 24px;
                }
            """)
            value_layout = QVBoxLayout(value_frame)
            value_layout.setContentsMargins(4, 2, 4, 2)
            card_value = QLabel(value)
            card_value.setFont(QFont("Consolas", 14, QFont.Bold))
            card_value.setStyleSheet("color: #00ff00; text-align: center;")
            card_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
            value_layout.addWidget(card_value)
            card_outer_layout.addWidget(value_frame)
            
            stats_layout.addWidget(card_outer)
            self.stat_cards.append((card_label, card_value))
        
        layout.addLayout(stats_layout)
        
        # Scan buttons row with enhanced styling
        scan_btn_layout = QHBoxLayout()
        scan_btn_layout.setSpacing(8)
        
        scan_all_btn = QPushButton("SCAN ALL DEVICES")
        scan_all_btn.setFont(QFont("Consolas", 11, QFont.Bold))
        scan_all_btn.setStyleSheet("""
            QPushButton {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 4px 8px;
                margin: 1px;
                font-weight: normal;
                letter-spacing: 0px;
                text-transform: none;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            QPushButton:pressed {
                background: #00ff00;
                color: #000000;
                border: 1px solid #00ff00;
            }
        """)
        scan_all_btn.setMinimumHeight(28)
        scan_btn_layout.addWidget(scan_all_btn, 1)
        scan_all_btn.clicked.connect(self.trigger_scan)
        
        scan_selected_btn = QPushButton("SCAN SELECTED")
        scan_selected_btn.setFont(QFont("Consolas", 11, QFont.Bold))
        scan_selected_btn.setStyleSheet("""
            QPushButton {
                background: #1a1a1a;
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 4px 8px;
                margin: 1px;
                font-weight: normal;
                letter-spacing: 0px;
                text-transform: none;
            }
            QPushButton:hover {
                background: #0f0f0f;
                color: #00ff00;
                border: 1px solid #00ff00;
            }
            QPushButton:pressed {
                background: #00ff00;
                color: #000000;
                border: 1px solid #00ff00;
            }
        """)
        scan_selected_btn.setMinimumHeight(28)
        scan_btn_layout.addWidget(scan_selected_btn, 1)
        scan_selected_btn.clicked.connect(self.dashboard_scan_selected)
        
        layout.addLayout(scan_btn_layout)
        
        # Connected Devices Section with enhanced styling
        devices_header = QFrame()
        devices_header.setStyleSheet("""
            QFrame {
                background: rgba(10, 10, 10, 0.3);
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 4px;
                margin: 2px 0;
            }
        """)
        devices_header_layout = QHBoxLayout(devices_header)
        
        devices_title = QLabel("CONNECTED USB DEVICES")
        devices_title.setFont(QFont("Consolas", 12, QFont.Bold))
        devices_title.setStyleSheet("color: #00ff00; letter-spacing: 0px;")
        devices_header_layout.addWidget(devices_title)
        
        layout.addWidget(devices_header)
        
        # Device blocks container
        self.dashboard_device_container = QWidget()
        self.dashboard_device_layout = QGridLayout(self.dashboard_device_container)
        self.dashboard_device_layout.setContentsMargins(0, 0, 0, 0)
        self.dashboard_device_layout.setSpacing(2)
        self.dashboard_device_layout.setVerticalSpacing(1)
        self.dashboard_device_blocks = []
        
        layout.addWidget(self.dashboard_device_container)
        
        # Device History panel with enhanced styling
        history_panel = QFrame()
        history_panel.setStyleSheet("""
            QFrame {
                background: rgba(10, 10, 10, 0.3);
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 6px;
                margin: 2px 0;
            }
        """)
        history_layout = QVBoxLayout(history_panel)
        
        history_title_layout = QHBoxLayout()
        history_icon = QLabel()
        history_icon.setPixmap(QPixmap("resources/icons/alert.svg").scaled(18, 18, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        history_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        history_title_layout.addWidget(history_icon)
        history_title = QLabel("USB CONNECTION HISTORY")
        history_title.setFont(QFont("Consolas", 12, QFont.Bold))
        history_title.setStyleSheet("color: #00ff00; letter-spacing: 0px; margin: 1px 0;")
        history_title_layout.addWidget(history_title)
        history_layout.addLayout(history_title_layout)
        
        self.dashboard_history_list = QListWidget()
        self.dashboard_history_list.setFont(QFont("Consolas", 9))
        self.dashboard_history_list.setStyleSheet("""
            QListWidget {
                background: rgba(10, 10, 10, 0.3);
                color: #00ff00;
                border: 1px solid #00ff00;
                border-radius: 0px;
                padding: 2px;
                selection-background-color: rgba(26, 26, 26, 0.7);
                selection-color: #00ff00;
                alternate-background-color: rgba(10, 10, 10, 0.2);
            }
            QListWidget::item {
                padding: 2px;
                border-bottom: 1px solid rgba(26, 26, 26, 0.5);
                border-radius: 0px;
                margin: 0px;
                background: transparent;
            }
            QListWidget::item:hover {
                background: rgba(26, 26, 26, 0.7);
                border: 1px solid #00ff00;
            }
        """)
        history_layout.addWidget(self.dashboard_history_list)
        
        layout.addWidget(history_panel)
        
        content_widget.setStyleSheet("background-color: rgba(10, 10, 10, 0.1);")
        content_widget.setLayout(layout)
        
        # Wrap the content widget in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_widget)
        scroll_area.setStyleSheet("background: rgba(10, 10, 10, 0.1); border: none;")
        
        # Return a QWidget with a single QVBoxLayout containing the scroll area
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(scroll_area)
        wrapper.setLayout(wrapper_layout)
        return wrapper

    def create_tab(self, name):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{name} panel coming soon...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget

    def init_usb_monitor(self):
        self.usb_monitor = USBMonitor()
        self.usb_monitor.register_callback(self.on_usb_event)
        self.usb_monitor.start_monitoring()
        # Populate initial device list
        devices = self.usb_monitor.get_connected_devices()
        self.device_scanner.update_devices(devices)
        self.access_control_widget.update_devices(devices)
        self.update_dashboard_stats(devices)
        self.log_activity("System started. Initial device scan.")
        
        # Only show real connected devices - no demo devices
        if not devices:
            self.refresh_dashboard_with_demo_devices()
    
    def refresh_dashboard_with_demo_devices(self):
        """Show only real connected devices - no demo devices"""
        # Only show real connected devices
        real_devices = self.usb_monitor.get_connected_devices()
        if real_devices:
            self.update_dashboard_stats(real_devices)
            self.device_scanner.update_devices(real_devices)
            self.access_control_widget.update_devices(real_devices)
            self.log_activity(f"Found {len(real_devices)} real connected USB device(s).")
        else:
            # Clear dashboard if no devices connected
            self.update_dashboard_stats([])
            self.device_scanner.update_devices([])
            self.access_control_widget.update_devices([])
            self.log_activity("No USB devices currently connected.")

    def apply_settings(self):
        # Load config from settings widget
        config_path = 'config.json'
        if not os.path.exists(config_path):
            return
        with open(config_path, 'r') as f:
            config = json.load(f)
        # Update AlertsManager
        self.alerts_manager.email_config['recipient'] = config.get('alert_email', '')
        self.alerts_manager.sms_config['phone_number'] = config.get('alert_phone', '')
        # Configure Twilio credentials
        self.alerts_manager.sms_config['account_sid'] = config.get('twilio_account_sid', '')
        self.alerts_manager.sms_config['auth_token'] = config.get('twilio_auth_token', '')
        self.alerts_manager.sms_config['from_number'] = config.get('twilio_from_number', '')
        self.enable_email = config.get('enable_email', True)
        self.enable_sms = config.get('enable_sms', True)
        # Update MalwareScanner engine (for future use)
        self.selected_engine = config.get('antivirus_engine', 'ClamAV')

    def init_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        logo_path = "resources/usb_hawkeye_logo.svg"
        if os.path.exists(logo_path):
            self.tray_icon.setIcon(QIcon(logo_path))
        else:
            self.tray_icon.setIcon(self.windowIcon())
        menu = QMenu()
        open_action = QAction("Open Dashboard", self)
        open_action.triggered.connect(self.showNormal)
        menu.addAction(open_action)
        scan_action = QAction("Scan Now", self)
        scan_action.triggered.connect(self.trigger_scan)
        menu.addAction(scan_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(QApplication.quit)
        menu.addAction(exit_action)
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def trigger_scan(self):
        # Trigger real scan of connected devices
        devices = self.usb_monitor.get_connected_devices()
        if devices:
            self.show_hacker_notification("USB HawkEye", f"Scanning {len(devices)} connected device(s)...", "scan")
            # Perform actual scan
            for device in devices:
                device_id = device.get('DeviceID', '')
                if device_id and os.path.exists(device_id):
                    results = self.device_scanner.scanner.scan_path(device_id)
                    if results:
                        self.show_hacker_notification("USB HawkEye", f"Threats detected in {device.get('Product', 'Unknown')}!", "threat")
                    else:
                        self.show_hacker_notification("USB HawkEye", f"{device.get('Product', 'Unknown')} is clean", "info")
        else:
            self.show_hacker_notification("USB HawkEye", "No USB devices connected to scan", "info")

    def show_hacker_notification(self, title, message, notification_type="info"):
        """Show a hacker-style notification popup"""
        self.notification_manager.show_notification(title, message, notification_type)
    
    def send_detailed_device_sms(self, device, event_type):
        """Send detailed SMS when device is connected"""
        if not self.enable_sms:
            return
            
        device_id = device.get('DeviceID', 'Unknown')
        vendor = device.get('Vendor', 'Unknown')
        product = device.get('Product', 'Unknown')
        serial = device.get('Serial', 'Unknown')
        size = device.get('Size', 'Unknown')
        
        message = f"🔌 USB Device Connected\n"
        message += f"📱 Device: {product}\n"
        message += f"🏢 Vendor: {vendor}\n"
        message += f"🆔 Serial: {serial}\n"
        message += f"💾 Size: {size}\n"
        message += f"📍 Path: {device_id}\n"
        message += f"⏰ Time: {self.get_current_time()}\n"
        message += f"🔍 Status: Scanning..."
        
        self.alerts_manager.send_sms_alert(
            message,
            self.alerts_manager.sms_config.get('phone_number', '')
        )
    
    def send_safe_device_sms(self, device):
        """Send SMS when device is confirmed safe"""
        if not self.enable_sms:
            return
            
        device_id = device.get('DeviceID', 'Unknown')
        product = device.get('Product', 'Unknown')
        
        message = f"✅ USB Device SAFE\n"
        message += f"📱 Device: {product}\n"
        message += f"📍 Path: {device_id}\n"
        message += f"🛡️ Scan Result: CLEAN\n"
        message += f"⏰ Time: {self.get_current_time()}\n"
        message += f"🎯 Status: Safe to use"
        
        self.alerts_manager.send_sms_alert(
            message,
            self.alerts_manager.sms_config.get('phone_number', '')
        )
    
    def send_threat_detected_sms(self, device, threats):
        """Send SMS when threats are detected"""
        if not self.enable_sms:
            return
            
        device_id = device.get('DeviceID', 'Unknown')
        product = device.get('Product', 'Unknown')
        threat_count = len(threats)
        
        message = f"⚠️ THREAT DETECTED!\n"
        message += f"📱 Device: {product}\n"
        message += f"📍 Path: {device_id}\n"
        message += f"🦠 Threats: {threat_count} file(s)\n"
        message += f"⏰ Time: {self.get_current_time()}\n"
        message += f"🚨 Status: QUARANTINE RECOMMENDED"
        
        # Add threat details if not too long
        if threat_count <= 3:
            for file_path, threat_type in list(threats.items())[:3]:
                filename = os.path.basename(file_path)
                message += f"\n📄 {filename}: {threat_type}"
        
        self.alerts_manager.send_sms_alert(
            message,
            self.alerts_manager.sms_config.get('phone_number', '')
        )
    
    def send_blacklisted_device_sms(self, device):
        """Send SMS when blacklisted device is connected"""
        if not self.enable_sms:
            return
            
        device_id = device.get('DeviceID', 'Unknown')
        product = device.get('Product', 'Unknown')
        vendor = device.get('Vendor', 'Unknown')
        
        message = f"🚫 BLACKLISTED DEVICE!\n"
        message += f"📱 Device: {product}\n"
        message += f"🏢 Vendor: {vendor}\n"
        message += f"📍 Path: {device_id}\n"
        message += f"⏰ Time: {self.get_current_time()}\n"
        message += f"🚨 Status: ACCESS DENIED"
        
        self.alerts_manager.send_sms_alert(
            message,
            self.alerts_manager.sms_config.get('phone_number', '')
        )
    
    def get_current_time(self):
        """Get current time in readable format"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def show_tray_message(self, title, message):
        if self.tray_icon:
            self.tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information)

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.showNormal()
            self.raise_()
            self.activateWindow()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.show_hacker_notification("USB HawkEye", "App minimized to tray. Double-click tray icon to restore.", "info")

    def on_usb_event(self, event_type, devices):
        self.apply_settings()
        self.device_scanner.update_devices(devices)
        self.access_control_widget.update_devices(devices)
        self.device_scanner.statusLabel.setText(f"Status: {event_type.capitalize()} event detected.")
        self.update_dashboard_stats(devices)
        self.log_activity(f"USB {event_type}: {len(devices)} device(s) connected.")
        self.logger.log_event("usb_event", f"{event_type}: {len(devices)} device(s) connected.")
        self.logs_viewer_widget.refresh_logs()
        
        # Send detailed SMS alerts for each device
        for device in devices:
            self.send_detailed_device_sms(device, event_type)
            # Send real alert/notification email for device events
            if self.enable_email:
                subject = f"USB HawkEye Alert: USB Device {event_type.capitalize()}"
                body = f"A USB device {event_type} event has occurred.\n\nDevice Info:\n{device}"
                self.alerts_manager.send_email_alert(
                    subject,
                    body,
                    self.alerts_manager.email_config.get('recipient', '')
                )
        
        # Real-time scan: scan all connected devices
        for device in devices:
            device_id = device.get('DeviceID', '')
            if device_id:
                # Add new device to access control system
                self.access_control_widget.access_control.add_new_device(device_id)
                
                # Real-time scan of actual device path
                if os.path.exists(device_id):
                    self.device_scanner.statusLabel.setText(f"Status: Real-time scanning {device_id}...")
                    results = self.device_scanner.scanner.scan_path(device_id)
                    if not results:
                        self.device_scanner.statusLabel.setText(f"Status: {device_id} clean.")
                        self.logger.log_event("scan", f"Device {device_id} scanned: clean.")
                        # Mark device as clean in access control
                        self.access_control_widget.access_control.mark_device_clean(device_id)
                        # Send safe device SMS
                        self.send_safe_device_sms(device)
                    else:
                        self.device_scanner.statusLabel.setText(f"Status: Threats detected in {device_id}!")
                        details = '\n'.join([f"{k}: {v}" for k, v in results.items()])
                        self.logger.log_event("threat", f"Device {device_id} scan: {details}")
                        # Mark device as threat and block it
                        self.access_control_widget.access_control.mark_device_threat(device_id)
                        # Send threat detected SMS
                        self.send_threat_detected_sms(device, results)
                        if self.alerts_manager:
                            self.alerts_manager.send_email_alert(
                                "USB HawkEye Alert: Threat Detected",
                                f"Threats detected in {len(results)} file(s):\n{details}",
                                self.alerts_manager.email_config.get('recipient', '')
                            )
        
        # Unauthorized access: check for blacklisted devices
        for device in devices:
            device_id = device.get('DeviceID', '')
            if self.access_control_widget.access_control.is_blacklisted(device_id):
                # Send blacklisted device SMS
                self.send_blacklisted_device_sms(device)
                if self.enable_email:
                    self.alerts_manager.send_email_alert(
                        "USB HawkEye Alert: Blacklisted Device Connected",
                        f"Blacklisted device connected: {device_id}",
                        self.alerts_manager.email_config.get('recipient', '')
                    )
                self.alerts_center_widget.refresh_alerts()
                self.logger.log_event("unauthorized_access", f"Blacklisted device connected: {device_id}")
                self.logs_viewer_widget.refresh_logs()
                self.show_hacker_notification("USB HawkEye", f"Blacklisted device connected: {device_id}", "threat")

    def on_scan_result(self, result):
        self.apply_settings()
        self.total_scans_count += 1
        from datetime import datetime
        self.last_scan_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if hasattr(self, 'stat_cards'):
            self.stat_cards[2][1].setText(str(self.total_scans_count))
            self.stat_cards[3][1].setText(self.last_scan_str)
        if result and isinstance(result, dict) and len(result) > 0:
            self.threat_count += len(result)
            self.log_activity(f"Threat detected: {len(result)} file(s) flagged.")
            self.logger.log_event("threat", f"{len(result)} file(s) flagged: {result}")
            
            # Mark device as threat in access control system
            # Note: This would need the device_id from the scan context
            # For now, we'll mark all scanned devices as threats if any threats are found
            for device in self.usb_monitor.get_connected_devices():
                device_id = device.get('DeviceID', '')
                if device_id and os.path.exists(device_id):
                    self.access_control_widget.access_control.mark_device_threat(device_id)
            
            # Send detailed threat SMS
            if self.enable_sms:
                threat_count = len(result)
                message = f"⚠️ MANUAL SCAN: THREATS FOUND!\n"
                message += f"🦠 Threats: {threat_count} file(s)\n"
                message += f"⏰ Time: {self.get_current_time()}\n"
                message += f"🚨 Status: DEVICE BLOCKED - IMMEDIATE ACTION REQUIRED"
                
                # Add threat details if not too long
                if threat_count <= 3:
                    for file_path, threat_type in list(result.items())[:3]:
                        filename = os.path.basename(file_path)
                        message += f"\n📄 {filename}: {threat_type}"
                
                self.alerts_manager.send_sms_alert(
                    message,
                    self.alerts_manager.sms_config.get('phone_number', '')
                )
            
            # Send email alert
            if self.enable_email:
                self.alerts_manager.send_email_alert(
                    "USB HawkEye Alert: Threat Detected - Device Blocked",
                    f"Threats detected in {len(result)} file(s). Device has been automatically blocked:\n{result}",
                    self.alerts_manager.email_config.get('recipient', '')
                )
            
            self.alerts_center_widget.refresh_alerts()
            self.show_hacker_notification("USB HawkEye", f"Threat detected! Device blocked automatically.", "threat")
        else:
            self.log_activity("Device scanned: No threats detected.")
            self.logger.log_event("scan", "Device scanned: No threats detected.")
            
            # Mark device as clean in access control system
            for device in self.usb_monitor.get_connected_devices():
                device_id = device.get('DeviceID', '')
                if device_id and os.path.exists(device_id):
                    self.access_control_widget.access_control.mark_device_clean(device_id)
            
            # Send safe scan SMS
            if self.enable_sms:
                message = f"✅ MANUAL SCAN: DEVICE SAFE\n"
                message += f"🛡️ Scan Result: CLEAN\n"
                message += f"⏰ Time: {self.get_current_time()}\n"
                message += f"🎯 Status: Device marked as clean - full access granted"
                
                self.alerts_manager.send_sms_alert(
                    message,
                    self.alerts_manager.sms_config.get('phone_number', '')
                )
        
        self.logs_viewer_widget.refresh_logs()

    def update_dashboard_stats(self, devices):
        # Update stat card values
        self.connected_devices_count = len(devices)
        for device in devices:
            self.total_devices_set.add(device.get('Serial', device.get('DeviceID', 'unknown')))
        total_devices = len(self.total_devices_set)
        # Update stat cards
        if hasattr(self, 'stat_cards'):
            self.stat_cards[0][1].setText(str(self.connected_devices_count))  # Connected Devices
            self.stat_cards[1][1].setText(str(total_devices))  # Total Devices
            self.stat_cards[2][1].setText(str(self.total_scans_count))  # Total Scans
            self.stat_cards[3][1].setText(self.last_scan_str)  # Last Scan
        # Update dashboard device blocks
        if hasattr(self, 'dashboard_device_blocks'):
            for block in self.dashboard_device_blocks:
                block.setParent(None)
            self.dashboard_device_blocks.clear()
            for i, device in enumerate(devices):
                from ui.device_scanner_widget import DeviceBlock
                block = DeviceBlock(device, self.dashboard_device_container)
                row = i // 2  # 2 blocks per row
                col = i % 2
                self.dashboard_device_layout.addWidget(block, row, col)
                self.dashboard_device_blocks.append(block)
        # Update dashboard history list
        if hasattr(self, 'dashboard_history_list'):
            self.dashboard_history_list.clear()
            for entry in self.activity_log:
                self.dashboard_history_list.addItem(entry)

    def log_activity(self, message):
        self.activity_log.append(message)
        if hasattr(self, 'dashboard_history_list'):
            self.dashboard_history_list.addItem(message)
            self.dashboard_history_list.scrollToBottom()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'cyberpunk_background'):
            self.cyberpunk_background.setGeometry(self.rect())

    def handle_logout(self):
        """Handle logout - switch back to login screen"""
        # Clear user info
        self.user_role = None
        self.username = None
        
        # Clear login form
        self.login_widget.user_input.clear()
        self.login_widget.pass_input.clear()
        
        # Switch back to login screen
        self.stacked_widget.setCurrentWidget(self.login_widget)
        
        # Update settings widget
        self.settings_widget.update_user_info(None, None)

    def dashboard_scan_selected(self):
        # Find the first device block that has focus
        selected_block = None
        for block in self.dashboard_device_blocks:
            if block.hasFocus():
                selected_block = block
                break
        
        if not selected_block:
            self.log_activity("Dashboard: Please select a device to scan.")
            return
            
        device_id = selected_block.device_info.get('DeviceID', '')
        if not device_id:
            self.log_activity("Dashboard: Invalid device selection.")
            return
            
        if not os.path.exists(device_id):
            self.log_activity(f"Dashboard: Device path not found: {device_id}")
            return
            
        self.device_scanner.statusLabel.setText(f"Status: Scanning {device_id} (from Dashboard)...")
        results = self.device_scanner.scanner.scan_path(device_id)
        
        if not results:
            msg = "No threats detected. Device is clean."
            self.device_scanner.statusLabel.setText(f"Status: {msg}")
            self.logger.log_event("scan", f"Device {device_id} scanned: clean.")
            
            # Send safe device SMS
            if self.enable_sms:
                product = selected_block.device_info.get('Product', 'Unknown')
                message = f"✅ DASHBOARD SCAN: SAFE\n"
                message += f"📱 Device: {product}\n"
                message += f"📍 Path: {device_id}\n"
                message += f"🛡️ Scan Result: CLEAN\n"
                message += f"⏰ Time: {self.get_current_time()}\n"
                message += f"🎯 Status: Safe to use"
                
                self.alerts_manager.send_sms_alert(
                    message,
                    self.alerts_manager.sms_config.get('phone_number', '')
                )
        else:
            msg = f"Threats detected in {len(results)} file(s)!"
            self.device_scanner.statusLabel.setText(f"Status: {msg}")
            details = '\n'.join([f"{k}: {v}" for k, v in results.items()])
            self.logger.log_event("threat", f"Device {device_id} scan: {details}")
            
            # Send detailed threat SMS
            if self.enable_sms:
                product = selected_block.device_info.get('Product', 'Unknown')
                threat_count = len(results)
                message = f"⚠️ DASHBOARD SCAN: THREATS!\n"
                message += f"📱 Device: {product}\n"
                message += f"📍 Path: {device_id}\n"
                message += f"🦠 Threats: {threat_count} file(s)\n"
                message += f"⏰ Time: {self.get_current_time()}\n"
                message += f"🚨 Status: QUARANTINE RECOMMENDED"
                
                # Add threat details if not too long
                if threat_count <= 3:
                    for file_path, threat_type in list(results.items())[:3]:
                        filename = os.path.basename(file_path)
                        message += f"\n📄 {filename}: {threat_type}"
                
                self.alerts_manager.send_sms_alert(
                    message,
                    self.alerts_manager.sms_config.get('phone_number', '')
                )
            
            # Send email alert
            if self.alerts_manager:
                self.alerts_manager.send_email_alert(
                    "USB HawkEye Alert: Threat Detected",
                    f"Threats detected in {len(results)} file(s):\n{details}",
                    self.alerts_manager.email_config.get('recipient', '')
                )

def main():
    app = QApplication(sys.argv)
    
    # Set application icon
    logo_path = "resources/usb_hawkeye_logo.svg"
    if os.path.exists(logo_path):
        app.setWindowIcon(QIcon(logo_path))
    
    # Set global cyberpunk theme stylesheet
    app.setStyleSheet('''
        QWidget, QMainWindow, QDialog, QTabWidget, QFrame, QGroupBox {
            background: rgba(10, 10, 10, 0.3);
            color: #00ff00;
            font-family: 'JetBrains Mono', 'Fira Mono', 'DejaVu Sans Mono', 'Consolas', monospace;
            font-size: 11px;
            border-radius: 0px;
        }
        
        QFrame[cyberpunk="true"] {
            border: 1px solid #00ff00;
            background: #0a0a0a;
        }
        
        QTabWidget::pane {
            background: rgba(10, 10, 10, 0.3);
            border: 1px solid #00ff00;
            border-radius: 0px;
        }
        
        QTabBar::tab {
            background: #1a1a1a;
            color: #00ff00;
            border: 1px solid #00ff00;
            border-bottom: none;
            border-radius: 0px;
            padding: 8px 16px;
            margin-right: 2px;
            font-family: 'Consolas', monospace;
            font-weight: normal;
            font-size: 10px;
            letter-spacing: 0px;
            text-transform: none;
        }
        
        QTabBar::tab:selected {
            background: #00ff00;
            color: #000000;
            border: 1px solid #00ff00;
        }
        
        QTabBar::tab:hover {
            background: #1f1f1f;
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        QTableWidget, QTableView, QListWidget, QTreeWidget {
            background: rgba(10, 10, 10, 0.3);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            selection-background-color: rgba(26, 26, 26, 0.7);
            selection-color: #00ff00;
            alternate-background-color: rgba(15, 15, 15, 0.5);
            gridline-color: rgba(26, 26, 26, 0.5);
        }
        
        QTableWidget::item, QListWidget::item, QTreeWidget::item {
            padding: 4px;
            border-bottom: 1px solid rgba(26, 26, 26, 0.5);
            border-radius: 0px;
            margin: 0px;
            background: transparent;
        }
        
        QTableWidget::item:hover, QListWidget::item:hover, QTreeWidget::item:hover {
            background: rgba(26, 26, 26, 0.7);
            border: 1px solid #00ff00;
        }
        
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
            background: rgba(26, 26, 26, 0.7);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 6px;
            selection-background-color: rgba(26, 26, 26, 0.8);
            selection-color: #00ff00;
            font-family: 'Consolas', monospace;
            font-size: 11px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {
            border: 1px solid #00ff00;
            background: rgba(15, 15, 15, 0.8);
        }
        
        QComboBox::drop-down {
            border: none;
            background: transparent;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #00ff00;
            margin-right: 8px;
        }
        
        QComboBox QAbstractItemView {
            background: rgba(10, 10, 10, 0.9);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            selection-background-color: rgba(26, 26, 26, 0.8);
            selection-color: #00ff00;
        }
        
        QPushButton {
            background: rgba(26, 26, 26, 0.7);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 8px 16px;
            font-weight: normal;
            font-family: 'Consolas', monospace;
            font-size: 11px;
            letter-spacing: 0px;
            text-transform: none;
        }
        
        QPushButton:hover {
            background: rgba(15, 15, 15, 0.8);
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        QPushButton:pressed {
            background: #00ff00;
            color: #000000;
            border: 1px solid #00ff00;
        }
        
        QPushButton:disabled {
            background: rgba(26, 26, 26, 0.5);
            color: #666666;
            border: 1px solid #666666;
        }
        
        QScrollBar:vertical, QScrollBar:horizontal {
            background: rgba(26, 26, 26, 0.7);
            border: 1px solid #00ff00;
            border-radius: 0px;
            width: 12px;
            height: 12px;
        }
        
        QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
            background: #00ff00;
            border-radius: 0px;
            min-height: 20px;
            min-width: 20px;
        }
        
        QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
            background: #00ff00;
        }
        
        QScrollBar::add-line, QScrollBar::sub-line, QScrollBar::add-page, QScrollBar::sub-page {
            background: transparent;
            border: none;
        }
        
        QHeaderView::section {
            background: rgba(26, 26, 26, 0.7);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 6px;
            font-weight: normal;
            font-family: 'Consolas', monospace;
        }
        
        QMenu {
            background: rgba(10, 10, 10, 0.9);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 4px;
        }
        
        QMenu::item {
            padding: 6px 16px;
            border-radius: 0px;
            margin: 0px;
        }
        
        QMenu::item:selected {
            background: rgba(26, 26, 26, 0.8);
            color: #00ff00;
            border: 1px solid #00ff00;
        }
        
        QToolTip {
            background: rgba(10, 10, 10, 0.9);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            padding: 6px;
            font-family: 'Consolas', monospace;
            font-size: 10px;
        }
        
        QCheckBox, QRadioButton {
            background: transparent;
            color: #00ff00;
            border: none;
            font-family: 'Consolas', monospace;
            spacing: 6px;
        }
        
        QCheckBox::indicator, QRadioButton::indicator {
            border: 1px solid #00ff00;
            background: rgba(26, 26, 26, 0.7);
            border-radius: 0px;
            width: 14px;
            height: 14px;
        }
        
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {
            background: #00ff00;
            border: 1px solid #00ff00;
        }
        
        QCheckBox::indicator:hover, QRadioButton::indicator:hover {
            border: 1px solid #00ff00;
        }
        
        QProgressBar {
            background: rgba(26, 26, 26, 0.7);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            text-align: center;
            font-family: 'Consolas', monospace;
            font-weight: normal;
        }
        
        QProgressBar::chunk {
            background: #00ff00;
            border-radius: 0px;
        }
        
        QDialog, QMessageBox {
            background: rgba(10, 10, 10, 0.9);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
        }
        
        QMessageBox QPushButton {
            min-width: 80px;
            min-height: 25px;
        }
        
        QLabel {
            color: #00ff00;
            font-family: 'Consolas', monospace;
        }
        
        QGroupBox {
            background: rgba(10, 10, 10, 0.3);
            color: #00ff00;
            border: 1px solid #00ff00;
            border-radius: 0px;
            margin-top: 8px;
            padding-top: 8px;
            font-weight: normal;
            font-family: 'Consolas', monospace;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 8px;
            padding: 0 8px 0 8px;
            color: #00ff00;
            background: rgba(10, 10, 10, 0.8);
            border-radius: 0px;
        }
    ''')
    window = MainDashboard()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
