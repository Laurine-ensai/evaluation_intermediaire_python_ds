import numpy as np

######## QUESTION 1 (a) ############

def taille_max_code_commune(df):
    taille_max = df['code_commune'].astype(str).str.len().max()
    print(f"La taille maximale du code commune est de {taille_max} caractères.")


def nb_occurence_longueur_code_departement(df):
    print(df['code_departement'].astype(str).str.len().value_counts())


def departement_11_caractères(df):
    df_louche = df[df['code_departement'].astype(str).str.len() == 11]
    print("Valeurs suspectes dans code_departement :")
    print(df_louche['code_departement'].unique())
    print("\nExtrait des lignes correspondantes :")
    print(df_louche.head())


def maj_code_commune(df):
    df['code_commune'] = (
        df['code_departement'].astype(str) +
        df['code_commune'].astype(str).str.zfill(3)
    )


def verification_Montrouge(df):
    print("Exemple Montrouge :")
    print(df[df['libelle_commune'].str.contains('Montrouge', na=False)][['code_commune', 'libelle_commune']].drop_duplicates().head())


######## QUESTION 1 (b) ############

def entites_uniques(df):
    entites_uniques = (
        df[['nom', 'prenom']]
        .drop_duplicates()
        .sort_values('nom')
        .reset_index(drop=True)
    )
    print(entites_uniques)


cas_speciaux = ['abstentions', 'blancs', 'nuls']


def creation_candidat(df):
    df['candidat'] = np.where(
        df['nom'].isin(cas_speciaux),
        df['nom'],
        df['prenom'].astype(str) + ' ' + df['nom'].astype(str)
    )


def aperçu_des_candidats(df):
    print("\nAperçu des candidats :")
    print(df['candidat'].unique()[:5])


######## QUESTION 2 ############

def nb_candidats(df):
    df_candidats_uniquement = df[~df['candidat'].isin(cas_speciaux)]
    candidats_reels = df_candidats_uniquement['candidat'].unique()
    candidats = len(candidats_reels)
    print(f"En 2022, il y avait {candidats} candidats à l'élection présidentielle.")
    print("\nListe des candidats :")
    for c in sorted(candidats_reels):
        print(f"  - {c}")


######## QUESTION 3 ############

def q3(df):
    df_candidats_uniquement = df[~df['candidat'].isin(cas_speciaux)].copy()
    total_exprimes = df_candidats_uniquement['voix'].sum()
    scores_nationaux = (
        df_candidats_uniquement
        .groupby('candidat', as_index=False)['voix']
        .sum()
        .rename(columns={'voix': 'votes_national'})
        .sort_values('votes_national', ascending=False)
        .reset_index(drop=True)
    )
    scores_nationaux['score_national'] = (
        scores_nationaux['votes_national'] / total_exprimes * 100
    ).round(2)

    # Affichage mis en forme
    display_df = scores_nationaux.copy()
    display_df['votes_national'] = display_df['votes_national'].apply(lambda x: f"{x:,}".replace(',', ' '))
    display_df['score_national'] = display_df['score_national'].apply(lambda x: f"{x:.2f}%")
    display_df.columns = ['Candidat', 'Nombre votes (total)', 'Score (% votes exprimés)']

    print("Résultats du premier tour (10 avril 2022)")
    print(display_df)




import pandas as pd
df = pd.read_csv(
 'https://www.data.gouv.fr/fr/datasets/r/182268fc-2103-4bcb-a850-6cf90b02a9eb'
)



