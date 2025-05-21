import logging, sys



def configure_logging(log_level) -> None:
    """configure logging for the application

    Args:
        log_level (_type_): log level to set for the logger
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logging.info(f"logging configured with level: {log_level}")
