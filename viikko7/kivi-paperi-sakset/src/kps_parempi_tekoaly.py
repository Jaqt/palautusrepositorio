from kps import KPS
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KPS):
    def __init__(self):
        self._tekoaly = TekoalyParannettu(10)

    def _ensimmaisen_siirto(self) -> str:
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self) -> str:
        siirto = self._tekoaly.anna_siirto()
        print(f"Tietokone valitsi: {siirto}")
        return siirto

    def _aseta_ekan_siirto(self, ekan_siirto: str) -> None:
        self._tekoaly.aseta_siirto(ekan_siirto)
