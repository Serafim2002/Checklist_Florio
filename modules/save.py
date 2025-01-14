def save_result(order_id, output, qr_data):
    """Salva o resultado do processamento em um arquivo de texto."""
    filename = f"{order_id}.txt"
    fileqr = f"QR.txt"
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(output)
        with open(fileqr, "w", encoding="utf-8") as file:
            file.write(qr_data)
        print(f"Resultado salvo em: {filename}")
        print(f"Resultado salvo em: {fileqr}")
    except Exception as e:
        print(f"Erro ao salvar resultado: {e}")
        print(f"Erro ao salvar resultado: {e}")