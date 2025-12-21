from kps import KPS


class KPSPelaajaVsPelaaja(KPS):
    def _ensimmaisen_siirto(self) -> str:
        return input("Ensimmäisen pelaajan siirto: ")

    def _toisen_siirto(self) -> str:
        return input("Toisen pelaajan siirto: ")