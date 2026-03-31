import numpy as np
from great_tables import GT, html, style, loc

CAS_SPECIAUX = ["abstentions", "blancs", "nuls"]

# QUESTION 1 (a)


def taille_max_code_commune(df):
    taille_max = df["code_commune"].astype(str).str.len().max()
    print(f"La taille maximale du code commune est de {taille_max} caractères.")


def nb_occurence_longueur_code_departement(df):
    print(df["code_departement"].astype(str).str.len().value_counts())


def departement_11_caractères(df):
    df_louche = df[df["code_departement"].astype(str).str.len() == 11]
    print("Valeurs suspectes dans code_departement :")
    print(df_louche["code_departement"].unique())
    print("\nExtrait des lignes correspondantes :")
    print(df_louche.head())


def maj_code_commune(df):
    df["code_commune"] = df["code_departement"].astype(str) + df["code_commune"].astype(
        str
    ).str.zfill(3)


def verification_Montrouge(df):
    print("Exemple Montrouge :")
    print(
        df[df["libelle_commune"].str.contains("Montrouge", na=False)][
            ["code_commune", "libelle_commune"]
        ]
        .drop_duplicates()
        .head()
    )


# QUESTION 1 (b)


def entites_uniques(df):
    entites_uniques = (
        df[["nom", "prenom"]]
        .drop_duplicates()
        .sort_values("nom")
        .reset_index(drop=True)
    )
    print(entites_uniques)


def creation_candidat(df):
    df["candidat"] = np.where(
        df["nom"].isin(CAS_SPECIAUX),
        df["nom"],
        df["prenom"].astype(str) + " " + df["nom"].astype(str),
    )


def aperçu_des_candidats(df):
    print("\nAperçu des candidats :")
    print(df["candidat"].unique())


# QUESTION 2


def filtrer_candidats(df):
    return df[~df["candidat"].isin(CAS_SPECIAUX)].copy()


def nb_candidats(df_candidats_uniquement):
    candidats_reels = df_candidats_uniquement["candidat"].unique()
    candidats = len(candidats_reels)
    print(f"En 2022, il y avait {candidats} candidats à l'élection présidentielle.")
    print("\nListe des candidats :")
    for c in candidats_reels:
        print(f"  - {c}")


# QUESTION 3
def scores_nationaux(df_candidats_uniquement):
    total_exprimes = df_candidats_uniquement["voix"].sum()
    df_scores_nationaux = (
        df_candidats_uniquement.groupby("candidat", as_index=False)["voix"]
        .sum()
        .rename(columns={"voix": "votes_national"})
        .sort_values("votes_national", ascending=False)
        .reset_index(drop=True)
    )
    df_scores_nationaux["score_national"] = (
        df_scores_nationaux["votes_national"] / total_exprimes * 100
    ).round(2)
    return df_scores_nationaux


def tableau_scores_nationaux(df_scores_nationaux):
    # Affichage mis en forme
    display_df = df_scores_nationaux.copy()
    display_df["votes_national"] = display_df["votes_national"].apply(
        lambda x: f"{x:,}".replace(",", " ")
    )
    display_df["score_national"] = display_df["score_national"].apply(
        lambda x: f"{x:.2f}%"
    )
    display_df.columns = [
        "Candidat",
        "Nombre votes (total)",
        "Score (% votes exprimés)",
    ]

    print("Résultats du premier tour (10 avril 2022)")
    print(display_df)


def tableau_scores_nationaux_gt(df_scores_nationaux):
    # création de l'objet GT
    st_table = (
        GT(df_scores_nationaux)
        .tab_header(
            title="Elections",
            subtitle="Résultats du premier tour (10 avril 2022)"
        )
        .cols_label(
            candidat="Candidat",
            votes_national="Nombre votes (total)",
            score_national="Score (% votes exprimés.)"
        )
        # Formatage des nombres (séparateur de milliers)
        .fmt_number(
            columns="votes_national",
            sep_mark=" ",
            decimals=0
        )
        # Formatage des pourcentages
        .fmt_percent(
            columns="score_national",
            decimals=2,
            scale_values=False
        )
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.body(columns="candidat")
        )
    )  
    return st_table

