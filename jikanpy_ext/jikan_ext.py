from collections import defaultdict
from copy import deepcopy
from typing import Optional, List, Any, Set

from jikanpy.jikan import Jikan

from .extension import Context, Extension
from .constants import wrapped_functions
from .exceptions import JikanException, APIException, ClientException, DeprecatedEndpoint, JikanExtException, PositionalArgumentException
from .utils import logger


class JikanExt(Jikan):

    def __init__(self, *args, **kwargs):

        extensions = kwargs.pop('extensions', [])

        super().__init__(*args, **kwargs)

        # hooks for extensions
        self._before_hooks: List = []
        self._after_hooks: List = []
        self._error_hooks: defaultdict = defaultdict(list)
        self.extensions = extensions
        for ext in self.extensions:
            self._apply_extension(ext)


    def _apply_extension(self, ext: Extension):

        self._before_hooks.append(ext.before_hook)
        self._after_hooks.append(ext.after_hook)
        for exc in ext.caught_exceptions:
            self._error_hooks[exc.__class__.__name__].append(ext.on_error)


    def __getattribute__(self, name):

        if name in wrapped_functions:
            # only accept keyword arguments so that hooks
            # have an easier time monitoring behavior
            def func(**kwargs):

                jikanpy_func = getattr(super(JikanExt, self), name)

                ctx = Context(request_name=name, jikanpy_func=jikanpy_func, jikanpy_kwargs=kwargs)

                # call any before_hook's from Extensions
                for hook in self._before_hooks:
                    hook(ctx)

                # catch any errors from Extensions
                try:
                    response: Any = jikanpy_func(**kwargs)
                # if theres an error
                except tuple(self._error_hooks.keys()) as caught_err:
                    # pass error to all Extension defined on_error function
                    for err_handler in self._error_hooks[caught_err.__class__.__name__]:
                        err_handler(ctx, caught_err)

                # attach context to response
                response["context"] = ctx
                ctx.response = response

                # call any after_hook's from Extensions
                for hook in self._after_hooks:
                    hook(ctx)

                return response
            return func
        else:
            return object.__getattribute__(self, name)

    def get_url(self, ctx: Context):
        if ctx.request_name not in wrapped_functions:
            raise ClientException(f"Not able to create URL for endpoint {ctx.request_name}, not in wrapped functions: {wrapped_functions}")
        url = None
        if ctx.request_name in ["anime", "manga", "character", "person", "club"]:
            url = self._get_url(ctx.request_name,
                                ctx.jikanpy_kwargs['id'],
                                ctx.jikanpy_kwargs.get("extension", None),
                                ctx.jikanpy_kwargs.get("page", None))
        elif ctx.request_name == "search":
            url = self._get_search_url(ctx.jikanpy_kwargs["search_type"],
                                       ctx.jikanpy_kwargs["query"],
                                       ctx.jikanpy_kwargs.get("page", None),
                                       ctx.jikanpy_kwargs.get("parameters", None))
        elif ctx.request_name == "season":
            url = self._get_season_url(ctx.jikanpy_kwargs["year"],
                                       ctx.jikanpy_kwargs["season"])
        elif ctx.request_name == "season_archive":
            url = str(self.season_archive_url)
        elif ctx.request_name == "season_later":
            url = str(self.season_later_url)
        elif ctx.request_name == "schedule":
            url = self._get_schedule_url(ctx.jikanpy_kwargs.get("day", None))
        elif ctx.request_name == "top":
            url = self._get_top_url(ctx.jikanpy_kwargs["type"],
                                    ctx.jikanpy_kwargs.get("page", None),
                                    ctx.jikanpy_kwargs.get("subtype", None))
        elif ctx.request_name == "genre":
            url = self._get_genre_url(ctx.jikanpy_kwargs["type"],
                                      ctx.jikanpy_kwargs["genre_id"],
                                      ctx.jikanpy_kwargs.get("page", None))
        elif ctx.request_name == "producer":
            url = self._get_creator_url(ctx.request_name,
                                        ctx.jikanpy_kwargs["producer_id"],
                                        ctx.jikanpy_kwargs.get("page", None))
        elif ctx.request_name == "magazine":
            url = self._get_creator_url(ctx.request_name,
                                        ctx.jikanpy_kwargs["magazine_id"],
                                        ctx.jikanpy_kwargs.get("page", None))
        elif ctx.request_name == "user":
            url = self._get_user_url(ctx.jikanpy_kwargs["username"],
                                     ctx.jikanpy_kwargs.get("request", None),
                                     ctx.jikanpy_kwargs.get("argument", None),
                                     ctx.jikanpy_kwargs.get("page", None),
                                     ctx.jikanpy_kwargs.get("parameters", None))
        elif ctx.request_name == "meta":
            url = self._get_meta_url(ctx.jikanpy_kwargs["request"],
                                    ctx.jikanpy_kwargs.get("type", None),
                                    ctx.jikanpy_kwargs.get("period", None),
                                    ctx.jikanpy_kwargs.get("offset", None))
        return url

