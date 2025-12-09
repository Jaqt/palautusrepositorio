class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        arvo = self._lue_syote()
        self._sovelluslogiikka.plus(arvo)

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen)

class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        arvo = self._lue_syote()
        self._sovelluslogiikka.miinus(arvo)
    
    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen)

class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._sovelluslogiikka = sovelluslogiikka
        self._lue_syote = lue_syote
        self._edellinen = 0

    def suorita(self):
        self._edellinen = self._sovelluslogiikka.arvo()
        self._sovelluslogiikka.nollaa()

    def kumoa(self):
        self._sovelluslogiikka.aseta_arvo(self._edellinen)

class Kumoa:
    def __init__(self, hae_viimeinen_komento):
        self._hae_viimeinen_komento = hae_viimeinen_komento

    def suorita(self):
        komento = self._hae_viimeinen_komento()
        if komento is not None:
            komento.kumoa()