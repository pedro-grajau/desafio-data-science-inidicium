"""Regera as tabelas de evidências em Markdown a partir do CSV do desafio."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, jaccard_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer


def tabela(titulo, colunas, linhas):
    def linha(itens):
        return "| " + " | ".join(str(v) for v in itens) + " |"
    return "\n".join(["## " + titulo, "", linha(colunas), linha(["---"] * len(colunas)),
                      *(linha(valores) for valores in linhas), ""])


def descrever(d):
    tabelas = []
    cobertura = []
    for dec, grupo in d.groupby("decada"):
        com = grupo.loc[grupo.receita.notna(), "No_of_Votes"]
        sem = grupo.loc[grupo.receita.isna(), "No_of_Votes"]
        cobertura.append([int(dec), len(grupo), len(com), len(sem), f"{len(sem)/len(grupo):.1%}",
                          com.median() if len(com) else "—", sem.median()])
    tabelas.append(tabela("Cobertura e votos por década",
                          ["Década", "Filmes", "Com receita", "Sem receita", "% ausente",
                           "Mediana de votos com receita", "Mediana sem receita"], cobertura))
    faixas = d.groupby(pd.qcut(d.No_of_Votes, 4), observed=True)
    tabelas.append(tabela("Notas por quartil de votos", ["Quartil", "Filmes", "Votos mín.",
                          "Votos máx.", "Nota mediana"], [
        [i, len(g), g.No_of_Votes.min(), g.No_of_Votes.max(), g.IMDB_Rating.median()]
        for i, (_, g) in enumerate(faixas, 1)]))
    rho = d.No_of_Votes.corr(d.IMDB_Rating, method="spearman")
    tabelas.append(f"Spearman entre votos e nota nos {len(d)} filmes = {rho:.3f}.\n")
    for multiplicador in [0.5, 1, 2]:
        media = d.IMDB_Rating.mean()
        peso = d.No_of_Votes / (d.No_of_Votes + d.No_of_Votes.median() * multiplicador)
        ranking = d.assign(score=media + peso * (d.IMDB_Rating - media)).nlargest(3, "score")
        tabelas.append(tabela(f"Recomendação com referência de {multiplicador:g} × mediana dos votos",
                              ["Filme", "Nota", "Votos", "Pontuação"], [
            [r.Series_Title, r.IMDB_Rating, r.No_of_Votes, f"{r.score:.3f}"]
            for r in ranking.itertuples()]))
    return tabelas


def faturamento(d):
    s = d.dropna(subset=["receita"]).copy()
    linhas = []
    for campo in ["No_of_Votes", "IMDB_Rating", "Meta_score", "minutos", "ano"]:
        pares = s[[campo, "receita"]].dropna()
        linhas.append([campo, len(pares), f"{pares[campo].corr(pares.receita, method='spearman'):.3f}"])
    tabelas = [tabela("Associações com faturamento", ["Variável", "Filmes", "Spearman"], linhas)]
    tabelas.append(tabela("Receita por quartil de votos entre filmes com receita",
                          ["Quartil", "Filmes", "Receita mediana"], [
        [i, len(g), g.receita.median()] for i, (_, g) in
        enumerate(s.groupby(pd.qcut(s.No_of_Votes, 4), observed=True), 1)]))
    s["aventura"] = s.Genre.str.split(", ").map(lambda tags: "Adventure" in tags)
    tabelas.append(tabela("Receita mediana por grupo", ["Década", "Aventura", "Filmes", "Mediana"],
                          [["Todas", a, len(g), g.receita.median()] for a, g in s.groupby("aventura")] +
                          [[int(dec), a, len(g), g.receita.median()]
                           for (dec, a), g in s.groupby(["decada", "aventura"])]))
    s = s.dropna(subset=["decada"]).copy()
    for q in [0.75, 0.90]:
        s["sucesso"] = s.receita >= s.groupby("decada").receita.transform("quantile", q=q)
        linhas = []
        for dec, grupo in [*s.groupby("decada"), ("Todas", s)]:
            for aventura, g in grupo.groupby("aventura"):
                linhas.append([dec, aventura, len(g), g.sucesso.sum(), f"{g.sucesso.mean():.1%}"])
        tabelas.append(tabela(f"Bilheteria no percentil {100*q:g} ou superior de cada década",
                              ["Década", "Aventura", "Filmes", "Sucessos", "Frequência"], linhas))
    return tabelas


def sinopses(d):
    treino, teste = train_test_split(np.arange(len(d)), test_size=.2, random_state=42)
    tags = d.Genre.str.split(", ")
    rotulos = MultiLabelBinarizer().fit(tags.iloc[treino])
    y = rotulos.transform(tags)
    vetor = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=2, sublinear_tf=True)
    x = vetor.fit_transform(d.Overview.iloc[treino])
    modelo = OneVsRestClassifier(LogisticRegression(class_weight="balanced", max_iter=1000)).fit(x, y[treino])
    p = modelo.predict(vetor.transform(d.Overview.iloc[teste]))
    base = np.tile(y[treino].mean(axis=0) >= .5, (len(teste), 1))
    metricas = []
    for nome, pred in [("Regra constante", base), ("TF-IDF + logística", p)]:
        linha = [nome]
        for metrica, media in [(precision_score, "micro"), (recall_score, "micro"), (f1_score, "micro"),
                               (precision_score, "samples"), (jaccard_score, "samples")]:
            linha.append(f"{metrica(y[teste], pred, average=media, zero_division=0):.3f}")
        linha += [f"{accuracy_score(y[teste], pred):.3f}", (pred.sum(axis=1) == 0).sum()]
        metricas.append(linha)
    termos = vetor.get_feature_names_out()
    exemplos = [[d.Series_Title.iloc[i], ", ".join(tags.iloc[i]),
                 ", ".join(rotulos.classes_[p[j].astype(bool)])]
                for j, i in enumerate(teste) if d.Series_Title.iloc[i] in {"Gone Girl", "Anatomy of a Murder"}]
    return [tabela("Gêneros a partir da sinopse", ["Método", "Precisão micro", "Cobertura micro",
                   "F1 micro", "Precisão por filme", "Jaccard por filme", "Acerto exato", "Sem sugestão"], metricas),
            tabela("Palavras e pares com maior coeficiente", ["Gênero", "Termos"], [
                [tag, ", ".join(termos[np.argsort(est.coef_[0])[-5:][::-1]])]
                for tag, est in zip(rotulos.classes_, modelo.estimators_)]),
            tabela("Exemplos no teste", ["Filme", "Cadastro", "Sugestão"], exemplos)]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    d = pd.read_csv(parser.parse_args().csv)
    d["ano"] = pd.to_numeric(d.Released_Year, errors="coerce")
    d["decada"] = d.ano // 10 * 10
    d["receita"] = pd.to_numeric(d.Gross.str.replace(",", ""))
    d["minutos"] = pd.to_numeric(d.Runtime.str.extract(r"(\d+)")[0])
    tabelas = descrever(d) + faturamento(d) + sinopses(d)
    Path(__file__).with_name("evidencias.md").write_text(
        "# Tabelas das análises\n\n" + "\n".join(tabelas), encoding="utf-8")
