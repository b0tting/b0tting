import sys


class ObjectHasher:

    @staticmethod
    def hash_objects(**kwargs):
        result = ObjectHasher.mash_input(**kwargs)
        hash_result = hash(result)
        if hash_result < 0:
            hash_result += sys.maxsize
        return hash_result

    @staticmethod
    def mash_input(**arguments):
        result = ""
        for key, value in arguments.items():
            if isinstance(value, dict):
                result += ObjectHasher.mash_input(**value)
            result += f"{key}:{value}"
        return result
