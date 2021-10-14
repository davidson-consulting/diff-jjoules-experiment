import os

def run_cmd(command):
    print(command)
    return os.system(command)

MVN_CMD_WITH_SKIPS_F = 'mvn -Drat.skip=true -Djacoco.skip=true -Danimal.sniffer.skip=true -Dproguard.skip=true -f '
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
        MVN_DATE_FORMAT_OPT if must_use_date_format else ''
    ]))

CMD_DIFF_TEST_SELECTION = 'eu.stamp-project:dspot-diff-test-selection:3.1.1-SNAPSHOT:list'

GOAL_DIFF_JJOULES_DIFF_JJOULES = 'fr.davidson:diff-jjoules:diff-jjoules'
OPT_PATH_DIR_SECOND_VERSION = '-Dpath-dir-second-version='
OPT_SUSPECT = "-Dsuspect="
OPT_REPO_V1 = '-Dpath-repo-v1='
OPT_REPO_V2 = '-Dpath-repo-v2='
OPT_NO_REPORT = '-Dreport=NONE'
OPT_ITERATION = '-Diterations='

def mvn_diff_jjoules_no_suspect(
    path_first_repository, path_first_version, 
    path_second_repository, path_second_version,
    output_path_file,
    must_use_date_format=False):
    return run_cmd(
        ' '.join([
            MVN_CMD_WITH_SKIPS_F,
            path_first_version + POM_FILE,
            LOG_FILE_OPT,
            output_path_file,
            MVN_DATE_FORMAT_OPT if must_use_date_format else ''
            CLEAN_GOAL,
            GOAL_DIFF_JJOULES_DIFF_JJOULES,
            OPT_SUSPECT + 'false',
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
            OPT_REPO_V1 + path_first_repository,
            OPT_REPO_V2 + path_second_repository,
            OPT_NO_REPORT,
            OPT_ITERATION + '100'
        ])
    )
