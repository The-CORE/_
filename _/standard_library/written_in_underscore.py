import _


# List = _.smart_compile('_/standard_library/written_in_underscore/list._', \
#     compiling_underscore_standard_library=True).run()['List']

six = _.smart_compile('_/standard_library/written_in_underscore/six._', \
    compiling_underscore_standard_library=True).run()['six']

WRITTEN_IN_UNDERSCORE = {
    'six': six
    #'List': List
}
