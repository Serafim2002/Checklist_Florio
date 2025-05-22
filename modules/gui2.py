import tkinter as tk
from tkinter import ttk
import subprocess
import sys

from modules.csv_handler import load_csv
from modules.qr_lote import qr_lote
from modules.utils import update_status

def setup_gui2():
    CSV_PATH = "D:/Projetos/Checklist_Florio/data/D04_Produto_Con.csv"
    prod_dict = load_csv(CSV_PATH)

    def carregar_escaneado():
        try:
            with open("D:/Projetos/Checklist_Florio/Result/QrLote.txt", "r", encoding="utf-8") as file:
                return file.read() 
        except FileNotFoundError:
            return "" 

    def process_qr():
        qr_data = input_field.get("1.0", tk.END).strip()
        if not qr_data:
            update_status(status_label, "Erro: QR Code vazio!", "red")
            return

        result = qr_lote(qr_data, prod_dict)
        if result["error"]:
            update_status(status_label, result["message"], "red")
        else:
            result_box.config(state="normal")
            result_box.delete("1.0", tk.END)
            result_box.insert(tk.END, result["output"])
            result_box.config(state="disabled")
            update_status(status_label, "QR Code processado com sucesso!", "green")

    def finalizar():
        with open("D:/Projetos/Checklist_Florio/Result/QrLote.txt", "w", encoding="utf-8") as file:
            file.write(input_field.get("1.0", tk.END))
        
        app.destroy()
        subprocess.run([sys.executable, "-m", "modules.gui3"], check=True)

    app = tk.Tk()
    app.title("Leitor de QR Code - Produto e Lote (Caixa)")
    try:
        app.state('zoomed')
    except:
        app.attributes('-zoomed', True)
    app.configure(bg="#dcdad5")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TLabel", background="#dcdad5", font=("Arial", 14))
    style.configure("TButton", font=("Arial", 14))

    frame = ttk.Frame(app, padding=20)
    frame.pack(expand=True, fill="both")

    ttk.Label(frame, text="Escaneie os códigos (Produto + Lote):").pack(anchor="w")

    input_field = tk.Text(frame, height=8, font=("Arial", 14))
    input_field.insert(tk.END, carregar_escaneado())
    input_field.pack(pady=8, fill="x")

    ttk.Button(frame, text="Processar", command=process_qr).pack(pady=5)

    status_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"))
    status_label.pack(pady=5, anchor="w")

    ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)

    ttk.Label(frame, text="Resultado:").pack(anchor="w")
    result_box = tk.Text(frame, height=15, font=("Arial", 13), state="disabled", bg="#fff")
    result_box.pack(pady=10, fill="both", expand=True)

    ttk.Button(frame, text="Finalizar e Conferir", command=finalizar).pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    setup_gui2()
