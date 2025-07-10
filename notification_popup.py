from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor, QLinearGradient, QPen
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect, QPoint, pyqtProperty
import os
from datetime import datetime

class HackerNotificationPopup(QWidget):
    """
    Cyberpunk/Termux-style notification popup with hacker aesthetics
    """
    def __init__(self, title="ALERT", message="", notification_type="info", parent=None):
        super().__init__(parent)
        self.title = title
        self.message = message
        self.notification_type = notification_type
        self.animation = None
        self.fade_timer = None
        self.init_ui()
        self.setup_animation()
        
    def init_ui(self):
        # Set window flags for popup behavior
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Main container
        self.container = QFrame()
        self.container.setStyleSheet(self.get_container_style())
        
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        # Icon based on notification type
        icon_label = QLabel()
        icon_path = self.get_icon_path()
        if os.path.exists(icon_path):
            icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            icon_label.setText(self.get_icon_text())
            icon_label.setFont(QFont("Consolas", 16, QFont.Bold))
            icon_label.setStyleSheet(f"color: {self.get_accent_color()};")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setFont(QFont("Consolas", 12, QFont.Bold))
        title_label.setStyleSheet(f"color: {self.get_accent_color()}; letter-spacing: 1px;")
        header_layout.addWidget(title_label)
        
        # Timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        time_label = QLabel(f"[{timestamp}]")
        time_label.setFont(QFont("Consolas", 10))
        time_label.setStyleSheet("color: #666666;")
        header_layout.addWidget(time_label)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFont(QFont("Consolas", 14, QFont.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666666;
                border: none;
                padding: 2px 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                color: #ff4444;
                background: rgba(255, 68, 68, 0.1);
            }
        """)
        close_btn.clicked.connect(self.close_notification)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background-color: {self.get_accent_color()}; max-height: 1px;")
        layout.addWidget(separator)
        
        # Message
        message_label = QLabel(self.message)
        message_label.setFont(QFont("Consolas", 11))
        message_label.setStyleSheet("color: #00ff00; line-height: 1.4;")
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.addWidget(message_label)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        # View Details button
        details_btn = QPushButton("VIEW DETAILS")
        details_btn.setFont(QFont("Consolas", 10, QFont.Bold))
        details_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {self.get_accent_color()};
                border: 1px solid {self.get_accent_color()};
                border-radius: 0px;
                padding: 6px 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }}
            QPushButton:hover {{
                background: {self.get_accent_color()};
                color: #000000;
            }}
        """)
        details_btn.clicked.connect(self.view_details)
        button_layout.addWidget(details_btn)
        
        button_layout.addStretch()
        
        # Dismiss button
        dismiss_btn = QPushButton("DISMISS")
        dismiss_btn.setFont(QFont("Consolas", 10, QFont.Bold))
        dismiss_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #666666;
                border: 1px solid #666666;
                border-radius: 0px;
                padding: 6px 12px;
                font-weight: bold;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: #666666;
                color: #000000;
            }
        """)
        dismiss_btn.clicked.connect(self.close_notification)
        button_layout.addWidget(dismiss_btn)
        
        layout.addLayout(button_layout)
        
        # Set main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.container)
        
        # Set size
        self.resize(400, 150)
        
    def get_container_style(self):
        """Get the container style based on notification type"""
        accent_color = self.get_accent_color()
        return f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(10, 10, 10, 0.95),
                    stop:1 rgba(20, 20, 20, 0.95));
                border: 2px solid {accent_color};
                border-radius: 0px;
            }}
        """
        
    def get_accent_color(self):
        """Get accent color based on notification type"""
        colors = {
            "info": "#00ff00",      # Green
            "warning": "#ffaa00",   # Orange
            "error": "#ff4444",     # Red
            "success": "#00ff88",   # Bright green
            "threat": "#ff0066",    # Pink/red
            "scan": "#00ffff",      # Cyan
            "device": "#ff00ff"     # Magenta
        }
        return colors.get(self.notification_type, "#00ff00")
        
    def get_icon_path(self):
        """Get icon path based on notification type"""
        icons = {
            "info": "resources/icons/alert.svg",
            "warning": "resources/icons/alert.svg", 
            "error": "resources/icons/alert.svg",
            "success": "resources/icons/scan.svg",
            "threat": "resources/icons/alert.svg",
            "scan": "resources/icons/scan.svg",
            "device": "resources/icons/usb.svg"
        }
        return icons.get(self.notification_type, "resources/icons/alert.svg")
        
    def get_icon_text(self):
        """Get fallback icon text"""
        icons = {
            "info": "ℹ",
            "warning": "⚠", 
            "error": "✗",
            "success": "✓",
            "threat": "☠",
            "scan": "🔍",
            "device": "💾"
        }
        return icons.get(self.notification_type, "ℹ")
        
    def setup_animation(self):
        """Setup slide-in animation"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def show_notification(self, screen_geometry):
        """Show the notification with animation"""
        # Position in top-right corner
        x = screen_geometry.width() - self.width() - 20
        y = 20
        
        # Start position (off-screen to the right)
        start_rect = QRect(screen_geometry.width(), y, self.width(), self.height())
        end_rect = QRect(x, y, self.width(), self.height())
        
        self.setGeometry(start_rect)
        self.show()
        
        # Animate in
        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        self.animation.start()
        
        # Auto-dismiss after 8 seconds
        self.fade_timer = QTimer()
        self.fade_timer.timeout.connect(self.close_notification)
        self.fade_timer.start(8000)
        
    def close_notification(self):
        """Close the notification with animation"""
        if self.fade_timer:
            self.fade_timer.stop()
            
        # Animate out
        current_rect = self.geometry()
        end_rect = QRect(current_rect.x() + self.width(), current_rect.y(), 
                        self.width(), self.height())
        
        self.animation.setStartValue(current_rect)
        self.animation.setEndValue(end_rect)
        self.animation.finished.connect(self.close)
        self.animation.start()
        
    def view_details(self):
        """Handle view details action"""
        # This can be connected to show more detailed information
        # For now, just close the notification
        self.close_notification()
        
    def paintEvent(self, event):
        """Custom paint event for additional effects"""
        super().paintEvent(event)
        
        # Add subtle glow effect
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw border glow
        accent_color = QColor(self.get_accent_color())
        pen = QPen(accent_color)
        pen.setWidth(2)
        painter.setPen(pen)
        
        # Draw subtle scan lines effect
        for i in range(0, self.height(), 3):
            alpha = 20 - (i % 20)
            painter.setPen(QPen(QColor(0, 255, 0, alpha), 1))
            painter.drawLine(0, i, self.width(), i)


class NotificationManager:
    """
    Manages multiple notification popups
    """
    def __init__(self, parent=None):
        self.parent = parent
        self.active_notifications = []
        self.max_notifications = 3
        self.notification_spacing = 10
        
    def show_notification(self, title, message, notification_type="info"):
        """Show a new notification"""
        # Remove old notifications if we have too many
        if len(self.active_notifications) >= self.max_notifications:
            old_notification = self.active_notifications.pop(0)
            old_notification.close()
            
        # Create new notification
        notification = HackerNotificationPopup(title, message, notification_type, self.parent)
        
        # Position the notification
        if self.parent:
            screen_geometry = self.parent.screen().geometry()
        else:
            from PyQt5.QtWidgets import QApplication
            screen_geometry = QApplication.primaryScreen().geometry()
            
        # Calculate position based on existing notifications
        base_y = 20
        y_offset = len(self.active_notifications) * (notification.height() + self.notification_spacing)
        notification.move(screen_geometry.width() - notification.width() - 20, base_y + y_offset)
        
        # Show notification
        notification.show_notification(screen_geometry)
        
        # Add to active list
        self.active_notifications.append(notification)
        
        # Connect close signal to remove from list
        notification.destroyed.connect(lambda: self.remove_notification(notification))
        
        return notification
        
    def remove_notification(self, notification):
        """Remove notification from active list"""
        if notification in self.active_notifications:
            self.active_notifications.remove(notification)
            
    def clear_all(self):
        """Clear all active notifications"""
        for notification in self.active_notifications[:]:
            notification.close()
        self.active_notifications.clear() 