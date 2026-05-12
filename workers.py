from PySide6.QtCore import QThread, Signal

from api_client import APIClient


class FetchPostsWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def run(self):
        try:
            posts = APIClient.get_posts()
            self.finished.emit(posts)
        except Exception as e:
            self.error.emit(str(e))


class FetchPostDetailWorker(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, post_id: int):
        super().__init__()
        self.post_id = post_id

    def run(self):
        try:
            post = APIClient.get_post_detail(self.post_id)
            self.finished.emit(post)
        except Exception as e:
            self.error.emit(str(e))


class CreatePostWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, title: str, body: str, author: str, slug: str, status: str):
        super().__init__()
        self.title = title
        self.body = body
        self.author = author
        self.slug = slug
        self.status = status

    def run(self):
        try:
            result = APIClient.create_post(self.title, self.body, self.author, self.slug, self.status)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class UpdatePostWorker(QThread):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, post_id: int, title: str, body: str, author: str, slug: str, status: str):
        super().__init__()
        self.post_id = post_id
        self.title = title
        self.body = body
        self.author = author
        self.slug = slug
        self.status = status

    def run(self):
        try:
            result = APIClient.update_post(self.post_id, self.title, self.body, self.author, self.slug, self.status)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class DeletePostWorker(QThread):
    finished = Signal(bool)
    error = Signal(str)

    def __init__(self, post_id: int):
        super().__init__()
        self.post_id = post_id

    def run(self):
        try:
            result = APIClient.delete_post(self.post_id)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
