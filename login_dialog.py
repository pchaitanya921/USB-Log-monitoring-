from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QFrame, QSizePolicy, QStackedWidget, QDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal
import json
import os
import hashlib
from ui.register_dialog import RegisterDialog

USERS_FILE = 'users.json'

class LoginWidget(QWidget):
    """Integrated login widget that can be embedded in the main window"""
    
    # Signal emitted when login is successful
    login_successful = pyqtSignal(str, str)  # username, role
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.role = None
        self.username = None
        self.email = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("font-family: 'JetBrains Mono', 'Fira Mono', 'DejaVu Sans Mono', 'Consolas', monospace;")
        layout.setSpacing(24)
        layout.setContentsMargins(32, 32, 32, 32)
        
        # Center the login form
        layout.addStretch(1)

        # Main container frame
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: rgba(12, 12, 20, 0.96);
                border: 2px solid #00ffe7;
                border-radius: 22px;
            }
        """)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(28, 28, 28, 28)

        # Header section
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap("resources/icons/alert.svg").scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title_layout.addWidget(icon_label)
        title = QLabel("USB HAWKEYE")
        title.setFont(QFont("Consolas", 22, QFont.Bold))
        title.setStyleSheet("color: #00ffe7; letter-spacing: 2px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_layout.addWidget(title)
        main_layout.addLayout(title_layout)

        subtitle = QLabel("CYBERPUNK SECURITY ACCESS")
        subtitle.setFont(QFont("Consolas", 12, QFont.Bold))
        subtitle.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle)

        main_layout.addSpacing(10)

        # Login form section
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)

        # Username field
        username_layout = QHBoxLayout()
        user_icon = QLabel()
        user_icon.setPixmap(QPixmap("resources/icons/user.svg").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        user_icon.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        username_layout.addWidget(user_icon)
        username_label = QLabel("USERNAME:")
        username_label.setFont(QFont("Consolas", 12, QFont.Bold))
        username_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        username_layout.addWidget(username_label)
        form_layout.addLayout(username_layout)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter your username...")
        self.user_input.setFont(QFont("Consolas", 12))
        self.user_input.setMinimumHeight(38)
        self.user_input.setStyleSheet("""
            QLineEdit {
                background: #18181e;
                color: #39ff14;
                border: 2px solid #00ffe7;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.user_input)

        # Email field
        email_label = QLabel("EMAIL:")
        email_label.setFont(QFont("Consolas", 12, QFont.Bold))
        email_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address...")
        self.email_input.setFont(QFont("Consolas", 12))
        self.email_input.setMinimumHeight(38)
        self.email_input.setStyleSheet("""
            QLineEdit {
                background: #18181e;
                color: #39ff14;
                border: 2px solid #00ffe7;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.email_input)

        # Password field
        password_label = QLabel("🔒 PASSWORD:")
        password_label.setFont(QFont("Segoe UI Emoji, Noto Color Emoji, Apple Color Emoji, Consolas, monospace", 12, QFont.Bold))
        password_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(password_label)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter your password...")
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setFont(QFont("Consolas", 12))
        self.pass_input.setMinimumHeight(38)
        self.pass_input.setStyleSheet("""
            QLineEdit {
                background: #18181e;
                color: #39ff14;
                border: 2px solid #00ffe7;
                border-radius: 10px;
                padding: 8px 14px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.pass_input)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(10)

        # Buttons section
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(18)

        self.login_btn = QPushButton("🚀 ACCESS SYSTEM")
        self.login_btn.setFont(QFont("Consolas", 13, QFont.Bold))
        self.login_btn.setMinimumHeight(44)
        self.login_btn.setStyleSheet("""
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
        self.login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(self.login_btn)

        self.abort_btn = QPushButton("✖ ABORT")
        self.abort_btn.setFont(QFont("Consolas", 13, QFont.Bold))
        self.abort_btn.setMinimumHeight(44)
        self.abort_btn.setStyleSheet("""
            QPushButton {
                background: rgba(32, 8, 16, 0.18);
                color: #ff003c;
                border: 2px solid #ff003c;
                border-radius: 12px;
                padding: 10px 18px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(255, 0, 60, 0.18);
                color: #fff;
                border: 2px solid #fff;
            }
        """)
        self.abort_btn.clicked.connect(self.handle_abort)
        btn_layout.addWidget(self.abort_btn)

        main_layout.addLayout(btn_layout)
        main_layout.addSpacing(10)

        # Register section
        register_layout = QHBoxLayout()
        register_layout.addStretch(1)
        self.register_btn = QPushButton("🗝 NEW ID / CREATE ACCOUNT")
        self.register_btn.setFont(QFont("Consolas", 11, QFont.Bold))
        self.register_btn.setMinimumHeight(36)
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: rgba(16, 32, 16, 0.18);
                color: #39ff14;
                border: 2px solid #39ff14;
                border-radius: 10px;
                padding: 8px 16px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: rgba(57, 255, 20, 0.18);
                color: #fff;
                border: 2px solid #fff;
            }
        """)
        self.register_btn.clicked.connect(self.show_register_dialog)
        register_layout.addWidget(self.register_btn)
        register_layout.addStretch(1)
        main_layout.addLayout(register_layout)

        layout.addWidget(main_frame)
        layout.addStretch(1)

        # Connect Enter key to login
        self.user_input.returnPressed.connect(self.handle_login)
        self.pass_input.returnPressed.connect(self.handle_login)

    def handle_login(self):
        user_or_email = self.user_input.text().strip()
        password = self.pass_input.text().strip()

        if not user_or_email or not password:
            QMessageBox.warning(self, "Access Denied", "Please enter both username/email and password.")
            return

        users = self.load_users()
        # Try login by username
        if user_or_email in users:
            stored_password_hash = users[user_or_email]['password']
            if self.hash_password(password) == stored_password_hash:
                self.role = users[user_or_email]['role']
                self.username = user_or_email
                self.email = users[user_or_email].get('email', '')
                self.login_successful.emit(self.username, self.role)
            return
        # Try login by email
        for uname, udata in users.items():
            if udata.get('email', '').lower() == user_or_email.lower():
                if self.hash_password(password) == udata['password']:
                    self.role = udata['role']
                    self.username = uname
                    self.email = udata.get('email', '')
                    self.login_successful.emit(self.username, self.role)
            return
        QMessageBox.critical(self, "Access Denied", "Invalid username/email or password.")

    def handle_abort(self):
        """Handle abort button - exit the application"""
        import sys
        sys.exit(0)

    def load_users(self):
        if os.path.exists(USERS_FILE):
            try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
            except:
                return {}
        return {}

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_register_dialog(self):
        register_dialog = RegisterDialog(self)
        if register_dialog.exec_() == register_dialog.Accepted:
            # Refresh the login form
            self.user_input.clear()
            self.pass_input.clear()
            self.user_input.setFocus()


class LoginDialog(QDialog):
    """Legacy dialog class for backward compatibility - now just wraps the widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 USB HawkEye Login")
        self.setFixedSize(500, 520)
        self.role = None
        self.username = None
        
        # Create the login widget
        self.login_widget = LoginWidget(self)
        self.login_widget.login_successful.connect(self.on_login_successful)
        
        # Set up layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.login_widget)
        
        # Set modal
        self.setModal(True)

    def on_login_successful(self, username, role):
        self.username = username
        self.role = role
        self.accept() 