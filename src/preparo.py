"""Preparação dos dados do WPP2024 para a clusterização.

Filtra apenas países, restringe o período, padroniza os indicadores e monta
as matrizes usadas pelos métodos de clusterização (vetor e série temporal).
"""

import numpy as np
import pandas as pd

from src.dados import carregar_medium

INDICADORES = ["TFR", "LEx", "IMR", "MedianAgePop"]
PERIODO_ESTIMADO = (1950, 2023)


def carregar_paises(anos=PERIODO_ESTIMADO, pop_minima_mil=None):
    """Países no período informado, com os indicadores de INDICADORES.

    `pop_minima_mil` exclui países cuja população média no período fica abaixo
    desse valor (em milhares). Por padrão nenhum país é excluído.
    """
    df = carregar_medium()
    df = df[df["LocTypeName"] == "Country/Area"]
    df = df[df["Time"].between(*anos)]

    if pop_minima_mil is not None:
        media = df.groupby("LocID")["TPopulation1July"].mean()
        validos = media[media >= pop_minima_mil].index
        df = df[df["LocID"].isin(validos)]

    colunas = ["LocID", "ISO3_code", "Location", "Time"] + INDICADORES
    return df[colunas].sort_values(["LocID", "Time"]).reset_index(drop=True)


def padronizar(df, indicadores=INDICADORES):
    """Z-score global por indicador, calculado sobre todos os países e anos.

    Usa média e desvio de todo o conjunto, e não de cada série, para manter as
    diferenças de nível entre países.
    """
    df = df.copy()
    media = df[indicadores].mean()
    desvio = df[indicadores].std()
    df[indicadores] = (df[indicadores] - media) / desvio
    return df


def matriz_series(df, indicadores=INDICADORES):
    """Array 3D (países, anos, indicadores) para o DTW do tslearn.

    Devolve também os LocIDs e os nomes na mesma ordem das linhas do array.
    Exige que todas as séries tenham o mesmo comprimento.
    """
    ids, nomes, series = [], [], []
    for loc_id, grupo in df.sort_values(["LocID", "Time"]).groupby("LocID"):
        ids.append(loc_id)
        nomes.append(grupo["Location"].iloc[0])
        series.append(grupo[indicadores].to_numpy())
    return np.stack(series), ids, nomes


def matriz_vetor(df, indicadores=INDICADORES, passo=5):
    """Uma linha por país, com indicadores × anos (a cada `passo` anos).

    Usada pelo k-means e pela clusterização hierárquica.
    """
    anos = sorted(df["Time"].unique())[::passo]
    filtrado = df[df["Time"].isin(anos)]
    wide = filtrado.pivot_table(index=["LocID", "Location"], columns="Time", values=indicadores)
    wide.columns = [f"{ind}_{ano}" for ind, ano in wide.columns]
    return wide.reset_index()
