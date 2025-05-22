import pandas as pd
from pandastable import Table
from collections import defaultdict
import codecs
import tkinter as tk
from tkinter import messagebox
import warnings
import os

warnings.filterwarnings("ignore", category=FutureWarning)

# Global variable definition
codigo_postal = ""

class PedidoJanela:
    def __init__(self, master):
        self.master = master
        master.title("Pedido do Cliente")

        self.label_pedido = tk.Label(master, text="Por favor escaneie o QRCODE:")
        self.label_pedido.config(font=("Arial", 15, "bold"))
        self.label_pedido.pack()

        self.texto_pedido = tk.Text(master, height=25, width=100)
        self.texto_pedido.pack()

        self.botao_salvar = tk.Button(master, text="Salvar Pedido", command=self.criar_pedido)
        self.botao_salvar.pack()

    def criar_pedido(self):
        pedido = self.texto_pedido.get("1.0", "end-1c").strip()
        if not pedido:
            messagebox.showwarning("Pedido vazio", "Você precisa escanear o QRCODE primeiro.")
            return
        with open("QRCODE.txt", "w") as arquivo:
            arquivo.write(pedido)
        messagebox.showinfo("Pedido Criado", "Pedido salvo com sucesso!")
        self.master.destroy()

root = tk.Tk()
PedidoJanela(root)
root.mainloop()

class QRCodeProcessor:
    def __init__(self, arquivo_entrada="QRCODE.txt", arquivo_saida="QRCODE.txt"):
        self.arquivo_entrada = arquivo_entrada
        self.arquivo_saida = arquivo_saida

    def processar_qrcode(self):
        with codecs.open(self.arquivo_entrada, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        global codigo_postal
        codigo_postal = linhas[0].strip()
        produtos_brutos = linhas[1].strip()

        # Converte string da lista para lista de strings
        try:
            produtos = eval(produtos_brutos)  # Cuidado com eval, só use se confiar na fonte
        except:
            messagebox.showerror("Erro", "Erro ao processar o conteúdo do QRCODE.")
            return

        produtos_processados = []
        for produto in produtos:
            partes = produto.strip().split(' ', 1)
            if len(partes) == 2:
                volume, descricao = partes
                produtos_processados.append([volume, descricao])

        with codecs.open(self.arquivo_entrada, "w", encoding="utf-8") as f:
            f.write(codigo_postal + "\n")
            for volume, descricao in produtos_processados:
                f.write(f"{volume}\t{descricao}\n")


qrcode_processor = QRCodeProcessor()
#qrcode_processor.processar_qrcode()

def Main_Janela():
    class LoteJanela:
        def __init__(self, master):
            self.master = master
            master.title("Lote do Pedido")

            self.label_pedido = tk.Label(master, text="Por favor escaneie os Lotes:")
            self.label_pedido.config(font=("Arial", 15, "bold"))
            self.label_pedido.grid(row=0, column=0, columnspan=2)

            self.texto_pedido = tk.Text(master, height=25, width=100)
            self.texto_pedido.grid(row=1, column=0, columnspan=2)

            self.botao_alterar = tk.Button(master, text="Voltar no último arquivo salvo", command=self.alterar)
            self.botao_alterar.grid(row=2, column=0)

            self.botao_salvar = tk.Button(master, text="Salvar Lote", command=self.salvar)
            self.botao_salvar.grid(row=2, column=1)

        def alterar(self):
            try:
                with open("LOTE1.txt", "r") as arquivo:
                    conteudo = arquivo.read()
                    self.texto_pedido.delete("1.0", tk.END)
                    self.texto_pedido.insert(tk.END, conteudo)
            except FileNotFoundError:
                messagebox.showwarning("Arquivo não encontrado", "O arquivo não existe.")

        def salvar(self):
            pedido = self.texto_pedido.get("1.0", tk.END)
            try:
                with open("LOTE1.txt", "w") as arquivo:
                    arquivo.write(pedido)
                messagebox.showinfo("Lote foi salvo", "Lote do pedido salvo com sucesso!")
                self.master.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao salvar", f"Erro: {e}")

    janela_pedido = tk.Tk()
    LoteJanela(janela_pedido)
    janela_pedido.mainloop()

    class LoteProcessor:
        def __init__(self, arquivo_entrada="LOTE1.txt", arquivo_saida="LOTE.txt"):
            self.arquivo_entrada = arquivo_entrada
            self.arquivo_saida = arquivo_saida

        def processar_lote(self):
            with open(self.arquivo_entrada, "r") as arquivo:
                linhas = arquivo.readlines()

            contagem_itens = {}
            for linha in linhas:
                item = linha.strip()
                if item != "":
                    contagem_itens[item] = contagem_itens.get(item, 0) + 1

            with open(self.arquivo_saida, "w") as resultado_arquivo:
                linha_formatada = f"{codigo_postal}\n"
                resultado_arquivo.write(linha_formatada)
                itens_ordenados = sorted(contagem_itens.keys())
                for item in itens_ordenados:
                    contagem = contagem_itens[item]
                    linha_formatada = f"{contagem}\t{item}\n"
                    resultado_arquivo.write(linha_formatada)

    lote_processor = LoteProcessor()
    lote_processor.processar_lote()

    class Comparacao_Janela:
        def __init__(self, master):
            self.master = master

            self.arquivo_pedidos = 'QRCODE.txt'
            self.df_pedidos = self.Conversor_Planilha(self.arquivo_pedidos)

            self.arquivo_lote = 'LOTE.txt'
            self.df_lote = self.Conversor_Planilha(self.arquivo_lote)

            master.title("Pedido do Cliente")

            botao_Voltar = tk.Button(master, text="Voltar", command=self.botao_voltar)
            botao_Voltar.grid(row=0, column=1, sticky=tk.N)

            botao_salvar = tk.Button(master, text="Salvar Edições", command=self.salvar_edicoes)
            botao_salvar.grid(row=0, column=2, sticky=tk.N)

            comparar_botao = tk.Button(master, text="Comparar", command=self.comparar_botao)
            comparar_botao.grid(row=0, column=2, sticky=tk.NW)

            finalizar_botao = tk.Button(master, text="Fecha", command=self.finalizar_botao)
            finalizar_botao.grid(row=0, column=2, sticky=tk.NE)

            frame_pedido = tk.Frame(master)
            frame_pedido.grid(row=1, column=1)

            frame_lote = tk.Frame(master)
            frame_lote.grid(row=1, column=2)

            self.table_pedido = Table(frame_pedido, dataframe=self.df_pedidos, width=600, height=400,
                                      showtoolbar=False, showstatusbar=False,
                                      editable=False, enable_menus=False)
            self.table_pedido.show()

            self.table_lote = Table(frame_lote, dataframe=self.df_lote, width=600, height=400,
                                    showtoolbar=False, showstatusbar=False,
                                    editable=True, enable_menus=False)
            self.table_lote.show()

        def comparar(self):
            class LoteProcessor:
                def __init__(self, input_file, output_file):
                    self.input_file = input_file
                    self.output_file = output_file

                def processa_arquivo(self):
                    produtos = defaultdict(int)

                    with open(self.input_file, 'r') as file:
                        for line in file:
                            line = line[:-8].strip()
                            campos = line.split('\t')

                            if len(campos) >= 2:
                                volume = int(campos[0])
                                produto = campos[1]

                                produtos[produto] += volume
                            else:
                                pass

                    with open(self.output_file, 'w') as file:
                        linha_formatada = f"{codigo_postal}\n"
                        file.write(linha_formatada)
                        for produto, volume in produtos.items():
                            file.write(f"{volume}\t{produto} CX\n")

            lote_processor = LoteProcessor('LOTE.txt', 'LOTE_.txt')
            lote_processor.processa_arquivo()

            class ComparadorDeArquivos:
                def __init__(self, arquivo1, arquivo2):
                    self.arquivo1 = arquivo1
                    self.arquivo2 = arquivo2

                def extrair_produtos_e_volumes(self, arquivo):
                    with open(arquivo, 'r') as file:
                        linhas = file.readlines()
                        produtos_e_volumes = {}

                        for linha in linhas:
                            partes = linha.split("\t")
                            if len(partes) == 2:
                                volume, produto_descricao = partes
                                volume = self.formatar_volume(volume)
                                produtos_e_volumes[produto_descricao] = volume

                        return produtos_e_volumes

                def formatar_volume(self, volume):
                    partes = volume.split()
                    if len(partes) == 2:
                        quantidade, unidade = partes
                        return f"{quantidade} {unidade}"
                    else:
                        return volume

                def verificar_presenca(self, produtos_volumes_arquivo1, produtos_volumes_arquivo2):
                    todos_corretos = True  # Inicialmente assume que todos estão corretos

                    for produto_descricao, volume in produtos_volumes_arquivo1.items():
                        if produto_descricao in produtos_volumes_arquivo2:
                            volume_arquivo2 = produtos_volumes_arquivo2[produto_descricao]
                            if volume_arquivo2 != volume:
                                print(f"Produto '{produto_descricao}' encontrado, mas volume diferente.")
                                todos_corretos = False  # Marca como incorreto se encontrar algum volume diferente
                        else:
                            print(f"Produto '{produto_descricao}' não encontrado no arquivo 2.")
                            todos_corretos = False  # Marca como incorreto se algum produto não for encontrado

                    return todos_corretos

                def comparar_e_mostrar_resultado(self):
                    produtos_volumes_arquivo1 = self.extrair_produtos_e_volumes(self.arquivo1)
                    produtos_volumes_arquivo2 = self.extrair_produtos_e_volumes(self.arquivo2)

                    presenca_arquivo1_em_arquivo2 = self.verificar_presenca(produtos_volumes_arquivo1, produtos_volumes_arquivo2)
                    presenca_arquivo2_em_arquivo1 = self.verificar_presenca(produtos_volumes_arquivo2, produtos_volumes_arquivo1)

                    presenca = presenca_arquivo1_em_arquivo2 and presenca_arquivo2_em_arquivo1

                    root = tk.Tk()
                    root.withdraw()

                    if presenca:
                        messagebox.showinfo("CHECKLIST", "ESTÁ TUDO CERTO")
                    else:
                        messagebox.showinfo("CHECKLIST", "TEM ALGO ERRADO")

                    root.destroy()

            comparador = ComparadorDeArquivos('QRCODE.txt', 'LOTE_.txt')
            comparador.comparar_e_mostrar_resultado()

            class End:
                def __init__(self, input_file, output_file):
                    self.input_file = input_file
                    self.output_file = output_file

                def processa_arquivo(self):
                    with open(self.input_file, 'r') as file:
                        lines = file.readlines()
                        if lines:
                            lines.pop(0)

                        new_lines = []

                        for line in lines:
                            campos = line.split('\t')
                            if len(campos) >= 2:
                                volume = int(campos[0])
                                produto = campos[1].strip()
                                new_line = f"{produto}\t\t{codigo_postal}\t{volume}\n"
                                new_lines.append(new_line)

                    with open(self.output_file, 'w') as file:
                        file.writelines(new_lines)

            Process = End('LOTE.txt', f"{codigo_postal}.txt")
            Process.processa_arquivo()

        def Conversor_Planilha(self, nome_arquivo):
            with open(nome_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()
                dados = [linha.strip().split('\t') for linha in linhas]
                df = pd.DataFrame(dados, columns=['Volume', 'Produto'])
            return df

        def salvar_arquivo_texto(self, nome_arquivo, dados):
            with open(nome_arquivo, 'w') as arquivo:
                for indice, linha in dados.iterrows():
                    linha_str = '\t'.join(map(lambda x: str(x) if pd.notnull(x) else '', linha))
                    arquivo.write(f"{linha_str}\n")

        def salvar_edicoes(self):
            messagebox.showinfo("CHECKLIST", "Edições salvas com sucesso!")
            dados_editados = self.table_lote.model.df
            self.salvar_arquivo_texto('LOTE.txt', dados_editados)

        def botao_voltar(self):
            self.master.destroy()
            Main_Janela()

        def comparar_botao(self):
            self.comparar()

        def finalizar_botao(self):
            os.remove('LOTE_.txt')
            os.remove('QRCODE.txt')
            os.remove('LOTE.txt')
            os.remove('LOTE1.txt')
            self.master.destroy()

    root = tk.Tk()
    Comparacao_Janela(root)
    root.mainloop()

Main_Janela()
