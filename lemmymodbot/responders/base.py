from lemmymodbot.handle import LemmyHandle
from lemmymodbot.models import Outcome, Content, ContentResult


class Responder:
    _content_suffix = "\n\nMod bot (with L plates)"

    def respond(self, outcome: Outcome, content: Content, result: ContentResult, handle: LemmyHandle):
        pass
