def save_resultL(output, qr_data):
    filename = f"D:/Projetos/Checklist_Florio/Result/QrLote(viewer).txt"
    fileqr = f"D:/Projetos/Checklist_Florio/Result/QrLote.txt"
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