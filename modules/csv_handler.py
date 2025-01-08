import pandas as pd

def load_csv(path):
    """Carrega o CSV e normaliza os dados."""
    try:
        df = pd.read_csv(path, sep=';', encoding='utf-8')
        if not {'Codigo', 'Descricao'}.issubset(df.columns):
            raise ValueError("Colunas 'Codigo' e 'Descricao' ausentes.")
        df['Codigo'] = df['Codigo'].astype(str).str.strip()
        df['Descricao'] = df['Descricao'].str.strip()
        return df.set_index('Codigo')['Descricao'].to_dict()
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return {}
