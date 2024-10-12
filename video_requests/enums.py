from enum import Enum


class VideoType(Enum):
    BIRTHDAY = 1
    QUESTION = 2
    ROAST = 3
    PEP_TALK = 4
    OTHER = 5

    labels = {
        BIRTHDAY: "Birthday",
        QUESTION: "Question",
        ROAST: "Roast",
        PEP_TALK: "Pep Talk",
        OTHER: "Other",
    }

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)
