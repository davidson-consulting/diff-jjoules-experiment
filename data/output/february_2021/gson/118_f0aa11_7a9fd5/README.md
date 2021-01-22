# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 1487179 | 1587825 | 100646 | 54253.50 | 3.65 | 107738.73 | 6.79 |
| 1 | 776732 | 798032 | 21300 | 45381.42 | 5.84 | 48203.41 | 6.04 |
| 2 | 288085 | 280517 | -7568 | 14545.73 | 5.05 | 24115.20 | 8.60 |
| 3 | 571959 | 566466 | -5493 | 37003.61 | 6.47 | 42169.10 | 7.44 |
| 4 | 230102 | 216491 | -13611 | 21919.65 | 9.53 | 19550.33 | 9.03 |
| 5 | 170043 | 170227 | 184 | 24405.20 | 14.35 | 23096.67 | 13.57 |
| 6 | 4488575 | 4283193 | -205382 | 128061.24 | 2.85 | 133146.79 | 3.11 |
| 7 | 3437552 | 3358573 | -78979 | 307495.02 | 8.95 | 131614.28 | 3.92 |
| 8 | 413024 | 424437 | 11413 | 36579.56 | 8.86 | 37938.58 | 8.94 |
| 9 | 221068 | 214050 | -7018 | 42653.87 | 19.29 | 122165.01 | 57.07 |
| 10 | 205321 | 204528 | -793 | 39912.14 | 19.44 | 21206.07 | 10.37 |
| 11 | 261535 | 229064 | -32471 | 72317.12 | 27.65 | 13461.24 | 5.88 |
| 12 | 274169 | 261230 | -12939 | 26693.18 | 9.74 | 27619.90 | 10.57 |
| 13 | 421935 | 433105 | 11170 | 34666.27 | 8.22 | 28058.85 | 6.48 |

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
| G | NEUTRAL | -219541.0 | - |
| N | NEGATIVE | -364254.0 | 11.11 |
| P | POSITIVE | 144713.0 | 20.00 |
| 0 | POSITIVE | 100646.0 | 69.55 |
| 6 | NEGATIVE | -205382.0 | 56.38 |
| 7 | NEGATIVE | -78979.0 | 21.68 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| negative | com.google.gson.DefaultDateTypeAdapter | 100 |
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

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [100](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L100) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 35.31309962272644 |
| Injection | 15.838767766952515 |
| Total | 211.7568211555481 |


