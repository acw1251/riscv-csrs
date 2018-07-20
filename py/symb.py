from functools import wraps

def args_to_str(*args, **kwargs):
    """Convert function arguments to string."""
    def kwarg_to_str(kwarg):
        name, value = kwarg
        return '%s=%s' % (name, str(value))
    all_args = list(map(str, args)) + list(map(kwarg_to_str, kwargs.items()))
    return ', '.join(all_args)

class SymbolicObject:
    """Track symbolic usage of function and method calls."""

    def __init__(self, name, function = None, args = [], kwargs = {}, symbol = None, strfunc = None):
        """Create a SymbolicObject for a variable, function call, or method call

        This class is used for symbolic variables, functions, and classes.
        - Variables have function set to None
        - Function calls have the function set to the function being called,
          and the arguments and keyword argumenrs are set appropriately. In
          the case of a unary or a binary function, a symbol can be provided
          to print the symbolic application of the function in prefix or infix
          notation.
        - Method calls are constructed similar to function calls, but the
          function argument for a method called foo must be something like
          this: 'lambda self, *arg, **kwarg: self.foo(*arg, **kwarg)'. In this
          case self must be passed as args[0], and the rest of the arguments
          are placed in arg[1:] and kwargs.
        """
        self._symb_name = name
        self._symb_function = function
        self._symb_args = args
        self._symb_kwargs = kwargs
        self._symb_symbol = symbol
        if strfunc is not None:
            self._symb_strfunc = strfunc
        elif function is None:
            self._symb_strfunc = lambda: self._symb_name
        elif self._symb_symbol is not None and len(args) == 1 and len(kwargs) == 0:
            # prefix
            self._symb_strfunc = lambda arg: '(%s%s)' % (self._symb_symbol, str(arg))
        elif self._symb_symbol is not None and len(args) == 2 and len(kwargs) == 0:
            # infix
            self._symb_strfunc = lambda left_arg, right_arg: '(%s %s %s)' % (str(left_arg), self._symb_symbol, str(right_arg))
        else:
            self._symb_strfunc = lambda *args, **kwargs: '%s(%s)' % (self._symb_name, args_to_str(*args, **kwargs))

    def __str__(self):
        if self._symb_strfunc is not None:
            return self._symb_strfunc(*self._symb_args, **self._symb_kwargs)
        else:
            return '%s(%s)' % (self._symb_name, args_to_str(*self._symb_args, **self._symb_kwargs))

    def __repr__(self):
        return "SymbolicObject(%s, function = %s, args = %s, kwargs = %s, symbol = %s)" % (self._symb_name, repr(self._symb_function), repr(self._symb_args), repr(self._symb_kwargs), repr(self._symb_symbol))

    def __hash__(self):
        return hash(repr(self))

    def __getattr__(self, attribute):
        illegal_methods = ['__bool__', '__iter__', '__delitem__', '__delslice__', '__getitem__', '__getslice__', '__len__']
        if attribute in illegal_methods:
            raise ValueError('%s not supported for SymbolicObject' % attribute)
        return SymbolicObject('__getattr__', lambda self, attribute: self.__getattribute__(attribute), [self, attribute],
                strfunc = lambda self, attribute: str(self) + '.' + str(attribute))

    def __call__(self, *args, **kwargs):
        return SymbolicObject('__call__', lambda self, *args, **kwargs: self.__call__(*args, **kwargs), (self,) + args, kwargs=kwargs,
                strfunc = lambda self, *args, **kwargs: '%s(%s)' % (self, args_to_str(*args, **kwargs)))

    def __abs__(self):
        return SymbolicObject('abs', lambda x: abs(x), [self])

    def __add__(self, other):
        return SymbolicObject('add', lambda x, y: x + y, [self, other], symbol = '+')

    def __and__(self, other):
        return SymbolicObject('and', lambda x, y: x & y, [self, other], symbol = '&')

    def __divmod__(self, other):
        return SymbolicObject('divmod', lambda x, y: divmod(x, y), [self, other])

    def __eq__(self, other):
        return SymbolicObject('eq', lambda x, y: x == y, [self, other], symbol = '==')

    def __floordiv__(self, other):
        return SymbolicObject('floordiv', lambda x, y: x // y, [self, other], symbol = '//')

    def __ge__(self, other):
        return SymbolicObject('ge', lambda x, y: x >= y, [self, other], symbol = '>=')

    def __gt__(self, other):
        return SymbolicObject('gt', lambda x, y: x > y, [self, other], symbol = '>')

    def __invert__(self):
        return SymbolicObject('invert', lambda x: ~x, [self], symbol = '~')

    def __le__(self, other):
        return SymbolicObject('le', lambda x, y: x <= y, [self, other], symbol = '<=')

    def __lshift__(self, other):
        return SymbolicObject('lshift', lambda x, y: x << y, [self, other], symbol = '<<')

    def __lt__(self, other):
        return SymbolicObject('lt', lambda x, y: x < y, [self, other], symbol = '<')

    def __mod__(self, other):
        return SymbolicObject('mod', lambda x, y: x % y, [self, other], symbol = '%')

    def __mul__(self, other):
        return SymbolicObject('mul', lambda x, y: x * y, [self, other], symbol = '*')

    def __ne__(self, other):
        return SymbolicObject('ne', lambda x, y: x != y, [self, other], symbol = '!=')

    def __neg__(self):
        return SymbolicObject('neg', lambda x: -x, [self], symbol = '-')

    def __or__(self, other):
        return SymbolicObject('or', lambda x, y: x | y, [self, other], symbol = '|')

    def __pos__(self):
        return SymbolicObject('pos', lambda x: +x, [self], symbol = '+')

    def __pow__(self, value, mod=None):
        return SymbolicObject('pow', lambda x, y, z: pow(x, y, z), [self, value, mod])

    def __radd__(self, other):
        return SymbolicObject('add', lambda x, y: x + y, [other, self], symbol = '+')

    def __rand__(self, other):
        return SymbolicObject('and', lambda x, y: x & y, [other, self], symbol = '&')

    def __rdivmod__(self, other):
        return SymbolicObject('divmod', lambda x, y: divmod(x, y), [other, self])

    def __rfloordiv__(self, other):
        return SymbolicObject('floordiv', lambda x, y: x // y, [other, self], symbol = '//')

    def __rlshift__(self, other):
        return SymbolicObject('lshift', lambda x, y: x << y, [other, self], symbol = '<<')

    def __rmod__(self, other):
        return SymbolicObject('mod', lambda x, y: x % y, [other, self], symbol = '%')

    def __rmul__(self, other):
        return SymbolicObject('mul', lambda x, y: x * y, [other, self], symbol = '*')

    def __ror__(self, other):
        return SymbolicObject('or', lambda x, y: x | y, [other, self], symbol = '|')

    def __rpow__(self, value, mod=None):
        return SymbolicObject('pow', lambda x, y, z: pow(x, y, z), [value, self, mod])

    def __rrshift__(self, other):
        return SymbolicObject('rshift', lambda x, y: x >> y, [other, self], symbol = '>>')

    def __rshift__(self, other):
        return SymbolicObject('rshift', lambda x, y: x >> y, [self, other], symbol = '>>')

    def __rsub__(self, other):
        return SymbolicObject('sub', lambda x, y: x - y, [other, self], symbol = '-')

    def __rtruediv__(self, other):
        return SymbolicObject('truediv', lambda x, y: x / y, [other, self], symbol = '/')

    def __rxor__(self, other):
        return SymbolicObject('xor', lambda x, y: x ^ y, [other, self], symbol = '^')

    def __sub__(self, other):
        return SymbolicObject('sub', lambda x, y: x - y, [self, other], symbol = '-')

    def __truediv__(self, other):
        return SymbolicObject('truediv', lambda x, y: x / y, [self, other], symbol = '/')

    def __xor__(self, other):
        return SymbolicObject('xor', lambda x, y: x ^ y, [self, other], symbol = '^')


class SymbolicCond(SymbolicObject):
    def __init__(self, name, args = []):
        SymbolicObject.__init__(self, name, args = args, strfunc = lambda condition, isTrue, isFalse: '(%s ? %s : %s)' % (str(condition), str(isTrue), str(isFalse)))

def cond(condition, ifTrue, ifFalse):
    return SymbolicCond( 'cond', args = [condition, ifTrue, ifFalse] )

def memoize_compute(f):
    memoized = {}
    @wraps(f)
    def wrapped_compute(symbol, context):
        key = (repr(symbol), repr(context))
        if key in memoized:
            return memoized[key]
        else:
            value = f(symbol, context)
            memoized[key] = value
            return value
    return wrapped_compute

@memoize_compute
def compute(symbol, context):
    """Compute the value of a SymbolicObject using a specified context.
    
    context is a dictionary mapping names of symbols to values. If a value for
    a symbol is not found, or a function is not callable, this function raises
    a ValueError."""
    if isinstance(symbol, SymbolicCond):
        condition = compute(symbol._symb_args[0], context)
        if condition:
            return compute(symbol._symb_args[1], context)
        else:
            return compute(symbol._symb_args[2], context)
    elif isinstance(symbol, SymbolicObject):
        if symbol._symb_function is None:
            if symbol._symb_name in context:
                return context[symbol._symb_name]
            else:
                raise ValueError('"%s" not found in context' % (symbol._symb_name))
        else:
            if callable(symbol._symb_function):
                # compute each argument recursively
                #computed_args = []
                #if symbol._symb_args is not None:
                #    computed_args = list(map(lambda x: compute(x, context), symbol._symb_args))
                computed_args = list(map(lambda x: compute(x, context), symbol._symb_args))
                #computed_kwargs = {}
                #if symbol._symb_kwargs is not None:
                #    computed_kwargs = dict(map(lambda k, x: (k, compute(x, context)), symbol._symb_kwargs.items()))
                computed_kwargs = dict(map(lambda k, x: (k, compute(x, context)), symbol._symb_kwargs.items()))
                # then apply function
                return symbol._symb_function( *computed_args, **computed_kwargs )
            else:
                raise ValueError("symbol._symb_function is not callable")
    elif isinstance(symbol, list):
        value_list = []
        for item in symbol:
            value_list.append( compute(item, context) )
        return value_list
    elif isinstance(symbol, tuple):
        value_tuple = tuple()
        for item in symbol:
            value_tuple = value_tuple + (compute(item, context), )
        return value_tuple
    else:
        return symbol

def symbolic(f):
    """Decorate a function or class for symbolic use.
    
    Using the symbolic decorator on a function or class definition causes
    the execution of the function or any functions called on the class to
    be delayed until the compute function is called on it.
    """
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if hasattr(f, '__name__'):
            return SymbolicObject(f.__name__, f, args, kwargs)
        else:
            raise ValueError("sylbolic(f) requires f.__name__ to exist")
    return wrapped_function

def symbol(name):
    return SymbolicObject(name)

def collect(all_list):
    def wrapper(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            return_value = f(*args, **kwargs)
            all_list.append(return_value)
            return return_value
        return wrapped_function
    return wrapper

top_level = False

def top_level_collect(collection):
    def func_wrapper(f):
        @wraps(f)
        def wrapped_f(*args, **kwargs):
            if top_level:
                top_level = False
                try:
                    value = f(*args, **kwargs)
                except:
                    top_level = True
                    raise
                top_level = True
                collection.append(value)
            else:
                return f(*args, **kwargs)

if __name__ == '__main__':
    x = symbol('x')

    test_strings = [ 'x + 1', '1 + x', 'x - 1', '1 - x', '+x', '-x',
                     'x / 2', '2 / x', '7 * x', 'x * 7', 'x // 5', '5 // x',
                     'x & 3', '3 & x', 'x | 8', '8 | x', 'x ^ 7', '7 ^ x']
    for string in test_strings:
        result = eval(string)
        print('%s => %s' % (string, repr(result)))

    @symbolic
    def kw_test(x, y, z = None):
        return x + y + z

    print(str(kw_test(1, 2, z = 3)))

    for string in test_strings:
        x = 6
        eval_result = eval(string)
        print('eval(%s) = %s' % (string, str(eval_result)))
        x = symbol('x')
        symb_eqn = eval(string)
        symb_result = compute(symb_eqn, {'x' : 6})
        print('compute(%s, {x: %d}) = %s' % (string, 6, str(symb_result)))
        if eval_result != symb_result:
            raise ValueError("eval results don't match symbolic compute results")

    @symbolic
    class PlusOne:
        def __init__(self, x):
            self.x = x
        def plusone(self):
            return self.x + 1

    y = PlusOne(symbol('x'))

    z = y.plusone()

    print('z = ' + str(z))
    print('compute(z, {x: %d}) = %d' % (12, compute(z, {'x': 12})))

