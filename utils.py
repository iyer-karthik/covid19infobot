from collections.abc import MutableMapping, Mapping
from collections import OrderedDict

class CaseAgnosticDict(MutableMapping):
    """
    Case agnostic dictionary like object. Inspired from a similar 
    data structure in `requests`
    """
    def __init__(self, data=None, **kwargs):
        self._internal_dict = OrderedDict()
        if data is None:
            data = {}
        self.update(data, **kwargs)
    
    def __setitem__(self, key, value):
        # Only supports strings as keys
        self._internal_dict[key.lower()] = (key, value)
    
    def __getitem__(self, key):
        _, actual_value = self._internal_dict[key.lower()]
        return actual_value
    
    def __delitem__(self, key):
        del self._internal_dict[key.lower()]
    
    def __iter__(self):
        # Return generator. Case sensitive
        return (casedkey for casedkey, value in self._internal_dict.values())
    
    def __len__(self):
        return len(self._internal_dict)
    
    def lower_items(self):
        return ((lowerkey, val[1]) for (lowerkey, val) in self._internal_dict.items())
    
    def __repr__(self):
        return str({lowerkey: val[1] for (lowerkey, val) in self._internal_dict.items()})
    
    def copy(self):
        return CaseAgnosticDict(dict(self.lower_items()))
    
    def __eq__(self, other):
        if isinstance(other, Mapping):
            other = CaseAgnosticDict(other)
        else:
            return NotImplemented
        return dict(self.lower_items()) == dict(other.lower_items())