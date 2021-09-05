from package import MaterialIterator

def test_start():
  m = MaterialIterator()
  assert next(m) == 0

def test_iterations():
  m = MaterialIterator()
  count = 0
  for i in m:
    count += 1
  assert i == 2.0
  assert count == 101

def test_fast_iterations():
  m = MaterialIterator(2)
  count = 0
  for i in m:
    count += 1
  assert i == 2.0
  # Half the number of iteration
  assert count == 51
