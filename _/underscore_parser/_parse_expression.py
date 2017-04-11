from _ import nodes
from _ import exceptions
from ._surrounding_whitespace_removed import _surrounding_whitespace_removed

@_surrounding_whitespace_removed
def _parse_expression(
        self,
        has_semi_colon=True,
        parsers_to_not_allow=[]
):
    """
    Parses an expression (see grammar for details). An expression consists
    of one of various other parsers, sometimes followed by a semi colon,
    (indicated by the has_semi_colon flag). Any parsers included in the
    parsers_to_not_allow list will not be permitted to be parsed as part of the
    expression.
    """
    # Assign the parsers that may make up the expression.
    valid_parsers = [
        self._parse_addition,
        self._parse_subtraction,
        self._parse_boolean_expression,
        self._parse_term,
        self._parse_object,
    ]

    # Remove any parsers not to be included...
    try:
        for parser_to_remove in parsers_to_not_allow:
            try:
                valid_parsers.remove(parser_to_remove)
            except ValueError:
                continue
    except TypeError:
        raise TypeError('parser_to_not_allow must be iterable.')

    expression = self._try_parsers(valid_parsers, 'expression')

    if self._peek() != ';' and has_semi_colon:
        raise exceptions.UnderscoreSyntaxError(
            "expected ';', got {}".format(
                self._peek() if self._peek() is not None else 'end of file',
            ),
            self.position_in_program,
        )
    # If it should have a semi colon, it is consumed here.
    if self._peek() == ';' and has_semi_colon:
        self._next()
    return expression