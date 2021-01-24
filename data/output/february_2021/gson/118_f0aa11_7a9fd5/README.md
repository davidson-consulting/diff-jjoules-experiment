# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 24810850 | 24163024 | -647826 | 1366573.27 | 5.51 | 741592.64 | 3.07 |
| 1 | 20014170 | 19653636 | -360534 | 1786782.10 | 8.93 | 1511443.86 | 7.69 |
| 2 | 6430770 | 5769821 | -660949 | 729935.28 | 11.35 | 834883.24 | 14.47 |
| 3 | 14198206 | 13327053 | -871153 | 592066.67 | 4.17 | 680865.98 | 5.11 |
| 4 | 6997235 | 7062665 | 65430 | 213961.74 | 3.06 | 389829.95 | 5.52 |
| 5 | 4413563 | 3771048 | -642515 | 598805.51 | 13.57 | 446795.86 | 11.85 |
| 6 | 50054742 | 49874873 | -179869 | 866261.28 | 1.73 | 1287543.41 | 2.58 |
| 7 | 32335488 | 31681254 | -654234 | 806491.78 | 2.49 | 1621145.59 | 5.12 |
| 8 | 22864505 | 23119753 | 255248 | 753775.29 | 3.30 | 1083268.59 | 4.69 |
| 9 | 6390609 | 6090317 | -300292 | 1019144.58 | 15.95 | 910074.50 | 14.94 |
| 10 | 5860947 | 6461653 | 600706 | 453143.96 | 7.73 | 781503.86 | 12.09 |
| 11 | 5389024 | 5992050 | 603026 | 1013798.13 | 18.81 | 1288382.30 | 21.50 |
| 12 | 8580605 | 8731484 | 150879 | 668496.09 | 7.79 | 831344.92 | 9.52 |
| 13 | 21580877 | 21939580 | 358703 | 2276381.31 | 10.55 | 625381.76 | 2.85 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.DefaultDateTypeAdapterTest | testParsingDatesFormattedWithUsLocale |
| 1 | com.google.gson.DefaultDateTypeAdapterTest | testDateDeserializationISO8601 |
| 2 | com.google.gson.DefaultDateTypeAdapterTest | testFormattingInEnUs |
| 3 | com.google.gson.DefaultDateTypeAdapterTest | testFormatUsesDefaultTimezone |
| 4 | com.google.gson.DefaultDateTypeAdapterTest | testDatePattern |
| 5 | com.google.gson.DefaultDateTypeAdapterTest | testDateSerialization |
| 6 | com.google.gson.DefaultDateTypeAdapterTest | testParsingDatesFormattedWithSystemLocale |
| 7 | com.google.gson.DefaultDateTypeAdapterTest | testFormattingInFr |
| 8 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPatternNotOverridenByTypeAdapter |
| 9 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPattern |
| 10 | com.google.gson.functional.DefaultTypeAdaptersTest | testSqlDateSerialization |
| 11 | com.google.gson.functional.DefaultTypeAdaptersTest | testTimestampSerialization |
| 12 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateDeserializationWithPattern |
| 13 | com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationInCollection |



## Classifications

### Tests
| ID | Class | Delta | Share |
| --- | --- | --- | --- |
| G | NEUTRAL | -2283380.0 | - |
| N | NEGATIVE | -4317372.0 | 12.50 |
| P | POSITIVE | 2033992.0 | 16.67 |
| 3 | NEGATIVE | -871153.0 | 20.18 |
| 10 | POSITIVE | 600706.0 | 29.53 |
| 11 | POSITIVE | 603026.0 | 29.65 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| unknown | com.google.gson.DefaultDateTypeAdapter | 100 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 87 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 88 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.functional.DefaultTypeAdaptersTest | testSqlDateSerialization |
| com.google.gson.functional.DefaultTypeAdaptersTest | testTimestampSerialization |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |
| com.google.gson.DefaultDateTypeAdapter | [101](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88#L101) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 103.65823650360107 |
| Injection | 154.4507429599762 |
| Total | 1374.4559228420258 |


