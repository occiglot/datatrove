from .base import BaseFormatter


class CustomFormatter(BaseFormatter):
    def __init__(self, replacements: list):
        super().__init__()
        self.replacements = replacements

    def format(self, text: str) -> str:
        for replacement in self.replacements:
            text = text.replace(replacement[0], replacement[1])

        return text
