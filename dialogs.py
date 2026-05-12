from typing import Optional

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QLabel, QVBoxLayout, QWidget
)

from models import Post


class PostFormDialog(QDialog):
    def __init__(self, parent=None, post: Optional[Post] = None):
        super().__init__(parent)
        self.post = post
        self.init_ui()
        if post:
            self.load_post_data()

    def init_ui(self):
        self.setWindowTitle("Add Post" if not self.post else "Edit Post")
        self.resize(640, 520)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.title_input = QLineEdit()
        form.addRow("Title:", self.title_input)

        self.body_input = QTextEdit()
        self.body_input.setMinimumHeight(180)
        form.addRow("Body:", self.body_input)

        self.author_input = QLineEdit()
        form.addRow("Author:", self.author_input)

        self.slug_input = QLineEdit()
        form.addRow("Slug:", self.slug_input)

        self.status_combo = QComboBox()
        self.status_combo.addItems(["published", "draft", "archived"])
        form.addRow("Status:", self.status_combo)

        layout.addLayout(form)

        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_post_data(self):
        self.title_input.setText(self.post.title)
        self.body_input.setPlainText(self.post.body)
        self.author_input.setText(self.post.author)
        self.slug_input.setText(self.post.slug)
        self.status_combo.setCurrentText(self.post.status)

    def get_data(self):
        return (
            self.title_input.text(),
            self.body_input.toPlainText(),
            self.author_input.text(),
            self.slug_input.text(),
            self.status_combo.currentText()
        )


class PostDetailDialog(QDialog):
    def __init__(self, parent=None, post: Optional[Post] = None):
        super().__init__(parent)
        self.post = post
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Post Details")
        self.resize(700, 620)

        layout = QVBoxLayout()
        if self.post:
            fields = [
                ("Title", self.post.title),
                ("Author", self.post.author),
                ("Slug", self.post.slug),
                ("Status", self.post.status),
                ("Body", self.post.body)
            ]
            for label_text, value in fields:
                label = QLabel(f"{label_text}:")
                label.setStyleSheet("font-weight: bold;")
                layout.addWidget(label)
                layout.addWidget(QLabel(value))

            layout.addWidget(QLabel("Comments:"))
            if self.post.comments:
                for comment in self.post.comments:
                    comment_widget = self.create_comment_widget(comment)
                    layout.addWidget(comment_widget)
            else:
                layout.addWidget(QLabel("No comments yet"))

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        self.setLayout(layout)

    def create_comment_widget(self, comment):
        widget = QWidget()
        inner_layout = QVBoxLayout()
        inner_layout.setContentsMargins(10, 8, 10, 8)
        inner_layout.addWidget(QLabel(f"<b>{comment.name}</b> ({comment.email})"))
        body_label = QLabel(comment.body)
        body_label.setWordWrap(True)
        inner_layout.addWidget(body_label)
        widget.setLayout(inner_layout)
        widget.setStyleSheet(
            "background: #292C33; border: 1px solid #3B3F46; border-radius: 8px;"
        )
        return widget
