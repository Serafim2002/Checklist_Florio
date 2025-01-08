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
    """Carrega o CSV com dados de produtos."""
    return pd.read_csv(path, sep=';', encoding='utf-8')

def get_order_num(txt):
    """Extrai o número do pedido do texto."""
    m = re.search(r'(\d+)\s*/1', txt)
    return m.group(1) if m else None

def get_products(txt, prod):
    """Verifica códigos do CSV no texto do PDF."""
    codes = prod['Codigo'].astype(str).tolist()
    lines = txt.splitlines()
    result = []

    for ln in lines:
        qty = re.match(r'^\d+', ln)
        if not qty:
            continue

        for code in codes:
            if code in ln:
                result.append(f"{qty.group()} {code}")
                break

    return result

def main():
    files = open_files()
    csv_path = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/data/Produto.csv"
    prod = load_csv(csv_path)

    for f in files:
        rdr = PdfReader(f)
        wtr = PdfWriter()
        temp_dir = os.path.dirname(f)

        for i, pg in enumerate(rdr.pages):
            txt = pg.extract_text()
            order_num = get_order_num(txt)
            prod_info = get_products(txt, prod)

            if order_num and prod_info:
                qr_data = f"{order_num}\n" + "\n".join(prod_info)
                qr_img = qrcode.make(qr_data)

                qr_path = os.path.join(temp_dir, f"qr_{i}.png")
                qr_img.save(qr_path)

                temp_pdf_path = os.path.join(temp_dir, f"temp_{i}.pdf")
                c = canvas.Canvas(temp_pdf_path, pagesize=letter)
                c.drawImage(qr_path, 450, 100, width=100, height=100)
                c.save()

                temp_pdf = PdfReader(temp_pdf_path)
                pg.merge_page(temp_pdf.pages[0])
                wtr.add_page(pg)

                os.remove(qr_path)
                os.remove(temp_pdf_path)

        out_file = f.replace(".pdf", "-mod.pdf")
        with open(out_file, 'wb') as out:
            wtr.write(out)

if __name__ == "__main__":
    main()
