import os
from shutil import copyfile, SameFileError, copytree, rmtree, move

POM_FILE = '/pom.xml'
JJOULED_POM_FILE = '/pom.xml'
# JJOULED_POM_FILE = '/pom_jjouled.xml'
MVN_CMD = 'mvn -Drat.skip=true -Djacoco.skip=true -Danimal.sniffer.skip=true -f '
MVN_CLEAN_GOAL = 'clean'
MVN_TEST = 'test'
OPT_TEST = '-Dtest='

MVN_LOG_OPT = '--log-file'

def print_to_file(text, filepath):
    with open(filepath, 'a') as file:
        file.write(str(text) + '\n')

def run_command(command):
    print(command)
    return os.system(command)

def delete_module_info_java(path):
    for dirName, subdirList, fileList in os.walk(path):
        for file in fileList:
            if file == 'module-info.java':
                delete_file(dirName + '/' + file)

def run_mvn_test(path, tests_to_execute, output_path_file, jjouled=False):
    return run_command(
        ' '.join([
            MVN_CMD,
            path + (JJOULED_POM_FILE if jjouled else POM_FILE),
            MVN_LOG_OPT,
            output_path_file,
            MVN_CLEAN_GOAL,
            MVN_TEST,
            OPT_TEST + ','.join([test + '#' + '+'.join(tests_to_execute[test]) for test in tests_to_execute]),
        ])
    )

CMD_DIFF_TEST_SELECTION = 'eu.stamp-project:dspot-diff-test-selection:3.1.1-SNAPSHOT:list'
CMD_DIFF_INSTRUMENT = 'fr.davidson:diff-jjoules:instrument'
OPT_PATH_DIR_SECOND_VERSION = '-Dpath-dir-second-version='
OPT_TEST_LISTS = '-Dtests-list='
VALUE_TEST_LISTS = 'testsThatExecuteTheChange.csv'

def run_mvn_diff_select(path_first_version, path_second_version, output_path_file):
    return run_command(
         ' '.join([
            MVN_CMD,
            path_first_version + POM_FILE,
            MVN_LOG_OPT,
            output_path_file,
            MVN_CLEAN_GOAL,
            CMD_DIFF_TEST_SELECTION,
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
        ])
    )

def run_mvn_instrument(path_first_version, path_second_version):
    return run_command(
         ' '.join([
            MVN_CMD,
            path_first_version + POM_FILE,
            CMD_DIFF_INSTRUMENT,
            OPT_TEST_LISTS + path_first_version + '/' + VALUE_TEST_LISTS,
            OPT_PATH_DIR_SECOND_VERSION + path_second_version
        ])
    )

MVN_INSTALL = 'install'
MVN_SKIP_TEST = '-DskipTests'

def run_mvn_clean_test(path):
    return run_command(
        ' '.join([
            MVN_CMD,
            path + POM_FILE,
            MVN_CLEAN_GOAL,
            MVN_INSTALL,
            MVN_SKIP_TEST,
        ])
    )

BUILD_CLASSPATH_GOAL = 'dependency:build-classpath'
OPT_OUTPUT_CP_FILE = '-Dmdep.outputFile=classpath'

OPT_CP_V2 = '-Dclasspath-path-v2=classpath'
OPT_CP_V1 = '-Dclasspath-path-v1=classpath'

def run_mvn_clean_test_build_cp(path):
    return run_command(
        ' '.join([
            MVN_CMD,
            path + POM_FILE,
            MVN_CLEAN_GOAL,
            MVN_TEST,
            MVN_SKIP_TEST,
             BUILD_CLASSPATH_GOAL,
            OPT_OUTPUT_CP_FILE,
        ])
    )

def run_mvn_build_classpath_and_instrument(path_first_version, path_second_version, output_path_file):
    return run_command(
         ' '.join([
            MVN_CMD,
            path_first_version + POM_FILE,
            MVN_CLEAN_GOAL,
            MVN_LOG_OPT,
            output_path_file,
            MVN_TEST,
            MVN_SKIP_TEST,
            BUILD_CLASSPATH_GOAL,
            OPT_OUTPUT_CP_FILE,
            CMD_DIFF_INSTRUMENT,
            #OPT_TEST_LISTS + path_first_version + '/' + VALUE_TEST_LISTS,
            OPT_TEST_LISTS + VALUE_TEST_LISTS,
            OPT_PATH_DIR_SECOND_VERSION + path_second_version,
            OPT_CP_V2,
            OPT_CP_V1,
        ])
    )

JJOULES_REPORT_FOLDER = 'jjoules-reports'

def move_directory(src_dir, dst):
    print('move', src_dir, 'to', dst)
    move(src_dir, dst)

def copy_jjoules_result(src_dir, dst):
    for dirName, subdirList, fileList in os.walk(src_dir):
        for subdir in subdirList:
            if subdir == JJOULES_REPORT_FOLDER:
                print('copy dir', dirName + '/' + subdir,  dst)
                copy_directory(dirName + '/' + subdir, dst)

def copy(src, dst):
    try:
        copyfile(src, dst)
    except (SameFileError):
       print('src and dst same file... passing', src)

def copy_directory(src, dst):
    try:
        copytree(src, dst)
    except (SameFileError):
       print('src and dst same file... passing', src)

def create_if_does_not_exist(directory):
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return directory

def delete_directory(directory):
    if os.path.isdir(directory):
        rmtree(directory)

def delete_file(file_path):
    try:
        os.remove(file_path)
    except (FileNotFoundError):
        print(file_path, 'does not exist. Pass...')

CMD_GIT = 'git'
CMD_GIT_CLONE = CMD_GIT + ' clone'

def clone(url, folder_path):
    run_command(
        ' '.join([
            CMD_GIT_CLONE,
            url,
            folder_path
        ])
    )

GIT_C = '-C'
LOG_CMD = 'log --pretty=format:"%H" >>'

def git_log(path_project, output_file_path):
    run_command(
        ' '.join([
            CMD_GIT,
            GIT_C,
            path_project,
            LOG_CMD,
            output_file_path
        ])
    )

def mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print('pass...')


CMD_GIT_RESET_HARD = 'git reset --hard'

def reset_hard(commitsha, git_repo_path):
    cwd = os.getcwd()
    os.chdir(git_repo_path)
    run_command(
        ' '.join([
            CMD_GIT_RESET_HARD,
            commitsha,
        ])
    )
    os.chdir(cwd)

def zip_folder(path_to_folder):
    run_command(' '.join([
            'zip',
            '-r',
            path_to_folder + '.zip',
            path_to_folder
        ]
    ))

def read_module_name(input_path):
    with open(input_path + '/module') as module_file:
        return module_file.readlines()[0]