""" """


def words_to_snake_case(s):
    components = s.split(' ')
    return '_'.join(x.lower() for x in components)
