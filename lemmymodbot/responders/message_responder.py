from lemmymodbot import Outcome, Content, ContentResult, LemmyHandle
from lemmymodbot.responders.base import Responder


class MessageResponder(Responder):
    content: str

    def __init__(self, content: str):
        self.content = content

    def respond(self, outcome: Outcome, content: Content, result: ContentResult, handle: LemmyHandle):
        handle.send_message_to_author(
            self.content + self._content_suffix
        )
