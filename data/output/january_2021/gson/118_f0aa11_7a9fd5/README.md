# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 74706 | 73852 | -854 | 15120.55 | 20.24 | 15785.54 | 21.37 |
| 1 | 37231 | 37170 | -61 | 6488.19 | 17.43 | 2416.70 | 6.50 |
| 2 | 36804 | 37292 | 488 | 6681.99 | 18.16 | 9825.75 | 26.35 |
| 3 | 73914 | 74462 | 548 | 20067.82 | 27.15 | 22100.46 | 29.68 |
| 4 | 74401 | 76477 | 2076 | 17261.85 | 23.20 | 16852.86 | 22.04 |
| 5 | 961118 | 978635 | 17517 | 499866.49 | 52.01 | 503860.77 | 51.49 |
| 6 | 364928 | 364867 | -61 | 145163.28 | 39.78 | 144183.35 | 39.52 |
| 7 | 36132 | 36560 | 428 | 3980.07 | 11.02 | 5202.10 | 14.23 |
| 8 | 35949 | 36804 | 855 | 322238.94 | 896.38 | 502478.52 | 1365.28 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPatternNotOverridenByTypeAdapter |
| 1 | com.google.gson.functional.DefaultTypeAdaptersTest | testSqlDateSerialization |
| 2 | com.google.gson.functional.DefaultTypeAdaptersTest | testTimestampSerialization |
| 3 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateDeserializationWithPattern |
| 4 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationInCollection |
| 5 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPattern |
| 6 | com.google.gson.DefaultDateTypeAdapterTest | testDateDeserializationISO8601 |
| 7 | com.google.gson.DefaultDateTypeAdapterTest | testDateSerialization |
| 8 | com.google.gson.DefaultDateTypeAdapterTest | testDatePattern |



## Classifications

### Tests
| ID | Class | Delta | Share |
| --- | --- | --- | --- |
| G | NEUTRAL | 20936.0 | - |
| N | NEGATIVE | -976.0 | 33.33 |
| P | POSITIVE | 21912.0 | 16.67 |
| 0 | NEGATIVE | -854.0 | 87.50 |
| 5 | POSITIVE | 17517.0 | 79.94 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| negative | com.google.gson.DefaultDateTypeAdapter | 87 |
| negative | com.google.gson.DefaultDateTypeAdapter | 88 |
| positive | com.google.gson.DefaultDateTypeAdapter | 87 |
| positive | com.google.gson.DefaultDateTypeAdapter | 88 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 100 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 101 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 87 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 88 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPattern |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.046000480651855 |
| Injection | 13.998331069946289 |
| Total | 1385.3567938804626 |


