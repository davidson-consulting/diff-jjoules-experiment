# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 6683638 | 6113204 | -570434 | 1001568.05 | 14.99 | 398423.82 | 6.52 |
| 1 | 6347946 | 5843064 | -504882 | 679240.75 | 10.70 | 311710.51 | 5.33 |
| 2 | 1821772 | 1839595 | 17823 | 89378.49 | 4.91 | 73176.79 | 3.98 |
| 3 | 3526358 | 3040093 | -486265 | 451486.35 | 12.80 | 197909.26 | 6.51 |
| 4 | 1490841 | 1529354 | 38513 | 101247.70 | 6.79 | 68327.26 | 4.47 |
| 5 | 856321 | 816771 | -39550 | 77439.89 | 9.04 | 100321.24 | 12.28 |
| 6 | 17998245 | 17927078 | -71167 | 1818301.57 | 10.10 | 332266.73 | 1.85 |
| 7 | 12498930 | 12579741 | 80811 | 1331119.27 | 10.65 | 1347688.41 | 10.71 |
| 8 | 3089836 | 2931450 | -158386 | 339424.79 | 10.99 | 87914.12 | 3.00 |
| 9 | 1320615 | 1231137 | -89478 | 58907.89 | 4.46 | 85164.62 | 6.92 |
| 10 | 1339657 | 1341305 | 1648 | 90170.18 | 6.73 | 63072.19 | 4.70 |
| 11 | 1407162 | 1374752 | -32410 | 88498.94 | 6.29 | 48940.06 | 3.56 |
| 12 | 1761104 | 1696285 | -64819 | 273936.14 | 15.55 | 52367.33 | 3.09 |
| 13 | 3015739 | 2969414 | -46325 | 703403.15 | 23.32 | 69094.35 | 2.33 |

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
| G | NEUTRAL | -1924921.0 | - |
| N | NEGATIVE | -2063716.0 | 10.00 |
| P | POSITIVE | 138795.0 | 25.00 |
| 0 | NEGATIVE | -570434.0 | 27.64 |
| 1 | NEGATIVE | -504882.0 | 24.46 |
| 3 | NEGATIVE | -486265.0 | 23.56 |
| 7 | POSITIVE | 80811.0 | 58.22 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| negative | com.google.gson.DefaultDateTypeAdapter | 100 |
| negative | com.google.gson.DefaultDateTypeAdapter | 87 |
| negative | com.google.gson.DefaultDateTypeAdapter | 88 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 100 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 101 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 87 |
| unknown | com.google.gson.DefaultDateTypeAdapter | 88 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapterTest | testParsingDatesFormattedWithUsLocale |
| com.google.gson.DefaultDateTypeAdapterTest | testDatePattern |
| com.google.gson.DefaultDateTypeAdapterTest | testFormattingInFr |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |
| com.google.gson.DefaultDateTypeAdapter | [100](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88#L100) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 99.60394024848938 |
| Injection | 54.40375995635986 |
| Total | 666.3676970005035 |


