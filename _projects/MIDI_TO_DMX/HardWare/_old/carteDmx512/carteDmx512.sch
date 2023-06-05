EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Interface_UART:MAX485E U3
U 1 1 6018535A
P 4750 5050
F 0 "U3" H 4950 5400 50  0000 C CNN
F 1 "MAX485" H 4750 5250 50  0000 C CNN
F 2 "Package_DIP:DIP-8_W7.62mm_Socket_LongPads" H 4750 4350 50  0001 C CNN
F 3 "" H 4750 5100 50  0001 C CNN
	1    4750 5050
	1    0    0    -1  
$EndComp
$Comp
L 4xxx_IEEE:4011 U1
U 4 1 6018989A
P 4100 3350
F 0 "U1" H 4350 3650 50  0000 L CNN
F 1 "4011" H 4350 3550 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 4100 3350 50  0001 C CNN
F 3 "" H 4100 3350 50  0001 C CNN
	4    4100 3350
	1    0    0    -1  
$EndComp
Text GLabel 1200 3700 0    50   Input ~ 0
5V
Text GLabel 1900 3700 2    50   Input ~ 0
5V
Text GLabel 4100 3050 1    50   Input ~ 0
5V
Text GLabel 4650 4500 0    50   Input ~ 0
5V
$Comp
L power:GND #PWR03
U 1 1 6018C0BF
P 1900 3900
F 0 "#PWR03" H 1900 3650 50  0001 C CNN
F 1 "GND" V 1905 3772 50  0000 R CNN
F 2 "" H 1900 3900 50  0001 C CNN
F 3 "" H 1900 3900 50  0001 C CNN
	1    1900 3900
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR02
U 1 1 6018C80F
P 1200 3900
F 0 "#PWR02" H 1200 3650 50  0001 C CNN
F 1 "GND" V 1205 3772 50  0000 R CNN
F 2 "" H 1200 3900 50  0001 C CNN
F 3 "" H 1200 3900 50  0001 C CNN
	1    1200 3900
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR07
U 1 1 6018CA32
P 4750 5750
F 0 "#PWR07" H 4750 5500 50  0001 C CNN
F 1 "GND" H 4755 5577 50  0000 C CNN
F 2 "" H 4750 5750 50  0001 C CNN
F 3 "" H 4750 5750 50  0001 C CNN
	1    4750 5750
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR06
U 1 1 6018CE50
P 4100 3650
F 0 "#PWR06" H 4100 3400 50  0001 C CNN
F 1 "GND" H 4105 3477 50  0000 C CNN
F 2 "" H 4100 3650 50  0001 C CNN
F 3 "" H 4100 3650 50  0001 C CNN
	1    4100 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4100 3650 4100 3550
Wire Wire Line
	4100 3150 4100 3050
Wire Wire Line
	4750 4550 4750 4500
Wire Wire Line
	4750 4500 4650 4500
Wire Wire Line
	4750 5750 4750 5700
Wire Wire Line
	1200 3800 1300 3800
Wire Wire Line
	1200 3900 1300 3900
Wire Wire Line
	1800 3800 1900 3800
Wire Wire Line
	1800 3900 1900 3900
Text GLabel 1200 4000 0    50   Input ~ 0
TX
Text GLabel 1900 4100 2    50   Input ~ 0
start
Text GLabel 1900 4200 2    50   Input ~ 0
out_s
Text GLabel 1900 4400 2    50   Input ~ 0
AnInR
Text GLabel 1900 4500 2    50   Input ~ 0
AnInG
Text GLabel 1900 4600 2    50   Input ~ 0
AnInB
Text GLabel 1900 3800 2    50   Input ~ 0
3.3V
$Comp
L Device:R_POT RV3
U 1 1 6018DF95
P 3300 1300
F 0 "RV3" H 3230 1346 50  0000 R CNN
F 1 "PotB" H 3230 1255 50  0000 R CNN
F 2 "Potentiometer_THT:Potentiometer_Vishay_T73YP_Vertical" H 3300 1300 50  0001 C CNN
F 3 "~" H 3300 1300 50  0001 C CNN
	1    3300 1300
	1    0    0    -1  
$EndComp
$Comp
L Device:R_POT RV1
U 1 1 6018EFA6
P 1350 1300
F 0 "RV1" H 1280 1346 50  0000 R CNN
F 1 "PotR" H 1280 1255 50  0000 R CNN
F 2 "Potentiometer_THT:Potentiometer_Vishay_T73YP_Vertical" H 1350 1300 50  0001 C CNN
F 3 "~" H 1350 1300 50  0001 C CNN
	1    1350 1300
	1    0    0    -1  
$EndComp
$Comp
L Device:R_POT RV2
U 1 1 6018F437
P 2350 1300
F 0 "RV2" H 2280 1346 50  0000 R CNN
F 1 "PotG" H 2280 1255 50  0000 R CNN
F 2 "Potentiometer_THT:Potentiometer_Vishay_T73YP_Vertical" H 2350 1300 50  0001 C CNN
F 3 "~" H 2350 1300 50  0001 C CNN
	1    2350 1300
	1    0    0    -1  
$EndComp
Text GLabel 1600 1300 2    50   Input ~ 0
AnInR
Text GLabel 2600 1300 2    50   Input ~ 0
AnInG
Text GLabel 3550 1300 2    50   Input ~ 0
AnInB
Text GLabel 1350 1050 1    50   Input ~ 0
3.3V
Text GLabel 2350 1050 1    50   Input ~ 0
3.3V
Text GLabel 3300 1050 1    50   Input ~ 0
3.3V
$Comp
L power:GND #PWR01
U 1 1 60190E29
P 1350 1550
F 0 "#PWR01" H 1350 1300 50  0001 C CNN
F 1 "GND" H 1355 1377 50  0000 C CNN
F 2 "" H 1350 1550 50  0001 C CNN
F 3 "" H 1350 1550 50  0001 C CNN
	1    1350 1550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 601912B1
P 2350 1550
F 0 "#PWR04" H 2350 1300 50  0001 C CNN
F 1 "GND" H 2355 1377 50  0000 C CNN
F 2 "" H 2350 1550 50  0001 C CNN
F 3 "" H 2350 1550 50  0001 C CNN
	1    2350 1550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR05
U 1 1 60191487
P 3300 1550
F 0 "#PWR05" H 3300 1300 50  0001 C CNN
F 1 "GND" H 3305 1377 50  0000 C CNN
F 2 "" H 3300 1550 50  0001 C CNN
F 3 "" H 3300 1550 50  0001 C CNN
	1    3300 1550
	1    0    0    -1  
$EndComp
Wire Wire Line
	1350 1550 1350 1450
Wire Wire Line
	1350 1150 1350 1050
Wire Wire Line
	1500 1300 1600 1300
Wire Wire Line
	2350 1150 2350 1050
Wire Wire Line
	2500 1300 2600 1300
Wire Wire Line
	2350 1550 2350 1450
Wire Wire Line
	3300 1550 3300 1450
Wire Wire Line
	3450 1300 3550 1300
Wire Wire Line
	3300 1150 3300 1050
$Comp
L Connector_Generic:Conn_02x10_Odd_Even J1
U 1 1 60192F27
P 1500 4100
F 0 "J1" H 1550 4717 50  0000 C CNN
F 1 "Conn_02x10_Odd_Even" H 1550 4626 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x10_P2.54mm_Vertical" H 1500 4100 50  0001 C CNN
F 3 "~" H 1500 4100 50  0001 C CNN
	1    1500 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	1800 3700 1900 3700
Wire Wire Line
	1200 3700 1300 3700
Wire Wire Line
	1800 4100 1900 4100
Wire Wire Line
	1800 4000 1900 4000
Wire Wire Line
	1800 4200 1900 4200
Wire Wire Line
	1800 4300 1900 4300
Wire Wire Line
	1800 4400 1900 4400
Wire Wire Line
	1800 4500 1900 4500
Wire Wire Line
	1800 4600 1900 4600
$Comp
L Connector_Generic:Conn_02x03_Odd_Even J3
U 1 1 60199F28
P 6100 5050
F 0 "J3" H 6150 5250 50  0000 C CNN
F 1 "To_Dmx" H 6150 4850 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x03_P2.54mm_Vertical" H 6100 5050 50  0001 C CNN
F 3 "~" H 6100 5050 50  0001 C CNN
	1    6100 5050
	1    0    0    -1  
$EndComp
Wire Wire Line
	5150 4950 5300 4950
Wire Wire Line
	5150 5250 5300 5250
Wire Wire Line
	5450 5250 5450 5050
Wire Wire Line
	5450 5050 5700 5050
Wire Wire Line
	4750 5700 5550 5700
Wire Wire Line
	5550 5700 5550 5150
Wire Wire Line
	5550 5150 5850 5150
Connection ~ 4750 5700
Wire Wire Line
	4750 5700 4750 5650
Wire Wire Line
	6400 5150 6400 5300
Wire Wire Line
	6400 5300 5850 5300
Wire Wire Line
	5850 5300 5850 5150
Connection ~ 5850 5150
Wire Wire Line
	5850 5150 5900 5150
Wire Wire Line
	5850 4950 5850 4800
Wire Wire Line
	5850 4800 6450 4800
Wire Wire Line
	6450 4800 6450 4950
Wire Wire Line
	6450 4950 6400 4950
Connection ~ 5850 4950
Wire Wire Line
	5850 4950 5900 4950
Wire Wire Line
	6400 5050 6500 5050
Wire Wire Line
	6500 5050 6500 4750
Wire Wire Line
	6500 4750 5700 4750
Wire Wire Line
	5700 4750 5700 5050
Connection ~ 5700 5050
Wire Wire Line
	5700 5050 5900 5050
$Comp
L Device:R R1
U 1 1 6019E031
P 5300 5100
F 0 "R1" H 5370 5146 50  0000 L CNN
F 1 "120" H 5370 5055 50  0000 L CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P15.24mm_Horizontal" V 5230 5100 50  0001 C CNN
F 3 "~" H 5300 5100 50  0001 C CNN
	1    5300 5100
	1    0    0    -1  
$EndComp
Connection ~ 5300 4950
Wire Wire Line
	5300 4950 5850 4950
Connection ~ 5300 5250
Wire Wire Line
	5300 5250 5450 5250
Text GLabel 3450 3350 0    50   Input ~ 0
start
Wire Wire Line
	3450 3350 3500 3350
Wire Wire Line
	3500 3350 3500 3250
Wire Wire Line
	3500 3250 3600 3250
Wire Wire Line
	3500 3350 3500 3450
Wire Wire Line
	3500 3450 3600 3450
Connection ~ 3500 3350
Text GLabel 4700 3300 1    50   Input ~ 0
notstart
Wire Wire Line
	4600 3350 4700 3350
Text GLabel 3450 2450 0    50   Input ~ 0
start
Text GLabel 3450 2250 0    50   Input ~ 0
out_s
Wire Wire Line
	3450 2250 3600 2250
Wire Wire Line
	3450 2450 3600 2450
$Comp
L 4xxx_IEEE:4011 U1
U 2 1 601A3E2D
P 5600 3250
F 0 "U1" H 5850 3550 50  0000 L CNN
F 1 "4011" H 5850 3450 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 5600 3250 50  0001 C CNN
F 3 "" H 5600 3250 50  0001 C CNN
	2    5600 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	4700 3300 4700 3350
Connection ~ 4700 3350
Text GLabel 5000 3150 0    50   Input ~ 0
TX
Wire Wire Line
	4700 3350 5100 3350
Wire Wire Line
	5000 3150 5100 3150
$Comp
L 4xxx_IEEE:4011 U2
U 2 1 601A8B96
P 6750 3250
F 0 "U2" H 7000 3550 50  0000 L CNN
F 1 "4011" H 7000 3450 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 6750 3250 50  0001 C CNN
F 3 "" H 6750 3250 50  0001 C CNN
	2    6750 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6100 3250 6150 3250
Wire Wire Line
	6150 3250 6150 3150
Wire Wire Line
	6150 3150 6250 3150
Wire Wire Line
	6150 3250 6150 3350
Wire Wire Line
	6150 3350 6250 3350
Connection ~ 6150 3250
$Comp
L 4xxx_IEEE:4011 U2
U 4 1 601ABF92
P 7850 2450
F 0 "U2" H 8100 2750 50  0000 L CNN
F 1 "4011" H 8100 2650 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 7850 2450 50  0001 C CNN
F 3 "" H 7850 2450 50  0001 C CNN
	4    7850 2450
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 3250 7300 3250
Wire Wire Line
	7300 3250 7300 2550
Wire Wire Line
	7300 2550 7350 2550
Wire Wire Line
	7350 2350 4600 2350
$Comp
L 4xxx_IEEE:4011 U1
U 1 1 601A142D
P 4100 2350
F 0 "U1" H 4350 2650 50  0000 L CNN
F 1 "4011" H 4350 2550 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 4100 2350 50  0001 C CNN
F 3 "" H 4100 2350 50  0001 C CNN
	1    4100 2350
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 601B1E58
P 8950 2550
F 0 "J2" H 9030 2592 50  0000 L CNN
F 1 "Conn_01x03" H 9030 2501 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 8950 2550 50  0001 C CNN
F 3 "~" H 8950 2550 50  0001 C CNN
	1    8950 2550
	1    0    0    -1  
$EndComp
$Comp
L 4xxx_IEEE:4011 U2
U 3 1 601B2BA9
P 8100 3400
F 0 "U2" H 8350 3700 50  0000 L CNN
F 1 "4011" H 8350 3600 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_Socket_LongPads" H 8100 3400 50  0001 C CNN
F 3 "" H 8100 3400 50  0001 C CNN
	3    8100 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	7600 3300 7550 3300
Wire Wire Line
	7550 3300 7550 3500
Wire Wire Line
	7550 3500 7600 3500
Wire Wire Line
	8600 3400 8650 3400
Wire Wire Line
	7550 3300 7550 2800
Wire Wire Line
	7550 2800 8350 2800
Wire Wire Line
	8350 2800 8350 2450
Connection ~ 7550 3300
Connection ~ 8350 2450
Text GLabel 8700 2550 0    50   Input ~ 0
DMX_TX
Wire Wire Line
	8350 2450 8750 2450
Wire Wire Line
	8750 2550 8700 2550
Wire Wire Line
	8750 2650 8650 2650
Wire Wire Line
	8650 2650 8650 3400
Text GLabel 1900 4300 2    50   Input ~ 0
enable
Text GLabel 4250 5150 0    50   Input ~ 0
enable
Wire Wire Line
	4250 5150 4350 5150
Text GLabel 4250 5250 0    50   Input ~ 0
DMX_TX
Wire Wire Line
	4350 5250 4250 5250
Text GLabel 4250 5050 0    50   Input ~ 0
5V
Wire Wire Line
	4250 5050 4350 5050
$Comp
L Device:R R2
U 1 1 601C92C8
P 4100 4950
F 0 "R2" V 3893 4950 50  0000 C CNN
F 1 "120" V 3984 4950 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0309_L9.0mm_D3.2mm_P15.24mm_Horizontal" V 4030 4950 50  0001 C CNN
F 3 "~" H 4100 4950 50  0001 C CNN
	1    4100 4950
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR08
U 1 1 601C960D
P 3850 4950
F 0 "#PWR08" H 3850 4700 50  0001 C CNN
F 1 "GND" V 3855 4822 50  0000 R CNN
F 2 "" H 3850 4950 50  0001 C CNN
F 3 "" H 3850 4950 50  0001 C CNN
	1    3850 4950
	0    1    1    0   
$EndComp
Wire Wire Line
	3850 4950 3950 4950
Wire Wire Line
	4250 4950 4350 4950
$Comp
L power:GND #PWR09
U 1 1 601DB75A
P 8100 3700
F 0 "#PWR09" H 8100 3450 50  0001 C CNN
F 1 "GND" H 8105 3527 50  0000 C CNN
F 2 "" H 8100 3700 50  0001 C CNN
F 3 "" H 8100 3700 50  0001 C CNN
	1    8100 3700
	1    0    0    -1  
$EndComp
Text GLabel 8100 3100 1    50   Input ~ 0
5V
Wire Wire Line
	8100 3200 8100 3100
Wire Wire Line
	8100 3700 8100 3600
Text GLabel 1900 4000 2    50   Input ~ 0
TX
Text GLabel 1200 4300 0    50   Input ~ 0
enable
Text GLabel 1200 4100 0    50   Input ~ 0
start
Text GLabel 1200 4200 0    50   Input ~ 0
out_s
Text GLabel 1200 4400 0    50   Input ~ 0
AnInR
Text GLabel 1200 4500 0    50   Input ~ 0
AnInG
Text GLabel 1200 4600 0    50   Input ~ 0
AnInB
Wire Wire Line
	1200 4000 1300 4000
Wire Wire Line
	1200 4100 1300 4100
Wire Wire Line
	1200 4200 1300 4200
Wire Wire Line
	1200 4300 1300 4300
Wire Wire Line
	1200 4400 1300 4400
Wire Wire Line
	1200 4500 1300 4500
Wire Wire Line
	1200 4600 1300 4600
Text GLabel 4100 2050 1    50   Input ~ 0
5V
Text GLabel 5600 2950 1    50   Input ~ 0
5V
Text GLabel 6750 2950 1    50   Input ~ 0
5V
Text GLabel 7850 2150 1    50   Input ~ 0
5V
$Comp
L power:GND #PWR0101
U 1 1 601FA927
P 5600 3550
F 0 "#PWR0101" H 5600 3300 50  0001 C CNN
F 1 "GND" H 5605 3377 50  0000 C CNN
F 2 "" H 5600 3550 50  0001 C CNN
F 3 "" H 5600 3550 50  0001 C CNN
	1    5600 3550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 601FABBA
P 6750 3550
F 0 "#PWR0102" H 6750 3300 50  0001 C CNN
F 1 "GND" H 6755 3377 50  0000 C CNN
F 2 "" H 6750 3550 50  0001 C CNN
F 3 "" H 6750 3550 50  0001 C CNN
	1    6750 3550
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 601FADED
P 4100 2650
F 0 "#PWR0103" H 4100 2400 50  0001 C CNN
F 1 "GND" H 4105 2477 50  0000 C CNN
F 2 "" H 4100 2650 50  0001 C CNN
F 3 "" H 4100 2650 50  0001 C CNN
	1    4100 2650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0104
U 1 1 601FB0CB
P 7850 2750
F 0 "#PWR0104" H 7850 2500 50  0001 C CNN
F 1 "GND" H 7855 2577 50  0000 C CNN
F 2 "" H 7850 2750 50  0001 C CNN
F 3 "" H 7850 2750 50  0001 C CNN
	1    7850 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7850 2750 7850 2650
Wire Wire Line
	7850 2250 7850 2150
Wire Wire Line
	4100 2050 4100 2150
Wire Wire Line
	4100 2550 4100 2650
Wire Wire Line
	5600 3050 5600 2950
Wire Wire Line
	5600 3550 5600 3450
Wire Wire Line
	6750 3550 6750 3450
Wire Wire Line
	6750 3050 6750 2950
Text GLabel 1200 3800 0    50   Input ~ 0
3.3V
$EndSCHEMATC
