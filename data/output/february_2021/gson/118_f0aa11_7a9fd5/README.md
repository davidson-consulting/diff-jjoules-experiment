# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6288070 | 6199996 | -88074 | 510540.88 | 8.12 | 553952.59 | 8.93 |
| 1 | 5681321 | 5705735 | 24414 | 508297.63 | 8.95 | 539941.20 | 9.46 |
| 2 | 1826778 | 1806270 | -20508 | 104575.85 | 5.72 | 96447.66 | 5.34 |
| 3 | 3120048 | 3158927 | 38879 | 348950.54 | 11.18 | 291433.29 | 9.23 |
| 4 | 1489071 | 1510006 | 20935 | 109548.77 | 7.36 | 115835.23 | 7.67 |
| 5 | 837706 | 817747 | -19959 | 87142.10 | 10.40 | 83353.31 | 10.19 |
| 6 | 17983474 | 18080520 | 97046 | 1587657.77 | 8.83 | 1412778.71 | 7.81 |
| 7 | 12733305 | 12596526 | -136779 | 1160280.66 | 9.11 | 1253979.77 | 9.95 |
| 8 | 2989311 | 2992363 | 3052 | 283625.02 | 9.49 | 285408.89 | 9.54 |
| 9 | 1234433 | 1236386 | 1953 | 103055.33 | 8.35 | 85933.13 | 6.95 |
| 10 | 1319576 | 1341061 | 21485 | 119605.51 | 9.06 | 104990.17 | 7.83 |
| 11 | 1364377 | 1383359 | 18982 | 119464.17 | 8.76 | 89527.46 | 6.47 |
| 12 | 1740840 | 1784053 | 43213 | 176321.15 | 10.13 | 161349.25 | 9.04 |
| 13 | 2972587 | 3009697 | 37110 | 380379.04 | 12.80 | 403398.48 | 13.40 |

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
| G | NEUTRAL | 41749.0 | - |
| N | NEGATIVE | -265320.0 | 25.00 |
| P | POSITIVE | 307069.0 | 10.00 |
| 6 | POSITIVE | 97046.0 | 31.60 |
| 7 | NEGATIVE | -136779.0 | 51.55 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| unknown | com.google.gson.DefaultDateTypeAdapter | 100 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 101 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 87 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 88 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapterTest | testParsingDatesFormattedWithUsLocale |
| com.google.gson.DefaultDateTypeAdapterTest | testParsingDatesFormattedWithSystemLocale |
| com.google.gson.DefaultDateTypeAdapterTest | testFormattingInFr |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [100](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L100) |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L100#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L100#L87#L88) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 97.22190856933594 |
| Injection | 53.430015087127686 |
| Total | 4845.886991024017 |


