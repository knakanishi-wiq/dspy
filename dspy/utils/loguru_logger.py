import logging
import re
from functools import partialmethod
from sys import stdout

from loguru import logger as loguru_logger


def formatter(record):
    """
    Custom formatter for loguru logger.

    This function formats the log record based on the log level and applies
    color formatting using predefined format strings. It replaces curly braces
    and xref tags to avoid conflicts with loguru color tags.

    Args:
        record (dict): The log record dictionary containing log information.

    Returns:
        str: The formatted log message with color formatting and time, level,
             and function information.

    Format Dictionary:
        The FORMAT_DICT contains predefined format strings for different log levels.
        Each format string includes color tags and placeholders for the log message.

    Example:
        record = {
            "message": "This is a log message with {curly braces} and <xref:123>",
            "level": logging.INFO,
            "function": "my_function"
        }
        formatted_message = formatter(record)
        print(formatted_message)
    """
    FORMAT_DICT = {
        "FORWARD": "<fg #ff91af>{MESSAGE}</fg #ff91af>",
        "RESPONSE": "<fg #9dd4f5>{MESSAGE}</fg #9dd4f5>",
        "LLM_CALL": "<fg #f4bbff>{MESSAGE}</fg #f4bbff>",
        "LLM_RESPONSE": "<fg #ff80ff>{MESSAGE}</fg #ff80ff>",
    }
    # Escape curly braces
    message = record["message"].replace("{", "{{").replace("}", "}}")
    # Replace xref tag which conflicts with loguru color tags
    message = re.sub(r"<xref:(\d+)>", r"{{xref:\1}}", message)
    message = re.sub(r"<locals>", r"\<locals>", message)
    message = re.sub(r"<lambda>", r"\<lambda>", message)
    color_format = FORMAT_DICT.get(record["level"].name, None)
    if color_format:
        message = color_format.replace("{MESSAGE}", message)
    return "<green>{time:YYYY-MM-DD HH:mm:ss}</green> |<level>{level: ^8}</level>| <cyan>{function}</cyan> - <level>" + message + "</level>\n"


def setup_logger(
    level: int = logging.DEBUG,
):
    """Setup the logger.
    See https://console.cloud.google.com/logs

    Args:
        level: The logging level.

    Returns:
        loguru logger
    """
    # Remove the default logger
    loguru_logger.remove()

    # Local Logging (GKE, GCE, ...):
    loguru_logger.add(stdout, level=level, format=formatter)

    # Define a new ReAct Node level. 25 is the severity level
    try:
        loguru_logger.level("FORWARD", no=25, color="<magenta>", icon="🔮")
    except TypeError:
        pass
    # Define a new ReAct Edge level. 25 is the severity level
    try:
        loguru_logger.level("SIGNATURE", no=25, color="<yellow>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("RESULT", no=10, color="<cyan>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("SIGNATURE_MANIPULATION", no=10, color="<green>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("OPTIMIZER", no=10, color="<red>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("LLM_CALL", no=10, color="<light-magenta>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("LLM_RESPONSE", no=10, color="<light-magenta>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("RETRIEVER", no=10, color="<light-magenta>", icon="🔮")
    except TypeError:
        pass
    try:
        loguru_logger.level("RAG", no=10, color="<light-magenta>", icon="🔮")
    except TypeError:
        pass

    return loguru_logger


logger = setup_logger()
logger.__class__.forward = partialmethod(logger.__class__.log, "FORWARD")
logger.__class__.signature = partialmethod(logger.__class__.log, "SIGNATURE")
logger.__class__.llm_call = partialmethod(logger.__class__.log, "LLM_CALL")
logger.__class__.llm_response = partialmethod(logger.__class__.log, "LLM_RESPONSE")
logger.__class__.signature_manipulation = partialmethod(logger.__class__.log, "SIGNATURE_MANIPULATION")
logger.__class__.optimizer = partialmethod(logger.__class__.log, "OPTIMIZER")
