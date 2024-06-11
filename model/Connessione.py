from dataclasses import dataclass
@dataclass
class Connessione:
    r1:int
    r2:int
    pn:int

    def __str__(self):
        return hash((self.r1,self.r2,self.pn))