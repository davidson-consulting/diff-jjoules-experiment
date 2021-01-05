# gson f2591b


https://github.com/google/gson/commit/f2591b



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)

![](./gson_delta_energy_1_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy |
| --- | --- | --- | --- |
| 0 | 57524.27086124027 | 39366.27728909762 | -18157.993572142652 |
| 1 | 98399.03359658715 | 140291.80366915406 | 41892.77007256691 |
| 2 | 34941.06561685386 | 35946.558357154936 | 1005.4927403010734 |
| 3 | 37892.727846043505 | 38944.684760806536 | 1051.9569147630318 |
| 4 | 37429.666828420464 | 36048.463738126346 | -1381.2030902941187 |
| 5 | 36061.936337361345 | 37395.51080667724 | 1333.5744693158922 |
| 6 | 34833.5755764297 | 37355.86827881993 | 2522.2927023902303 |
| 7 | 38111.77015058898 | 36254.67856073816 | -1857.0915898508174 |
| 8 | 38813.97261003691 | 36581.86652548119 | -2232.106084555715 |
| 9 | 35704.177122365494 | 53336.80489326181 | 17632.627770896317 |
| 10 | 141317.50898697673 | 91747.13238968732 | -49570.3765972894 |
| 11 | 411995.84966692823 | 34025.28704300485 | -377970.5626239234 |
| 12 | 38065.82155745666 | 43242.050923053175 | 5176.229365596519 |
| 13 | 31218.877152442932 | 35969.09623578265 | 4750.219083339718 |
| 14 | 39587.146118856086 | 35137.20836574491 | -4449.937753111175 |
| 15 | 212359.06312057463 | 204767.92703316174 | -7591.136087412888 |
| 16 | 42447.10641355591 | 32074.5162396873 | -10372.590173868615 |

## Delta Duration per test method

![](./gson_delta_duration_0_v.png)

![](./gson_delta_duration_1_v.png)


| ID | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- |
| 0 | 1736244.5993259833 | 1266885.3745124186 | -469359.2248135647 |
| 1 | 2808386.645489782 | 4550767.319960135 | 1742380.674470353 |
| 2 | 1244602.4336799658 | 1103100.674354732 | -141501.75932523375 |
| 3 | 1481193.699512772 | 1487185.6711157896 | 5991.971603017533 |
| 4 | 1324359.028064777 | 1183190.846253228 | -141168.181811549 |
| 5 | 801709.614931558 | 803019.6525385433 | 1310.0376069853082 |
| 6 | 848785.8866134076 | 813375.4343166782 | -35410.45229672943 |
| 7 | 1162352.365670084 | 893696.5141560042 | -268655.85151407984 |
| 8 | 1097867.5914478574 | 1154515.6751898266 | 56648.083741969196 |
| 9 | 1296071.662743358 | 1849287.9461028972 | 553216.2833595392 |
| 10 | 4786634.852949573 | 3533217.5100669293 | -1253417.3428826435 |
| 11 | 12396344.81346118 | 1438659.5108186274 | -10957685.302642554 |
| 12 | 657947.3949348532 | 1165064.2657182813 | 507116.8707834281 |
| 13 | 805628.211008668 | 648299.141309422 | -157329.06969924597 |
| 14 | 632288.1460227689 | 616647.2913878546 | -15640.854634914314 |
| 15 | 6421008.808033582 | 6775440.782014883 | 354431.9739813013 |
| 16 | 720887.4439403412 | 901776.1910491083 | 180888.74710876704 |

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


