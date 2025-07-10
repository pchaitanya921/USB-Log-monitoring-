from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QComboBox, QPushButton, QHBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QFrame, QDialog, QScrollArea, QCompleter
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
import json
import os
from ui.register_dialog import RegisterDialog
import smtplib
from email.mime.text import MIMEText
from ui.email_compose_dialog import EmailComposeDialog

CONFIG_FILE = 'config.json'

# Add these SMTP config variables at the top of the file (replace with your real credentials)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = 'chaitanyasai9391@gmail.com'  # Updated to provided email
SMTP_PASSWORD = 'gbnzgqbxiwgwddvq'      # Updated to provided app password

class SettingsWidget(QWidget):
    def __init__(self, parent=None, username=None, role=None, logout_callback=None, scan_callback=None):
        super().__init__(parent)
        self.username = username
        self.role = role
        self.logout_callback = logout_callback
        self.scan_callback = scan_callback
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #00ffe7;
                border-radius: 0px;
                padding: 15px;
                margin-bottom: 10px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        settings_icon = QLabel()
        settings_icon.setPixmap(QPixmap("resources/icons/settings.svg").scaled(28, 28, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        settings_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(settings_icon)
        title = QLabel("SYSTEM SETTINGS")
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("color: #00ffe7; text-shadow: 0 0 10px #00ffe7, 0 0 20px #00ffe7; letter-spacing: 2px; margin: 5px 0;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # User info and actions
        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 10px;
            }
        """)
        user_layout = QHBoxLayout(user_frame)
        self.user_label = QLabel(f"👤 Logged in as: <b>{self.username or '-'} ({self.role or '-'})</b>" if self.username or self.role else "👤 Not logged in")
        self.user_label.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 12, QFont.Bold))
        self.user_label.setStyleSheet("color: #00ffe7; text-shadow: 0 0 5px #00ffe7;")
        user_layout.addWidget(self.user_label)
        self.change_pass_btn = QPushButton("Change Password")
        self.change_pass_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0,255,231,0.12);
                color: #00ffe7;
                border: 2px solid #00ffe7;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(0,255,231,0.18);
                color: #39ff14;
                border: 2px solid #39ff14;
            }
        """)
        user_layout.addWidget(self.change_pass_btn)
        self.login_btn = QPushButton("🔐 LOGIN")
        self.login_btn.setEnabled(not self.username)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background: rgba(64, 64, 64, 0.5);
                color: #666666;
                border: 2px solid #666666;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
        """)
        user_layout.addWidget(self.login_btn)
        self.logout_btn = QPushButton("🚪 LOGOUT")
        self.logout_btn.setEnabled(bool(self.username))
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 0, 0, 0.3), 
                    stop:1 rgba(255, 0, 0, 0.2));
                color: #ff4444;
                border: 2px solid #ff4444;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
                box-shadow: 0 0 8px #ff4444;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 0, 0, 0.4), 
                    stop:1 rgba(255, 0, 0, 0.3));
                color: #ff6666;
                border: 2px solid #ff6666;
                box-shadow: 0 0 12px #ff6666;
            }
        """)
        self.logout_btn.clicked.connect(self.handle_logout)
        user_layout.addWidget(self.logout_btn)
        header_layout.addWidget(user_frame)
        layout.addWidget(header_frame)
        
        # --- Settings Section ---
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #00ffe7;
                border-radius: 0px;
                padding: 20px;
            }
        """)
        settings_layout = QVBoxLayout(settings_frame)
        settings_layout.setSpacing(20)
        
        # Alert Recipients & Preferences
        recipients_frame = QFrame()
        recipients_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #39ff14;
                border-radius: 0px;
                padding: 15px;
            }
        """)
        recipients_vbox = QVBoxLayout(recipients_frame)
        recipients_vbox.setSpacing(10)
        recipients_title = QLabel("ALERT RECIPIENTS & PREFERENCES")
        recipients_title.setFont(QFont("Consolas", 14, QFont.Bold))
        recipients_title.setStyleSheet("color: #39ff14; text-shadow: 0 0 5px #39ff14; margin-bottom: 10px;")
        recipients_vbox.addWidget(recipients_title)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address for alerts...")
        recipients_vbox.addWidget(QLabel("📧 Alert Email:"))
        recipients_vbox.addWidget(self.email_input)
        # Full, up-to-date, alphabetically sorted country code list with country names
        country_codes = [
            '+93 (Afghanistan)', '+355 (Albania)', '+213 (Algeria)', '+1684 (American Samoa)', '+376 (Andorra)', '+244 (Angola)', '+1264 (Anguilla)', '+672 (Antarctica)', '+1268 (Antigua and Barbuda)', '+54 (Argentina)', '+374 (Armenia)', '+297 (Aruba)', '+61 (Australia)', '+43 (Austria)', '+994 (Azerbaijan)', '+1242 (Bahamas)', '+973 (Bahrain)', '+880 (Bangladesh)', '+1246 (Barbados)', '+375 (Belarus)', '+32 (Belgium)', '+501 (Belize)', '+229 (Benin)', '+1441 (Bermuda)', '+975 (Bhutan)', '+591 (Bolivia)', '+387 (Bosnia and Herzegovina)', '+267 (Botswana)', '+55 (Brazil)', '+246 (British Indian Ocean Territory)', '+1284 (British Virgin Islands)', '+673 (Brunei)', '+359 (Bulgaria)', '+226 (Burkina Faso)', '+257 (Burundi)', '+855 (Cambodia)', '+237 (Cameroon)', '+1 (Canada)', '+238 (Cape Verde)', '+1345 (Cayman Islands)', '+236 (Central African Republic)', '+235 (Chad)', '+56 (Chile)', '+86 (China)', '+61 (Christmas Island)', '+61 (Cocos Islands)', '+57 (Colombia)', '+269 (Comoros)', '+682 (Cook Islands)', '+506 (Costa Rica)', '+385 (Croatia)', '+53 (Cuba)', '+599 (Curacao)', '+357 (Cyprus)', '+420 (Czech Republic)', '+243 (Democratic Republic of the Congo)', '+45 (Denmark)', '+253 (Djibouti)', '+1767 (Dominica)', '+1809 (Dominican Republic)', '+1829 (Dominican Republic)', '+1849 (Dominican Republic)', '+670 (East Timor)', '+593 (Ecuador)', '+20 (Egypt)', '+503 (El Salvador)', '+240 (Equatorial Guinea)', '+291 (Eritrea)', '+372 (Estonia)', '+251 (Ethiopia)', '+500 (Falkland Islands)', '+298 (Faroe Islands)', '+679 (Fiji)', '+358 (Finland)', '+33 (France)', '+594 (French Guiana)', '+689 (French Polynesia)', '+241 (Gabon)', '+220 (Gambia)', '+995 (Georgia)', '+49 (Germany)', '+233 (Ghana)', '+350 (Gibraltar)', '+30 (Greece)', '+299 (Greenland)', '+1473 (Grenada)', '+590 (Guadeloupe)', '+1671 (Guam)', '+502 (Guatemala)', '+44 (Guernsey)', '+224 (Guinea)', '+245 (Guinea-Bissau)', '+592 (Guyana)', '+509 (Haiti)', '+504 (Honduras)', '+852 (Hong Kong)', '+36 (Hungary)', '+354 (Iceland)', '+91 (India)', '+62 (Indonesia)', '+98 (Iran)', '+964 (Iraq)', '+353 (Ireland)', '+44 (Isle of Man)', '+972 (Israel)', '+39 (Italy)', '+225 (Ivory Coast)', '+1876 (Jamaica)', '+81 (Japan)', '+44 (Jersey)', '+962 (Jordan)', '+7 (Kazakhstan)', '+254 (Kenya)', '+686 (Kiribati)', '+383 (Kosovo)', '+965 (Kuwait)', '+996 (Kyrgyzstan)', '+856 (Laos)', '+371 (Latvia)', '+961 (Lebanon)', '+266 (Lesotho)', '+231 (Liberia)', '+218 (Libya)', '+423 (Liechtenstein)', '+370 (Lithuania)', '+352 (Luxembourg)', '+853 (Macau)', '+389 (Macedonia)', '+261 (Madagascar)', '+265 (Malawi)', '+60 (Malaysia)', '+960 (Maldives)', '+223 (Mali)', '+356 (Malta)', '+692 (Marshall Islands)', '+596 (Martinique)', '+222 (Mauritania)', '+230 (Mauritius)', '+262 (Mayotte)', '+52 (Mexico)', '+691 (Micronesia)', '+373 (Moldova)', '+377 (Monaco)', '+976 (Mongolia)', '+382 (Montenegro)', '+1664 (Montserrat)', '+212 (Morocco)', '+258 (Mozambique)', '+95 (Myanmar)', '+264 (Namibia)', '+674 (Nauru)', '+977 (Nepal)', '+31 (Netherlands)', '+599 (Netherlands Antilles)', '+687 (New Caledonia)', '+64 (New Zealand)', '+505 (Nicaragua)', '+227 (Niger)', '+234 (Nigeria)', '+683 (Niue)', '+672 (Norfolk Island)', '+850 (North Korea)', '+1670 (Northern Mariana Islands)', '+47 (Norway)', '+968 (Oman)', '+92 (Pakistan)', '+680 (Palau)', '+970 (Palestine)', '+507 (Panama)', '+675 (Papua New Guinea)', '+595 (Paraguay)', '+51 (Peru)', '+63 (Philippines)', '+48 (Poland)', '+351 (Portugal)', '+1787 (Puerto Rico)', '+1939 (Puerto Rico)', '+974 (Qatar)', '+242 (Republic of the Congo)', '+40 (Romania)', '+7 (Russia)', '+250 (Rwanda)', '+590 (Saint Barthelemy)', '+290 (Saint Helena)', '+1869 (Saint Kitts and Nevis)', '+1758 (Saint Lucia)', '+590 (Saint Martin)', '+508 (Saint Pierre and Miquelon)', '+1784 (Saint Vincent and the Grenadines)', '+685 (Samoa)', '+378 (San Marino)', '+239 (Sao Tome and Principe)', '+966 (Saudi Arabia)', '+221 (Senegal)', '+381 (Serbia)', '+248 (Seychelles)', '+232 (Sierra Leone)', '+65 (Singapore)', '+421 (Slovakia)', '+386 (Slovenia)', '+677 (Solomon Islands)', '+252 (Somalia)', '+27 (South Africa)', '+82 (South Korea)', '+211 (South Sudan)', '+34 (Spain)', '+94 (Sri Lanka)', '+249 (Sudan)', '+597 (Suriname)', '+47 (Svalbard and Jan Mayen)', '+268 (Swaziland)', '+46 (Sweden)', '+41 (Switzerland)', '+963 (Syria)', '+886 (Taiwan)', '+992 (Tajikistan)', '+255 (Tanzania)', '+66 (Thailand)', '+228 (Togo)', '+690 (Tokelau)', '+676 (Tonga)', '+1868 (Trinidad and Tobago)', '+216 (Tunisia)', '+90 (Turkey)', '+993 (Turkmenistan)', '+1649 (Turks and Caicos Islands)', '+688 (Tuvalu)', '+256 (Uganda)', '+380 (Ukraine)', '+971 (United Arab Emirates)', '+44 (United Kingdom)', '+1 (United States)', '+598 (Uruguay)', '+998 (Uzbekistan)', '+678 (Vanuatu)', '+379 (Vatican)', '+58 (Venezuela)', '+84 (Vietnam)', '+1284 (Virgin Islands, British)', '+1340 (Virgin Islands, U.S.)', '+681 (Wallis and Futuna)', '+212 (Western Sahara)', '+967 (Yemen)', '+260 (Zambia)', '+263 (Zimbabwe)'
        ]
        country_codes = sorted(country_codes, key=lambda x: x.split(' ', 1)[1].lower())
        self.country_code_combo = QComboBox()
        self.country_code_combo.addItems(country_codes)
        self.country_code_combo.setCurrentText('+91 (India)')
        # Make the dropdown searchable
        completer = QCompleter(country_codes)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.country_code_combo.setEditable(True)
        self.country_code_combo.setCompleter(completer)
        phone_hbox = QHBoxLayout()
        phone_hbox.addWidget(self.country_code_combo)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number (e.g., 9944273645)")
        phone_hbox.addWidget(self.phone_input)
        recipients_vbox.addWidget(QLabel("📱 Alert Phone (SMS) with Country Code:"))
        recipients_vbox.addLayout(phone_hbox)
        self.pref_email = QCheckBox("Enable Email Alerts")
        self.pref_sms = QCheckBox("Enable SMS Alerts")
        self.pref_email.setChecked(True)
        self.pref_sms.setChecked(True)
        prefs_hbox = QHBoxLayout()
        prefs_hbox.addWidget(self.pref_email)
        prefs_hbox.addWidget(self.pref_sms)
        recipients_vbox.addLayout(prefs_hbox)
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Low", "Medium", "High", "Critical"])
        self.level_combo.setCurrentIndex(2)
        recipients_vbox.addWidget(QLabel("Alert Level:"))
        recipients_vbox.addWidget(self.level_combo)
        # Test Email/SMS buttons
        test_hbox = QHBoxLayout()
        self.test_email_btn = QPushButton("Test Email")
        self.test_email_btn.clicked.connect(self.test_email)
        self.test_sms_btn = QPushButton("Test SMS")
        self.test_sms_btn.clicked.connect(self.test_sms)
        self.send_email_btn = QPushButton("Send Email")
        self.send_email_btn.setStyleSheet(self.test_email_btn.styleSheet())
        self.send_email_btn.clicked.connect(self.open_email_compose_dialog)
        test_hbox.addWidget(self.test_email_btn)
        test_hbox.addWidget(self.test_sms_btn)
        test_hbox.addWidget(self.send_email_btn)
        recipients_vbox.addLayout(test_hbox)
        settings_layout.addWidget(recipients_frame)
        
        # --- Appearance Section ---
        appearance_frame = QFrame()
        appearance_frame.setStyleSheet("border: 1px solid #00ffe7; border-radius: 0px; padding: 15px;")
        appearance_vbox = QVBoxLayout(appearance_frame)
        appearance_vbox.setSpacing(10)
        appearance_title = QLabel("APPEARANCE & PERSONALIZATION")
        appearance_title.setFont(QFont("Consolas", 14, QFont.Bold))
        appearance_title.setStyleSheet("color: #00ffe7; margin-bottom: 10px;")
        appearance_vbox.addWidget(appearance_title)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Cyberpunk", "Dark", "Light"])
        self.theme_combo.setCurrentIndex(0)
        appearance_vbox.addWidget(QLabel("Theme:"))
        appearance_vbox.addWidget(self.theme_combo)
        settings_layout.addWidget(appearance_frame)
        
        # --- Session Section ---
        session_frame = QFrame()
        session_frame.setStyleSheet("border: 1px solid #00ffe7; border-radius: 0px; padding: 15px;")
        session_vbox = QVBoxLayout(session_frame)
        session_vbox.setSpacing(10)
        session_title = QLabel("SECURITY & SESSION")
        session_title.setFont(QFont("Consolas", 14, QFont.Bold))
        session_title.setStyleSheet("color: #00ffe7; margin-bottom: 10px;")
        session_vbox.addWidget(session_title)
        self.session_timeout_combo = QComboBox()
        self.session_timeout_combo.addItems(["5 min", "10 min", "30 min", "60 min", "Never"])
        self.session_timeout_combo.setCurrentIndex(2)
        session_vbox.addWidget(QLabel("Session Timeout:"))
        session_vbox.addWidget(self.session_timeout_combo)
        settings_layout.addWidget(session_frame)
        
        # --- Export/Import/Reset Section ---
        export_frame = QFrame()
        export_frame.setStyleSheet("border: 1px solid #00ffe7; border-radius: 0px; padding: 15px;")
        export_hbox = QHBoxLayout(export_frame)
        self.export_btn = QPushButton("Export Settings")
        self.export_btn.clicked.connect(self.export_settings)
        self.import_btn = QPushButton("Import Settings")
        self.import_btn.clicked.connect(self.import_settings)
        self.reset_btn = QPushButton("Reset All Settings")
        self.reset_btn.clicked.connect(self.reset_settings)
        export_hbox.addWidget(self.export_btn)
        export_hbox.addWidget(self.import_btn)
        export_hbox.addWidget(self.reset_btn)
        settings_layout.addWidget(export_frame)
        
        # --- User Management Section (Admin only) ---
        if self.role == 'admin':
            self.add_user_management_section(settings_layout)
        
        # --- Save Button ---
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(0, 255, 231, 0.25),
                    stop:1 rgba(0, 255, 231, 0.12));
                color: #00ffe7;
                border: 2px solid #00ffe7;
                border-radius: 12px;
                padding: 10px 18px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(0, 255, 231, 0.18);
                color: #39ff14;
                border: 2px solid #39ff14;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        settings_layout.addWidget(save_btn)
        settings_frame.setLayout(settings_layout)
        layout.addWidget(settings_frame)
        layout.addStretch(1)

        # At the end of init_ui, add content_widget to scroll area and scroll to main_layout
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def save_settings(self):
        config = {
            'alert_email': self.email_input.text().strip(),
            'alert_phone': f"{self.country_code_combo.currentText().split()[0]}{self.phone_input.text().strip()}",
            'enable_email': self.pref_email.isChecked(),
            'enable_sms': self.pref_sms.isChecked(),
            'alert_level': self.level_combo.currentText(),
            'twilio_account_sid': 'AC4544919cc73bcf457fb39c6233172cc9',
            'twilio_auth_token': 'eb4db71b98889b2f36b9d5f639368b33',
            'twilio_from_number': '+13094980484'
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    def load_settings(self):
        if not os.path.exists(CONFIG_FILE):
            return
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        self.email_input.setText(config.get('alert_email', ''))
        phone = config.get('alert_phone', '')
        if phone:
            # Try to split country code and number
            for i in range(min(5, len(phone))):
                if phone[:i].startswith('+') and phone[i:].isdigit():
                    self.country_code_combo.setCurrentText(phone[:i])
                    self.phone_input.setText(phone[i:])
                    break
            else:
                self.phone_input.setText(phone)
        self.pref_email.setChecked(config.get('enable_email', True))
        self.pref_sms.setChecked(config.get('enable_sms', True))
        idx = self.level_combo.findText(config.get('alert_level', 'Medium'))
        if idx >= 0:
            self.level_combo.setCurrentIndex(idx)
        idx = self.theme_combo.findText(config.get('theme', 'Cyberpunk'))
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)
        idx = self.session_timeout_combo.findText(config.get('session_timeout', '30 min'))
        if idx >= 0:
            self.session_timeout_combo.setCurrentIndex(idx)
        QMessageBox.information(self, "Import Settings", f"Settings imported from {CONFIG_FILE}")

    def handle_logout(self):
        if self.logout_callback:
            self.logout_callback()
    
    def update_user_info(self, username, role, email=None):
        self.username = username
        self.role = role
        self.email = email
        if username or role:
            self.user_label.setText(f"👤 Logged in as: <b>{username or '-'} ({role or '-'})</b>\n📧 {email or '-'}")
        else:
            self.user_label.setText("👤 Not logged in")

    def handle_scan(self):
        if self.scan_callback:
            self.scan_callback()
    
    def test_sms(self):
        """Test SMS functionality with Twilio"""
        try:
            from core.alerts import AlertsManager
            import json
            
            # Load current config
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                
                # Create alerts manager with Twilio config
                alerts_manager = AlertsManager()
                alerts_manager.sms_config = {
                    'account_sid': config.get('twilio_account_sid', ''),
                    'auth_token': config.get('twilio_auth_token', ''),
                    'from_number': config.get('twilio_from_number', ''),
                    'phone_number': config.get('alert_phone', '')
                }
                
                # Send test SMS
                success = alerts_manager.send_sms_alert(
                    "USB HawkEye Test: SMS notifications are working! 🔥", 
                    config.get('alert_phone', '')
                )
                
                if success:
                    QMessageBox.information(self, "SMS Test", "Test SMS sent successfully! Check your phone.")
                else:
                    QMessageBox.warning(self, "SMS Test", "Failed to send test SMS. Check Twilio credentials.")
            else:
                QMessageBox.warning(self, "SMS Test", "Configuration file not found.")
                
        except Exception as e:
            QMessageBox.critical(self, "SMS Test Error", f"Error testing SMS: {str(e)}")
    
    def test_email(self):
        recipient = self.email_input.text().strip()
        if not recipient:
            QMessageBox.warning(self, "Test Email", "Please enter a recipient email address in the settings.")
            return
        try:
            # Send a real alert message instead of a test message
            msg = MIMEText("A real USB HawkEye alert: A USB device event has occurred.\n\nThis is a real alert message, not a test.")
            msg['Subject'] = 'USB HawkEye Real Alert Notification'
            msg['From'] = SMTP_USERNAME
            msg['To'] = recipient

            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [recipient], msg.as_string())
            server.quit()
            QMessageBox.information(self, "Test Email", f"Real alert email sent to {recipient}!")
        except Exception as e:
            QMessageBox.critical(self, "Test Email Failed", f"Failed to send real alert email: {str(e)}")
    
    def open_email_compose_dialog(self):
        dialog = EmailComposeDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            recipient, subject, body = dialog.get_email_data()
            try:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = SMTP_USERNAME
                msg['To'] = recipient
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.sendmail(SMTP_USERNAME, [recipient], msg.as_string())
                server.quit()
                QMessageBox.information(self, "Email Sent", f"Email sent to {recipient}!")
            except Exception as e:
                QMessageBox.critical(self, "Email Failed", f"Failed to send email: {str(e)}")
    
    def add_user_management_section(self, layout):
        # User Management Section with enhanced styling
        user_mgmt_frame = QFrame()
        user_mgmt_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #ff00cc;
                border-radius: 0px;
                padding: 20px;
                margin-top: 20px;
            }
        """)
        user_mgmt_layout = QVBoxLayout(user_mgmt_frame)
        user_mgmt_layout.setSpacing(15)
        
        # User Management Title
        user_mgmt_title = QLabel("👥 USER MANAGEMENT (ADMIN ONLY)")
        user_mgmt_title.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 16, QFont.Bold))
        user_mgmt_title.setStyleSheet("""
            color: #ff00cc; 
            text-shadow: 0 0 10px #ff00cc, 0 0 20px #ff00cc;
            letter-spacing: 2px;
            margin: 5px 0;
        """)
        user_mgmt_layout.addWidget(user_mgmt_title)
        
        # User Management Buttons
        user_btn_frame = QFrame()
        user_btn_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #ff00cc;
                border-radius: 0px;
                padding: 15px;
            }
        """)
        user_btn_layout = QHBoxLayout(user_btn_frame)
        user_btn_layout.setSpacing(10)
        
        self.add_user_btn = QPushButton("➕ ADD USER")
        self.add_user_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(57, 255, 20, 0.3), 
                    stop:1 rgba(57, 255, 20, 0.2));
                color: #39ff14;
                border: 2px solid #39ff14;
                border-radius: 8px;
                padding: 10px 15px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
                box-shadow: 0 0 8px #39ff14;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(57, 255, 20, 0.4), 
                    stop:1 rgba(57, 255, 20, 0.3));
                color: #00ffe7;
                border: 2px solid #00ffe7;
                box-shadow: 0 0 12px #00ffe7;
            }
        """)
        self.add_user_btn.clicked.connect(self.add_user)
        user_btn_layout.addWidget(self.add_user_btn)
        
        self.delete_user_btn = QPushButton("🗑️ DELETE USER")
        self.delete_user_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 68, 68, 0.3), 
                    stop:1 rgba(255, 68, 68, 0.2));
                color: #FF4444;
                border: 2px solid #FF4444;
                border-radius: 8px;
                padding: 10px 15px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
                box-shadow: 0 0 8px #FF4444;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 68, 68, 0.4), 
                    stop:1 rgba(255, 68, 68, 0.3));
                color: #ff6666;
                border: 2px solid #ff6666;
                box-shadow: 0 0 12px #ff6666;
            }
        """)
        self.delete_user_btn.clicked.connect(self.delete_user)
        user_btn_layout.addWidget(self.delete_user_btn)
        
        self.refresh_users_btn = QPushButton("🔄 REFRESH")
        self.refresh_users_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(0, 255, 231, 0.3), 
                    stop:1 rgba(0, 255, 231, 0.2));
                color: #00ffe7;
                border: 2px solid #00ffe7;
                border-radius: 8px;
                padding: 10px 15px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
                box-shadow: 0 0 8px #00ffe7;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(0, 255, 231, 0.4), 
                    stop:1 rgba(0, 255, 231, 0.3));
                color: #39ff14;
                border: 2px solid #39ff14;
                box-shadow: 0 0 12px #39ff14;
            }
        """)
        self.refresh_users_btn.clicked.connect(self.refresh_users_table)
        user_btn_layout.addWidget(self.refresh_users_btn)
        
        user_mgmt_layout.addWidget(user_btn_frame)
        
        # Users Table with enhanced styling
        table_frame = QFrame()
        table_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: 1px solid #ff00cc;
                border-radius: 0px;
                padding: 10px;
            }
        """)
        table_layout = QVBoxLayout(table_frame)
        
        table_title = QLabel("📊 REGISTERED USERS")
        table_title.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 12, QFont.Bold))
        table_title.setStyleSheet("color: #ff00cc; text-shadow: 0 0 5px #ff00cc; margin-bottom: 10px;")
        table_layout.addWidget(table_title)
        
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(3)
        self.users_table.setHorizontalHeaderLabels(['👤 Username', '🎭 Role', '⚡ Actions'])
        self.users_table.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 10))
        self.users_table.setStyleSheet("""
            QTableWidget {
                background: transparent;
                color: #ff00cc;
                border: 1px solid #ff00cc;
                border-radius: 0px;
                alternate-background-color: transparent;
            }
        """)
        table_layout.addWidget(self.users_table)
        
        user_mgmt_layout.addWidget(table_frame)
        layout.addWidget(user_mgmt_frame)
        
        # Load initial users
        self.refresh_users_table()
    
    def add_user(self):
        register_dialog = RegisterDialog(self)
        if register_dialog.exec_() == register_dialog.Accepted:
            self.refresh_users_table()
            QMessageBox.information(self, "User Added", f"User '{register_dialog.username}' has been added successfully.")
    
    def delete_user(self):
        current_row = self.users_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete.")
            return
        
        item = self.users_table.item(current_row, 0)
        if item is None:
            QMessageBox.warning(self, "No Selection", "Please select a user to delete.")
            return
        username = item.text()
        if username == self.username:
            QMessageBox.warning(self, "Cannot Delete", "You cannot delete your own account.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete user '{username}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                users = self.load_users()
                if username in users:
                    del users[username]
                    with open('users.json', 'w') as f:
                        json.dump(users, f, indent=2)
                    self.refresh_users_table()
                    QMessageBox.information(self, "User Deleted", f"User '{username}' has been deleted.")
                else:
                    QMessageBox.warning(self, "User Not Found", f"User '{username}' not found.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {str(e)}")
    
    def refresh_users_table(self):
        try:
            users = self.load_users()
            self.users_table.setRowCount(len(users))
            
            for row, (username, user_data) in enumerate(users.items()):
                self.users_table.setItem(row, 0, QTableWidgetItem(username))
                self.users_table.setItem(row, 1, QTableWidgetItem(user_data.get('role', 'user')))
                
                # Add action button
                action_btn = QPushButton("Delete")
                action_btn.setStyleSheet("background-color: #8B0000; color: white; border: 1px solid #FF0000;")
                action_btn.clicked.connect(lambda checked, row=row: self.delete_user_at_row(row))
                self.users_table.setCellWidget(row, 2, action_btn)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load users: {str(e)}")
    
    def delete_user_at_row(self, row):
        item = self.users_table.item(row, 0)
        if item is None:
            return
        username = item.text()
        if username == self.username:
            QMessageBox.warning(self, "Cannot Delete", "You cannot delete your own account.")
            return
        
        reply = QMessageBox.question(self, "Confirm Delete", 
                                   f"Are you sure you want to delete user '{username}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                users = self.load_users()
                if username in users:
                    del users[username]
                    with open('users.json', 'w') as f:
                        json.dump(users, f, indent=2)
                    self.refresh_users_table()
                    QMessageBox.information(self, "User Deleted", f"User '{username}' has been deleted.")
                else:
                    QMessageBox.warning(self, "User Not Found", f"User '{username}' not found.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete user: {str(e)}")
    
    def load_users(self):
        if not os.path.exists('users.json'):
            # Create default users if file doesn't exist
            default = {
                'admin': {
                    'password': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # admin123
                    'role': 'admin'
                },
                'user': {
                    'password': '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',  # user123
                    'role': 'user'
                }
            }
            with open('users.json', 'w') as f:
                json.dump(default, f, indent=2)
            return default
        with open('users.json', 'r') as f:
            return json.load(f) 

    def export_settings(self):
        config = {
            'alert_email': self.email_input.text().strip(),
            'alert_phone': self.phone_input.text().strip(),
            'enable_email': self.pref_email.isChecked(),
            'enable_sms': self.pref_sms.isChecked(),
            'alert_level': self.level_combo.currentText(),
            'theme': self.theme_combo.currentText(),
            'session_timeout': self.session_timeout_combo.currentText(),
        }
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Settings", "settings.json", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(config, f, indent=2)
                QMessageBox.information(self, "Export Settings", f"Settings exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export settings: {str(e)}")

    def import_settings(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Settings", "", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    config = json.load(f)
                self.email_input.setText(config.get('alert_email', ''))
                self.phone_input.setText(config.get('alert_phone', ''))
                self.pref_email.setChecked(config.get('enable_email', True))
                self.pref_sms.setChecked(config.get('enable_sms', True))
                idx = self.level_combo.findText(config.get('alert_level', 'Medium'))
                if idx >= 0:
                    self.level_combo.setCurrentIndex(idx)
                idx = self.theme_combo.findText(config.get('theme', 'Cyberpunk'))
                if idx >= 0:
                    self.theme_combo.setCurrentIndex(idx)
                idx = self.session_timeout_combo.findText(config.get('session_timeout', '30 min'))
                if idx >= 0:
                    self.session_timeout_combo.setCurrentIndex(idx)
                QMessageBox.information(self, "Import Settings", f"Settings imported from {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Import Error", f"Failed to import settings: {str(e)}")

    def reset_settings(self):
        self.email_input.setText("")
        self.phone_input.setText("")
        self.pref_email.setChecked(True)
        self.pref_sms.setChecked(True)
        self.level_combo.setCurrentIndex(self.level_combo.findText("Medium"))
        self.theme_combo.setCurrentIndex(self.theme_combo.findText("Cyberpunk"))
        self.session_timeout_combo.setCurrentIndex(self.session_timeout_combo.findText("30 min"))
        QMessageBox.information(self, "Reset Settings", "All settings have been reset to defaults.") 