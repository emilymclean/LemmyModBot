from lemmymodbot import LemmyHandle, Content, ContentResult


class Processor:

    def setup(self) -> None:
        pass

    def execute(self, content: Content, handle: LemmyHandle) -> ContentResult:
        return ContentResult.nothing()



