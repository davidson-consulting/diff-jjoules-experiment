# gson 7a9fd5


https://github.com/google/gson/commit/7a9fd5



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 4405812 | 4324880 | -80932 | 318453.80 | 7.23 | 317048.41 | 7.33 |
| 1 | 3530631 | 3535086 | 4455 | 333517.53 | 9.45 | 282162.89 | 7.98 |
| 2 | 832761 | 830992 | -1769 | 88659.20 | 10.65 | 86235.42 | 10.38 |
| 3 | 1851619 | 1861079 | 9460 | 107319.87 | 5.80 | 116081.51 | 6.24 |
| 4 | 730833 | 736571 | 5738 | 90093.36 | 12.33 | 85785.30 | 11.65 |
| 5 | 331359 | 331237 | -122 | 79010.94 | 23.84 | 88562.34 | 26.74 |
| 6 | 10048009 | 10107518 | 59509 | 342337.36 | 3.41 | 407645.79 | 4.03 |
| 7 | 6453231 | 6448043 | -5188 | 280466.13 | 4.35 | 396597.08 | 6.15 |
| 8 | 1867793 | 1885677 | 17884 | 120539.00 | 6.45 | 95254.14 | 5.05 |
| 9 | 493407 | 473937 | -19470 | 68315.66 | 13.85 | 72907.98 | 15.38 |
| 10 | 656859 | 648619 | -8240 | 93629.81 | 14.25 | 88040.94 | 13.57 |
| 11 | 669615 | 645201 | -24414 | 81015.47 | 12.10 | 90031.62 | 13.95 |
| 12 | 915830 | 939512 | 23682 | 73205.17 | 7.99 | 80189.65 | 8.54 |
| 13 | 2045283 | 2049189 | 3906 | 72479.88 | 3.54 | 89032.50 | 4.34 |

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
| G | NEUTRAL | -15501.0 | - |
| N | NEGATIVE | -140135.0 | 14.29 |
| P | POSITIVE | 124634.0 | 14.29 |
| 0 | NEGATIVE | -80932.0 | 57.75 |
| 6 | POSITIVE | 59509.0 | 47.75 |

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

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.DefaultDateTypeAdapter | [100](https://github.com/google/gson/tree/7a9fd5/gson/src/main/java/com/google/gson/DefaultDateTypeAdapter.java#L100) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.62282061576843 |
| Injection | 23.488861322402954 |
| Total | 1863.7621393203735 |


