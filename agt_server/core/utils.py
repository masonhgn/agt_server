



def server_print(message: str, flush: bool = True):
    """Unified print method for all server output."""
    print(f"[SERVER] {message}", flush=flush)