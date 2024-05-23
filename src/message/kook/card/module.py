from message.kook.card.element import Element


class Module:
    def __init__(self, type: str) -> None:
        self.body = {"type": type}


class Section(Module):
    def __init__(self, text: Element) -> None:
        super().__init__("section")
        self.body["text"] = text.body

    def accessory(self, accessory: Element) -> Module:
        self.body["mode"] = "right"
        self.body["accessory"] = accessory.body
        return self


class ActionGroup(Module):
    def __init__(self) -> None:
        super().__init__("action-group")
        self.body["elements"] = []

    def append_element(self, element: Element) -> Module:
        self.body["elements"].append(element.body)
        return self
