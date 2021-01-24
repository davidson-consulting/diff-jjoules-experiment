# gson 2


https://github.com/google/gson/commit/2



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 24779050 | 24682615 | -96435 | 1103241.27 | 4.45 | 1114888.81 | 4.52 |
| 1 | 19689281 | 19733348 | 44067 | 1640770.15 | 8.33 | 1644061.91 | 8.33 |
| 2 | 5799363 | 5830612 | 31249 | 622584.67 | 10.74 | 637214.66 | 10.93 |
| 3 | 13977809 | 13909083 | -68726 | 678984.70 | 4.86 | 663104.83 | 4.77 |
| 4 | 7037335 | 7030011 | -7324 | 394718.27 | 5.61 | 365980.20 | 5.21 |
| 5 | 3777456 | 3792898 | 15442 | 564231.16 | 14.94 | 527398.63 | 13.90 |
| 6 | 50258172 | 50118524 | -139648 | 991590.05 | 1.97 | 952602.94 | 1.90 |
| 7 | 31616984 | 31501628 | -115356 | 974756.17 | 3.08 | 936618.92 | 2.97 |
| 8 | 22544498 | 22255253 | -289245 | 1031747.77 | 4.58 | 927854.05 | 4.17 |
| 9 | 5931381 | 5938767 | 7386 | 765830.99 | 12.91 | 770819.71 | 12.98 |
| 10 | 6323409 | 6289717 | -33692 | 744420.19 | 11.77 | 770933.30 | 12.26 |
| 11 | 5710496 | 5797044 | 86548 | 934957.55 | 16.37 | 969801.12 | 16.73 |
| 12 | 8693764 | 8642740 | -51024 | 728854.45 | 8.38 | 618475.34 | 7.16 |
| 13 | 22194524 | 22182926 | -11598 | 1243364.54 | 5.60 | 1427198.43 | 6.43 |

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
| G | NEUTRAL | -628356.0 | - |
| N | NEGATIVE | -813048.0 | 11.11 |
| P | POSITIVE | 184692.0 | 20.00 |
| 6 | NEGATIVE | -139648.0 | 17.18 |
| 8 | NEGATIVE | -289245.0 | 35.58 |
| 11 | POSITIVE | 86548.0 | 46.86 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
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
| com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPatternNotOverridenByTypeAdapter |
| com.google.gson.functional.DefaultTypeAdaptersTest | testTimestampSerialization |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/2/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/2/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |
| com.google.gson.DefaultDateTypeAdapter | [101](https://github.com/google/gson/tree/2/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88#L101) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 106.28706216812134 |
| Injection | 155.6600558757782 |
| Total | 106452.18586015701 |


