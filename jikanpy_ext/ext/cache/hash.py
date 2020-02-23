import os
import pathlib
import json
import hashlib

from jikanpy_ext.exceptions import CacheMiss


class OpenAddressedFileHasher:

    """
    id refers to the unique string for each query, e.g.:
    'search|page|1|parameters|genre|12|genre_exclude|0|order_by|id|sort|desc|query||search_type|anime|'
    hex refers to the corresponding hex digest:
    211d70f1c6b6c197be2e681e1eeb04d926fb7d53
    """

    @staticmethod
    def sha1(id: str):
        return hashlib.sha1(id.strip().encode()).hexdigest()

    @staticmethod
    def increment_hex(hex: str):
        i = int(hex, 16)
        i += 1
        return hex(i)

    def __init__(self, cache_dir):

        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)


    def verify_file_for_id(self, id):
        """
        Returns the corresponding file for an id, if it exists in cache

        Raises:
            CacheMiss: if corresponding id isn't in cache
        """

        # have to mark if you delete items from cache
        hex = OpenAddressedFileHasher.sha1(id)
        file = None
        while file is None:
            if key_exists(hex=hex):
                try:
                    # verify file contents is the same
                except json.JSONDecodeError:

                    # or call super calls to reduce a string to the URL itself

                    # if there was an error reading from a cache file
                    # remove it so that we can re-search for the current id
                    # mark the removed file with a special marker:
                    # https://stackoverflow.com/a/9127262/9348376

            else:
                raise CacheMiss()







    def key_exists(self, *, id=None, hex=None):
        if id is not None:
            hex = OpenAddressedFileHasher.sha1(id)
        if hex is None:
            raise TypeError("'key_exists' missing 'id' or 'hex' keyword argument")
        else:
            return os.path.exists(self.filepath_for(hex))


    def filepath_for(self, hex_code):
        return os.path.join(self.cache_dir, "{}.json".format(hex_code))


    def read_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
