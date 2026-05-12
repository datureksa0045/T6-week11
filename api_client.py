import requests
from typing import Dict, Any, List

from models import Post, Comment


class APIClient:
    BASE_URL = "https://api.pahrul.my.id/api/posts"
    TIMEOUT = 10

    @staticmethod
    def _normalize_response(response: requests.Response) -> Any:
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, dict) and 'data' in payload:
            return payload['data']
        return payload

    @staticmethod
    def _build_comments(comment_list: List[dict]) -> List[Comment]:
        return [
            Comment(
                id=c.get('id'),
                post_id=c.get('post_id'),
                name=c.get('name', ''),
                email=c.get('email', ''),
                body=c.get('body', '')
            )
            for c in (comment_list or [])
        ]

    @staticmethod
    def _build_post(item: dict) -> Post:
        return Post(
            id=item.get('id'),
            title=item.get('title', ''),
            body=item.get('body', ''),
            author=item.get('author', 'Unknown'),
            slug=item.get('slug', ''),
            status=item.get('status', 'published'),
            comments=APIClient._build_comments(item.get('comments', []))
        )

    @staticmethod
    def get_posts() -> List[Post]:
        try:
            items = APIClient._normalize_response(
                requests.get(APIClient.BASE_URL, timeout=APIClient.TIMEOUT)
            )
            return [APIClient._build_post(item) for item in items] if isinstance(items, list) else []
        except Exception as e:
            raise Exception(f"Failed to fetch posts: {e}")

    @staticmethod
    def get_post_detail(post_id: int) -> Post:
        try:
            item = APIClient._normalize_response(
                requests.get(f"{APIClient.BASE_URL}/{post_id}", timeout=APIClient.TIMEOUT)
            )
            return APIClient._build_post(item)
        except Exception as e:
            raise Exception(f"Failed to fetch post detail: {e}")

    @staticmethod
    def create_post(title: str, body: str, author: str, slug: str, status: str) -> Dict[str, Any]:
        try:
            payload = {
                'title': title,
                'body': body,
                'author': author,
                'slug': slug,
                'status': status
            }
            return requests.post(APIClient.BASE_URL, json=payload, timeout=APIClient.TIMEOUT).json()
        except Exception as e:
            raise Exception(f"Failed to create post: {e}")

    @staticmethod
    def update_post(post_id: int, title: str, body: str, author: str, slug: str, status: str) -> Dict[str, Any]:
        try:
            payload = {
                'title': title,
                'body': body,
                'author': author,
                'slug': slug,
                'status': status
            }
            return requests.put(
                f"{APIClient.BASE_URL}/{post_id}",
                json=payload,
                timeout=APIClient.TIMEOUT
            ).json()
        except Exception as e:
            raise Exception(f"Failed to update post: {e}")

    @staticmethod
    def delete_post(post_id: int) -> bool:
        try:
            response = requests.delete(
                f"{APIClient.BASE_URL}/{post_id}",
                timeout=APIClient.TIMEOUT
            )
            response.raise_for_status()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete post: {e}")
