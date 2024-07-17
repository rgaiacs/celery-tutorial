import logging

logger = logging.getLogger(__name__)


def mul(a, b):
    logger.info("Ready to multiply %d x %d" % (a, b))
    return a * b
