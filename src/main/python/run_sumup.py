import sys
from utils.cmd_utils import *
import csv

def write_test_list_in_csv(test_list, path_to_csv):
    test_method_per_test_class = {}
    for test_name in test_list:
        split = test_name.split('-')
        test_class = split[0]
        test_method = split[1]
        if not test_class in test_method_per_test_class:
            test_method_per_test_class[test_class] = []
        test_method_per_test_class[test_class].append(test_method)

    tests_values = []
    with open(path_to_csv, mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        for test_class in test_method_per_test_class:
            writer.writerow([test_class, ';'.join(test_method_per_test_class[test_class])])
            for test_method in test_method_per_test_class[test_class]:
                tests_values.append(test_class + '_' + test_method)
    return tests_values

def read_classpath(path):
    with open(path + '/classpath') as classpath_file:
        classpath = classpath_file.read()
    return classpath

def run_tests(PATH_V1, nb_iteration, output_path, tests_to_execute):
    mkdir(output_path)
    for i in range(nb_iteration):
        print(i)
        result_folder = output_path + '/' + str(i)
        delete_directory(result_folder)
        run_mvn_test_class(PATH_V1, tests_to_execute, result_folder + '/mvn_test.log', True)
        copy_jjoules_result(PATH_V1, result_folder)

def run_test_command(PATH_V1, nb_iteration, output_path, tests_to_execute):
    classpath = '~/workspace/test-runner/target/test-runner-2.3.0-SNAPSHOT-jar-with-dependencies.jar:' + read_classpath(PATH_V1)
    classpath = classpath + ':' + PATH_V1 + '/target/classes/' + ':' + PATH_V1 + '/target/test-classes/'
    mkdir(output_path)
    for i in range(nb_iteration):
        print(i)
        result_folder = output_path + '/' + str(i)
        delete_directory(result_folder)
        run_command(' '.join([
            'java',
            '-Djava.locale.providers=COMPAT,CLDR,SPI',
            '-classpath',
            classpath,
            'eu.stamp_project.testrunner.runner.JUnit4Runner',
            '--class',
            ':'.join(tests_to_execute)
        ]))
        copy_jjoules_result('.', result_folder)

def get_test_list(duplication):
    test_list = [
        'com.google.gson.functional.CollectionTest_testWildcardCollectionField',
        'com.google.gson.functional.CustomSerializerTest_testSerializerReturnsNull',
        'com.google.gson.functional.DefaultTypeAdaptersTest_testBitSetSerialization',
        'com.google.gson.functional.EnumTest_testEnumSubclass',
        'com.google.gson.functional.ExposeFieldsTest_testExposeAnnotationSerialization',
        'com.google.gson.functional.InheritanceTest_testBaseSerializedAsBaseWhenSpecifiedWithExplicitTypeForToJsonMethod',
        'com.google.gson.functional.MapTest_testMapSerializationWithIntegerKeys',
        'com.google.gson.functional.NullObjectAndFieldTest_testCustomSerializationOfNulls',
        'com.google.gson.functional.ObjectTest_testAnonymousLocalClassesSerialization',
        'com.google.gson.functional.PrettyPrintingTest_testMap',
        'com.google.gson.functional.PrimitiveTest_testPrimitiveBooleanAutoboxedSerialization',
        'com.google.gson.functional.RawSerializationTest_testTwoLevelParameterizedObject',
        'com.google.gson.GsonTypeAdapterTest_testTypeAdapterProperlyConvertsTypes',
        'com.google.gson.MixedStreamTest_testWriteDoesNotMutateState',
        'com.google.gson.functional.ArrayTest_testTopLevelArrayOfIntsSerialization',
        'com.google.gson.functional.CustomDeserializerTest_testDefaultConstructorNotCalledOnField',
        'com.google.gson.functional.CustomTypeAdaptersTest_testCustomSerializers',
        'com.google.gson.functional.DefaultTypeAdaptersTest_testBitSetDeserialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest_testDefaultDateSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest_testDefaultJavaSqlDateSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest_testStringBuilderSerialization',
        'com.google.gson.functional.MapTest_testGeneralMapField',
        'com.google.gson.functional.NamingPolicyTest_testGsonWithSerializedNameFieldNamingPolicySerialization',
        'com.google.gson.functional.ObjectTest_testNullFieldsSerialization',
        'com.google.gson.functional.ParameterizedTypesTest_testParameterizedTypesSerialization',
        'com.google.gson.functional.PrettyPrintingTest_testMultipleArrays',
        'com.google.gson.functional.PrimitiveTest_testReallyLongValuesSerialization',
        'com.google.gson.functional.ReadersWritersTest_testReadWriteTwoObjects',
        'com.google.gson.functional.SecurityTest_testNonExecutableJsonSerialization',
        'com.google.gson.functional.StringTest_testEscapingQuotesInStringSerialization',
        'com.google.gson.functional.UncategorizedTest_testObjectEqualButNotSameSerialization',
        'com.google.gson.functional.VersioningTest_testVersionedGsonMixingSinceAndUntilSerialization',
        'com.google.gson.DefaultMapJsonSerializerTest_testNonEmptyMapSerialization',
        'com.google.gson.MixedStreamTest_testWriteLenient'
    ]
    return [test + '_' + duplication for test in test_list]

def run_sumup(PATH_V1, nb_iteration, output_path):
    
    # test_list_10 = get_test_list('10')
    # test_list_100 = get_test_list('100')
    # test_list_1000 = get_test_list('1000')
    test_list_2000 = get_test_list('2000')

    #run_test_command(PATH_V1, nb_iteration, output_path + '_java_10', test_list_10)
    #run_test_command(PATH_V1, nb_iteration, output_path + '_java_100', test_list_100)
    #run_test_command(PATH_V1, nb_iteration, output_path + '_java_1000', test_list_1000)

    #run_tests(PATH_V1, nb_iteration, output_path + '_mvn_10', test_list_10)
    #run_tests(PATH_V1, nb_iteration, output_path + '_mvn_100', test_list_100)
    #run_tests(PATH_V1, nb_iteration, output_path + '_mvn_1000', test_list_1000)
    run_tests(PATH_V1, nb_iteration, output_path + '_mvn_2000', test_list_2000)

if __name__ == '__main__':

    PATH_V1 = '/tmp/v1/'
    repo_url = 'https://github.com/danglotb/gson.git'
    delete_directory(PATH_V1)
    clone(repo_url, PATH_V1)

    #commit_sha = '83c0c1d1852fab6ea636acb7c596c0fcb78a80c3'
    commit_sha = '1a4942c624b3ddcd3d3b2e79ef07326afd071ab1'
    #commit_sha = 'af8a45aecd5132207b8beda58cf3f0e7ae158129'
    PATH_V1 = '/tmp/v1/gson'
    reset_hard(commit_sha, PATH_V1)
    delete_module_info_java(PATH_V1)

    run_mvn_clean_test_build_cp(PATH_V1)
    run_sumup(PATH_V1, 100, 'data/output/sumup')