# commons-io 8ae947


https://github.com/apache/commons-io/commit/8ae947


| Index | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 993824.5031531989 | 1095184.7330522835 | -101360.22989908466 | 34937089.41542565 | 39759845.57407952 | -4822756.15865387 |
| 1 | 680333.6554852668 | 553052.7449840959 | 127280.9105011709 | 19825437.12160531 | 18957263.12176095 | 868173.9998443611 |
| 2 | 617392.2468906936 | 621655.3791398075 | -4263.132249113987 | 24194439.842617948 | 21073393.412022356 | 3121046.4305955917 |
| 3 | 1291056.5526349612 | 1154363.3214445957 | 136693.2311903655 | 35257870.350170344 | 31844761.857751887 | 3413108.492418457 |
| 4 | 810429.6407377246 | 820164.483865917 | -9734.843128192355 | 28859328.368948393 | 29145007.769041248 | -285679.4000928551 |
| 5 | 6969212.130210134 | 6995408.161440964 | -26196.031230829656 | 532935350.8319085 | 534326109.1227176 | -1390758.290809095 |
| 6 | 18272140.150146745 | 10616591.112064661 | 7655549.038082084 | 1141808196.3657005 | 872309374.1574292 | 269498822.20827127 |
| 7 | 6984719.822459599 | 7125686.290798358 | -140966.46833875868 | 536963094.8691577 | 532973723.7827536 | 3989371.086404085 |

![](./commons-io.png)

![](./commons-io_delta.png)

| TestClassName | Index |
| --- | --- |
| org.apache.commons.io.FileUtilsCleanSymlinksTestCase | 0 |
| org.apache.commons.io.FileDeleteStrategyTestCase | 1 |
| org.apache.commons.io.filefilter.FileFilterTestCase | 2 |
| org.apache.commons.io.FileUtilsTestCase | 3 |
| org.apache.commons.io.FileUtilsCleanDirectoryTestCase | 4 |
| org.apache.commons.io.FileCleaningTrackerTestCase | 5 |
| org.apache.commons.io.monitor.FileAlterationObserverTestCase | 6 |
| org.apache.commons.io.FileCleanerTestCase | 7 |
## org.apache.commons.io.FileUtilsCleanSymlinksTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileUtilsCleanSymlinksTestCase-testStillClearsIfGivenDirectoryIsASymlink | 58753.095607483 | 63769.46888382842 | -5016.373276345417 | 2561376.232963763 | 2466242.840494871 | 95133.39246889204 |
| org.apache.commons.io.FileUtilsCleanSymlinksTestCase-testCleanDirWithParentSymlinks | 789239.8704386402 | 869461.347569999 | -80221.47713135881 | 26411106.21805748 | 30863325.18497301 | -4452218.966915529 |
| org.apache.commons.io.FileUtilsCleanSymlinksTestCase-testCleanDirWithSymlinkFile | 77733.25026506867 | 80006.44308805716 | -2273.1928229884943 | 3142768.0017955047 | 3196655.093989988 | -53887.09219448315 |
| org.apache.commons.io.FileUtilsCleanSymlinksTestCase-testCleanDirWithASymlinkDir | 68098.28684200702 | 81947.47351039897 | -13849.18666839195 | 2821838.9626089004 | 3233622.4546216484 | -411783.492012748 |

![](./org.apache.commons.io.FileUtilsCleanSymlinksTestCase-graph.png)

## org.apache.commons.io.FileDeleteStrategyTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileDeleteStrategyTestCase-testDeleteForce | 680333.6554852668 | 553052.7449840959 | 127280.9105011709 | 19825437.12160531 | 18957263.12176095 | 868173.9998443611 |

![](./org.apache.commons.io.FileDeleteStrategyTestCase-graph.png)

## org.apache.commons.io.filefilter.FileFilterTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.filefilter.FileFilterTestCase-testEmpty | 617392.2468906936 | 621655.3791398075 | -4263.132249113987 | 24194439.842617948 | 21073393.412022356 | 3121046.4305955917 |

![](./org.apache.commons.io.filefilter.FileFilterTestCase-graph.png)

## org.apache.commons.io.FileUtilsTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileUtilsTestCase-testCopyDirectoryToDirectory_NonExistingDest | 112728.40764928047 | 84377.7140470485 | 28350.69360223197 | 3492472.487059836 | 2891376.751801093 | 601095.7352587427 |
| org.apache.commons.io.FileUtilsTestCase-testCopyDirectoryToNonExistingDest | 414102.76319004584 | 344120.4281374963 | 69982.33505254955 | 11133299.808340639 | 9754776.321036708 | 1378523.4873039313 |
| org.apache.commons.io.FileUtilsTestCase-testForceDeleteAFile2 | 36722.816614757205 | 34982.652663923815 | 1740.1639508333901 | 1046991.6745947524 | 745503.8858785073 | 301487.7887162451 |
| org.apache.commons.io.FileUtilsTestCase-testForceDeleteAFile3 | 38873.56892710138 | 36402.47026622041 | 2471.0986608809762 | 1257196.2481262612 | 1023261.7747935597 | 233934.47333270148 |
| org.apache.commons.io.FileUtilsTestCase-testCopyDirectoryPreserveDates | 274448.98676744406 | 261309.75437138564 | 13139.232396058418 | 7052492.649105699 | 6951254.34934257 | 101238.2997631291 |
| org.apache.commons.io.FileUtilsTestCase-testForceDeleteDir | 40239.904454733 | 39310.14569867301 | 929.7587560599859 | 913651.8223445385 | 1041378.4800523263 | -127726.65770778782 |
| org.apache.commons.io.FileUtilsTestCase-testForceDeleteReadOnlyFile | 241211.2055544424 | 226325.94024597196 | 14885.265308470436 | 6848312.622000558 | 6155528.932823666 | 692783.6891768919 |
| org.apache.commons.io.FileUtilsTestCase-testDeleteQuietlyDir | 40771.76801660817 | 37483.109099739166 | 3288.6589168690043 | 1036240.3397962234 | 789787.0619924413 | 246453.27780378214 |
| org.apache.commons.io.FileUtilsTestCase-testMoveDirectory_CopyDelete | 56899.20928271371 | 54986.10150451002 | 1913.1077782036882 | 1483174.4534104879 | 1472671.1490425067 | 10503.304367981153 |
| org.apache.commons.io.FileUtilsTestCase-testForceDeleteAFile1 | 35057.92217783495 | 35065.0054096267 | -7.083231791744765 | 994038.2453913454 | 1019223.1509885115 | -25184.90559716616 |

![](./org.apache.commons.io.FileUtilsTestCase-graph.png)

## org.apache.commons.io.FileUtilsCleanDirectoryTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileUtilsCleanDirectoryTestCase-testThrowsOnCannotDeleteFile | 246759.10412088135 | 277581.1145449161 | -30822.01042403473 | 10400831.400092177 | 10534355.723674387 | -133524.32358220965 |
| org.apache.commons.io.FileUtilsCleanDirectoryTestCase-testDeletesNested | 79639.03690188305 | 65532.363626916056 | 14106.673274966997 | 2829749.8407181487 | 2764171.058394637 | 65578.78232351178 |
| org.apache.commons.io.FileUtilsCleanDirectoryTestCase-testDeletesRegular | 484031.4997149602 | 477051.0056940848 | 6980.494020875427 | 15628747.128138065 | 15846480.986972226 | -217733.8588341605 |

![](./org.apache.commons.io.FileUtilsCleanDirectoryTestCase-graph.png)

## org.apache.commons.io.FileCleaningTrackerTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileCleaningTrackerTestCase-testFileCleanerDirectory_ForceStrategy | 6969212.130210134 | 6995408.161440964 | -26196.031230829656 | 532935350.8319085 | 534326109.1227176 | -1390758.290809095 |

![](./org.apache.commons.io.FileCleaningTrackerTestCase-graph.png)

## org.apache.commons.io.monitor.FileAlterationObserverTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.monitor.FileAlterationObserverTestCase-testDirectory | 18272140.150146745 | 10616591.112064661 | 7655549.038082084 | 1141808196.3657005 | 872309374.1574292 | 269498822.20827127 |

![](./org.apache.commons.io.monitor.FileAlterationObserverTestCase-graph.png)

## org.apache.commons.io.FileCleanerTestCase

| Test | EnergyV1 | EnergyV2 | DeltaEnergy | DurationV1 | DurationsV2 | DeltaDuration |
| --- | --- | --- | --- | --- | --- | --- |
| org.apache.commons.io.FileCleanerTestCase-testFileCleanerDirectory_ForceStrategy | 6984719.822459599 | 7125686.290798358 | -140966.46833875868 | 536963094.8691577 | 532973723.7827536 | 3989371.086404085 |

![](./org.apache.commons.io.FileCleanerTestCase-graph.png)

