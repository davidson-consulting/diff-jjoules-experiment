import os

def run_cmd(command):
    print(command)
    return os.system(command)

MVN_CMD_WITH_SKIPS_F = 'mvn -Drat.skip=true -Djacoco.skip=true -Danimal.sniffer.skip=true -Dproguard.skip=true -Dmaven.javadoc.skip=true -Dlicense.skip=true -f '
POM_FILE = '/pom.xml'
MVN_DATE_FORMAT_OPT = '-Djava.locale.providers=COMPAT,CLDR,SPI'

CLEAN_GOAL = 'clean'
INSTALL_GOAL = 'install'
TEST_GOAL = 'test'
SKIP_TESTS = '-DskipTests'
LOG_FILE_OPT = '--log-file'
OPT_TEST = '-Dtest='

def mvn_install_skip_test_build_classpath(path, must_use_date_format=False):
    return run_cmd(' '.join([
        MVN_CMD_WITH_SKIPS_F,
        path + POM_FILE,
        CLEAN_GOAL,
        INSTALL_GOAL,
        SKIP_TESTS,
        'dependency:build-classpath',
        '-Dmdep.outputFile=classpath',
        '--fail-never',
        '-U',
        MVN_DATE_FORMAT_OPT if must_use_date_format else ''
    ]))

CMD_DIFF_TEST_SELECTION = 'eu.stamp-project:dspot-diff-test-selection:3.1.1-SNAPSHOT:list'

GOAL_DIFF_JJOULES_DIFF_JJOULES = 'fr.davidson:diff-jjoules-maven:diff-jjoules'
GOAL_DIFF_JJOULES_MARK = 'fr.davidson:diff-jjoules-maven:mark'
OPT_PATH_DIR_SECOND_VERSION = '-Dpath-dir-second-version='
OPT_SUSPECT = "-Dsuspect="
OPT_MARK = '-Dmark='
OPT_REPO_V1 = '-Dpath-repo-v1='
OPT_REPO_V2 = '-Dpath-repo-v2='
OPT_NO_REPORT = '-Dreport=NONE'
OPT_ITERATION = '-Diterations='
OPT_MEASURE = '-Dmeasure'

def mvn_diff_jjoules_no_mark(
    path_first_repository, path_first_version, 
    path_second_repository, path_second_version,
    output_path_file,
    must_use_date_format=False):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            #LOG_FILE_OPT,
            #output_path_file,
            MVN_DATE_FORMAT_OPT if must_use_date_format else '',
            CLEAN_GOAL,
            GOAL_DIFF_JJOULES_DIFF_JJOULES,
            OPT_MARK + 'false',
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
            OPT_REPO_V1 + path_first_repository,
            OPT_REPO_V2 + path_second_repository,
            OPT_NO_REPORT,
            OPT_ITERATION + '2',
            OPT_MEASURE,
            '>' + output_path_file,
            '2>&1'
        ])
    )

GOAL_DIFF_JJOULES_MUTATE = 'fr.davidson:diff-jjoules-mutation:mutate'
OPT_METHOD_LIST_PATH = '-Dmethod-list-path='
OPT_CONSUMPTION = '-Dconsumption='

def mvn_diff_jjoules_mutate(path_version, path_to_method_names, energy_to_consume):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_version + POM_FILE,
            CLEAN_GOAL,
            TEST_GOAL,
            SKIP_TESTS,
            GOAL_DIFF_JJOULES_MUTATE,
            OPT_METHOD_LIST_PATH + path_to_method_names,
            OPT_CONSUMPTION + energy_to_consume,
        ])
    )

def mvn_diff_jjoules_with_mark_no_suspect(
    path_first_repository, path_first_version, 
    path_second_repository, path_second_version,
    output_path_file,
    must_use_date_format=False):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            #LOG_FILE_OPT,
            #output_path_file,
            MVN_DATE_FORMAT_OPT if must_use_date_format else '',
            CLEAN_GOAL,
            GOAL_DIFF_JJOULES_DIFF_JJOULES,
            OPT_MARK + 'true',
            OPT_SUSPECT + 'false',
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
            OPT_REPO_V1 + path_first_repository,
            OPT_REPO_V2 + path_second_repository,
            OPT_NO_REPORT,
            OPT_ITERATION + '100',
            OPT_MEASURE,
            #'>' + output_path_file,
            #'2>&1'
        ])
    )

OPT_DATA_V1 = '-Dpath-data-v1='
OPT_DATA_V2 = '-Dpath-data-v2='
OPT_TEST_FILTER = '-Dtest-filter='
OPT_MARK_STRATEGY = '-Dmark-strategy='
OPT_DELTAS_PATH = '-Dpath-deltas='
OPT_COHEN_S_D = '-Dcohen-s-d='
OPT_PATH_COVERAGE_V1 = '-Dpath-coverage-v1='
OPT_PATH_COVERAGE_V2 = '-Dpath-coverage-v2='

def mvn_diff_jjoules_mark(
    path_first_repository,
    path_first_version, 
    path_second_repository,
    path_second_version,
    output_path_file, 
    deltas_json_path,
    path_data_v1,
    path_data_v2,
    test_filter,
    mark_strategy,
    cohen_s_d,
    path_coverage_v1 = '',
    path_coverage_v2 = '',
    ):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            #LOG_FILE_OPT,
            #output_path_file,
            GOAL_DIFF_JJOULES_MARK,
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
            OPT_REPO_V1 + path_first_repository,
            OPT_REPO_V2 + path_second_repository,
            OPT_NO_REPORT,
            OPT_DELTAS_PATH + '\'' + deltas_json_path + '\'',
            OPT_DATA_V1 + '\'' + path_data_v1 + '\'',
            OPT_DATA_V2 + '\'' + path_data_v2 + '\'',
            OPT_TEST_FILTER + test_filter,
            OPT_MARK_STRATEGY + mark_strategy,
            OPT_COHEN_S_D + cohen_s_d,
            '' if path_coverage_v1 == '' else OPT_PATH_COVERAGE_V1 + path_coverage_v1,
            '' if path_coverage_v2 == '' else OPT_PATH_COVERAGE_V2 + path_coverage_v2
        ])
    )

SETUP_CLOVER_GOAL = 'org.openclover:clover-maven-plugin:4.4.1:setup'
CLOVER_CLOVER_GOAL = 'org.openclover:clover-maven-plugin:4.4.1:clover'

def mvn_clover(path_first_version):
     return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            '-Dmaven.test.failure.ignore=true',
            '--fail-never',
            CLEAN_GOAL,
            SETUP_CLOVER_GOAL,
            TEST_GOAL,
            CLOVER_CLOVER_GOAL
        ])
    )
     
def mvn_clover_instr(path_first_version):
     return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            CLEAN_GOAL,
            SETUP_CLOVER_GOAL,
            '-Dmaven.clover.excludesList=org/apache/commons/lang3/function/Objects.java'
        ])
    )

GOAL_DIFF_JJOULES_COVERAGE = 'fr.davidson:diff-jjoules-maven:coverage'

def mvn_diff_jjoules_coverage(path_first_version):
     return run_cmd(' '.join([
        MVN_CMD_WITH_SKIPS_F,
        path_first_version + POM_FILE,
        #CLEAN_GOAL,
        #INSTALL_GOAL,
        TEST_GOAL,
        'dependency:build-classpath',
        '-Dmdep.outputFile=classpath',
        GOAL_DIFF_JJOULES_COVERAGE
    ]))