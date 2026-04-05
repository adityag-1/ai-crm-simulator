from dataclasses import dataclass

@dataclass
class CRMData:
    """The actual data row the AI is looking at."""
    raw_name: str = ""
    raw_phone: str = ""
    raw_title: str = ""
    correct_name: str = ""
    correct_phone: str = ""
    correct_title: str = ""

@dataclass
class CRMAction:
    """What the AI sends back to fix the data."""
    fixed_name: str = None
    fixed_phone: str = None
    fixed_title: str = None

@dataclass
class CRMObservation:
    """What the AI sees after its action."""
    current_row: dict = None
    message: str = ""
    is_correct: bool = False