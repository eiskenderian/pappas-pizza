from package import MaterialIterator

def test_start():
    m = MaterialIterator()
    assert next(m) == 0