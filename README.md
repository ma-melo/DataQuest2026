# DataQuest 2026 (ASA)

Análise dos dados do **World Population Prospects 2024 (WPP2024)** da ONU para o
ASA DataQuest 2026.

## Estrutura

```
data/
  raw/          dados originais (NÃO versionados)
  processed/    dados derivados (NÃO versionados)
src/
  dados.py      funções de carregamento dos dados
notebooks/
  01_exploracao.ipynb
figures/        gráficos gerados
slides/         apresentação
```

## Dados

Os dados **não** são commitados. Baixe a pasta do DataQuest e coloque os arquivos
diretamente em `data/raw/`:

- `WPP2024_Demographic_Indicators_Medium_csv` (ou a versão `.gz`)
- `WPP2024_Demographic_Indicators_OtherVariants.csv` (ou a versão `.gz`)
- `WPP2024_Demographic_Indicators_notes.csv`: dicionário dos indicadores
- `WPP2024_Supplement_Births_and_LE60.csv`
- `2026DataQuest_WPP2024_Getting_Started.docx` e `WPP2024_Supplement_Description.docx`

## Como rodar

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
```

Teste o carregamento a partir da raiz do repositório:

```bash
python -c "from src.dados import carregar_medium; print(carregar_medium().shape)"
```

No notebook:

```python
from src.dados import carregar_medium, carregar_notas, paises
df = carregar_medium()
```

## Fluxo de trabalho

- Não faça push direto na `main`: crie um branch e abra um Pull Request.
- Nunca commite arquivos de `data/raw/` (o `.gitignore` já bloqueia).
