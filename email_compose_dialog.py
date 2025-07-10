from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTextEdit, QLabel, QPushButton, QHBoxLayout

class EmailComposeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compose Email")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        self.recipient_input = QLineEdit()
        self.recipient_input.setPlaceholderText("Recipient Email")
        layout.addWidget(QLabel("To:"))
        layout.addWidget(self.recipient_input)

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")
        layout.addWidget(QLabel("Subject:"))
        layout.addWidget(self.subject_input)

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText("Message Body")
        layout.addWidget(QLabel("Message:"))
        layout.addWidget(self.body_input)

        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton("Send")
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

    def get_email_data(self):
        return (
            self.recipient_input.text().strip(),
            self.subject_input.text().strip(),
            self.body_input.toPlainText().strip()
        ) 