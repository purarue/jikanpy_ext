# Unfinished code

I ended up contributing directly to jikanpy instead of using this, leaving this up here as I think [./jikanpy_ext/jikan_ext.py](./jikanpy_ext/jikan_ext.py) is a decent use case of `__getattribute__`.

Initially, the usecase was to use this to wrap `jikanpy` calls with logs/ratelimits/get metadata about the request.

### jikanpy_ext

#### Installation

Install `jikanpy`, then `jikanpy_ext`:

```

pip install git+git://github.com/AWConant/jikanpy.git
pip install git+git://github.com/seanbreckenridge/jikanpy_ext.git

```

Since this is wrapping commands and passing the arguments to `Extension`s, you must use keyword arguments for API calls. i.e. `j.anime(id=1)` instead of `j.anime(1)`

This currently only supports the synchronous wrapper.

