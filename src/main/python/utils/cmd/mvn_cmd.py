import os

def run_cmd(command):
    print(command)
    return os.system(command)

MVN_CMD_WITH_SKIPS_F = 'mvn -Drat.skip=true -Djacoco.skip=true -Danimal.sniffer.skip=true -f '
POM_FILE = '/pom.xml'
CLEAN_GOAL = 'clean'
INSTALL_GOAL = 'install'
TEST_GOAL = 'test'
SKIP_TESTS = '-DskipTests'
LOG_FILE_OPT = '--log-file'
OPT_TEST = '-Dtest='

def mvn_install_skip_test_build_classpath(path):
    return run_cmd(' '.join([
        MVN_CMD_WITH_SKIPS_F,
        path + POM_FILE,
        CLEAN_GOAL,
        INSTALL_GOAL,
        SKIP_TESTS,
        'dependency:build-classpath',
        '-Dmdep.outputFile=classpath'
    ]))

def mvn_clean_test_skip_test(path):
    return run_cmd(' '.join([
        MVN_CMD_WITH_SKIPS_F,
        path + POM_FILE,
        CLEAN_GOAL,
        TEST_GOAL,
        SKIP_TESTS
    ]))

CMD_DIFF_TEST_SELECTION = 'eu.stamp-project:dspot-diff-test-selection:3.1.1-SNAPSHOT:list'
OPT_PATH_DIR_SECOND_VERSION = '-Dpath-dir-second-version='

def mvn_diff_test_selection(path_first_version, path_second_version, output_path_file):
    return run_cmd(
         ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            LOG_FILE_OPT,
            output_path_file,
            CLEAN_GOAL,
            CMD_DIFF_TEST_SELECTION,
            '-Dpath-dir-second-version=' + path_second_version,
        ])
    )

CMD_DIFF_INSTRUMENT = 'fr.davidson:diff-jjoules:instrument'
OPT_CP_V2 = '-Dclasspath-path-v2=classpath'
OPT_CP_V1 = '-Dclasspath-path-v1=classpath'
OPT_VALUE_TEST_LISTS = '-Dtests-list=testsThatExecuteTheChange.csv'

def mvn_diff_jjoules_instrument(path_v1, path_v2, log_path):
    return run_cmd(
         ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_v1 + POM_FILE,
            CLEAN_GOAL,
            LOG_FILE_OPT,
            log_path,
            TEST_GOAL,
            SKIP_TESTS,
            CMD_DIFF_INSTRUMENT,
            OPT_VALUE_TEST_LISTS,
            '-Dpath-dir-second-version=' + path_v2,
            OPT_CP_V2,
            OPT_CP_V1,
        ])
    )

def mvn_clean_test(path, tests_to_execute, log_path):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path + POM_FILE,
            LOG_FILE_OPT,
            log_path,
            CLEAN_GOAL,
            TEST_GOAL,
            OPT_TEST + ','.join([test + '#' + '+'.join(tests_to_execute[test]) for test in tests_to_execute]),
        ])
    )

def mvn_test(path, tests_to_execute, log_path):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path + POM_FILE,
            LOG_FILE_OPT,
            log_path,
            TEST_GOAL,
            OPT_TEST + ','.join([test + '#' + '+'.join(tests_to_execute[test]) for test in tests_to_execute]),
        ])
    )