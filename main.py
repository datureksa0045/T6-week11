# NAMA     : Datu Reksa hamza Putra
# NIM      : F1D02310045
import sys
from typing import List, Dict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QLabel, QPushButton, QTextEdit,
    QSplitter, QStatusBar, QProgressBar, QHeaderView, QMessageBox, QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from style import app_stylesheet
from dialogs import PostFormDialog
from workers import (
    FetchPostsWorker, FetchPostDetailWorker,
    CreatePostWorker, UpdatePostWorker, DeletePostWorker
)
from models import Post


class PostManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.posts: List[Post] = []
        self.current_worker = None
        self.init_ui()
        self.load_posts()

    def init_ui(self):
        self.setWindowTitle("Post Manager")
        self.resize(1240, 760)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        top_row = QHBoxLayout()

        title_label = QLabel("Post Manager")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        top_row.addWidget(title_label)

        self.count_label = QLabel("Posts: 0")
        self.count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_row.addWidget(self.count_label)

        left_panel.addLayout(top_row)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Title", "Author", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemClicked.connect(self.on_row_clicked)
        left_panel.addWidget(self.table)

        controls = QHBoxLayout()
        add_btn = QPushButton("+ Add")
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")
        refresh_btn = QPushButton("Refresh")
        delete_btn.setObjectName("danger")
        add_btn.clicked.connect(self.open_add_dialog)
        edit_btn.clicked.connect(self.open_edit_dialog)
        delete_btn.clicked.connect(self.delete_post)
        refresh_btn.clicked.connect(self.load_posts)
        controls.addWidget(add_btn)
        controls.addWidget(edit_btn)
        controls.addWidget(delete_btn)
        controls.addWidget(refresh_btn)
        left_panel.addLayout(controls)

        right_panel = QVBoxLayout()
        info_title = QLabel("Post Details")
        info_font = QFont()
        info_font.setPointSize(13)
        info_font.setBold(True)
        info_title.setFont(info_font)
        right_panel.addWidget(info_title)

        self.detail_header = QLabel("Select a post to see details")
        self.detail_header.setStyleSheet("font-size: 11pt; margin-bottom: 8px;")
        right_panel.addWidget(self.detail_header)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setPlaceholderText("Post detail, body and comments will appear here.")
        right_panel.addWidget(self.detail_text)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(0)
        self.progress_bar.setVisible(False)
        right_panel.addWidget(self.progress_bar)

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def load_posts(self):
        if self.current_worker and self.current_worker.isRunning():
            self.status_bar.showMessage("Still loading... wait a moment")
            return

        self.show_loading(True)
        self.status_bar.showMessage("Loading posts...")
        self.current_worker = FetchPostsWorker()
        self.current_worker.finished.connect(self.on_posts_loaded)
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.start()

    def on_posts_loaded(self, posts: List[Post]):
        self.posts = posts
        self.count_label.setText(f"Posts: {len(posts)}")
        self.populate_table(posts)
        self.show_loading(False)
        self.status_bar.showMessage(f"Loaded {len(posts)} posts")

    def populate_table(self, posts: List[Post]):
        self.table.setRowCount(len(posts))
        for row, post in enumerate(posts):
            self.table.setItem(row, 0, QTableWidgetItem(str(post.id)))
            self.table.setItem(row, 1, QTableWidgetItem(post.title))
            self.table.setItem(row, 2, QTableWidgetItem(post.author))
            status_item = QTableWidgetItem(post.status)
            if post.status == "published":
                status_item.setBackground(QColor(84, 185, 84))
            elif post.status == "draft":
                status_item.setBackground(QColor(241, 196, 15))
            else:
                status_item.setBackground(QColor(229, 83, 83))
            self.table.setItem(row, 3, status_item)

    def on_row_clicked(self, item):
        row = item.row()
        if 0 <= row < len(self.posts):
            self.show_post_details(self.posts[row])

    def show_post_details(self, post: Post):
        if self.current_worker and self.current_worker.isRunning():
            return

        self.show_loading(True)
        self.status_bar.showMessage(f"Loading details for post {post.id}...")
        self.current_worker = FetchPostDetailWorker(post.id)
        self.current_worker.finished.connect(self.on_post_detail_loaded)
        self.current_worker.error.connect(self.on_api_error)
        self.current_worker.start()

    def on_post_detail_loaded(self, post: Post):
        self.show_loading(False)
        self.detail_header.setText(f"{post.title} — {post.author}")
        detail_text = (
            f"ID: {post.id}\n"
            f"Slug: {post.slug}\n"
            f"Status: {post.status}\n\n"
            f"{post.body}\n\n"
            f"Comments ({len(post.comments)}):\n"
        )
        if post.comments:
            for comment in post.comments:
                detail_text += f"\n• {comment.name} ({comment.email})\n{comment.body}\n"
        else:
            detail_text += "\nNo comments found."
        self.detail_text.setPlainText(detail_text)
        self.status_bar.showMessage(f"Showing post: {post.title}")

    def open_add_dialog(self):
        dialog = PostFormDialog(self)
        if dialog.exec() == QDialog.Accepted:
            title, body, author, slug, status = dialog.get_data()
            if not all([title, body, author, slug]):
                QMessageBox.warning(self, "Validation Error", "Please fill all fields")
                return
            self.show_loading(True)
            self.status_bar.showMessage("Creating post...")
            self.current_worker = CreatePostWorker(title, body, author, slug, status)
            self.current_worker.finished.connect(self.on_post_created)
            self.current_worker.error.connect(self.on_api_error)
            self.current_worker.start()

    def on_post_created(self, result: Dict):
        self.show_loading(False)
        new_post_id = result.get('data', {}).get('id') if isinstance(result, dict) else None
        QMessageBox.information(self, "Success", f"Post created successfully! New ID: {new_post_id}")
        self.load_posts()

    def open_edit_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a post to edit")
            return
        post = self.posts[selected_row]
        dialog = PostFormDialog(self, post)
        if dialog.exec() == QDialog.Accepted:
            title, body, author, slug, status = dialog.get_data()
            if not all([title, body, author, slug]):
                QMessageBox.warning(self, "Validation Error", "Please fill all fields")
                return
            self.show_loading(True)
            self.status_bar.showMessage(f"Updating post {post.id}...")
            self.current_worker = UpdatePostWorker(post.id, title, body, author, slug, status)
            self.current_worker.finished.connect(self.on_post_updated)
            self.current_worker.error.connect(self.on_api_error)
            self.current_worker.start()

    def on_post_updated(self, result: Dict):
        self.show_loading(False)
        QMessageBox.information(self, "Success", "Post updated successfully!")
        self.load_posts()

    def delete_post(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a post to delete")
            return
        post = self.posts[selected_row]
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete '{post.title}' and its {len(post.comments)} comments?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.show_loading(True)
            self.status_bar.showMessage(f"Deleting post {post.id}...")
            self.current_worker = DeletePostWorker(post.id)
            self.current_worker.finished.connect(self.on_post_deleted)
            self.current_worker.error.connect(self.on_api_error)
            self.current_worker.start()

    def on_post_deleted(self, result: bool):
        self.show_loading(False)
        QMessageBox.information(self, "Success", "Post deleted successfully!")
        self.detail_header.setText("Select a post to see details")
        self.detail_text.clear()
        self.load_posts()

    def on_api_error(self, error_message: str):
        self.show_loading(False)
        self.status_bar.showMessage(f"Error: {error_message}")
        QMessageBox.critical(self, "API Error", error_message)

    def show_loading(self, loading: bool):
        self.progress_bar.setVisible(loading)
        self.status_bar.showMessage("Loading..." if loading else "Ready")


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(app_stylesheet())
    window = PostManagerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
