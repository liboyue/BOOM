from boom import Parameter

int_conf = {
        'name': 'p',
        'type': 'int',
        'start': 1,
        'end': 10,
        'step_size': 1
        }

float_conf = {
        'name': 'p',
        'type': 'float',
        'start': 0,
        'end': 1,
        'step_size': 0.1
        }

collection_conf = {
        'name': 'p',
        'type': 'collection',
        'values': ['a', 'b', 'c']
        }

def test_init():
    Parameter(int_conf)
    Parameter(float_conf)
    Parameter(collection_conf)

def test_to_str():
    assert str(Parameter(int_conf)) == 'name: p, type: int, start: 1, end: 10, step size: 1'
    assert str(Parameter(float_conf)) == 'name: p, type: float, start: 0, end: 1, step size: 0.1'
    assert str(Parameter(collection_conf)) == "name: p, type: collection, values: ['a', 'b', 'c']"

def test_get_values():
    def _compare_lists(a, b):
        for x, y in zip(a, b):
            if x != y:
                return False
        return True

    def _compare_float_lists(a, b):
        for x, y in zip(a, b):
            if abs(x-y) > 1e-4:
                return False
        return True

    assert _compare_lists(list(Parameter(int_conf).get_values()), list(range(1, 11)))
    assert _compare_float_lists(list(Parameter(float_conf).get_values()), list([x/10.0 for x in range(0, 11)]))
    assert _compare_lists(list(Parameter(collection_conf).get_values()), ['a', 'b', 'c'])

def test_get_n_choices():
    assert Parameter(int_conf).get_n_choices() == 10
    assert Parameter(float_conf).get_n_choices() == 11
    assert Parameter(collection_conf).get_n_choices() == 3
