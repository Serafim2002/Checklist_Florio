import tkinter as tk
from tkinter import ttk
from modules.csv_handler import load_csv
from modules.qr_processor import process_qr_data
from modules.utils import update_status
import subprocess

# Carregar o dicionário de produtos
csv_path = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/data/Produto.csv"
prod_dict = load_csv(csv_path)

def process_qr(event=None):
    """Função para processar o QR Code."""
    qr_data = input_field.get().strip()
    input_field.delete(0, tk.END)
    result_box.delete("1.0", tk.END)

    if not qr_data: 
        update_status(status_label, "Erro QR Code vazio!", "red")
        return

    result = process_qr_data(qr_data, prod_dict)
    if result["error"]:
        update_status(status_label, result["message"], "red")
    else:
        result_box.insert(tk.END, result["output"])
        update_status(status_label, "QR Code processado!", "green")

def finalizar():
    """Função executada ao clicar em 'Finalizar'."""
    try:
        subprocess.run(["python", "outro_programa.py"], check=True)
        update_status(status_label, "Processo finalizado com sucesso!", "green")
    except Exception as e:
        update_status(status_label, f"Erro ao executar o programa: {e}", "red")

# Configuração da interface
app = tk.Tk()
app.title("Leitor de QR Code")
app.geometry("800x600")
app.configure(bg="#dcdad5")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#dcdad5", font=("Arial", 14))
style.configure("TEntry", font=("Arial", 14))
style.configure("TButton", font=("Arial", 14))

frame = ttk.Frame(app, padding=20)
frame.pack(expand=True, fill="both")

ttk.Label(frame, text="Escaneie o QR Code:").pack(anchor="w")
input_field = ttk.Entry(frame, width=60)
input_field.pack(pady=10, fill="x")
input_field.bind("<Return>", process_qr)

status_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"))
status_label.pack(pady=5, anchor="w")

ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

ttk.Label(frame, text="Resultado:").pack(anchor="w")
result_box = tk.Text(frame, height=15, wrap="word", bg="#fff", font=("Arial", 13))
result_box.pack(pady=10, fill="both", expand=True)

ttk.Button(frame, text="Finalizar", command=finalizar).pack(pady=20)

app.mainloop()
