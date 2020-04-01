# Visualization Term Project: AR/VR Representation of ADS-B Data #


## FlightGear Setup ##
Not actual ADS-B formats. But this may be the best we can do.

Add in all the data typical ADS-B data would have for each type.

### Messages ###
From the [FAA Spec](https://www.faa.gov/nextgen/programs/adsb/Archival/media/GDL90_Public_ICD_RevA.PDF).

#### Heartbeat [ OUT ] ####

| Byte # | Name           | Size | Value             |
|-------:|:--------------:|:----:|:------------------|
|     1  | Message ID     |    1 | 0x00 [ Hearbeat ] |
|     2  | Status Byte 1* |    1 | 0x??*             |
|     3  | Status Byte 2**|    1 | 0x??**            |
|   4-5  | Time Stamp     |    2 | Seconds since 0000Z, bits 15-0 (LSB first)|
|   6-7  | Message Counts |    2 | ***               |

##### * Status Byte 1 #####
| Bit # | Name            | Meaning                  |
|------:|:---------------:|:-------------------------|
|     7 | GPS Pos Valid   | 1: Position is available for ADS-B Tx |
|     6 | Maint Req'd     | 1: GDL 90 Maint. Req'd      |
|     5 | IDENT           | 1: IDENT talkback           |
|     4 | Addr Type       | 1: Address type talkback |
|     3 | GPS Batt Low    | 1: GPS Batt low volts    |
|     2 | RATCS           | 1: ATC Services talkback |
|     1 | reserved        | ---                      |
|     0 | UAT Init'd      | 1: GDL 90 is initiailized |

##### ** Status Byte 2 #####
| Bit # | Name            | Meaning                  |
|------:|:---------------:|:-------------------------|
|     7 | Timestamp MSB   | -Seconds since 0000Z bit 16 |
|     6 | CSA Requested   | 1: CSA has been requested |
|     5 | CSA Not Available | CSA Not available      |
|     4 | reserved        | ---                      |
|     3 | reserved        | ---                      |
|     2 | reserved        | ---                      |
|     1 | reserved        | ---                      |
|     0 | UTC OK          | UTC timing is valid      |

##### *** Message Counts #####
> Two bytes are used to report the number of UAT messages received by 
> the GDL 90 during the previous second.

| Bit # | Name            | Meaning                  |
|------:|:---------------:|:-------------------------|
| 15-11 | Count uplink messages received |           |
|    10 | reserved        | ---                      |
|   9-0 | Total number basic and long receptions | Holds at max if > 1023 |

