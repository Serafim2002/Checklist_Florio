import pandas as pd
from pandastable import Table
from collections import defaultdict
import codecs
import tkinter as tk
from tkinter import messagebox
import warnings
import os

warnings.filterwarnings("ignore",category=FutureWarning)


def janela_pedido():
    def criar_pedido():
        pedido = texto_pedido.get("1.0","end-1c")
        with open("QRCODE.txt","w") as arquivo:
            arquivo.write(pedido)
        messagebox.showinfo("Pedido Criado","Pedido salvo com sucesso!")
        janela_pedido.destroy()

    janela_pedido = tk.Tk()
    janela_pedido.title("Pedido do Cliente")

    label_pedido = tk.Label(janela_pedido,text="Por favor escaneie o QRCODE:")
    label_pedido.config(font=("Arial",15,"bold"))
    label_pedido.pack()

    texto_pedido = tk.Text(janela_pedido,height=25,width=100)
    texto_pedido.pack()

    botao_salvar = tk.Button(janela_pedido,text="Salvar Pedido",command=criar_pedido)
    botao_salvar.pack()

    janela_pedido.mainloop()

    def QRCODE():
        def processar_arquivo_entrada(nome_arquivo_entrada):
            with codecs.open(nome_arquivo_entrada,"r",encoding='utf-8') as f:
                linhas = f.readlines()

            global codigo_postal
            codigo_postal = linhas[0].strip()
            codigo_postal = str(codigo_postal)

            produtos = []
            for linha in linhas[1:]:
                produtos.extend(linha.strip().strip('[]').replace("'","").split(', '))

            with codecs.open("QRCODE.txt","w",encoding='utf-8') as f:
                f.write(codigo_postal + "\n")
                for produto in produtos:
                    f.write(produto + "\n")

            with open('QRCODE.txt','r') as arquivo_entrada:
                linhas = arquivo_entrada.readlines()

            linhas_processadas = [processar_linha(linha) for linha in linhas]

            with open('QRCODE.txt','w') as arquivo_saida:
                arquivo_saida.writelines(linhas_processadas)

        def processar_linha(linha):
            partes = linha.split(' ',2)
            if len(partes) == 3:
                Volume = partes[1]
                descricao_produto = partes[2].strip()
                return f"{Volume}\t{descricao_produto}\n"
            else:
                return linha

        processar_arquivo_entrada("QRCODE.txt")

    QRCODE()


janela_pedido()


def janela_lote():
    class PedidoApp:
        def __init__(self,master):
            self.master = master
            master.title("Lote do Pedido")

            self.label_pedido = tk.Label(master,text="Por favor escaneie os Lotes:")
            self.label_pedido.config(font=("Arial",15,"bold"))
            self.label_pedido.grid(row=0,column=0,columnspan=2)

            self.texto_pedido = tk.Text(master,height=25,width=100)
            self.texto_pedido.grid(row=1,column=0,columnspan=2)

            self.botao_alterar = tk.Button(master,text="Voltar no último arquivo salvo",command=self.alterar)
            self.botao_alterar.grid(row=2,column=0)

            self.botao_salvar = tk.Button(master,text="Salvar Lote",command=self.salvar)
            self.botao_salvar.grid(row=2,column=1)

        def alterar(self):
            try:
                with open("LOTE1.txt","r") as arquivo:
                    conteudo = arquivo.read()
                    self.texto_pedido.delete("1.0",tk.END)
                    self.texto_pedido.insert(tk.END,conteudo)
            except FileNotFoundError:
                messagebox.showwarning("Arquivo não encontrado","O arquivo não existe.")

        def salvar(self):
            pedido = self.texto_pedido.get("1.0",tk.END)
            try:
                with open("LOTE1.txt","w") as arquivo:
                    arquivo.write(pedido)
                messagebox.showinfo("Lote foi salvo","Lote do pedido salvo com sucesso!")
                self.master.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao salvar",f"Erro: {e}")

    if __name__ == "__main__":
        janela_pedido = tk.Tk()
        PedidoApp(janela_pedido)
        janela_pedido.mainloop()

    def LOTE():
        def contar_itens(nome_arquivo_entrada,nome_arquivo_saida):
            with open(nome_arquivo_entrada,'r') as arquivo:
                linhas = arquivo.readlines()

            contagem_itens = {}
            for linha in linhas:
                item = linha.strip()
                if item != '':
                    contagem_itens[item] = contagem_itens.get(item,0) + 1

            with open(nome_arquivo_saida,'w') as resultado_arquivo:
                linha_formatada = f"{codigo_postal}\n"
                resultado_arquivo.write(linha_formatada)
                itens_ordenados = sorted(contagem_itens.keys())
                for item in itens_ordenados:
                    contagem = contagem_itens[item]
                    linha_formatada = f"{contagem}\t{item}\n"
                    resultado_arquivo.write(linha_formatada)

        contar_itens('LOTE1.txt','LOTE.txt')

    LOTE()

    def janela_comp():
        def comparar():
            def LOTE_():
                def processa_arquivo(input_file,output_file):
                    produtos = defaultdict(int)

                    with open(input_file,'r') as file:
                        for line in file:
                            line = line[:-8].strip()
                            campos = line.split('\t')

                            if len(campos) >= 2:
                                volume = int(campos[0])
                                produto = campos[1]

                                produtos[produto] += volume
                            else:
                                pass

                    with open(output_file,'w') as file:
                        linha_formatada = f"{codigo_postal}\n"
                        file.write(linha_formatada)
                        for produto,volume in produtos.items():
                            file.write(f"{volume}\t{produto} CX\n")

                processa_arquivo('LOTE.txt','LOTE_.txt')

            LOTE_()

            def comparar_arquivos(arquivo1,arquivo2):
                def extrair_produtos_e_volumes(arquivo):
                    with open(arquivo,'r') as file:
                        linhas = file.readlines()
                        produtos_e_volumes = {}

                        for linha in linhas:
                            partes = linha.split()
                            if len(partes) > 2:
                                volume = partes[0]
                                produto = ' '.join(partes[1:-2])
                                produtos_e_volumes[produto] = volume

                        return produtos_e_volumes

                def verificar_presenca(produtos_volumes_arquivo1,arquivo2):
                    produtos_e_volumes_arquivo2 = extrair_produtos_e_volumes(arquivo2)

                    for produto,volume in produtos_volumes_arquivo1.items():
                        if produto in produtos_e_volumes_arquivo2 and produtos_e_volumes_arquivo2[produto] == volume:
                            continue
                        else:
                            return False

                    return True

                produtos_volumes_arquivo1 = extrair_produtos_e_volumes(arquivo1)
                presenca = verificar_presenca(produtos_volumes_arquivo1,arquivo2)

                root = tk.Tk()
                root.withdraw()

                if presenca:
                    messagebox.showinfo("CHECKLIST","ESTÁ TUDO CERTO")
                else:
                    messagebox.showinfo("CHECKLIST","TEM ALGO ERRADO")

                root.destroy()

            comparar_arquivos('QRCODE.txt','LOTE_.txt')

            def End():
                def processa_arquivo(input_file,output_file):
                    with open(input_file,'r') as file:
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

                    with open(output_file,'w') as file:
                        file.writelines(new_lines)

                nome = f"{codigo_postal}.txt"
                processa_arquivo('LOTE.txt',nome)

            End()

        def ler_arquivo_texto(nome_arquivo):
            with open(nome_arquivo,'r') as arquivo:
                linhas = arquivo.readlines()
                dados = [linha.strip().split('\t') for linha in linhas]
                df = pd.DataFrame(dados,columns=['Volume','Produto'])
            return df

        def salvar_arquivo_texto(nome_arquivo,dados):
            with open(nome_arquivo,'w') as arquivo:
                for indice,linha in dados.iterrows():
                    linha_str = '\t'.join(map(lambda x: str(x) if pd.notnull(x) else '',linha))
                    arquivo.write(f"{linha_str}\n")

        def salvar_edicoes():
            messagebox.showinfo("CHECKLIST","Edições salvo com sucesso!")
            dados_editados = table_lote.model.df
            salvar_arquivo_texto('LOTE.txt',dados_editados)

        def botao_voltar():
            root.destroy()
            janela_lote()

        def comparar_botao():
            comparar()

        def finalizar_botao():
            os.remove('LOTE_.txt')
            os.remove('QRCODE.txt')
            os.remove('LOTE.txt')
            os.remove('LOTE1.txt')
            root.destroy()

        arquivo_pedidos = 'QRCODE.txt'
        df_pedidos = ler_arquivo_texto(arquivo_pedidos)

        arquivo_lote = 'LOTE.txt'
        df_lote = ler_arquivo_texto(arquivo_lote)

        root = tk.Tk()
        root.title("Pedido do Cliente")
        botao_Voltar = tk.Button(root,text="Voltar",command=botao_voltar)
        botao_Voltar.grid(row=0,column=1,sticky=tk.N)
        botao_salvar = tk.Button(root,text="Salvar Edições",command=salvar_edicoes)
        botao_salvar.grid(row=0,column=2,sticky=tk.N)
        comparar_botao = tk.Button(root,text="Comparar",command=comparar_botao)
        comparar_botao.grid(row=0,column=2,sticky=tk.NW)
        finalizar_botao = tk.Button(root,text="Fecha",command=finalizar_botao)
        finalizar_botao.grid(row=0,column=2,sticky=tk.NE)

        frame_pedido = tk.Frame(root)
        frame_pedido.grid(row=1,column=1)

        frame_lote = tk.Frame(root)
        frame_lote.grid(row=1,column=2)

        table_pedido = Table(frame_pedido,dataframe=df_pedidos,width=600,height=400,
                             showtoolbar=False,showstatusbar=False,
                             editable=False,enable_menus=False)
        table_pedido.show()

        table_lote = Table(frame_lote,dataframe=df_lote,width=600,height=400,
                           showtoolbar=False,showstatusbar=False,
                           editable=True,enable_menus=False)
        table_lote.show()

        root.mainloop()

    janela_comp()


janela_lote()
