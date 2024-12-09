import subprocess
import sys
import os
import re
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader, PdfWriter
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd

# Função para carregar a planilha Excel
def carregar_planilha(caminho_arquivo):
    try:
        # Ler o arquivo Excel
        dados = pd.read_excel(caminho_arquivo)
        print("Planilha carregada com sucesso.")
        print("Colunas disponíveis:", dados.columns)  # Exibe as colunas para conferir o nome
        return dados
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado no caminho '{caminho_arquivo}'.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None

# Função para abrir o diálogo de seleção de arquivos
def open_file_dialog():
    Janela = Tk()
    Janela.withdraw()
    file_dir = filedialog.askopenfilenames()
    return file_dir

# Função para extrair números do texto do PDF
def ext_num(text):
    # Procurar por números de 5 dígitos seguidos por /1 no texto
    match = re.search(r'(\d+)\s*/1', text)
    if match:
        return match.group(1)
    return None

# Função para buscar códigos do Excel dentro do texto do PDF
def bus_pdf(text, dataframe, coluna_codigo):
    # Para cada código na coluna do Excel, verificar se aparece no texto extraído do PDF
    cod_encon = []
    for codigo in dataframe[coluna_codigo]:
        # Verificar se o código está no texto da página
        if str(codigo) in text:
            cod_encon.append(codigo)
    return cod_encon

def extract_volume_and_product(text):
    # Procurar por padrões de volume (número + espaço + texto) no texto
    matches = re.findall(r'\d+\s+(.+?\s*)C/', text)
    return matches

def main():
    # Carregar o Excel
    excel = "C:/Users/Faturamento/Desktop/Projetos/Checklist/Excel/Produto.xls"
    planilha_df = carregar_planilha(excel)

    # Garantir que o DataFrame foi carregado corretamente
    if planilha_df is None:
        print("Erro ao carregar a planilha.")
        return
    
    # Nome da coluna do Excel que contém os códigos
    col = "COD"

    file_dir = open_file_dialog()

    for arquivo in file_dir:
        # Abrir o arquivo PDF
        with open(arquivo, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            pdf_writer = PdfWriter()

            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                print(f"{page_text}")
                
                # Chamar a função extract_number para localizar o número do pedido
                pedido_numero = ext_num(page_text)
                # Chamar a função extract_volume_and_product para localizar o volume e o produto
                product = extract_volume_and_product(page_text)
                

                # Procurar códigos do Excel no texto do PDF
                cod_encon = bus_pdf(page_text, planilha_df, col)
                # Gerar o QR code com as informações encontradas
                conteudo_qr_code = f"{pedido_numero}\n{product,cod_encon}"
                qr_code_img = qrcode.make(conteudo_qr_code)

                # Salvar o QR code temporariamente como uma imagem PNG
                pasta_origem = os.path.dirname(arquivo)
                caminho_qr_code_temporario = os.path.join(pasta_origem, f"qr_code_temporario_{page_num}.png")
                qr_code_img.save(caminho_qr_code_temporario)

                # Criar um novo PDF contendo o QR code como imagem
                caminho_pdf_temporario = os.path.join(pasta_origem, f"pdf_temporario_{page_num}.pdf")
                pdf_canvas = canvas.Canvas(caminho_pdf_temporario, pagesize=letter)
                pdf_canvas.drawImage(caminho_qr_code_temporario, 450, 100, width=100, height=100)
                pdf_canvas.save()

                # Adicionar o QR code na página atual do PDF original
                with open(caminho_pdf_temporario, 'rb') as arquivo_pdf_temporario:
                    pdf_temporario_reader = PdfReader(arquivo_pdf_temporario)
                    pagina_qr_code = pdf_temporario_reader.pages[0]

                    pagina_atual = page
                    pagina_atual.merge_page(pagina_qr_code)

                    # Adicionar página modificada ao PDF final
                    pdf_writer.add_page(pagina_atual)

            # Salvar o PDF modificado com os QR codes individuais
            caminho_pdf_modificado = arquivo.replace(".pdf", "-modificado.pdf")
            with open(caminho_pdf_modificado, 'wb') as arquivo_pdf_modificado:
                pdf_writer.write(arquivo_pdf_modificado)

            # Remover os arquivos temporários
            for page_num in range(len(pdf_reader.pages)):
                os.remove(os.path.join(pasta_origem, f"qr_code_temporario_{page_num}.png"))
                os.remove(os.path.join(pasta_origem, f"pdf_temporario_{page_num}.pdf"))

if __name__ == "__main__":
    main()
