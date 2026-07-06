# logging_config.py
"""
Central logging configuration for the SC Probate Caseload ETL pipeline.
Import get_logger(__name__) in each stage module instead of using print(),
so every stage's output goes to both the console and a persistent log file.
"""

import logging
from pathlib import Path


def get_logger(name, log_dir=None):
    """Returns a configured logger for the given module name.

    log_dir: if provided, also writes logs to {log_dir}/pipeline.log.
    If omitted, logs only go to the console (useful for quick standalone runs).
    """
    logger = logging.getLogger(name)

    # Guard against duplicate handlers if get_logger is called more than once
    # for the same name (e.g. once by a stage module, once by the orchestrator)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Always log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optionally also log to a file, for runs that need a persistent audit trail
    if log_dir is not None:
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_dir / "pipeline.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger