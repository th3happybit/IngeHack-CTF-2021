import pickle
import io
import builtins

class MySuperSecureUnpickler(pickle.Unpickler):
    def find_class(self, m, n):
        if m == "builtins":
            return getattr(builtins, n)
        raise pickle.UnpicklingError("Something went wrong xD")


class PickleSerializer():
    def dumps(self, obj):
        return pickle.dumps(obj)

    def loads(self, data):
        try:
            if isinstance(data, str):
                raise TypeError("Something went wrong xD")
            file = io.BytesIO(data)
            return MySuperSecureUnpickler(file,
                                          encoding='ASCII', errors='strict').load()
        except Exception as e:
            raise e
