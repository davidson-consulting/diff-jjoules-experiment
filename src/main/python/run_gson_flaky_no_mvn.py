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

def run_test_command(PATH_V1, PATH_V2, nb_iteration, output_path, tests_to_execute):
    classpath = '~/workspace/test-runner/target/test-runner-2.3.0-SNAPSHOT-jar-with-dependencies.jar:' + read_classpath(PATH_V1)
    classpath = classpath + ':' + PATH_V1 + '/target/classes/' + ':' + PATH_V1 + '/target/test-classes/'
    mkdir(output_path + '/v1/')
    for i in range(nb_iteration):
        print(i)
        v1_result_folder = output_path + '/v1/' + str(i)
        delete_directory(v1_result_folder)
        run_command(' '.join([
            'java', '-classpath',
            classpath,
            'eu.stamp_project.testrunner.runner.JUnit4Runner',
            '--class',
            ':'.join(tests_to_execute)
        ]))
        run_command('ls target/')
        copy_jjoules_result('.', v1_result_folder)

if __name__ == '__main__':

    selected_not_flaky_tests = [
        'com.google.gson.functional.CustomTypeAdaptersTest-testCustomAdapterInvokedForCollectionElementSerializationWithType',
        'com.google.gson.functional.MapTest-testMapSerializationWithIntegerKeys',
        'com.google.gson.functional.EnumTest-testEnumSubclass',
        'com.google.gson.functional.ExposeFieldsTest-testExposeAnnotationSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testDefaultDateSerializationUsingBuilder',
        'com.google.gson.functional.CustomSerializerTest-testSerializerReturnsNull',
        'com.google.gson.functional.CustomTypeAdaptersTest-testCustomTypeAdapterDoesNotAppliesToSubClasses',
        'com.google.gson.functional.ArrayTest-testArrayOfPrimitivesAsObjectsSerialization',
        'com.google.gson.functional.PrimitiveTest-testSmallValueForBigIntegerSerialization',
        'com.google.gson.MixedStreamTest-testWriteDoesNotMutateState',
        'com.google.gson.functional.PrettyPrintingTest-testMap',
        'com.google.gson.functional.NullObjectAndFieldTest-testCustomSerializationOfNulls',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testBitSetSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testBigDecimalFieldSerialization',
        'com.google.gson.functional.PrimitiveTest-testPrimitiveBooleanAutoboxedSerialization',
        'com.google.gson.functional.InheritanceTest-testBaseSerializedAsBaseWhenSpecifiedWithExplicitTypeForToJsonMethod',
        'com.google.gson.functional.ArrayTest-testEmptyArraySerialization',
        'com.google.gson.functional.RawSerializationTest-testTwoLevelParameterizedObject',
        'com.google.gson.functional.ObjectTest-testAnonymousLocalClassesSerialization',
        'com.google.gson.functional.PrimitiveTest-testLongAsStringSerialization',
        'com.google.gson.functional.CollectionTest-testWildcardCollectionField',
        'com.google.gson.GsonTypeAdapterTest-testTypeAdapterProperlyConvertsTypes'
    ]

    selected_not_flaky_tests = [
        'com.google.gson.functional.CollectionTest-testWildcardCollectionField',
        'com.google.gson.functional.CustomSerializerTest-testSerializerReturnsNull',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testBitSetSerialization',
        'com.google.gson.functional.EnumTest-testEnumSubclass',
        'com.google.gson.functional.ExposeFieldsTest-testExposeAnnotationSerialization',
        'com.google.gson.functional.InheritanceTest-testBaseSerializedAsBaseWhenSpecifiedWithExplicitTypeForToJsonMethod',
        'com.google.gson.functional.MapTest-testMapSerializationWithIntegerKeys',
        'com.google.gson.functional.NullObjectAndFieldTest-testCustomSerializationOfNulls',
        'com.google.gson.functional.ObjectTest-testAnonymousLocalClassesSerialization',
        'com.google.gson.functional.PrettyPrintingTest-testMap',
        'com.google.gson.functional.PrimitiveTest-testPrimitiveBooleanAutoboxedSerialization',
        'com.google.gson.functional.RawSerializationTest-testTwoLevelParameterizedObject',
        'com.google.gson.GsonTypeAdapterTest-testTypeAdapterProperlyConvertsTypes',
        'com.google.gson.MixedStreamTest-testWriteDoesNotMutateState',
    ]

    selected_flaky_tests = [
        'com.google.gson.functional.DefaultTypeAdaptersTest-testDefaultDateDeserializationUsingBuilder',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testStringBuilderSerialization',
        'com.google.gson.functional.CircularReferenceTest-testSelfReferenceArrayFieldSerialization',
        'com.google.gson.functional.NullObjectAndFieldTest-testTopLevelNullObjectSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testDefaultDateSerialization',
        'com.google.gson.functional.ParameterizedTypesTest-testParameterizedTypeWithVariableTypeDeserialization',
        'com.google.gson.functional.CustomDeserializerTest-testDefaultConstructorNotCalledOnField',
        'com.google.gson.functional.CustomSerializerTest-testBaseClassSerializerInvokedForBaseClassFieldsHoldingSubClassInstances',
        'com.google.gson.functional.CollectionTest-testLinkedListSerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testBitSetDeserialization',
        'com.google.gson.functional.ParameterizedTypesTest-testParameterizedTypesSerialization',
        'com.google.gson.functional.CustomTypeAdaptersTest-testCustomSerializers',
        'com.google.gson.functional.ObjectTest-testNullFieldsSerialization',
        'com.google.gson.functional.PrimitiveTest-testFloatInfinitySerialization',
        'com.google.gson.functional.StringTest-testEscapingQuotesInStringSerialization',
        'com.google.gson.functional.CollectionTest-testQueueSerialization',
        'com.google.gson.functional.UncategorizedTest-testObjectEqualButNotSameSerialization',
        'com.google.gson.functional.PrimitiveTest-testReallyLongValuesSerialization',
        'com.google.gson.functional.ArrayTest-testTopLevelArrayOfIntsSerialization', 
        'com.google.gson.functional.NullObjectAndFieldTest-testPrintPrintingArraysWithNulls',
        'com.google.gson.functional.PrimitiveTest-testPrimitiveLongAutoboxedSerialization',
        'com.google.gson.functional.ParameterizedTypesTest-testParameterizedTypesWithWriterSerialization',
        'com.google.gson.DefaultMapJsonSerializerTest-testNonEmptyMapSerialization',
        'com.google.gson.functional.InheritanceTest-testBaseSerializedAsBaseWhenSpecifiedWithExplicitType,'
        'com.google.gson.functional.ParameterizedTypesTest-testVariableTypeFieldsAndGenericArraysSerialization',
        'com.google.gson.functional.VersioningTest-testVersionedGsonMixingSinceAndUntilSerialization',
        'com.google.gson.functional.SecurityTest-testNonExecutableJsonSerialization',
        'com.google.gson.functional.NamingPolicyTest-testGsonWithSerializedNameFieldNamingPolicySerialization',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testDefaultJavaSqlDateSerialization',
        'com.google.gson.functional.ReadersWritersTest-testReadWriteTwoObjects',
        'com.google.gson.functional.DefaultTypeAdaptersTest-testDefaultGregorianCalendarSerialization',
        'com.google.gson.functional.CustomSerializerTest-testSubClassSerializerInvokedForBaseClassFieldsHoldingSubClassInstances',
        'com.google.gson.functional.PrettyPrintingTest-testMultipleArrays',
        'com.google.gson.functional.CircularReferenceTest-testSelfReferenceCustomHandlerSerialization',
        'com.google.gson.functional.MapTest-testGeneralMapField',
        'com.google.gson.MixedStreamTest-testWriteLenient',
    ]

    PATH_V1 = '/tmp/v1/'
    PATH_V2 = '/tmp/v2/'
    repo_url = 'https://github.com/google/gson.git'
    commit_sha_v1 = 'd26c8189182fa96691cc8e0d0f312469ee0627bb'
    commit_sha_v2 = '364de8061173b4b91f4477a55059f68e765fc3d1'

    delete_directory(PATH_V1)
    delete_directory(PATH_V2)
    clone(repo_url, PATH_V1)
    clone(repo_url, PATH_V2)

    PATH_V1 = '/tmp/v1/gson'
    PATH_V2 = '/tmp/v2/gson'
   
    path_to_not_flaky_csv = PATH_V1 + '/' + 'not_flaky_tests.csv'
    path_to_flaky_csv = PATH_V1 + '/' + 'flaky_tests.csv'

    selected_not_flaky_tests_value = write_test_list_in_csv(selected_not_flaky_tests, path_to_not_flaky_csv)
    selected_flaky_tests_value = write_test_list_in_csv(selected_flaky_tests, path_to_flaky_csv)

    reset_hard(commit_sha_v1, PATH_V1)
    reset_hard(commit_sha_v2, PATH_V2)
    delete_module_info_java(PATH_V1)
    delete_module_info_java(PATH_V2)

    nb_duplication = '-Dnb-duplication=1000'

    run_mvn_clean_test_build_cp(PATH_V2)
    run_command(
         ' '.join([
            MVN_CMD,
            PATH_V1 + POM_FILE,
            MVN_CLEAN_GOAL,
            MVN_TEST,
            MVN_DATE_FORMAT_OPT,
            MVN_SKIP_TEST,
            BUILD_CLASSPATH_GOAL,
            OPT_OUTPUT_CP_FILE,
            CMD_DIFF_CLASS_INSTRUMENT,
            nb_duplication,
            OPT_TEST_LISTS + 'not_flaky_tests.csv',
            OPT_PATH_DIR_SECOND_VERSION + PATH_V2,
            OPT_CP_V2,
            OPT_CP_V1,
        ])
    )

    run_mvn_clean_test_build_cp(PATH_V1)
    run_test_command(PATH_V1, PATH_V2, 100, 'data/output/gson_flaky/794_d26c81_364de8/', selected_not_flaky_tests_value)