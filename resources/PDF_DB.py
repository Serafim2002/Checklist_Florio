import os
import re
from tkinter import Tk, filedialog
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def open_files():
    """Abre um diálogo para selecionar arquivos PDF."""
    Tk().withdraw()
    return filedialog.askopenfilenames()

def load_csv(path):
    """Carrega o CSV com dados de produtos e converte os códigos para strings."""
    df = pd.read_csv(path, sep=';', encoding='utf-8')
    df['D04_cod'] = df['D04_cod'].astype(str)  # Converte a coluna 'D04_cod' para string
    return df

def get_order(txt):
    """Extrai o número do pedido do texto."""
    match = re.search(r'(\d+)\s*/1', txt)
    return match.group(1) if match else None

def get_type(code):
    """Retorna 'UNIDADE' ou 'CAIXA' com base nos dois últimos dígitos."""
    code = str(code)  # Converte para string
    if code[-2:] == "01":
        return "UNIDADE"
    else:
        return "CAIXA"


def get_products(txt, prod):
    """Extrai produtos do texto do PDF."""
    codes = prod['D04_cod'].astype(str).tolist()
    lines = txt.splitlines()
    res = []

    for ln in lines:
        qty = re.match(r'^\d+', ln)
        if not qty:
            continue

        for code in codes:
            if code in ln:
                type = get_type(code)
                res.append(f" {qty.group()} {code[:-2]}")
                break


    return res

def create_qr(data, path):
    """Gera e salva um QR Code com os dados fornecidos."""
    qr = qrcode.make(data)
    qr.save(path)

def merge_pdf(qr_path, temp_path, pg):
    """Insere o QR Code em um PDF temporário e o mescla na página."""
    c = canvas.Canvas(temp_path, pagesize=letter)
    c.drawImage(qr_path, 450, 100, width=100, height=100)
    c.save()

    temp_pdf = PdfReader(temp_path)
    pg.merge_page(temp_pdf.pages[0])

    os.remove(qr_path)
    os.remove(temp_path)

def main():
    files = open_files()
    csv_path = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/data/D04_Produto_Con.csv"
    prod = load_csv(csv_path)

    for f in files:
        rdr = PdfReader(f)
        wtr = PdfWriter()
        temp_dir = os.path.dirname(f)

        for i, pg in enumerate(rdr.pages):
            txt = pg.extract_text()
            order = get_order(txt)
            prod_info = get_products(txt, prod)

            if order and prod_info:
                qr_data = f"{order}\n"+ "\n".join(prod_info)

                qr_path = os.path.join(temp_dir, f"qr_{i}.png")
                temp_pdf_path = os.path.join(temp_dir, f"temp_{i}.pdf")

                create_qr(qr_data, qr_path)
                merge_pdf(qr_path, temp_pdf_path, pg)

                wtr.add_page(pg)

        out_file = f.replace(".pdf", "-mod.pdf")
        with open(out_file, 'wb') as out:
            wtr.write(out)

if __name__ == "__main__":
    main()
