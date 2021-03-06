from ..exceptions import UnderscoreTypeError, UnderscoreValueError, \
    UnderscoreIncorrectNumberOfArgumentsError
from .constants import BASIC_TYPES


class _Caster:
    def __init__(
        self,
        time_limit,
        memory_limit,
        running_underscore_standard_library
    ):
        self.time_limit = time_limit
        self.memory_limit = memory_limit
        self.running_underscore_standard_library = \
            running_underscore_standard_library

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.TYPE + '_caster'

    def __call__(self, memory_from_call_location, expressions, character):
        if len(expressions) != 1:
            raise UnderscoreTypeError(
                '{} expressions passed, {} required'.format(
                    len(expressions),
                    1
                ),
                character
            )

        value_to_cast = expressions[0].run(
            memory=memory_from_call_location,
            time_limit=self.time_limit,
            memory_limit=self.memory_limit,
            running_underscore_standard_library=\
                self.running_underscore_standard_library
        )
        cannot_cast_error = UnderscoreValueError(
            'could not cast {} to {}'.format(
                expressions[0],
                self.TYPE
            ),
            character
        )

        if type(value_to_cast) in BASIC_TYPES:
            try:
                return self.PYTHON_CASTER(value_to_cast)
            except ValueError:
                raise cannot_cast_error

        if not isinstance(value_to_cast, dict):
            # If it is not a basic type, and it is not a template instance, it
            # cannot be cast. (i.e. it is an uncalled function or template).
            raise cannot_cast_error

        try:
            value_to_return = value_to_cast['__' + self.TYPE]({}, [])
        except UnderscoreIncorrectNumberOfArgumentsError:
            # Their caster method must take zero arguments, if it doesn't, it
            # will raise an UnderscoreIncorrectNumberOfArgumentsError, which
            # means we need to raise an UnderscoreTypeError here, to tell them
            # what to change.
            raise UnderscoreTypeError(
                '{} method must take 0 arguments'.format('__' + self.TYPE),
                character
            )
        except KeyError:
            # If the casting magic method is not defined, the template instance
            # cannot be cast.
            raise cannot_cast_error
        # Otherwise, this is just a problem with their function that they
        # need to see.
        else:
            if not isinstance(value_to_return, self.PYTHON_CASTER):
                raise UnderscoreTypeError(
                    '{} method did not return correct type'.format(
                        '__' + self.TYPE
                    ),
                    character
                )
            return value_to_cast['__' + self.TYPE]({}, [])


class FloatCaster(_Caster):
    TYPE = 'float'
    PYTHON_CASTER = float


class IntegerCaster(_Caster):
    TYPE = 'integer'
    PYTHON_CASTER = int


class BooleanCaster(_Caster):
    TYPE = 'boolean'
    PYTHON_CASTER = bool


class StringCaster(_Caster):
    TYPE = 'string'
    PYTHON_CASTER = str


def get_casters(
    time_limit,
    memory_limit,
    running_underscore_standard_library
):
    casters = {}
    names_and_casters = (
        ('float', FloatCaster),
        ('integer', IntegerCaster),
        ('boolean', BooleanCaster),
        ('string', StringCaster)
    )
    for name, caster in names_and_casters:
        casters[name] = caster(
            time_limit,
            memory_limit,
            running_underscore_standard_library
        )
    return casters
