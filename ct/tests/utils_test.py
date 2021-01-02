from ct.blueprints.utils import get_query_arg

def test_string_args_work():
    actual_args = {
        'string_arg_name': 'string_value'
    }
    arg_defaults = {
        'string_arg_name': 'string_value1',
        'string_arg_name2': 'default_value'
    }
    assert get_query_arg(actual_args, 'string_arg_name', arg_defaults) == 'string_value'
    assert get_query_arg(actual_args, 'string_arg_name2', arg_defaults) == 'default_value'

def test_int_args_work():
    actual_args = {
        'int_arg_name': '12'
    }
    arg_defaults = {
        'int_arg_name': 1,
        'int_arg_name2': 13
    }
    assert get_query_arg(actual_args, 'int_arg_name', arg_defaults) == 12
    assert get_query_arg(actual_args, 'int_arg_name2', arg_defaults) == 13

def test_bool_args_work():
    actual_args = {
        'bool_arg_name': 'False'
    }
    arg_defaults = {
        'bool_arg_name': True,
        'bool_arg_name2': False
    }
    assert get_query_arg(actual_args, 'bool_arg_name', arg_defaults) == False
    assert get_query_arg(actual_args, 'bool_arg_name2', arg_defaults) == False