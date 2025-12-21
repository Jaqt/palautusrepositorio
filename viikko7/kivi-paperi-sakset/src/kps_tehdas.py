from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(vastaus: str):
    if vastaus.endswith("a"):
        return KPSPelaajaVsPelaaja()
    if vastaus.endswith("b"):
        return KPSTekoaly()
    if vastaus.endswith("c"):
        return KPSParempiTekoaly()
    return None
