"""Funções para carregar os dados do World Population Prospects 2024 (WPP2024).

Os arquivos ficam em data/raw/ e não são versionados.
"""

from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
DADOS_RAW = RAIZ / "data" / "raw"


def _primeiro_existente(*nomes):
    """Retorna o caminho do primeiro arquivo de `nomes` que existe em data/raw."""
    for nome in nomes:
        caminho = DADOS_RAW / nome
        if caminho.exists():
            return caminho
    raise FileNotFoundError(
        f"Nenhum dos arquivos {nomes} foi encontrado em {DADOS_RAW}. "
        "Coloque os dados do DataQuest em data/raw/ (veja o README)."
    )


def _ler_csv(caminho):
    # utf-8-sig remove o BOM do início dos CSVs do WPP
    return pd.read_csv(caminho, encoding="utf-8-sig", low_memory=False)


def carregar_medium():
    """Indicadores demográficos, variante Medium (1950-2100)."""
    return _ler_csv(_primeiro_existente(
        "WPP2024_Demographic_Indicators_Medium.csv",
        "WPP2024_Demographic_Indicators_Medium_csv",
        "WPP2024_Demographic_Indicators_Medium_csv.gz",
    ))


def carregar_outras_variantes():
    """Indicadores demográficos das demais variantes de projeção (High, Low, ...)."""
    return _ler_csv(_primeiro_existente(
        "WPP2024_Demographic_Indicators_OtherVariants.csv",
        "WPP2024_Demographic_Indicators_OtherVariants_csv.gz",
    ))


def carregar_notas():
    """Dicionário dos indicadores (nome, descrição e unidade)."""
    return _ler_csv(_primeiro_existente("WPP2024_Demographic_Indicators_notes.csv"))


def carregar_suplemento():
    """Suplemento: nascimentos por sexo e expectativa de vida aos 60 anos."""
    return _ler_csv(_primeiro_existente("WPP2024_Supplement_Births_and_LE60.csv"))


def paises(df):
    """Filtra apenas linhas de países/áreas (exclui regiões e agregados)."""
    return df[df["ISO3_code"].notna()]
