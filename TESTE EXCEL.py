import pandas as pd
import re

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

# Função para buscar códigos no arquivo de texto
def buscar_codigos_no_txt(caminho_txt, codigos):
    try:
        with open(caminho_txt, 'r', encoding='utf-8') as arquivo:
            conteudo_txt = arquivo.read()

            # Procurar por cada código no arquivo .txt
            codigos_encontrados = {}
            for codigo in codigos:
                # Usar expressão regular para buscar o código no texto
                ocorrencias = re.findall(rf'\b{codigo}\b', conteudo_txt)
                if ocorrencias:
                    codigos_encontrados[codigo] = len(ocorrencias)
            
            if codigos_encontrados:
                return codigos_encontrados
            else:
                print("Nenhum código encontrado no arquivo de texto.")
                return None

    except FileNotFoundError:
        print(f"Erro: Arquivo de texto '{caminho_txt}' não encontrado.")
        return None

# Função principal
if __name__ == "__main__":
    # Caminho do arquivo Excel
    caminho_arquivo_excel = "C:/Users/Faturamento/Desktop/Projetos/Checklist/Excel/Produto.xls"

    # Caminho do arquivo de texto
    caminho_arquivo_txt = "C:/Users/Faturamento/Desktop/Projetos/Checklist/Texto/produtos.txt"

    # Carregar a planilha
    planilha_df = carregar_planilha(caminho_arquivo_excel)

    if planilha_df is not None:
        # Verificar se a coluna 'COD' existe
        if 'COD' in planilha_df.columns:
            # Extrair os códigos da coluna 'COD'
            codigos = planilha_df['COD'].astype(str).tolist()  # Convertendo para string para evitar problemas

            # Buscar os códigos no arquivo .txt
            codigos_encontrados = buscar_codigos_no_txt(caminho_arquivo_txt, codigos)

            # Exibir os resultados se houverem
            if codigos_encontrados:
                print("Códigos encontrados no arquivo de texto:")
                for codigo, quantidade in codigos_encontrados.items():
                    print(f"Código: {codigo} | Ocorrências: {quantidade}")
        else:
            print("Erro: A coluna 'COD' não existe na planilha.")
