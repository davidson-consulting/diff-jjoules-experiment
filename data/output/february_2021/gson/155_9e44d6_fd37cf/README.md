# gson fd37cf


https://github.com/google/gson/commit/fd37cf



## Delta Energy per test method

![](./gson_delta_energy_0_v.png)


| ID | EnergyV1 | EnergyV2 | DeltaEnergy | σV1 | %σV1 | σV2 | %σV2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 116210 | 131347 | 15137 | 17896.46 | 15.40 | 15072.35 | 11.48 |
| 1 | 633787 | 590147 | -43640 | 70724.77 | 11.16 | 47811.18 | 8.10 |

## Misc.

| ID | Test Class | Test Method |
| --- | --- | --- |
| 0 | com.google.gson.JsonArrayTest | testDeepCopy |
| 1 | com.google.gson.JsonObjectTest | testDeepCopy |



## Classifications

### Tests
| ID | Class | Delta | Share |
| --- | --- | --- | --- |
| G | NEUTRAL | -28503.0 | - |
| N | NEGATIVE | -43640.0 | 100.00 |
| P | POSITIVE | 15137.0 | 100.00 |

### Lines
| Class | Java Class | Line |
| --- | --- | --- |
| unknown | com.google.gson.JsonArray | 49 |
| unknown | com.google.gson.JsonArray | 50 |
| unknown | com.google.gson.JsonArray | 56 |
| unknown | com.google.gson.JsonArray | 44 |
| unknown | com.google.gson.JsonArray | 45 |



## Localization of Green Regression
### Selected Tests
| Test class | test method |
| --- | --- |
| com.google.gson.JsonArrayTest | testDeepCopy |

### Suspected lines
| Class | line |
| --- | --- |
| com.google.gson.JsonArray | [49](https://github.com/google/gson/tree/fd37cf/gson/src/main/java/com/google/gson/JsonArray.java#L49) |
| com.google.gson.JsonArray | [44](https://github.com/google/gson/tree/fd37cf/gson/src/main/java/com/google/gson/JsonArray.java#L49#L44) |
| com.google.gson.JsonArray | [50](https://github.com/google/gson/tree/fd37cf/gson/src/main/java/com/google/gson/JsonArray.java#L49#L44#L50) |
| com.google.gson.JsonArray | [56](https://github.com/google/gson/tree/fd37cf/gson/src/main/java/com/google/gson/JsonArray.java#L49#L44#L50#L56) |
| com.google.gson.JsonArray | [45](https://github.com/google/gson/tree/fd37cf/gson/src/main/java/com/google/gson/JsonArray.java#L49#L44#L50#L56#L45) |



| Time Label | Time (s) |
| --- | --- |
| Selection | 34.29595732688904 |
| Injection | 13.68557596206665 |
| Total | 195.80166792869568 |


