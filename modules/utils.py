def update_status(label, message, color):
    """Atualiza a mensagem de status."""
    label.config(text=message, foreground=color)
