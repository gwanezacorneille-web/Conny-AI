import logging
from pathlib import Path


def create_audit_logger(path):

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(
        f"conny_security_{path}"
    )

    if not logger.handlers:

        handler = logging.FileHandler(path)

        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s %(message)s"
            )
        )

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = False

    return logger


def audit(logger, event, user_id=None):

    if user_id:
        logger.info(
            "%s user_id=%s",
            event,
            user_id,
        )
    else:
        logger.info(event)
