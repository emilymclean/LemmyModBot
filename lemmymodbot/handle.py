from io import BytesIO
from typing import Union, Optional, Dict

import imagehash
import requests
from PIL import Image, UnidentifiedImageError
from pylemmy import Lemmy
from pylemmy.models.comment import Comment
from pylemmy.models.post import Post

from lemmymodbot import LemmyModHttp
from lemmymodbot.database import Database


class LemmyHandle:

    def __init__(self, lemmy: Lemmy, elem: Union[Post, Comment], database: Database, config, matrix_facade):
        self.elem = elem
        self.lemmy = lemmy
        self.lemmy_http = LemmyModHttp(lemmy)
        self.database = database
        self.config = config
        self.matrix_facade = matrix_facade

    def send_message_to_author(self, content: str):
        if self.config.debug_mode:
            print(f"{content}")
            return
        actor_id = self.elem.post_view.post.creator_id if isinstance(self.elem, Post) else self.elem.comment_view
        self.lemmy_http.send_message(actor_id, f"{content}")

    def post_comment(self, content: str):
        if self.config.debug_mode:
            print(f"{content}")
            return
        self.elem.create_comment(f"{content}")

    def remove_thing(self, reason: str):
        if self.config.debug_mode:
            print(f"Remove {reason}")
            return
        if isinstance(self.elem, Post):
            self.lemmy_http.remove_post(self.elem.post_view.post.id, reason)
        elif isinstance(self.elem, Comment):
            self.lemmy_http.remove_comment(self.elem.comment_view.comment.id, reason)

    def report(self, reason: str):
        if self.config.debug_mode:
            print(f"Report {reason}")
        self.elem.create_report(reason)

    def _get_url(self) -> Optional[str]:
        if self.elem is not Post or self.elem.post_view.post.url is None:
            return None
        return self.elem.post_view.post.url

    def fetch_image(self, url: str = None) -> (Image, str):
        if url is None:
            url = self._get_url()
        try:
            img = Image.open(BytesIO(requests.get(url).content))
            return img, str(imagehash.phash(img))
        except UnidentifiedImageError:
            return None, None

    def fetch_content(self, url: str = None) -> (bytes, Dict[str, str]):
        if url is None:
            url = self._get_url()

        cont = requests.get(
            url,
            allow_redirects=True,
            headers={
                "Accepts": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0"
            }
        )
        return cont.content, cont.headers

    def send_message_to_matrix(self, message):
        if self.matrix_facade is None:
            return
        self.matrix_facade.send_message_to_matrix(
            self.config.matrix_config.room_id,
            message
        )
