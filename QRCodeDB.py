import tkinter as tk
from tkinter import ttk
import pandas as pd

def load_csv(path):
    """Carrega o CSV e normaliza os dados."""
    try:
        df = pd.read_csv(path, sep=';', encoding='utf-8')
        if not {'Codigo', 'Descricao'}.issubset(df.columns):
            raise ValueError("Colunas 'Codigo' e 'Descricao' ausentes.")
        df['Codigo'] = df['Codigo'].astype(str).str.strip()
        df['Descricao'] = df['Descricao'].str.strip()
        return df
    except Exception as e:
        print(f"Erro ao carregar CSV: {e}")
        return pd.DataFrame()

def process_qr(event):
    """Processa o QR Code e exibe os produtos."""
    qr_data = input_field.get().strip()
    input_field.delete(0, tk.END)
    # Limpa os resultados anteriores
    result_box.delete("1.0", tk.END)

    if not qr_data:
        update_status("Erro QR Code vazio!", "red")
        return

    lines = qr_data.splitlines()
    if len(lines) < 2:
        update_status("Formato inválido!", "red")
        return

    order_id = lines[0]
    items = process_items(lines[1:])

    display_results(order_id, items)
    update_status("QR Code processado!", "green")

def process_items(lines):
    """Processa os itens do QR Code."""
    items = []
    for line in lines:
        try:
            qty, code = line.split()
            name = prod_dict.get(code.strip(), "Produto não encontrado")
            items.append(f"{qty}x          {name}")
        except ValueError:
            items.append(f"{line} - Formato inválido")
    return items

def display_results(order_id, items):
    """Exibe os resultados no Text widget."""
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"Pedido: {order_id}\n\n")
    result_box.insert(tk.END, "Qty:       Des:\n")
    result_box.insert(tk.END, "\n".join(items))

def update_status(message, color):
    """Atualiza a mensagem de status."""
    status_label.config(text=message, foreground=color)

# Configurações iniciais
csv_path = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/Excel/Produto.csv"
prod_df = load_csv(csv_path)
prod_dict = prod_df.set_index('Codigo')['Descricao'].to_dict() if not prod_df.empty else {}

# Janela principal
app = tk.Tk()
app.title("Leitor de QR Code")
app.geometry("600x500")  # Aumenta o tamanho da janela
app.configure(bg="#dcdad5")

# Estilo
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#dcdad5", foreground="#000", font=("Arial", 14))  # Aumenta o tamanho da fonte
style.configure("TEntry", font=("Arial", 14))  # Aumenta o tamanho da fonte
style.configure("TButton", font=("Arial", 14))  # Aumenta o tamanho da fonte

# Layout
frame = ttk.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Escaneie o QR Code:").pack(anchor="w")
input_field = ttk.Entry(frame, width=60)  # Aumenta a largura do campo de entrada
input_field.pack(pady=10, fill="x")
input_field.bind("<Return>", process_qr)

status_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"))  # Aumenta o tamanho da fonte
status_label.pack(pady=5, anchor="w")

ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

ttk.Label(frame, text="Resultado:").pack(anchor="w")
result_box = tk.Text(frame, height=15, wrap="word", bg="#fff", fg="#000", font=("Arial", 13))  # Aumenta o tamanho da fonte e a altura da caixa de texto
result_box.pack(pady=10, fill="both", expand=True)

# Inicia o app
app.mainloop()
