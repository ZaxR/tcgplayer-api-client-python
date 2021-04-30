# Python imports
import re


""" Basic utility functions """


#####################################################################################
# STRING FUNCTIONS
#####################################################################################

def camel_to_snake_case(camel_str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', camel_str).lower()

def snake_to_camel_case(snake_str):
    components = snake_str.split('_')
    # We capitalize the first letter of each component except the first one
    # with the 'capitalize' method and join them together.
    return components[0] + ''.join(x.capitalize() for x in components[1:])

def words_to_snake_case(s):
    components = s.split(' ')
    return '_'.join(x.lower() for x in components)
