import sys
from utils.cmd_utils import *
from utils.run_for_project_args import *
import csv
import datetime
import time
import os

def write_test_list_in_csv(test_list, path_to_csv):
    test_method_per_test_class = {}
    for test_name in test_list:
        split = test_name.split('_')
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

if __name__ == '__main__':

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
    repo_url = 'https://github.com/danglotb/gson.git'
    commit_sha = '83c0c1d1852fab6ea636acb7c596c0fcb78a80c3'
    #commit_sha = 'af8a45aecd5132207b8beda58cf3f0e7ae158129'

    PATH_V1 = '/tmp/v1/'
    delete_directory(PATH_V1)
    clone(repo_url, PATH_V1)
    PATH_V2 = '/tmp/v2/'
    delete_directory(PATH_V2)
    clone(repo_url, PATH_V2)
   
    PATH_V1 = '/tmp/v1/gson'
    PATH_V2 = '/tmp/v2/gson'
    reset_hard(commit_sha, PATH_V1)
    delete_module_info_java(PATH_V1)
    reset_hard(commit_sha, PATH_V2)
    delete_module_info_java(PATH_V2)

    write_test_list_in_csv(test_list, PATH_V1 + '/testsThatExecuteTheChange.csv')

    run_mvn_clean_test_build_cp(PATH_V2)
    run_mvn_build_classpath_and_instrument_class(PATH_V1, PATH_V2, '/dev/null')
