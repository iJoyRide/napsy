from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Virus:
    malicious: Optional[str] = None
    suspicious: Optional[str] = None
    undetected: Optional[str] = None
    
if "__name__" == "__main__":
    print(Virus)