# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4332752 | 4314869 | -17883 | 180480.28 | 4.17 | 372177.10 | 8.63 |
| 1 | 3444754 | 3482780 | 38026 | 148652.51 | 4.32 | 133635.30 | 3.84 |
| 2 | 814268 | 950864 | 136596 | 41410.47 | 5.09 | 105340.86 | 11.08 |
| 3 | 1837215 | 1881709 | 44494 | 100081.24 | 5.45 | 64632.44 | 3.43 |
| 4 | 735228 | 738035 | 2807 | 94241.95 | 12.82 | 53191.44 | 7.21 |
| 5 | 295837 | 442870 | 147033 | 16117.81 | 5.45 | 93892.66 | 21.20 |
| 6 | 9904699 | 9952855 | 48156 | 311916.02 | 3.15 | 236980.16 | 2.38 |
| 7 | 6565108 | 6453475 | -111633 | 238670.47 | 3.64 | 359038.72 | 5.56 |
| 8 | 1815242 | 1824764 | 9522 | 50704.56 | 2.79 | 94148.66 | 5.16 |
| 9 | 483763 | 490355 | 6592 | 90834.62 | 18.78 | 52662.93 | 10.74 |
| 10 | 642149 | 765562 | 123413 | 74930.84 | 11.67 | 75018.98 | 9.80 |
| 11 | 652159 | 616087 | -36072 | 74807.18 | 11.47 | 88448.65 | 14.36 |
| 12 | 890135 | 932737 | 42602 | 32898.19 | 3.70 | 22921.56 | 2.46 |
| 13 | 2037593 | 2065852 | 28259 | 51335.55 | 2.52 | 30229.50 | 1.46 |

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
| G | NEUTRAL | 461912.0 | - |
| N | NEGATIVE | -165588.0 | 33.33 |
| P | POSITIVE | 627500.0 | 9.09 |
| 2 | POSITIVE | 136596.0 | 21.77 |
| 5 | POSITIVE | 147033.0 | 23.43 |
| 7 | NEGATIVE | -111633.0 | 67.42 |
| 10 | POSITIVE | 123413.0 | 19.67 |

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
| com.google.gson.DefaultDateTypeAdapterTest | testFormattingInFr |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.447208642959595 |
| Injection | 23.202263832092285 |
| Total | 254.4712688922882 |


