import inspect
import re
import ast


def valid_params(*varargs, **keywords):
    '''valid decorator'''
    # resolve list params
    varargs_s = list(map(_toStandardCondition, varargs))
    # resolve dict params
    keywords_s = dict((k, _toStandardCondition(keywords[k])) for k in keywords)

    def generator(func):
        # get params of input func
        args, varargs, varkw = inspect.getfullargspec(func)[:3]
        dict_validator = _getcallargs(args, varargs, varkw, varargs_s, keywords_s)

        def wrapper(*callvarargs, **callkeywords):
            dict_callargs = _getcallargs(args, varargs, varkw, callvarargs, callkeywords)

            k, item = None, None
            try:
                for k in dict_validator:
                    if k == varargs:
                        for item in dict_callargs[k]:
                            assert dict_validator[k](item)
                    elif k == varkw:
                        for item in dict_callargs[k].values():
                            assert dict_validator[k](item)
                    else:
                        item = dict_callargs[k]
                        assert dict_validator[k](item)
            except Exception as e:
                pass

            return func(*callvarargs, **callkeywords)

        wrapper = _wrapps(wrapper, func)
        return wrapper

    return generator


def _toStandardCondition(condition):
    '''change check condition to check functions'''

    # when condition is a simple class. such as valid(str,int)
    if inspect.isclass(condition):
        return lambda x: isinstance(x, condition)
    # when condition is a k-v style. such as valid(i=(int,'10<x<20'))
    if isinstance(condition, (tuple, list)):
        cls, condition = condition[:2]
        # condition is none. such as valid(i=(int,))
        if condition is None:
            return _toStandardCondition(cls)
        # condition is a string with regex. such as valid('/^\d+$/')
        if cls is str and condition[0] == condition[-1] == '/':
            return lambda x: (isinstance(x, cls) and re.match(condition[1:-1], x) is not None)
        # x is int and condition like '1<x<5'
        return lambda x: (isinstance(x, cls) and ast.literal_eval(condition))
    return condition


def _getcallargs(args, varargname, kwname, varargs_s, keywords_s):
    '''获取调用时，各参数k-v的字典'''
    dict_args = {}
    varargs_s = tuple(varargs_s)
    keywords_s = dict(keywords_s)

    argcount = len(args)
    varcount = len(varargs_s)
    callvarargs = ()
    if argcount <= varcount:
        for n, argname in enumerate(args):
            dict_args[argname] = varargs_s[n]
        callvarargs = varargs_s[(argcount - varcount):]
    else:
        for n, var in enumerate(varargs_s):
            dict_args[args[n]] = var

        for argname in args[(varcount - argcount):]:
            if argname in keywords_s:
                dict_args[argname] = keywords_s.pop(argname)

    if varargname is not None:
        dict_args[varargname] = callvarargs
    if kwname is not None:
        dict_args[kwname] = keywords_s

    dict_args.update(keywords_s)
    return dict_args


def _wrapps(wrapper, wrapped):
    '''Copy metadata'''

    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))

    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr))
    return wrapper


def null_ok(cls, condition=None):
    return lambda x: x is None or _toStandardCondition((cls, condition))(x)


def multi_type(*conditions):
    ''' just need one condition to be passed'''
    list_validator = map(_toStandardCondition, conditions)

    def validate(x):
        for v in list_validator:
            if v(x):
                return True

    return validate
