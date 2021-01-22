# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4427784 | 4561878 | 134094 | 331474.21 | 7.49 | 293988.45 | 6.44 |
| 1 | 3473807 | 3607779 | 133972 | 276262.48 | 7.95 | 451356.34 | 12.51 |
| 2 | 853147 | 853453 | 306 | 103050.29 | 12.08 | 79570.06 | 9.32 |
| 3 | 1807246 | 1803890 | -3356 | 111409.33 | 6.16 | 71308.53 | 3.95 |
| 4 | 730955 | 717222 | -13733 | 85157.02 | 11.65 | 50181.91 | 7.00 |
| 5 | 335571 | 332152 | -3419 | 92529.71 | 27.57 | 74811.82 | 22.52 |
| 6 | 10115513 | 10220250 | 104737 | 161398.38 | 1.60 | 316096.64 | 3.09 |
| 7 | 6369491 | 6494674 | 125183 | 264821.22 | 4.16 | 348440.48 | 5.37 |
| 8 | 1826045 | 1925777 | 99732 | 80621.59 | 4.42 | 78831.11 | 4.09 |
| 9 | 451842 | 477660 | 25818 | 74396.55 | 16.47 | 99029.05 | 20.73 |
| 10 | 726438 | 677916 | -48522 | 102492.33 | 14.11 | 109198.71 | 16.11 |
| 11 | 671934 | 660093 | -11841 | 72324.12 | 10.76 | 113307.02 | 17.17 |
| 12 | 945799 | 952024 | 6225 | 71346.86 | 7.54 | 63486.06 | 6.67 |
| 13 | 2055354 | 2034663 | -20691 | 94926.06 | 4.62 | 71260.30 | 3.50 |

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
| G | NEUTRAL | 528505.0 | - |
| N | NEGATIVE | -101562.0 | 16.67 |
| P | POSITIVE | 630067.0 | 12.50 |
| 0 | POSITIVE | 134094.0 | 21.28 |
| 1 | POSITIVE | 133972.0 | 21.26 |
| 7 | POSITIVE | 125183.0 | 19.87 |
| 10 | NEGATIVE | -48522.0 | 47.78 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| positive | com.google.gson.DefaultDateTypeAdapter | 100 |
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
| com.google.gson.functional.DefaultTypeAdaptersTest | testSqlDateSerialization |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |
| com.google.gson.DefaultDateTypeAdapter | [101](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88#L101) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.29764699935913 |
| Injection | 23.560192823410034 |
| Total | 255.28955483436584 |


