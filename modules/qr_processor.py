from modules.save import save_result

def ind(cod):
    type = cod[-2:]
    return "UNIDADE" if type == "01" else "CAIXA"

def process_qr_data(qr_data, prod_dict):
    try:
        lines = qr_data.splitlines()
        if len(lines) < 2:
            return {"error": True, "message": "Formato inválido!", "output": ""}

        order_id = lines[0]
        items = []
        last_vcode = None
        for line in lines[1:]:
            try:
                qty, code = line.split()
                code = code.strip()
                last_vcode = code
                name = prod_dict.get(code, "Produto não encontrado")
                items.append(f"{qty}x          {name}")
            except ValueError:
                items.append(f"{line} - Formato inválido")


        formato = ind(last_vcode) if last_vcode else "N/D"
        output = (
            f"Pedido: {order_id}\nFormato: {formato}\n\n"
            f"Qty:       Des:\n" + "\n".join(items)
        )


        save_result(order_id, output, qr_data)

        return {"error": False, "message": "QR Code processado!", "output": output}
    except Exception as e:
        return {"error": True, "message": f"Erro ao processar QR Code: {e}", "output": ""}


