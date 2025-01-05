import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import tempfile
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/laske", methods=["POST"])
def laske():
    try:
        # Kotitalouden henkilömäärä
        henkilot = int(request.form.get("henkilot"))

        # Käyttäjän valinta: kuukausi- vai vuositason tiedot
        aikavaly = request.form.get("aikavaly")
        kerroin = 12 if aikavaly == "kuukausi" else 1

        # Sähkönkulutus
        sahko_kulutus = float(request.form.get("sahko_kulutus")) * kerroin

        # Autojen tiedot
        autojen_maara = int(request.form.get("autojen_maara"))
        auto_paastot = 0
        for i in range(1, autojen_maara + 1):
            auton_tyyppi = request.form.get(f"auton_tyyppi_{i}")
            polttoaine_kulutus = float(request.form.get(f"polttoaine_kulutus_{i}")) * kerroin

            if auton_tyyppi == "bensa":
                auto_paastot += polttoaine_kulutus * 2.31  # Bensan päästökerroin
            elif auton_tyyppi == "diesel":
                auto_paastot += polttoaine_kulutus * 2.68  # Dieselin päästökerroin
            elif auton_tyyppi == "hybridi":
                auto_paastot += polttoaine_kulutus * 1.2  # Hybridi päästökerroin
            elif auton_tyyppi == "sahko":
                auto_paastot += polttoaine_kulutus * 0.015  # Sähköauton päästökerroin kWh:lle
                sahko_kulutus += polttoaine_kulutus  # Lisätään sähköauton kulutus kotitalouden sähkönkulutukseen

        # Julkinen liikenne
        julkiset_kilometrit = float(request.form.get("julkiset_kilometrit")) * kerroin
        julkisten_paastokerroin = 0.1  # Oletus: 100 g CO₂/km
        julkiset_paastot = julkiset_kilometrit * julkisten_paastokerroin

        # Lihan ja kasvisten kulutus
        liha_kulutus = float(request.form.get("liha_kulutus")) * kerroin
        kasvis_kulutus = float(request.form.get("kasvis_kulutus")) * kerroin

        # Jätteet ja kompostointi
        jate_maara = float(request.form.get("jate_maara")) * kerroin
        kompostointi = float(request.form.get("kompostointi")) * kerroin

        # Päästökertoimet (kg CO₂)
        sahkon_paastokerroin = 0.083
        lihan_paastokerroin = 27
        kasvisten_paastokerroin = 2
        jatteiden_paastokerroin = 0.5
        kompostoinnin_vahennys = -0.25  # Kompostointi vähentää päästöjä

        # Päästölaskenta
        sahko_paastot = sahko_kulutus * sahkon_paastokerroin
        liha_paastot = liha_kulutus * lihan_paastokerroin
        kasvis_paastot = kasvis_kulutus * kasvisten_paastokerroin
        jate_paastot = (jate_maara * jatteiden_paastokerroin) + (kompostointi * kompostoinnin_vahennys)

        kokonais_paastot = sahko_paastot + auto_paastot + julkiset_paastot + liha_paastot + kasvis_paastot + jate_paastot
        paastot_henkiloa_kohden = kokonais_paastot / henkilot

        # Luo kaavio ja tallenna väliaikaiseen tiedostoon
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png", dir="static") as temp_file:
            kaavio_polku = temp_file.name
            plt.figure(figsize=(10, 6))
            plt.bar(
                ['Sähkö', 'Autot', 'Julkiset', 'Liha', 'Kasvikset', 'Jätteet'], 
                [sahko_paastot, auto_paastot, julkiset_paastot, liha_paastot, kasvis_paastot, jate_paastot], 
                color='skyblue'
            )
            plt.title('Kotitalouden hiilijalanjälki (kg CO₂/vuosi)')
            plt.ylabel('Päästöt (kg CO₂)')
            plt.savefig(kaavio_polku)
            plt.close()

        # Palauta tulossivu ja väliaikaisen tiedoston polku
        return render_template(
            "result.html",
            kokonais_paastot=kokonais_paastot,
            paastot_henkiloa_kohden=paastot_henkiloa_kohden,
            paastot_kaavio=os.path.basename(kaavio_polku),  # Vain tiedoston nimi
            aikavaly=aikavaly
        )
    except Exception as e:
        return f"Virhe tietojen käsittelyssä: {e}"

@app.route("/lataa/<filename>")
def lataa(filename):
    tiedosto_polku = os.path.join("static", filename)
    try:
        return send_file(tiedosto_polku, as_attachment=True)
    finally:
        # Poistetaan tiedosto latauksen jälkeen
        if os.path.exists(tiedosto_polku):
            os.remove(tiedosto_polku)

if __name__ == "__main__":
    app.run(debug=True)