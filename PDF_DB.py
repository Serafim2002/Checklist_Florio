import os
import re
from tkinter import Tk, filedialog
import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def open_file_dialog():
    """Abre um diálogo para o usuário selecionar arquivos PDF."""
    janela = Tk()
    janela.withdraw()
    return filedialog.askopenfilenames()

def carregar_csv(caminho_csv):
    """Carrega o CSV com dados de produtos usando pandas."""
    return pd.read_csv(caminho_csv)

def verificar_produto(codigo, dados_produtos):
    """Verifica se o código de produto está no CSV e retorna o mesmo código se encontrado."""
    produto_encontrado = dados_produtos[dados_produtos['Codigo'] == int(codigo)]
    return int(codigo) if not produto_encontrado.empty else "Código não encontrado"

def extract_number(text):
    """Extrai o número do pedido do texto usando regex."""
    match = re.search(r'(\d+)\s*/1', text)
    return match.group(1) if match else None

def extract_volume_and_product(text, dados_produtos):
    """Extrai códigos de 6 dígitos do texto e verifica se existem no CSV."""
    codigos = re.findall(r'\b(\d{6,10})\b', text)  # Extrai números de 6 dígitos
    produtos_verificados = [verificar_produto(codigo, dados_produtos) for codigo in codigos]
    return [str(p) for p in produtos_verificados if p != "Código não encontrado"]

def main():
    file_dir = open_file_dialog()
    caminho_csv = "C:/Users/Faturamento/Desktop/Projetos/Checklist_Florio/Excel/Produto.csv"
    dados_produtos = pd.read_csv(caminho_csv, sep=';')

    for arquivo in file_dir:
        pdf_reader = PdfReader(arquivo)
        pdf_writer = PdfWriter()

        for page_num, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()
            pedido_numero = extract_number(page_text)
            code = extract_volume_and_product(page_text, dados_produtos)

            if pedido_numero and code:
                # Gerar QR Code com informações do pedido e produto
                qr_conteudo = f"{pedido_numero}\n" + "\n".join(code)  # Certifique-se de que cada código é uma string simples
                print (f"{qr_conteudo}")
                qrcode_img = qrcode.make(qr_conteudo)

                # Salvar o QR code temporariamente
                pasta_origem = os.path.dirname(arquivo)
                qr_path = os.path.join(pasta_origem, f"qr_code_{page_num}.png")
                qrcode_img.save(qr_path)

                # Criar um PDF temporário com o QR Code
                temp_pdf_path = os.path.join(pasta_origem, f"temp_pdf_{page_num}.pdf")
                c = canvas.Canvas(temp_pdf_path, pagesize=letter)
                c.drawImage(qr_path, 450, 100, width=100, height=100)
                c.save()

                # Adicionar o QR Code no PDF original
                with open(arquivo, 'rb') as original_pdf, open(temp_pdf_path, 'rb') as temp_pdf:
                    reader_original = PdfReader(original_pdf)
                    reader_temp = PdfReader(temp_pdf)
                    page_qr = reader_temp.pages[0]
                    page_atual = reader_original.pages[page_num]
                    page_atual.merge_page(page_qr)
                    pdf_writer.add_page(page_atual)

                # Remover arquivos temporários
                os.remove(qr_path)
                os.remove(temp_pdf_path)

        # Salvar o PDF final
        output_pdf = arquivo.replace(".pdf", "-modificado.pdf")
        with open(output_pdf, 'wb') as output:
            pdf_writer.write(output)

if __name__ == "__main__":
    main()
