class Element:
    def __init__(self, type: str) -> None:
        self.body = {"type": type}


class KMarkdown(Element):
    def __init__(self, content: str) -> None:
        super().__init__("kmarkdown")
        self.body["content"] = content


class Button(Element):
    def __init__(self, theme: str, text: Element, value: str) -> None:
        super().__init__("button")
        self.body["theme"] = theme
        self.body["text"] = text.body
        self.body["value"] = value
