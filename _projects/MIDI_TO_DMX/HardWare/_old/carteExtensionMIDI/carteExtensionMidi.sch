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
Text GLabel 8400 1600 1    50   Input ~ 0
5V
Text GLabel 7600 2700 0    50   Input ~ 0
out_s
Text GLabel 8800 3300 2    50   Input ~ 0
AnInR
Text GLabel 8300 1600 1    50   Input ~ 0
3.3V
Text GLabel 8100 1600 1    50   Input ~ 0
Vinput
Text GLabel 7600 2600 0    50   Input ~ 0
start
Text GLabel 7600 2800 0    50   Input ~ 0
enable
$Comp
L Connector_Generic:Conn_02x04_Odd_Even J8
U 1 1 614A2725
P 5350 1700
F 0 "J8" H 5400 2017 50  0000 C CNN
F 1 "Conn_02x04_Odd_Even" H 5400 1926 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x04_P2.54mm_Vertical" H 5350 1700 50  0001 C CNN
F 3 "~" H 5350 1700 50  0001 C CNN
	1    5350 1700
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR02
U 1 1 614A32F7
P 5050 1600
F 0 "#PWR02" H 5050 1350 50  0001 C CNN
F 1 "GND" H 5055 1427 50  0000 C CNN
F 2 "" H 5050 1600 50  0001 C CNN
F 3 "" H 5050 1600 50  0001 C CNN
	1    5050 1600
	0    1    1    0   
$EndComp
Wire Wire Line
	5050 1600 5150 1600
Text GLabel 5750 1600 2    50   Input ~ 0
3.3V
Wire Wire Line
	5650 1600 5750 1600
Text GLabel 5050 1700 0    50   Input ~ 0
CE_nrF
Text GLabel 5050 1800 0    50   Input ~ 0
SCK_nrF
Text GLabel 5050 1900 0    50   Input ~ 0
MISO_nrF
Text GLabel 5750 1900 2    50   Input ~ 0
IRQ_nrF
Text GLabel 5750 1800 2    50   Input ~ 0
MOSI_nrF
Text GLabel 5750 1700 2    50   Input ~ 0
CSN_nrF
Wire Wire Line
	5050 1700 5150 1700
Wire Wire Line
	5650 1700 5750 1700
Wire Wire Line
	5050 1800 5150 1800
Wire Wire Line
	5650 1800 5750 1800
Wire Wire Line
	5050 1900 5150 1900
Wire Wire Line
	5650 1900 5750 1900
$Comp
L power:GND #PWR0106
U 1 1 615634FF
P 8300 4000
F 0 "#PWR0106" H 8300 3750 50  0001 C CNN
F 1 "GND" H 8305 3827 50  0000 C CNN
F 2 "" H 8300 4000 50  0001 C CNN
F 3 "" H 8300 4000 50  0001 C CNN
	1    8300 4000
	1    0    0    -1  
$EndComp
$Comp
L Device:R R1
U 1 1 618CCFF3
P 2350 2950
F 0 "R1" V 2143 2950 50  0000 C CNN
F 1 "220" V 2234 2950 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 2280 2950 50  0001 C CNN
F 3 "~" H 2350 2950 50  0001 C CNN
	1    2350 2950
	0    1    1    0   
$EndComp
$Comp
L Diode:1N4148 D1
U 1 1 618CDD43
P 2650 3200
F 0 "D1" V 2600 3000 50  0000 L CNN
F 1 "1N4148" V 2700 2800 50  0000 L CNN
F 2 "Diode_THT:D_DO-35_SOD27_P7.62mm_Horizontal" H 2650 3025 50  0001 C CNN
F 3 "https://assets.nexperia.com/documents/data-sheet/1N4148_1N4448.pdf" H 2650 3200 50  0001 C CNN
	1    2650 3200
	0    1    1    0   
$EndComp
$Comp
L Connector:DIN-5 J2
U 1 1 618D10E0
P 5800 4100
F 0 "J2" V 5754 3870 50  0000 R CNN
F 1 "MIDI_OUT" V 5845 3870 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 5800 4100 50  0001 C CNN
F 3 "http://www.mouser.com/ds/2/18/40_c091_abd_e-75918.pdf" H 5800 4100 50  0001 C CNN
	1    5800 4100
	0    1    1    0   
$EndComp
Text GLabel 8800 3100 2    50   Input ~ 0
PitchIn
Text GLabel 8800 2800 2    50   Input ~ 0
DMX_TX
Text GLabel 8800 3200 2    50   Input ~ 0
VolumeIn_Adapt
Wire Wire Line
	8300 4000 8300 3950
Connection ~ 8300 3950
Wire Wire Line
	8300 3950 8300 3900
Wire Wire Line
	8200 3900 8200 3950
Wire Wire Line
	8200 3950 8300 3950
Wire Wire Line
	7600 2600 7700 2600
Wire Wire Line
	7600 2700 7700 2700
Wire Wire Line
	7600 2800 7700 2800
Wire Wire Line
	8700 2800 8800 2800
Wire Wire Line
	8700 3100 8800 3100
Wire Wire Line
	8700 3200 8800 3200
Wire Wire Line
	8700 3300 8800 3300
Wire Wire Line
	8100 1600 8100 1800
Wire Wire Line
	8300 1600 8300 1800
Wire Wire Line
	8400 1600 8400 1800
Wire Wire Line
	1750 3600 1750 3650
Wire Wire Line
	1750 3650 2650 3650
Wire Wire Line
	2650 3650 2650 3350
Wire Wire Line
	2800 3150 2800 3650
Wire Wire Line
	2800 3650 2650 3650
Connection ~ 2650 3650
Wire Wire Line
	2500 2950 2650 2950
Wire Wire Line
	2650 2950 2650 3050
Wire Wire Line
	2650 2950 2800 2950
Connection ~ 2650 2950
Wire Wire Line
	2200 2950 1750 2950
Wire Wire Line
	1750 2950 1750 3000
$Comp
L Isolator:CNY17-1 U1
U 1 1 618CC0D8
P 3100 3050
F 0 "U1" H 3100 3375 50  0000 C CNN
F 1 "CNY17_1" H 3100 3284 50  0000 C CNN
F 2 "Package_DIP:DIP-6_W7.62mm_LongPads" H 3100 3050 50  0001 L CNN
F 3 "" H 3100 3050 50  0001 L CNN
	1    3100 3050
	1    0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 618E0399
P 3550 2800
F 0 "R2" H 3480 2754 50  0000 R CNN
F 1 "1.2k" H 3480 2845 50  0000 R CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 3480 2800 50  0001 C CNN
F 3 "~" H 3550 2800 50  0001 C CNN
	1    3550 2800
	-1   0    0    1   
$EndComp
Text GLabel 3550 2550 1    50   Input ~ 0
3.3V
Text GLabel 3700 3050 2    50   Input ~ 0
MIDI_IN_RX
Wire Wire Line
	3550 2950 3550 3050
Wire Wire Line
	3400 3050 3550 3050
Wire Wire Line
	3550 3050 3700 3050
Connection ~ 3550 3050
Wire Wire Line
	3550 2650 3550 2550
$Comp
L power:GND #PWR01
U 1 1 618E28F4
P 3450 3250
F 0 "#PWR01" H 3450 3000 50  0001 C CNN
F 1 "GND" H 3455 3077 50  0000 C CNN
F 2 "" H 3450 3250 50  0001 C CNN
F 3 "" H 3450 3250 50  0001 C CNN
	1    3450 3250
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 3150 3450 3150
Wire Wire Line
	3450 3150 3450 3250
$Comp
L Connector:DIN-5 J1
U 1 1 618E93AF
P 1650 3300
F 0 "J1" V 1604 3071 50  0000 R CNN
F 1 "MIDI_IN" V 1695 3071 50  0000 R CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x05_P2.54mm_Vertical" H 1650 3300 50  0001 C CNN
F 3 "http://www.mouser.com/ds/2/18/40_c091_abd_e-75918.pdf" H 1650 3300 50  0001 C CNN
	1    1650 3300
	0    1    1    0   
$EndComp
$Comp
L Device:R R3
U 1 1 618EA274
P 5650 3650
F 0 "R3" V 5443 3650 50  0000 C CNN
F 1 "220" V 5534 3650 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5580 3650 50  0001 C CNN
F 3 "~" H 5650 3650 50  0001 C CNN
	1    5650 3650
	0    1    1    0   
$EndComp
$Comp
L Device:R R4
U 1 1 618EAB13
P 5650 4650
F 0 "R4" V 5443 4650 50  0000 C CNN
F 1 "220" V 5534 4650 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal" V 5580 4650 50  0001 C CNN
F 3 "~" H 5650 4650 50  0001 C CNN
	1    5650 4650
	0    1    1    0   
$EndComp
Wire Wire Line
	5800 3650 5900 3650
Wire Wire Line
	5900 3650 5900 3800
Wire Wire Line
	5800 4650 5900 4650
Wire Wire Line
	5900 4650 5900 4400
$Comp
L power:GND #PWR05
U 1 1 618EC38D
P 6150 4150
F 0 "#PWR05" H 6150 3900 50  0001 C CNN
F 1 "GND" H 6155 3977 50  0000 C CNN
F 2 "" H 6150 4150 50  0001 C CNN
F 3 "" H 6150 4150 50  0001 C CNN
	1    6150 4150
	1    0    0    -1  
$EndComp
Text GLabel 5400 3650 0    50   Input ~ 0
5V
Wire Wire Line
	5400 3650 5500 3650
Wire Wire Line
	6100 4100 6150 4100
Wire Wire Line
	6150 4100 6150 4150
$Comp
L 4xxx_IEEE:4011 U2
U 1 1 618EE970
P 3750 4650
F 0 "U2" H 3900 5000 50  0000 L CNN
F 1 "4011" H 3900 4900 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_LongPads" H 3750 4650 50  0001 C CNN
F 3 "" H 3750 4650 50  0001 C CNN
	1    3750 4650
	1    0    0    -1  
$EndComp
$Comp
L 4xxx_IEEE:4011 U2
U 2 1 618F06E3
P 4900 4650
F 0 "U2" H 5050 5000 50  0000 L CNN
F 1 "4011" H 5050 4900 50  0000 L CNN
F 2 "Package_DIP:DIP-14_W7.62mm_LongPads" H 4900 4650 50  0001 C CNN
F 3 "" H 4900 4650 50  0001 C CNN
	2    4900 4650
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR03
U 1 1 618F160C
P 3750 4950
F 0 "#PWR03" H 3750 4700 50  0001 C CNN
F 1 "GND" H 3755 4777 50  0000 C CNN
F 2 "" H 3750 4950 50  0001 C CNN
F 3 "" H 3750 4950 50  0001 C CNN
	1    3750 4950
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR04
U 1 1 618F1B56
P 4900 4950
F 0 "#PWR04" H 4900 4700 50  0001 C CNN
F 1 "GND" H 4905 4777 50  0000 C CNN
F 2 "" H 4900 4950 50  0001 C CNN
F 3 "" H 4900 4950 50  0001 C CNN
	1    4900 4950
	1    0    0    -1  
$EndComp
Text GLabel 3750 4350 1    50   Input ~ 0
5V
Text GLabel 4900 4350 1    50   Input ~ 0
5V
Wire Wire Line
	5400 4650 5500 4650
Wire Wire Line
	4250 4650 4350 4650
Wire Wire Line
	4350 4650 4350 4550
Wire Wire Line
	4350 4550 4400 4550
Wire Wire Line
	4350 4650 4350 4750
Wire Wire Line
	4350 4750 4400 4750
Connection ~ 4350 4650
Text GLabel 3150 4650 0    50   Input ~ 0
MIDI_OUT_TX
Wire Wire Line
	3150 4650 3200 4650
Wire Wire Line
	3200 4650 3200 4550
Wire Wire Line
	3200 4550 3250 4550
Wire Wire Line
	3200 4650 3200 4750
Wire Wire Line
	3200 4750 3250 4750
Connection ~ 3200 4650
Text GLabel 7600 2400 0    50   Input ~ 0
MIDI_IN_RX
Text GLabel 7600 3000 0    50   Input ~ 0
MIDI_OUT_TX
Text GLabel 7600 3500 0    50   Input ~ 0
SCK_nrF
Text GLabel 7600 3400 0    50   Input ~ 0
MISO_nrF
Text GLabel 7600 3300 0    50   Input ~ 0
MOSI_nrF
Wire Wire Line
	7600 3300 7700 3300
Wire Wire Line
	7600 3400 7700 3400
Wire Wire Line
	7600 3500 7700 3500
Wire Wire Line
	7600 2400 7700 2400
Wire Wire Line
	7600 3000 7700 3000
Text GLabel 7600 3100 0    50   Input ~ 0
CE_nrF
Text GLabel 8800 3600 2    50   Input ~ 0
IRQ_nrF
Text GLabel 7600 3200 0    50   Input ~ 0
CSN_nrF
Wire Wire Line
	7600 2900 7700 2900
Wire Wire Line
	7600 3100 7700 3100
Wire Wire Line
	7600 3200 7700 3200
Wire Wire Line
	4900 4950 4900 4850
Wire Wire Line
	4900 4350 4900 4450
Wire Wire Line
	3750 4350 3750 4450
Wire Wire Line
	3750 4950 3750 4850
Wire Wire Line
	8700 3600 8800 3600
$Comp
L MCU_Module:Arduino_UNO_R3 A1
U 1 1 618C72CF
P 8200 2800
F 0 "A1" H 7850 3750 50  0000 C CNN
F 1 "Arduino_UNO_R3" V 8200 2800 50  0000 C CNN
F 2 "Module:Arduino_UNO_R3" H 8200 2800 50  0001 C CIN
F 3 "https://www.arduino.cc/en/Main/arduinoBoardUno" H 8200 2800 50  0001 C CNN
	1    8200 2800
	1    0    0    -1  
$EndComp
$EndSCHEMATC
