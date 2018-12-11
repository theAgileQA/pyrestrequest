"""
Basic context implementation for binding variables to values
"""
import logging
import types

LOGGER = logging.getLogger('pyresttest.binding')


class Context(object):
    """ Manages binding of variables & generators,
    with both variable name and generator name being strings """

    variables = dict()  # Maps variable name to current value
    generators = dict()  # Maps generator name to generator function
    mod_count = 0  # Lets us see if something has been altered, avoiding needless retemplating

    def bind_variable(self, variable_name, variable_value):
        """ Bind a named variable to a value within the context
            This allows for passing in variables in testing """
        str_name = str(variable_name)
        prev = self.variables.get(str_name)
        if prev != variable_value:
            self.variables[str(variable_name)] = variable_value
            self.mod_count = self.mod_count + 1

    def bind_variables(self, variable_map):
        """ bind values in map """
        for key, value in variable_map.items():
            self.bind_variable(key, value)

    def add_generator(self, generator_name, generator):
        """ Adds a generator to the context, this can be used to set values for a variable
            Once created, you can set values with the generator via bind_generator_next """

        if not isinstance(generator, types.GeneratorType):
            raise ValueError(
                'Cannot add generator named {0}, it is not a generator type'.format(generator_name))

        self.generators[str(generator_name)] = generator

    def bind_generator_next(self, variable_name, generator_name):
        """ Binds the next value for generator_name to variable_name and return value used """
        str_gen_name = str(generator_name)
        str_name = str(variable_name)
        val = next(self.generators[str_gen_name])

        prev = self.variables.get(str_name)
        if prev != val:
            self.variables[str_name] = val
            self.mod_count = self.mod_count + 1
            # Logging is /expensive/
        return val

    def get_values(self):
        """ returns variables list """
        return self.variables

    def get_value(self, variable_name):
        """ Get bound variable value, or return none if not set """
        return self.variables.get(str(variable_name))

    def get_generators(self):
        """ returns generators list """
        return self.generators

    def get_generator(self, generator_name):
        """ returns generator name from list """
        return self.generators.get(str(generator_name))

    def __init__(self):
        self.variables = dict()
        self.generators = dict()
