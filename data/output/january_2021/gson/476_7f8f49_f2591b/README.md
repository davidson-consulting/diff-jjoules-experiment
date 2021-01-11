# gson f2591b


https://github.com/google/gson/commit/f2591b



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)

![](./gson_delta_energy_1_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | σV2 |
| --- | --- | --- | --- | --- | --- |
| 0 | 37292 | 37842 | 550 | 70155.99783826852 | 27001.427124608723 |
| 1 | 79773 | 76599 | -3174 | 118545.75280479279 | 133197.21678540946 |
| 2 | 33447 | 32959 | -488 | 3724.611611610588 | 56573.567710602925 |
| 3 | 37536 | 38696 | 1160 | 12772.173470002557 | 14061.167836087403 |
| 4 | 39673 | 37781 | -1892 | 30151.883755126928 | 35756.62887366015 |
| 5 | 36927 | 36072 | -855 | 4281.273177552833 | 3820.321350773768 |
| 6 | 36621 | 36438 | -183 | 4158.9150307735945 | 4468.281942005271 |
| 7 | 35279 | 36621 | 1342 | 4493.188888640737 | 3346.040309184256 |
| 8 | 36804 | 36194 | -610 | 7180.009441483759 | 4525.059542474561 |
| 9 | 38513 | 37170 | -1343 | 13472.196859533686 | 17613.55464438882 |
| 10 | 79956 | 81604 | 1648 | 43964.793290727735 | 38749.521771061525 |
| 11 | 43090 | 42663 | -427 | 592950.2334446383 | 468275.9802561908 |
| 12 | 38452 | 38940 | 488 | 379400.7942522359 | 300438.927051062 |
| 13 | 35767 | 37415 | 1648 | 4088.21068490442 | 4787.235550264769 |
| 14 | 37231 | 37537 | 306 | 4102.348810095905 | 3773.100175916351 |
| 15 | 170288 | 178283 | 7995 | 205418.22654506814 | 210699.2224166451 |
| 16 | 37232 | 36987 | -245 | 3681.8521358685757 | 7307.775742905207 |

## Delta Duration per test method


| ID | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- |
| 0 | 1700922.9152542374 | 1217003.2 | -483919.7152542374 |
| 1 | 3852134.010752688 | 4013807.6063829786 | 161673.59563029045 |
| 2 | 1033972.9841269841 | 1270956.492063492 | 236983.50793650793 |
| 3 | 1485847.3711340206 | 1527971.6224489796 | 42124.25131495902 |
| 4 | 1931340.355263158 | 2090758.349206349 | 159417.99394319113 |
| 5 | 807776.5277777778 | 862085.5744680851 | 54309.046690307325 |
| 6 | 809746.1219512195 | 845504.1860465116 | 35758.064095292124 |
| 7 | 972122.7346938775 | 950311.9444444445 | -21810.79024943302 |
| 8 | 1094219.6857142858 | 1109003.6721311475 | 14783.986416861648 |
| 9 | 1488710.5833333333 | 1550511.8450704226 | 61801.26173708937 |
| 10 | 3157556.707070707 | 3138718.373737374 | -18838.333333333023 |
| 11 | 10185531.662790697 | 6361186.619565218 | -3824345.0432254793 |
| 12 | 3046999.225 | 2427940.4827586208 | -619058.7422413793 |
| 13 | 801042.3333333334 | 695635.2142857143 | -105407.11904761905 |
| 14 | 701933.9736842106 | 718237.5625 | 16303.588815789437 |
| 15 | 7497178.98989899 | 7829253.868686869 | 332074.8787878789 |
| 16 | 913653.72 | 938146.125 | 24492.405000000028 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.functional.CustomDeserializerTest | testDefaultConstructorNotCalledOnField |
| 1 | com.google.gson.functional.CustomDeserializerTest | testDefaultConstructorNotCalledOnObject |
| 2 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPatternNotOverridenByTypeAdapter |
| 3 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExclusionStrategyWithMode |
| 4 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExclusionStrategySerializationDoesNotImpactDeserialization |
| 5 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExcludeTopLevelClassDeserializationDoesNotImpactSerialization |
| 6 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExcludeTopLevelClassSerializationDoesNotImpactDeserialization |
| 7 | com.google.gson.functional.ExclusionStrategyFunctionalTest | testExclusionStrategySerializationDoesNotImpactSerialization |
| 8 | com.google.gson.functional.JsonAdapterAnnotationOnClassesTest | testRegisteredDeserializerOverridesJsonAdapter |
| 9 | com.google.gson.functional.JsonAdapterAnnotationOnClassesTest | testRegisteredSerializerOverridesJsonAdapter |
| 10 | com.google.gson.GsonTypeAdapterTest | testDeserializerForAbstractClass |
| 11 | com.google.gson.functional.TypeAdapterPrecedenceTest | testNonstreamingFollowedByNonstreaming |
| 12 | com.google.gson.functional.TypeAdapterPrecedenceTest | testStreamingHierarchicalFollowedByNonstreaming |
| 13 | com.google.gson.functional.TypeAdapterPrecedenceTest | testStreamingFollowedByNonstreaming |
| 14 | com.google.gson.functional.TypeAdapterPrecedenceTest | testNonstreamingHierarchicalFollowedByNonstreaming |
| 15 | com.google.gson.functional.DelegateTypeAdapterTest | testDelegateInvoked |
| 16 | com.google.gson.functional.DelegateTypeAdapterTest | testDelegateInvokedOnStrings |




| Test | IterationV1 | IterationV2 | DeltaIteration |
| --- | --- | --- | --- |
| 0 | 59 | 60 | 1 |
| 1 | 93 | 94 | 1 |
| 2 | 63 | 63 | 0 |
| 3 | 97 | 98 | 1 |
| 4 | 76 | 63 | -13 |
| 5 | 36 | 47 | 11 |
| 6 | 41 | 43 | 2 |
| 7 | 49 | 54 | 5 |
| 8 | 70 | 61 | -9 |
| 9 | 72 | 71 | -1 |
| 10 | 99 | 99 | 0 |
| 11 | 86 | 92 | 6 |
| 12 | 40 | 29 | -11 |
| 13 | 24 | 42 | 18 |
| 14 | 38 | 32 | -6 |
| 15 | 99 | 99 | 0 |
| 16 | 50 | 48 | -2 |



| Time Label | Time (s) |
| --- | --- |
| Selection | 28.03425931930542 |
| Injection | 11.41769552230835 |
| Total | 1013.7438170909882 |


