"""Compara estimadores da nota IMDb após o lançamento dos filmes."""
from pathlib import Path
import argparse
import pickle

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import FunctionTransformer
from entradas import preparar


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    dados = pd.read_csv(parser.parse_args().csv)
    x, teste, y, notas = train_test_split(
        preparar(dados), dados.IMDB_Rating, test_size=0.2, random_state=42
    )
    referencia = DummyRegressor(strategy="median")
    modelos = {
        "Mediana": referencia,
        "Ridge": make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                               StandardScaler(), Ridge(alpha=1)),
        "Floresta": make_pipeline(SimpleImputer(strategy="median", add_indicator=True),
                                  RandomForestRegressor(n_estimators=300, min_samples_leaf=5,
                                                        random_state=42)),
    }
    partes = KFold(n_splits=5, shuffle=True, random_state=42)
    erros = {}
    for nome, modelo in modelos.items():
        erros[nome] = -cross_val_score(modelo, x, y, cv=partes,
                                       scoring="neg_mean_absolute_error").mean()
        print(f"{nome}: MAE em validação = {erros[nome]:.4f}")
    vencedor = min(erros, key=erros.get)
    sem_votos = -cross_val_score(modelos[vencedor], x.drop(columns="log_votos"), y,
                                 cv=partes, scoring="neg_mean_absolute_error").mean()
    print(f"{vencedor} sem votos: MAE em validação = {sem_votos:.4f}")
    for nome in dict.fromkeys(["Mediana", vencedor]):
        previsto = clone(modelos[nome]).fit(x, y).predict(teste)
        print(f"{nome} no teste: MAE={mean_absolute_error(notas, previsto):.4f}, "
              f"RMSE={root_mean_squared_error(notas, previsto):.4f}, "
              f"R2={r2_score(notas, previsto):.4f}")
    pipeline = make_pipeline(FunctionTransformer(preparar), clone(modelos[vencedor]))
    pipeline.fit(dados.loc[x.index], y)
    destino = (Path(__file__).resolve().parents[1] / "modelos" / "modelo_imdb.pkl")
    pacote = pickle.dumps(pipeline, protocol=5)
    recarregado = pickle.loads(pacote)
    np.testing.assert_allclose(recarregado.predict(dados.loc[teste.index]), previsto, rtol=0, atol=0)
    destino.write_bytes(pacote)
    print(f"{vencedor}: {len(teste)} previsões reproduzidas. Modelo salvo em {destino.name}.")


if __name__ == "__main__":
    main()
