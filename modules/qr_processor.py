from modules.save import save_result

def ind(cod):
    """Identifica se o produto é unidade ou caixa."""
    type_ = cod[-2:]
    if type_ == "01":
        return "UNIDADE"
    else:
        return "CAIXA"

def process_qr_data(qr_data, prod_dict):
    """Processa o QR Code, retorna os resultados e salva em um arquivo."""
    try:
        lines = qr_data.splitlines()
        if len(lines) < 2:
            return {"error": True, "message": "Formato inválido!", "output": ""}

        order_id = lines[0]
        items = []
        for line in lines[1:]:
            try:
                qty, code = line.split()
                name = prod_dict.get(code.strip(), "Produto não encontrado")
                items.append(f"{qty}x          {name}")
            except ValueError:
                items.append(f"{line} - Formato inválido")

        output = (
            f"Pedido: {order_id}\nFormato: {ind(code)}\n\n"
            f"Qty:       Des:\n" + "\n".join(items)
        )

        # Salvar resultado em um arquivo de texto
        save_result(order_id, output, qr_data)

        return {"error": False, "message": "QR Code processado!", "output": output}
    except Exception as e:
        return {"error": True, "message": f"Erro ao processar QR Code: {e}", "output": ""}


