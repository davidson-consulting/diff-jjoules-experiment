# gson 7a9fd5


https://github.com/google/gson.git/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy |
| --- | --- | --- | --- |
| 0 | 70890.03151856292 | 78382.37112252257 | 7492.3396039596555 |
| 1 | 919864.3259811391 | 423464.1423577115 | -496400.1836234276 |
| 2 | 36507.28520228628 | 37361.223892472044 | 853.9386901857652 |
| 3 | 35146.656511677334 | 35999.91659774162 | 853.2600860642851 |
| 4 | 71670.38661440223 | 58276.53974963733 | -13393.846864764899 |
| 5 | 72705.37227740994 | 91128.31192753691 | 18422.939650126966 |
| 6 | 319069.9581747161 | 339054.4003772752 | 19984.44220255909 |
| 7 | 33190.53840724717 | 269143.4014224454 | 235952.8630151982 |
| 8 | 37562.36950085628 | 37456.97828004153 | -105.39122081475216 |

## Delta Duration per test method

![](./gson_delta_duration_0_v.png)


| ID | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- |
| 0 | 2518274.7823719773 | 2609985.387283192 | 91710.60491121467 |
| 1 | 28876802.05012335 | 12638403.060759824 | -16238398.989363525 |
| 2 | 1305287.1737210508 | 1310469.8326907614 | 5182.658969710581 |
| 3 | 1432830.0804689876 | 1374901.9444174403 | -57928.13605154725 |
| 4 | 2739073.3552636867 | 2464801.2133588265 | -274272.14190486027 |
| 5 | 2743249.1001959005 | 2690582.089584068 | -52667.01061183261 |
| 6 | 9460671.653349183 | 10149531.481847452 | 688859.8284982685 |
| 7 | 1184476.2989599076 | 7813503.729553086 | 6629027.430593178 |
| 8 | 979645.8260806922 | 999928.4469850727 | 20282.620904380456 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPatternNotOverridenByTypeAdapter |
| 1 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPattern |
| 2 | com.google.gson.functional.DefaultTypeAdaptersTest | testSqlDateSerialization |
| 3 | com.google.gson.functional.DefaultTypeAdaptersTest | testTimestampSerialization |
| 4 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateDeserializationWithPattern |
| 5 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationInCollection |
| 6 | com.google.gson.DefaultDateTypeAdapterTest | testDateDeserializationISO8601 |
| 7 | com.google.gson.DefaultDateTypeAdapterTest | testDatePattern |
| 8 | com.google.gson.DefaultDateTypeAdapterTest | testDateSerialization |


| Test | IterationV1 | IterationV2 | DeltaIteration |
| --- | --- | --- | --- |
| 0 | 99 | 99 | 0 |
| 1 | 92 | 95 | 3 |
| 2 | 91 | 90 | -1 |
| 3 | 97 | 98 | 1 |
| 4 | 99 | 99 | 0 |
| 5 | 99 | 99 | 0 |
| 6 | 99 | 99 | 0 |
| 7 | 55 | 52 | -3 |
| 8 | 57 | 65 | 8 |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.945706605911255 |
| Injection | 14.244420528411865 |
| Total | 1387.9878978729248 |


## Aggregation per test class


![](./gson.png)

![](./gson_delta_1_v.png)

| Index | EnergyV1 | EnergyV2 | DeltaEnergy |
| --- | --- | --- | --- |
| 0 | 1206784.058105478 | 724612.505647622 | -482171.552457856 |
| 1 | 389822.8660828195 | 645654.7800797621 | 255831.91399694257 |

| Index | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- |
| 0 | 39615516.542144954 | 23089143.52809411 | -16526373.014050845 |
| 1 | 11624793.778389784 | 18962963.658385612 | 7338169.8799958285 |
| Index | TestClassName | #Tests |
| --- | --- | --- |
| 0 | com.google.gson.functional.DefaultTypeAdaptersTest | 6 |
| 1 | com.google.gson.DefaultDateTypeAdapterTest | 3 |
