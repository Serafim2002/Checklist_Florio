from collections import defaultdict
from modules.saveLote import save_resultL

def qr_lote(qr_data, prod_dict):
    try:
        lines = qr_data.splitlines()
        if not lines:
            return {"error": True, "message": "Nenhum dado fornecido!", "output": ""}

        contagem = defaultdict(int)
        for line in lines:
            try:
                code, lote = line.strip().split()
                contagem[(code, lote)] += 1
            except ValueError:
                contagem[(line.strip(), "Formato inválido")] += 1

        items = []
        for (code, lote), qtd in sorted(contagem.items()):
            if lote == "Formato inválido":
                items.append(f"{code} - Formato inválido")
            else:
                nome_produto = prod_dict.get(code.strip(), "Produto não encontrado")
                items.append(f"{qtd}x          {nome_produto}   {lote}")

        output = (
            f"Leitura de caixas (sem identificação de pedido):\n\n"
            f"Qty:       Des:\n" + "\n".join(items)
        )

        save_resultL(output, qr_data)

        return {"error": False, "message": "QR Code processado!", "output": output}
    except Exception as e:
        return {"error": True, "message": f"Erro ao processar QR Code: {e}", "output": ""}
