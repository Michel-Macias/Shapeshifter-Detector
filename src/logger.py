import logging
from rich.logging import RichHandler

def setup_logger(name="identify-files"):
    """
    Configura un logger profesional utilizando RichHandler para una salida visual estéticamente premium.
    """
    FORMAT = "%(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )

    logger = logging.getLogger(name)
    return logger

# Instancia global para facilitar el uso en todo el proyecto
logger = setup_logger()
