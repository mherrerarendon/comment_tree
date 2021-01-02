def get_query_arg(args, arg_name, arg_defaults):
    if arg_name not in args:
        return arg_defaults[arg_name]
    arg_value = args[arg_name]
    try:
        return to_bool(arg_value)
    except:
        pass
    try:
        return int(arg_value)
    except:
        pass
    return arg_value

def to_bool(arg_value):
    arg_value_lower = arg_value.lower()
    if arg_value_lower != 'false' and arg_value_lower != 'true':
        raise Exception('Not a bool value')
    return arg_value_lower == 'true'

    