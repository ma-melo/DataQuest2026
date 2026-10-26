"""Copia os arquivos do DataQuest para data/raw/.

A origem pode ser a pasta descompactada ou o próprio .zip baixado.

Uso (a partir da raiz do repositório):

    python scripts/copiar_dados.py                        # origem padrão (abaixo)
    python scripts/copiar_dados.py CAMINHO_DA_PASTA       # pasta descompactada
    python scripts/copiar_dados.py "2026 ASA DataQuest.zip"  # o zip direto

Sem argumento, usa a pasta "2026 ASA DataQuest/" ou, se ela não existir,
o zip "2026 ASA DataQuest.zip", ambos na raiz do repositório.

Os arquivos são copiados, não movidos: a origem continua intacta.
"""

import shutil
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "data" / "raw"
ORIGEM_PADRAO_PASTA = RAIZ / "2026 ASA DataQuest"
ORIGEM_PADRAO_ZIP = RAIZ / "2026 ASA DataQuest.zip"

ARQUIVOS = [
    "WPP2024_Demographic_Indicators_Medium_csv.gz",
    "WPP2024_Demographic_Indicators_OtherVariants_csv.gz",
    "WPP2024_Demographic_Indicators_notes.csv",
    "WPP2024_Supplement_Births_and_LE60.csv",
    "2026DataQuest_WPP2024_Getting_Started.docx",
    "WPP2024_Supplement_Description.docx",
]


def _origem_padrao():
    if ORIGEM_PADRAO_PASTA.is_dir():
        return ORIGEM_PADRAO_PASTA
    return ORIGEM_PADRAO_ZIP


def _copiar_de_pasta(pasta):
    faltando = []
    for nome in ARQUIVOS:
        arquivo = pasta / nome
        if not arquivo.exists():
            faltando.append(nome)
            continue
        shutil.copy2(arquivo, DESTINO / nome)
        print(f"Copiado: {nome}")
    return faltando


def _copiar_de_zip(caminho_zip):
    faltando = []
    with zipfile.ZipFile(caminho_zip) as zf:
        # Procura pelo nome do arquivo, ignorando qualquer pasta dentro do zip
        membros = {
            Path(info.filename).name: info
            for info in zf.infolist()
            if not info.is_dir()
        }
        for nome in ARQUIVOS:
            if nome not in membros:
                faltando.append(nome)
                continue
            with zf.open(membros[nome]) as origem, open(DESTINO / nome, "wb") as destino:
                shutil.copyfileobj(origem, destino)
            print(f"Copiado: {nome}")
    return faltando


def main():
    origem = Path(sys.argv[1]) if len(sys.argv) > 1 else _origem_padrao()

    DESTINO.mkdir(parents=True, exist_ok=True)

    if origem.is_dir():
        faltando = _copiar_de_pasta(origem)
    elif origem.is_file() and zipfile.is_zipfile(origem):
        faltando = _copiar_de_zip(origem)
    else:
        print(f"Pasta ou zip não encontrado: {origem}")
        return 1

    if faltando:
        print("\nArquivos não encontrados na origem:")
        for nome in faltando:
            print(f"  - {nome}")
        return 1

    print(f"\nPronto. Dados disponíveis em {DESTINO}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
