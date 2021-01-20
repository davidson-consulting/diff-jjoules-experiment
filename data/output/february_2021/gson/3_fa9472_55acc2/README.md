# gson 55acc2


https://github.com/google/gson/commit/55acc2



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)

![](./gson_delta_energy_1_v.png)

![](./gson_delta_energy_2_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 173950 | 175719 | 1769 | 24069.98 | 13.84 | 16541.24 | 9.41 |
| 1 | 162414 | 165344 | 2930 | 21271.61 | 13.10 | 30012.75 | 18.15 |
| 2 | 358031 | 352599 | -5432 | 37401.13 | 10.45 | 29414.37 | 8.34 |
| 3 | 371703 | 189087 | -182616 | 184199.05 | 49.56 | 148260.00 | 78.41 |
| 4 | 265563 | 290405 | 24842 | 32732.55 | 12.33 | 26573.71 | 9.15 |
| 5 | 252013 | 263000 | 10987 | 55173.61 | 21.89 | 28409.93 | 10.80 |
| 6 | 932492 | 875364 | -57128 | 83424.62 | 8.95 | 63661.89 | 7.27 |
| 7 | 343261 | 316405 | -26856 | 47528.87 | 13.85 | 40878.27 | 12.92 |
| 8 | 413879 | 415526 | 1647 | 37820.32 | 9.14 | 31088.79 | 7.48 |
| 9 | 221130 | 203796 | -17334 | 19990.22 | 9.04 | 21343.94 | 10.47 |
| 10 | 186828 | 220947 | 34119 | 35463.66 | 18.98 | 36532.45 | 16.53 |
| 11 | 392516 | 349059 | -43457 | 111472.84 | 28.40 | 46439.21 | 13.30 |
| 12 | 734373 | 716917 | -17456 | 76898.26 | 10.47 | 51746.97 | 7.22 |
| 13 | 348448 | 339781 | -8667 | 47236.27 | 13.56 | 53428.61 | 15.72 |
| 14 | 519102 | 538023 | 18921 | 59394.15 | 11.44 | 54562.46 | 10.14 |
| 15 | 138305 | 137084 | -1221 | 15026.54 | 10.86 | 24038.19 | 17.54 |
| 16 | 1210141 | 1193235 | -16906 | 115375.40 | 9.53 | 93285.22 | 7.82 |
| 17 | 180359 | 171691 | -8668 | 27302.02 | 15.14 | 25127.60 | 14.64 |
| 18 | 154235 | 147644 | -6591 | 29508.60 | 19.13 | 53938.98 | 36.53 |
| 19 | 412231 | 408934 | -3297 | 58634.75 | 14.22 | 42240.32 | 10.33 |
| 20 | 130065 | 127075 | -2990 | 30394.51 | 23.37 | 29096.62 | 22.90 |
| 21 | 198425 | 194580 | -3845 | 23421.31 | 11.80 | 23821.40 | 12.24 |
| 22 | 164001 | 155029 | -8972 | 27867.09 | 16.99 | 29547.33 | 19.06 |
| 23 | 386413 | 353088 | -33325 | 26902.82 | 6.96 | 34381.42 | 9.74 |
| 24 | 438232 | 380431 | -57801 | 40019.97 | 9.13 | 44635.53 | 11.73 |
| 25 | 238891 | 244811 | 5920 | 18838.37 | 7.89 | 40808.16 | 16.67 |
| 26 | 648558 | 614562 | -33996 | 73291.50 | 11.30 | 57921.07 | 9.42 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.functional.InheritanceTest | testBaseSerializedAsBaseWhenSpecifiedWithExplicitType |
| 1 | com.google.gson.functional.InheritanceTest | testBaseSerializedAsSubWhenSpecifiedWithExplicitType |
| 2 | com.google.gson.functional.InheritanceTest | testClassWithBaseArrayFieldSerialization |
| 3 | com.google.gson.functional.InheritanceTest | testBaseSerializedAsSub |
| 4 | com.google.gson.functional.InheritanceTest | testClassWithBaseCollectionFieldSerialization |
| 5 | com.google.gson.functional.InheritanceTest | testClassWithBaseFieldSerialization |
| 6 | com.google.gson.functional.MapTest | testInterfaceTypeMapWithSerializer |
| 7 | com.google.gson.functional.JsonTreeTest | testJsonTreeNull |
| 8 | com.google.gson.functional.JsonTreeTest | testJsonTreeToString |
| 9 | com.google.gson.functional.JsonTreeTest | testToJsonTreeObjectType |
| 10 | com.google.gson.functional.JsonTreeTest | testToJsonTree |
| 11 | com.google.gson.functional.MapAsArrayTypeAdapterTest | testMultipleEnableComplexKeyRegistrationHasNoEffect |
| 12 | com.google.gson.functional.MapAsArrayTypeAdapterTest | testSerializeComplexMapWithTypeAdapter |
| 13 | com.google.gson.functional.MapAsArrayTypeAdapterTest | testMapWithTypeVariableSerialization |
| 14 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExclusionStrategyWithMode |
| 15 | com.google.gson.internal.bind.JsonTreeWriterTest | testSerializeNullsFalse |
| 16 | com.google.gson.internal.bind.JsonTreeWriterTest | testSerializeNullsTrue |
| 17 | com.google.gson.internal.bind.JsonTreeWriterTest | testNestedObject |
| 18 | com.google.gson.internal.bind.JsonTreeWriterTest | testObject |
| 19 | com.google.gson.functional.CustomSerializerTest | testSubClassSerializerInvokedForBaseClassFieldsHoldingSubClassInstances |
| 20 | com.google.gson.functional.CustomSerializerTest | testBaseClassSerializerInvokedForBaseClassFieldsHoldingSubClassInstances |
| 21 | com.google.gson.functional.CustomSerializerTest | testBaseClassSerializerInvokedForBaseClassFields |
| 22 | com.google.gson.functional.CustomSerializerTest | testSubClassSerializerInvokedForBaseClassFieldsHoldingArrayOfSubClassInstances |
| 23 | com.google.gson.DefaultMapJsonSerializerTest | testNonEmptyMapSerialization |
| 24 | com.google.gson.functional.MoreSpecificTypeSerializationTest | testMapOfParameterizedSubclassFields |
| 25 | com.google.gson.functional.MoreSpecificTypeSerializationTest | testMapOfSubclassFields |
| 26 | com.google.gson.functional.TypeHierarchyAdapterTest | testTypeHierarchy |



## Classifications

### Tests
| ID | Class | Delta | Share |
| --- | --- | --- | --- |
| G | NEUTRAL | -435423.0 | - |
| N | NEGATIVE | -536558.0 | 5.26 |
| P | POSITIVE | 101135.0 | 12.50 |
| 3 | NEGATIVE | -182616.0 | 34.03 |
| 4 | POSITIVE | 24842.0 | 24.56 |
| 6 | NEGATIVE | -57128.0 | 10.65 |
| 10 | POSITIVE | 34119.0 | 33.74 |
| 11 | NEGATIVE | -43457.0 | 8.10 |
| 24 | NEGATIVE | -57801.0 | 10.77 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| negative | com.google.gson.internal.bind.JsonTreeWriter | 133 |
| positive | com.google.gson.internal.bind.JsonTreeWriter | 133 |
| unknown | com.google.gson.internal.bind.JsonTreeWriter | 133 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.functional.JsonTreeTest | testToJsonTree |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.internal.bind.JsonTreeWriter | [133](https://github.com/google/gson/tree/55acc2/gson/src/main/java/com/google/gson/internal/bind/JsonTreeWriter.java#L133) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 36.8092520236969 |
| Injection | 30.781214714050293 |
| Total | 245.6114559173584 |


