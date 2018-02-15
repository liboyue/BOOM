from src import Parameter

conf = {
        'name': 'test_param',
        'start': 1,
        'end': 10,
        'step size': 2
        }

def test_to_str():
    p = Parameter(conf)
    assert str(p) == 'name: test_param, start: 1, end: 10, step size: 2'

def test_get_value():
    p = Parameter(conf)
    assert p.get_value() == 1

def test_set_value():
    p = Parameter(conf)
    assert p.get_value() == 1
    p.set_value(100)
    assert p.get_value() == 100

def test_next_value():
    p = Parameter(conf)
    assert p.get_value() == 1
    p.next_value()
    assert p.get_value() == 3

def test_reset_value():
    p = Parameter(conf)
    assert p.get_value() == 1
    p.set_value(100)
    assert p.get_value() == 100
    p.reset_value()
    assert p.get_value() == 1
