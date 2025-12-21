from kps import KPS
from tekoaly import Tekoaly


class KPSTekoaly(KPS):
    def __init__(self):
        self._tekoaly = Tekoaly()

    def _ensimmaisen_siirto(self) -> str:
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self) -> str:
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto
