class Response:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    # Backward compatibility with dict
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __contains__(self, key):
        return hasattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def update(self, other):
        if isinstance(other, dict):
            for key, value in other.items():
                setattr(self, key, value)
        elif hasattr(other, '__dict__'):
            self.__dict__.update(other.__dict__)
        else:
             # try to iterate as (key, value) pairs
             for key, value in other:
                 setattr(self, key, value)

    def __repr__(self):
        return f"Response({self.__dict__})"
