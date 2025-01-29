import pandas as pd
import tkinter as tk
from tkinter import messagebox

def msg_erro(msg):
    root = tk.Tk()
    root.withdraw() 
    messagebox.showerror("Erro", msg)
    root.quit()

def load_csv(path):
    """Carrega o CSV e normaliza os dados."""
    try:
        df = pd.read_csv(path, sep=';', encoding='utf-8')
        
        if not {'D04_cod', 'D04_Descricao'}.issubset(df.columns):
            raise ValueError("Colunas 'D04_cod' e 'D04_Descricao' ausentes.")
        
        df['D04_cod'] = df['D04_cod'].astype(str).str.strip()
        df['D04_Descricao'] = df['D04_Descricao'].str.strip()
        
        return df.set_index('D04_cod')['D04_Descricao'].to_dict()
    except Exception as e:
        msg = f"Erro ao carregar CSV: {e}"
        msg_erro(msg)
