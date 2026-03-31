import matplotlib.pyplot as plt

# QUESTION 4


def calculer_score_departements(df_candidats_uniquement):
    total_par_dept = (
        df_candidats_uniquement.groupby("code_departement")["voix"]
        .sum()
        .reset_index()
        .rename(columns={"voix": "total_dept"})
    )
    votes_dept = (
        df_candidats_uniquement.groupby(
            ["code_departement", "candidat"], as_index=False
        )["voix"]
        .sum()
        .rename(columns={"voix": "votes"})
    )
    score_departements = votes_dept.merge(total_par_dept, on="code_departement")
    score_departements["score"] = (
        score_departements["votes"] / score_departements["total_dept"] * 100
    ).round(2)
    score_departements = score_departements.drop(columns="total_dept")
    return score_departements


def verifier_resultats_aude_q4(score_departements):
    print("Vérification pour l'Aude (dept 11) :")
    dept11 = score_departements[
        score_departements["code_departement"].astype(str) == "11"
    ].sort_values("votes", ascending=False)
    dept11_display = dept11.copy()
    dept11_display["score"] = dept11_display["score"].apply(lambda x: f"{x:.2f}%")
    print(dept11_display)


# QUESTION 5


def comparer_scores_departementaux_nationaux(
    df_scores_nationaux, df_score_departements
):
    score_departements = df_score_departements.merge(
        df_scores_nationaux[["candidat", "votes_national", "score_national"]],
        on="candidat",
    ).rename(columns={"votes": "votes_departement", "score": "score_departement"})
    return score_departements


def verifier_resultats_aude_q5(score_departements):
    mask_aude = score_departements["code_departement"].astype(str) == "11"
    aude_top = (
        score_departements[mask_aude]
        .sort_values("votes_departement", ascending=False)
        .copy()
    )

    for col in ["score_departement", "score_national"]:
        aude_top[col] = aude_top[col].map("{:.2f}%".format)

    print("\nVérification Question 5 - Département 11 (Aude) :")
    print(aude_top.to_string(index=False))


# QUESTION 6


def creation_surrepresentation(score_departements):
    score_departements["surrepresentation"] = (
        (score_departements["score_departement"] - score_departements["score_national"])
        / score_departements["score_national"]
        * 100
    ).round(2)




# QUESTION 7


def plot_surrepresentation(score_departements, candidat_nom, n_top=5):
    data = score_departements[score_departements["candidat"] == candidat_nom].copy()

    if data.empty:
        print(f"Candidat '{candidat_nom}' non trouvé.")
        return

    data["abs_surrepresentation"] = data["surrepresentation"].abs()
    top_data = data.nlargest(n_top, "abs_surrepresentation").sort_values(
        "surrepresentation"
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(
        top_data["code_departement"].astype(str),
        top_data["surrepresentation"],
        color="blue",
        edgecolor="white",
    )

    ax.axvline(0, color="black", linewidth=0.8)
    nom_affiche = candidat_nom.split()[-1]  # Affiche le nom de famille
    ax.set_title(
        f"Top {n_top} des surreprésentations de {nom_affiche}",
        fontsize=13,
        fontweight="bold",
    )
    ax.set_xlabel("Surreprésentation")
    ax.set_ylabel("Département")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()
