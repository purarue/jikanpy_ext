import copy
from typing import Optional, Callable, Dict

import jikanpy

from .constants import wrapped_functions
from .exceptions import JikanException, ClientException, JikanExtException, PositionalArgumentException


class Context():
    def __init__(self, request_name: str, jikanpy_func: Callable, jikanpy_kwargs: Dict, response: Dict = None):

        self.request_name = request_name
        self.jikanpy_func = jikanpy_func
        self.kwargs = jikanpy_kwargs  # reference, Extensions have the oppurtunity to modify these
        self.jikanpy_kwargs = copy.deepcopy(jikanpy_kwargs)  # copy, to use for other uses
        self.response = response

        # allow args to be accessible through 'ctx.' syntax
        for k, v in self.jikanpy_kwargs.items():
            setattr(self, k, v)            




class Extension():

    def before_hook(self, ctx: Context):
        pass

    def after_hook(self, ctx: Context):
        pass


    def on_error(self, ctx: Context, error: Exception):
        pass

    @property
    def caught_exceptions(self):
        """instance variable; a set() of errors caught by this Extension"""
        return set([])
