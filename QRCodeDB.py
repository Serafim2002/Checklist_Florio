import tkinter as tk
from tkinter import ttk
import pandas as pd

def load_csv(path):
    """Carrega o CSV com dados de produtos e normaliza os dados."""
    try:
        df = pd.read_csv(path, sep=';', encoding='utf-8')
        if 'Codigo' not in df.columns or 'Descricao' not in df.columns:
            raise ValueError("Colunas 'Codigo' e 'Descricao' não encontradas no CSV.")
        # Normaliza os dados
        df['Codigo'] = df['Codigo'].astype(str).str.strip()  # Garante que 'Codigo' é string e remove espaços
        df['Descricao'] = df['Descricao'].str.strip()  # Remove espaços da descrição
        return df
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        return pd.DataFrame()  # Retorna DataFrame vazio em caso de erro

def process_data(event):
    """Lê o QR Code e exibe os nomes dos produtos."""
    data = input_field.get().strip()
    input_field.delete(0, tk.END)  # Limpa o campo de entrada

    if not data:
        status_label.config(text="Erro: QR Code vazio!", foreground="red")
        return

    lines = data.splitlines()
    if len(lines) < 2:
        status_label.config(text="Formato inválido do QR Code!", foreground="red")
        return

    order = lines[0]  # Número do pedido
    codes = lines[1:]  # Lista de códigos de produtos

    # Buscar nomes dos produtos
    items = []
    for code in codes:
        try:
            qty, product_code = code.split()  # Divide quantidade e código
            product_code = product_code.strip()
            name = products_dict.get(product_code, "Produto não encontrado")
            items.append(f"{qty}x {name}")
        except ValueError:
            items.append(f"{code} - Formato inválido")

    # Atualizar a área de resultado
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"Pedido: {order}\n\n")
    result_box.insert(tk.END, "Itens:\n")
    for item in items:
        result_box.insert(tk.END, f"- {item}\n")

    status_label.config(text="QR Code processado!", foreground="green")

# Caminho para o CSV
csv_path = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/Excel/Produto.csv"
prod_df = load_csv(csv_path)
products_dict = prod_df.set_index('Codigo')['Descricao'].to_dict() if not prod_df.empty else {}

# Janela principal
app = tk.Tk()
app.title("Leitor de QR Code")
app.geometry("500x400")
app.configure(bg="#dcdad5")

# Estilo
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#dcdad5", foreground="#000000", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))
style.configure("TButton", font=("Arial", 12))

# Layout
frame = ttk.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Escaneie o QR Code:").pack(anchor="w")

input_field = ttk.Entry(frame, width=50)
input_field.pack(pady=10, fill="x")
input_field.bind("<Return>", process_data)

status_label = ttk.Label(frame, text="", font=("Arial", 10, "bold"))
status_label.pack(pady=5, anchor="w")

ttk.Label(frame, text="Resultado:").pack(anchor="w")
result_box = tk.Text(frame, height=10, wrap="word", bg="#ffffff", fg="#000000", font=("Arial", 11))
result_box.pack(pady=10, fill="both", expand=True)

# Inicia o app
input_field.focus()
app.mainloop()
