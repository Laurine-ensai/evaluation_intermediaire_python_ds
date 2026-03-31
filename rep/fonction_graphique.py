import matplotlib.pyplot as plt
import cartiflette

# Question 8

from cartiflette import carti_download
departement_borders = carti_download(
 values = ["France"],
 crs = 4326,
 borders = "DEPARTEMENT",
 vectorfile_format="geojson",
 simplification=50,
 filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
 source="EXPRESS-COG-CARTO-TERRITOIRE",
 year=2022)

# Fonction pour filtrer score_departement :

def filtrer_candidat(score_departements, candidat):
    """
    Retourne un nouveau dataframe restreint à un candidat.
    Ne modifie pas score_departements.
    """
    return score_departements.loc[
        score_departements["candidat"] == candidat
    ].copy()

# Identifier la bonne colonne :

def trouver_colonne_departement(gdf):
    candidats = ["code_departement", "CODE_DEPT", "INSEE_DEP", "DEP", "id"]
    for col in candidats:
        if col in gdf.columns:
            return col
    raise ValueError("Impossible de trouver la colonne du code département dans le fond de carte.")

# Fonction de cartographie :

def cartographier_candidat(score_departements, departement_borders, candidat):
    # filtrage du candidat
    df_candidat = score_departements.loc[
        score_departements["candidat"] == candidat,
        ["code_departement", "candidat", "surrepresentation"]
    ].copy()

    # harmonisation des types
    df_candidat["code_departement"] = df_candidat["code_departement"].astype(str).str.zfill(2)

    gdf = departement_borders.copy()
    col_dep = trouver_colonne_departement(gdf)
    gdf[col_dep] = gdf[col_dep].astype(str).str.zfill(2)

    # jointure
    carte = gdf.merge(
        df_candidat,
        left_on=col_dep,
        right_on="code_departement",
        how="left"
    )

    # bornes symétriques pour une palette centrée sur 0
    vmax = carte["surrepresentation"].abs().max()

    # graphique
    fig, ax = plt.subplots(figsize=(10, 10))
    carte.plot(
        column="surrepresentation",
        cmap="bwr",
        linewidth=0.8,
        edgecolor="black",
        legend=True,
        vmin=-vmax,
        vmax=vmax,
        missing_kwds={"color": "lightgrey", "label": "Données manquantes"},
        ax=ax
    )

    ax.set_title(f"Surreprésentation de {candidat} par département", fontsize=14)
    ax.axis("off")
    plt.show()

    return carte