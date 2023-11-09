from lemmymodbot import Outcome, Content, ContentResult, LemmyHandle
from lemmymodbot.responders.base import Responder


class ReportResponder(Responder):

    def respond(self, outcome: Outcome, content: Content, result: ContentResult, handle: LemmyHandle):
        handle.report(
            ', '.join(result.flags) + self._content_suffix
        )
