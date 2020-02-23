import os
import pathlib

from jikanpy_ext.extension import Extension
from jikanpy_ext.utils import logger
from .utils import stringify

default_cache_location = os.path.join(pathlib.Path.home(), '.jikanpy_ext_cache')



class Cache(Extension):

    # def __init__(self, default_cache_location: str = None):
    #     pass

    def before_hook(self, ctx):
        logger.info(stringify(ctx))

    def after_hook(self, ctx):
        pass
