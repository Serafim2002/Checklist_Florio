import subprocess
import sys
import os
import re
from tkinter import Tk, filedialog

def activate_venv_and_run():
    venv_path = r'C:\Users\Faturamento\Desktop\Projetos\All_Editor\.venv\Scripts\activate'
    script_path = sys.argv[0]  # Pega o caminho do script atual

    # Usar 'call' para ativar o ambiente virtual e executar o script no mesmo comando
    subprocess.call(f'{venv_path} & python {script_path}', shell=True)

if 'venv' not in sys.executable:
    activate_venv_and_run()
else:
    from PyPDF2 import PdfReader, PdfWriter
    import qrcode
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas

    def open_file_dialog():
        Janela = Tk()
        Janela.withdraw()
        file_dir = filedialog.askopenfilenames()
        return file_dir

    def extract_number(text):
        # Procurar por números de 5 dígitos seguidos por /1 em qualquer parte do texto
        match = re.search(r'(\d+)\s*/1', text)
        if match:
            return match.group(1)
        return None

    def extract_volume_and_product(text):
        # Procurar por padrões de volume (número + espaço + texto) no texto
        matches = re.findall(r'\d+\s+(.+?\s*)C/', text)
        return matches

    def main():
        file_dir = open_file_dialog()

        for arquivo in file_dir:
            # Abrir o arquivo PDF
            with open(arquivo, 'rb') as pdf_file:
                pdf_reader = PdfReader(pdf_file)
                pdf_writer = PdfWriter()

                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    '''print(f"{page_text}")'''

                    # Chamar a função extract_number para localizar o número do pedido
                    pedido_numero = extract_number(page_text)

                    # Chamar a função extract_volume_and_product para localizar o volume e o produto
                    product = extract_volume_and_product(page_text)
                    print (f"{product}")



                    # Gerar o QR code
                    conteudo_qr_code = f"{pedido_numero}\n{product}"
                    '''print(f"{conteudo_qr_code}")'''
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
                    with open(arquivo, 'rb') as arquivo_pdf:
                        pdf_reader_original = PdfReader(arquivo_pdf)
                        with open(caminho_pdf_temporario, 'rb') as arquivo_pdf_temporario:
                            pdf_temporario_reader = PdfReader(arquivo_pdf_temporario)
                            pagina_qr_code = pdf_temporario_reader.pages[0]

                            pagina_atual = pdf_reader_original.pages[page_num]
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
