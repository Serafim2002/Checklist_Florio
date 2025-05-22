import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys
from collections import defaultdict

def setup_gui3():
    def parse_viewer(path):
        with open(path, encoding="utf-8") as f:
            return [(line.strip().split("x", 1)[1].strip(), int(line.strip().split("x", 1)[0].strip()))
                    for line in f if "x" in line]

    def parse_lote_viewer(path):
        with open(path, encoding="utf-8") as f:
            contagem = {}
            for line in f:
                if "x" in line and not line.startswith("Qty"):
                    try:
                        parte1, lote = line.strip().rsplit(" ", 1)
                        qtd, desc = parte1.strip().split("x", 1)
                        desc = desc.strip()
                        qtd = int(qtd.strip())
                        contagem[desc] = contagem.get(desc, 0) + qtd
                    except:
                        continue
        return contagem

    def conferir():
        tree.delete(*tree.get_children())

        pedido = parse_viewer("D:/Projetos/Checklist_Florio/Result/Pedido(viewer).txt")
        escaneado = parse_lote_viewer("D:/Projetos/Checklist_Florio/Result/QrLote(viewer).txt")

        descs_pedido = {desc for desc, _ in pedido}

        for desc, qtd_esp in pedido:
            qtd_real = escaneado.get(desc, 0)
            diff = qtd_real - qtd_esp

            if desc not in escaneado:
                status, color = "⚠ Não encontrado", "red"
            elif diff == 0:
                status, color = "✔ OK", "green"
            elif diff < 0:
                status, color = f"⚠ Faltam {abs(diff)}", "orange"
            else:
                status, color = f"❌ {diff} a mais", "red"

            tree.insert("", "end", values=(desc, qtd_esp, qtd_real, status), tags=(color,))

        for desc, qtd in escaneado.items():
            if desc not in descs_pedido:
                tree.insert("", "end", values=(desc, "N/A", qtd, "❌ Mercadoria errada"), tags=("red",))

    def voltar():
        root.destroy()
        subprocess.run([sys.executable, "-m", "modules.gui2"], check=True)

    def finalizar():
        try:
            base_path = "D:/Projetos/Checklist_Florio/Result"
            arq_pedido_viewer = f"{base_path}/Pedido(viewer).txt"

            with open(arq_pedido_viewer, "r", encoding="utf-8") as f:
                linha = f.readline().strip()
                order_id = linha.split(":")[1].strip() 

            arq_qr = f"{base_path}/{order_id}QR.txt"
            arq_lote = f"{base_path}/QrLote.txt"
            arq_saida = f"D:/Projetos/Checklist_Florio/{order_id}.txt"

            with open(arq_lote, "r", encoding="utf-8") as f:
                linhas = [l.strip().split() for l in f if l.strip()]
            contagem = defaultdict(int)
            for cod, lote in linhas:
                contagem[(cod, lote)] += 1

            with open(arq_qr, "r", encoding="utf-8") as f:
                codigos_validos = {l.split()[1] for l in f.readlines()[1:] if l.strip()}

            with open(arq_saida, "w", encoding="utf-8") as f:
                f.write(f"{order_id}\n")
                for (cod, lote), qtd in sorted(contagem.items()):
                    if cod in codigos_validos:
                        f.write(f"{qtd} {cod}   {lote}\n")

            root.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao finalizar: {e}")

    root = tk.Tk()
    root.title("GUI3 - Conferência Final de Pedido")
    try:
        root.state('zoomed')
    except:
        root.attributes('-zoomed', True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", rowheight=35, font=("Arial", 16))  # Aumenta fonte da tabela
    style.configure("Treeview.Heading", font=("Arial", 18, "bold"))  # Aumenta fonte dos títulos
    style.map("Treeview", background=[("selected", "#ececec")])

    tree = ttk.Treeview(root, columns=("desc", "esperada", "real", "status"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col.capitalize())
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    tree.tag_configure("green", background="#d0f0c0")
    tree.tag_configure("orange", background="#fff3b0")
    tree.tag_configure("red", background="#f7b6b6")

    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)

    button_font = ("Arial", 16, "bold")

    tk.Button(btn_frame, text="Conferir", command=conferir, bg="#4CAF50", fg="white", height=2, font=button_font).pack(side="left", expand=True, fill="x", padx=5)
    tk.Button(btn_frame, text="Voltar", command=voltar, bg="#f44336", fg="white", height=2, font=button_font).pack(side="left", expand=True, fill="x", padx=5)
    tk.Button(btn_frame, text="Finalizar", command=finalizar, bg="#1e88e5", fg="white", height=2, font=button_font).pack(side="left", expand=True, fill="x", padx=5)

    root.mainloop()

if __name__ == "__main__":
    setup_gui3()
