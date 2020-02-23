from typing import Union
from jikanpy_ext.utils import setupLogger
from jikanpy_ext.extension import Extension

class Logger(Extension):

    def __init__(self, file: str = None, loglevel: Union[str, int] = "INFO"):

        self._logger = setupLogger(name=__package__,
                                   format_str="%(asctime)s %(message)s",
                                   log_to=file,
                                   datefmt="%x %H:%M:%S")
        self._logger.setLevel(loglevel)

    def before_hook(self, ctx):
        self._logger.info("{}: with {}".format(ctx.request_name, ctx.jikanpy_kwargs))

    def after_hook(self, ctx):
        self._logger.debug("request_hash: {}".format(ctx.response['request_hash']))
