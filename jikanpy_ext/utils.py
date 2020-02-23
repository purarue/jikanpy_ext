import logging

# logging related

default_format = "%(asctime)s %(levelname)s %(message)s"

#name should be the logger name, its typically __package__
def setupLogger(name: str = None, log_to: str = None, format_str: str = None, datefmt: str = None):
    """
    name: name of the logger
    log_to: optional file to log to (relative)
    """

    if name is None:
        name = __package__
    lgr = logging.getLogger(name)
    if not lgr.hasHandlers():
        if format_str is None:
            format_str = default_format
        lgr.setLevel(logging.INFO)
        fmtr = logging.Formatter(format_str)
        sh = logging.StreamHandler()
        sh.setFormatter(fmtr)
        lgr.addHandler(sh)
        if log_to:
            lgr = addFileHandler(lgr, log_to, format_str, datefmt)
    return lgr


def addFileHandler(lgr: logging.Logger, filename: str, format_str: str = None, datefmt: str = None):
    if format_str is None:
        format_str = default_format
    fh = logging.FileHandler(log_to, datefmt=datefmt)
    fh.setFormatter(fmtr)
    lgr.addHandler(logging.FileHandler(log_to))
    return lgr


logger = setupLogger(name=__package__)
