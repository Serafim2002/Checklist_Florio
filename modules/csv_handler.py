import pandas as pd
import tkinter as tk
from tkinter import messagebox

def mostrar_erro(mensagem_erro):
    root = tk.Tk()
    root.withdraw() 
    messagebox.showerror("Erro", mensagem_erro)
    root.quit()

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
        mensagem_erro = f"Erro ao carregar CSV: {e}"
        mostrar_erro(mensagem_erro)
