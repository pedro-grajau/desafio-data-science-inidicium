"""Estima a nota IMDb a partir de um objeto JSON."""
import argparse
import json
import pickle
from pathlib import Path

import pandas as pd


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("filme", type=Path)
    registro = json.loads(parser.parse_args().filme.read_text(encoding="utf-8"))
    with Path(__file__).with_name("modelo_imdb.pkl").open("rb") as arquivo:
        modelo = pickle.load(arquivo)
    nota = modelo.predict(pd.DataFrame([registro]))[0]
    print(f"Nota IMDb estimada: {nota:.1f} ({nota:.4f} antes do arredondamento)")
