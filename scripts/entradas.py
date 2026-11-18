"""Conversão dos cinco campos disponíveis após o lançamento."""
import numpy as np
import pandas as pd


def preparar(dados):
    return pd.DataFrame({
        "ano": pd.to_numeric(dados.Released_Year, errors="coerce"),
        "minutos": pd.to_numeric(dados.Runtime.astype("string").str.extract(r"(\d+)")[0]),
        "critica": pd.to_numeric(dados.Meta_score),
        "log_votos": np.log1p(pd.to_numeric(dados.No_of_Votes)),
        "log_receita": np.log1p(pd.to_numeric(dados.Gross.astype("string").str.replace(",", ""))),
    }).astype(float)
