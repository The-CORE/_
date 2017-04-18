import _
from .underscore_node import UnderscoreNode


class TemplateFunctionNode(UnderscoreNode):
    """
    A function has returns=something.
    """
    def __init__(self, sections, returns, names):
        self.sections = sections
        self.returns = returns
        self.names = names

    def __str__(self):
        return self.__repr__()

    def run(self, memory, *args, **kwargs):
        class TemplateOrFunction:
            def __init__(
                    self,
                    sections,
                    returns,
                    names,
                    memory,
                    *args,
                    **kwargs
            ):
                self.sections = sections
                self.returns = returns
                self.names = names
                self.memory = memory
                self.args = args
                self.kwargs = kwargs

            def __call__(self, expressions=[]):
                if len(expressions) != len(self.names):
                    raise _.exceptions.UnderscoreTypeError(
                        'number of expressions passed does not match number '
                        'required'

                    )
                internal_memory = {
                    'container': self.memory
                }
                values = [
                    expression.run(self.memory) for expression in expressions
                ]
                for name, value in zip(self.names, values):
                    internal_memory[name] = value
                for section in self.sections:
                    section.pre_run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                for section in self.sections:
                    section.run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                if self.returns is not None:
                    return self.returns.run(
                        memory=internal_memory,
                        *self.args,
                        **self.kwargs
                    )
                return internal_memory
        return TemplateOrFunction(
            self.sections,
            self.returns,
            self.names,
            memory,
            *args,
            **kwargs
        )
