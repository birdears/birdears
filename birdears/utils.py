class DictCallback(dict):
    
    callback = None
    
    callback_args = list()
    callback_kwargs = dict()
    
    def __init__(self, other=None, **kwargs):
        #super(DictCallback, self).__init__(self, other, **kwargs)
        super(DictCallback, self).__init__()
        self.update(other)
        
    def __setitem__(self, key, value):
        super(DictCallback, self).__setitem__(self, key, value)
        
        if self.callback:
            self.callback(*self.callback_args, **self.callback_kwargs)
            
    def update(self, other=None):
        super(DictCallback, self).update(other)
        
        if self.callback:
            self.callback(*self.callback_args, **self.callback_kwargs)
