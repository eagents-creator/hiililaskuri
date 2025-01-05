# Kotitalouden Hiilijalanjälki Mittari

Tämä on Python-pohjainen web-sovellus, jolla voit laskea kotitaloutesi hiilijalanjäljen. Sovellus ottaa huomioon sähkönkulutuksen, autojen käytön, julkisen liikenteen, ruokavalion, jätteiden määrän sekä kompostoinnin. Lisäksi voit syöttää kotitalouden henkilömäärän, ja sovellus laskee hiilijalanjäljen myös henkilöä kohden.

## Ominaisuudet
- **Sähkönkulutus**: Laskenta sähkönkulutuksen ja päästökertoimen perusteella.
- **Liikenne**: Tuki autoille (bensa, hybridi, sähkö) ja julkisen liikenteen käytölle.
- **Ruokailutottumukset**: Lihan ja kasvisten kulutus.
- **Jätteet**: Jätteiden määrä ja kompostointi.
- **Henkilömäärä**: Hiilijalanjälki lasketaan myös henkilöä kohden.
- **Kaavio**: Päästöjen jakautuminen eri osa-alueille esitetään visuaalisesti.

## Asennusohjeet

### 1. Lataa ja asenna tarvittavat riippuvuudet
Luo virtuaaliympäristö (valinnainen mutta suositeltava):
```bash
python -m venv env