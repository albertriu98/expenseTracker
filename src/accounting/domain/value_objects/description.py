from dataclasses import dataclass

@dataclass(frozen=True)
class Description:
    _text : str

    @property
    def text(self):
        return self._text