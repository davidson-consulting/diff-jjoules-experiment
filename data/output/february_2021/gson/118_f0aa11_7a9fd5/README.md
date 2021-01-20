# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2181025 | 2173396 | -7629 | 205708.34 | 9.43 | 190348.76 | 8.76 |
| 1 | 493590 | 572447 | 78857 | 133692.95 | 27.09 | 73236.65 | 12.79 |
| 2 | 685667 | 671507 | -14160 | 115334.15 | 16.82 | 27871.50 | 4.15 |
| 3 | 656309 | 659117 | 2808 | 147702.07 | 22.50 | 42070.15 | 6.38 |
| 4 | 1198667 | 1195920 | -2747 | 184235.78 | 15.37 | 160783.10 | 13.44 |
| 5 | 2287226 | 2437982 | 150756 | 211688.62 | 9.26 | 88253.83 | 3.62 |
| 6 | 4694995 | 4629261 | -65734 | 306554.54 | 6.53 | 291170.65 | 6.29 |
| 7 | 1557186 | 1612056 | 54870 | 151134.84 | 9.71 | 74983.15 | 4.65 |
| 8 | 4299977 | 4215504 | -84473 | 280301.42 | 6.52 | 612184.83 | 14.52 |
| 9 | 1450130 | 1302121 | -148009 | 153917.99 | 10.61 | 207534.71 | 15.94 |
| 10 | 615233 | 547301 | -67932 | 72804.76 | 11.83 | 76331.51 | 13.95 |
| 11 | 6902448 | 6841902 | -60546 | 656705.80 | 9.51 | 168362.15 | 2.46 |

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
| 7 | com.google.gson.DefaultDateTypeAdapterTest | testFormattingInEnUs |
| 8 | com.google.gson.DefaultDateTypeAdapterTest | testFormatUsesDefaultTimezone |
| 9 | com.google.gson.DefaultDateTypeAdapterTest | testDatePattern |
| 10 | com.google.gson.DefaultDateTypeAdapterTest | testDateSerialization |
| 11 | com.google.gson.DefaultDateTypeAdapterTest | testFormattingInFr |



## Classifications

### Tests
| ID | Class | Delta | Share |
| --- | --- | --- | --- |
| G | NEUTRAL | -163939.0 | - |
| N | NEGATIVE | -451230.0 | 12.50 |
| P | POSITIVE | 287291.0 | 25.00 |
| 5 | POSITIVE | 150756.0 | 52.48 |
| 9 | NEGATIVE | -148009.0 | 32.80 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| negative | com.google.gson.DefaultDateTypeAdapter | 87 |
| negative | com.google.gson.DefaultDateTypeAdapter | 88 |
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
| com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationInCollection |
| com.google.gson.functional.DefaultTypeAdaptersTest | testDateSerializationWithPattern |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [87](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87) |
| com.google.gson.DefaultDateTypeAdapter | [88](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88) |
| com.google.gson.DefaultDateTypeAdapter | [100](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L87#L88#L100) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 33.89952874183655 |
| Injection | 20.469573497772217 |
| Total | 237.01659202575684 |


