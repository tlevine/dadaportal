from .models import Cache

class SomeModel(Cache):
    def reify(filename):
        return {'endpoint': 'a/b/c'}

def test_add_and_sync():
    open('/tmp/blahblahblah', 'w').write('')
    obj = SomeModel.add('/tmp/blahblahblah')
    assert obj.sync() == False
    
    open('/tmp/blahblahblah', 'w').write('')
    assert obj.sync() == True
