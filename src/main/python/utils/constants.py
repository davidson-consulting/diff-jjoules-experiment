V1 = 'v1'
V2 = 'v2'

PATH_V1 = '/tmp/' + V1
PATH_V2 = '/tmp/' + V2

COMMITS_FILE_PATH = 'input'
MODULE_FILE_PATH = 'module'

VALUE_TEST_LISTS = 'testsThatExecuteTheChange.csv'

DIRECTORIES_TO_COPY = [
    'diff-jjoules',
]

FILES_TO_COPY = [
    'classpath',
    'srcpatch.diff',
    'logs',
#    'methodNames.csv',
    'testsThatExecuteTheChange_coverage.csv',
    'testsThatExecuteTheChange.csv'
]

FILES_TO_COPY_SUSPECT = [
    'TODO'
]

CONSIDERED_TEST_METHODS_JSON_FILE_NAME = '/consideredTestMethods.json'
DELTA_FILE_NAME = '/deltas.json'
DELTA_OMEGA_FILE_NAME = '/deltaOmega.json'
DIFF_JJOULES_SEC_JSON_FILE_NAME = '/diff_jjoules.json'

DATA_V1_JSON_FILE_NAME = '/data_v1.json'
DATA_V2_JSON_FILE_NAME = '/data_v2.json'

PACKAGE_KEY = 'package-0|uJ'
ENERGY_KEY = 'energy'
INSTR_KEY = 'instructions'
DURATIONS_KEY = 'durations'
DURATIONS_NS_KEY = 'duration|ns'
CYCLES_KEY = 'cycles'

PROJECTS = [
    'gson', 
    'jsoup', 
    'commons-io',
    'commons-lang',
    'mustache.java',
    'xwiki'
]


TEST_FILTERS = ['ALL', 'EMPTY_INTERSECTION', 'STUDENTS_T_TEST']
MARK_STRATEGIES = ['STRICT', 'AGGREGATE', 'CODE_COVERAGE', 'DIFF_COVERAGE']
COHEN_S_DS = ['0.20', '0.50', '0.80', '1.20']