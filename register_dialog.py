from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QMessageBox, QComboBox, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import os
import hashlib
import re

USERS_FILE = 'users.json'

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📝 USB HawkEye - Cyberpunk Registration")
        self.setFixedSize(500, 450)
        self.username = None
        self.role = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setStyleSheet("font-family: 'JetBrains Mono', 'Fira Mono', 'DejaVu Sans Mono', 'Consolas', monospace;")
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Main container frame
        main_frame = QFrame()
        main_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(8, 8, 12, 0.95), 
                    stop:1 rgba(16, 16, 24, 0.95));
                border: 3px solid #00ffe7;
                border-radius: 25px;
            }
        """)
        main_layout = QVBoxLayout(main_frame)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(0, 255, 231, 0.1), 
                    stop:0.5 rgba(255, 0, 204, 0.1), 
                    stop:1 rgba(57, 255, 20, 0.1));
                border: 2px solid #39ff14;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("📝 CREATE NEW ACCOUNT")
        title.setFont(QFont("Consolas", 18, QFont.Bold))
        title.setStyleSheet("""
            color: #00ffe7; 
            letter-spacing: 2px;
            margin: 5px 0;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("JOIN THE CYBERPUNK SECURITY NETWORK")
        subtitle.setFont(QFont("Consolas", 11, QFont.Bold))
        subtitle.setStyleSheet("""
            color: #39ff14; 
            letter-spacing: 1px;
            margin: 5px 0;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header_frame)
        
        # Registration form section
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: rgba(16, 16, 24, 0.8);
                border: 2px solid #00ffe7;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(18)
        
        # Username field
        username_label = QLabel("👤 USERNAME:")
        username_label.setFont(QFont("Consolas", 12, QFont.Bold))
        username_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(username_label)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your desired username...")
        self.username_input.setFont(QFont("Consolas", 12))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 16, 24, 0.9), 
                    stop:1 rgba(24, 24, 32, 0.9));
                color: #39ff14;
                border: 3px solid #00ffe7;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 12px;
                selection-background-color: rgba(255, 0, 204, 0.6);
                selection-color: #ff00cc;
            }
            QLineEdit:focus {
                border: 3px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Email field
        email_label = QLabel("📧 EMAIL:")
        email_label.setFont(QFont("Consolas", 12, QFont.Bold))
        email_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(email_label)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address...")
        self.email_input.setFont(QFont("Consolas", 12))
        self.email_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 16, 24, 0.9), 
                    stop:1 rgba(24, 24, 32, 0.9));
                color: #39ff14;
                border: 3px solid #00ffe7;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 12px;
                selection-background-color: rgba(255, 0, 204, 0.6);
                selection-color: #ff00cc;
            }
            QLineEdit:focus {
                border: 3px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.email_input)
        
        # Password field
        password_label = QLabel("🔒 PASSWORD:")
        password_label.setFont(QFont("Consolas", 12, QFont.Bold))
        password_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(password_label)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your secure password...")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Consolas", 12))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 16, 24, 0.9), 
                    stop:1 rgba(24, 24, 32, 0.9));
                color: #39ff14;
                border: 3px solid #00ffe7;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 12px;
                selection-background-color: rgba(255, 0, 204, 0.6);
                selection-color: #ff00cc;
            }
            QLineEdit:focus {
                border: 3px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # Confirm password field
        confirm_label = QLabel("🔐 CONFIRM PASSWORD:")
        confirm_label.setFont(QFont("Consolas", 12, QFont.Bold))
        confirm_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(confirm_label)
        
        self.confirm_input = QLineEdit()
        self.confirm_input.setPlaceholderText("Confirm your password...")
        self.confirm_input.setEchoMode(QLineEdit.Password)
        self.confirm_input.setFont(QFont("Consolas", 12))
        self.confirm_input.setStyleSheet("""
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 16, 24, 0.9), 
                    stop:1 rgba(24, 24, 32, 0.9));
                color: #39ff14;
                border: 3px solid #00ffe7;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 12px;
                selection-background-color: rgba(255, 0, 204, 0.6);
                selection-color: #ff00cc;
            }
            QLineEdit:focus {
                border: 3px solid #ff00cc;
            }
            QLineEdit::placeholder {
                color: rgba(57, 255, 20, 0.5);
                font-style: italic;
            }
        """)
        form_layout.addWidget(self.confirm_input)
        
        # Role selection
        role_label = QLabel("🎭 ACCESS ROLE:")
        role_label.setFont(QFont("Consolas", 12, QFont.Bold))
        role_label.setStyleSheet("color: #39ff14; letter-spacing: 1px;")
        form_layout.addWidget(role_label)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["user", "admin"])
        self.role_combo.setFont(QFont("Consolas", 12))
        self.role_combo.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(16, 16, 24, 0.9), 
                    stop:1 rgba(24, 24, 32, 0.9));
                color: #39ff14;
                border: 3px solid #00ffe7;
                border-radius: 12px;
                padding: 12px 15px;
                font-size: 12px;
                selection-background-color: rgba(255, 0, 204, 0.6);
                selection-color: #ff00cc;
            }
            QComboBox:focus {
                border: 3px solid #ff00cc;
            }
            QComboBox::drop-down {
                border: none;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #00ffe7;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                    stop:0 rgba(8, 8, 12, 0.95), 
                    stop:1 rgba(16, 16, 24, 0.95));
                color: #39ff14;
                border: 2px solid #00ffe7;
                border-radius: 10px;
                selection-background-color: rgba(255, 0, 204, 0.4);
                selection-color: #ff00cc;
            }
        """)
        form_layout.addWidget(self.role_combo)
        
        main_layout.addWidget(form_frame)
        
        # Buttons section
        btn_frame = QFrame()
        btn_frame.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(15)
        
        # Register button
        self.register_btn = QPushButton("🚀 CREATE ACCOUNT")
        self.register_btn.setFont(QFont("Consolas", 13, QFont.Bold))
        self.register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(57, 255, 20, 0.3), 
                    stop:1 rgba(57, 255, 20, 0.2));
                color: #39ff14;
                border: 3px solid #39ff14;
                border-radius: 15px;
                padding: 15px 20px;
                font-weight: bold;
                letter-spacing: 2px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(57, 255, 20, 0.4), 
                    stop:1 rgba(57, 255, 20, 0.3));
                color: #00ffe7;
                border: 3px solid #00ffe7;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 0, 204, 0.4), 
                    stop:1 rgba(255, 0, 204, 0.3));
                color: #ff00cc;
                border: 3px solid #ff00cc;
            }
        """)
        self.register_btn.setMinimumHeight(50)
        self.register_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(self.register_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton("❌ CANCEL")
        self.cancel_btn.setFont(QFont("Consolas", 12, QFont.Bold))
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 0, 0, 0.2), 
                    stop:1 rgba(255, 0, 0, 0.1));
                color: #ff4444;
                border: 2px solid #ff4444;
                border-radius: 12px;
                padding: 10px 15px;
                font-weight: bold;
                letter-spacing: 1px;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 rgba(255, 0, 0, 0.3), 
                    stop:1 rgba(255, 0, 0, 0.2));
                color: #ff6666;
                border: 2px solid #ff6666;
            }
        """)
        self.cancel_btn.setMinimumHeight(50)
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancel_btn)
        
        main_layout.addWidget(btn_frame)
        
        layout.addWidget(main_frame)
        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_input.text().strip()
        role = self.role_combo.currentText()
        
        # Validation
        if not username or not email or not password or not confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Please fill in all fields.")
            return
        
        if len(username) < 3:
            QMessageBox.warning(self, "Registration Failed", "Username must be at least 3 characters long.")
            return
        
        if len(password) < 6:
            QMessageBox.warning(self, "Registration Failed", "Password must be at least 6 characters long.")
            return
        
        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match.")
            return
        
        # Check if user already exists
        users = self.load_users()
        if username in users:
            QMessageBox.warning(self, "Registration Failed", "Username already exists.")
            return
        
        # Check email format
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            QMessageBox.warning(self, "Registration Failed", "Please enter a valid email address.")
            return
        
        # Check if email is already used
        for u in users.values():
            if u.get('email', '').lower() == email.lower():
                QMessageBox.warning(self, "Registration Failed", "Email is already registered.")
                return
        
        # Create new user
        users[username] = {
            'password': self.hash_password(password),
            'role': role,
            'email': email
        }
        
        # Save to file
        try:
            with open(USERS_FILE, 'w') as f:
                json.dump(users, f, indent=2)
            
            QMessageBox.information(self, "Registration Successful", 
                                  f"Account created successfully!\nUsername: {username}\nRole: {role}")
            
            self.username = username
            self.role = role
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Registration Failed", f"Error saving user data: {str(e)}")

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            # Create default admin user if file doesn't exist
            default = {
                'admin': {
                    'password': self.hash_password('admin123'),
                    'role': 'admin'
                },
                'user': {
                    'password': self.hash_password('user123'),
                    'role': 'user'
                }
            }
            with open(USERS_FILE, 'w') as f:
                json.dump(default, f, indent=2)
            return default
        with open(USERS_FILE, 'r') as f:
            return json.load(f)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest() 