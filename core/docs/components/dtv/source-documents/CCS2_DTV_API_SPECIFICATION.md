
--- Page 1 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
   
 
API Specification Document  
 
DTV – CCS2  
 
  
  
Author(s):


--- Page 2 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Revision History  
Version  History  Date  
v0.2.0 Initial Release  16/06/2022  
v0.2.1  2.2.5  Signal Status Update  
- Removes TRMPERROR from DtvSignalStatus  08/07/2022  
2.1.3  Channel Up Down  
- Adds additional description  
V0.3.0  2. Service Information  
      - Adds Service Information section  
4.1 Startup Communication Sequence  
     - Adds sequence for application handling on startup  
3.1.4  Select Preset Channe l 
    - Changed parameter name from presetChannelNumber to presetNumber  
3.1.5 Store  Preset Channe l 
    - Changed parameter name from presetChannelNumber to presetNumber  
23/09/2022  3.3.1 Get Preset List  
Adds additional description  
3.1.7 Direct Channel Select  
3.1.8 Dtv Initialize  
3.2.1 Set Auto Tune Mode   
3.2.2 Set Auto Broadcast Search Mod e 
3.2.1 Set Auto Event Relay Mode  
3.2.1 Set Closed Caption Mode  
3.2.1 Set Audio Mode  
3.1.9 Reception Monitor (Test Mode)  
3.2.6 Set Physical Channel  
3.3.3 Get Version Info  
3.3.4 Get Program Info  
3.4.7 Reception Monitor Update (Test Mode)  
3.1.10  Dtv Firmware Update  
3.4.6 Dtv Status Update  
3.4.8 Dtv Firmware Update  
3.3.5  Get RMP Manufacturer Id  
Added  new sequences  
4.8 Dtv Status Update  
4.9 Direct Channel Select  
4.10 Dtv Initi alize 
4.11 Dtv Settings Basic  
4.11.1  Get Configure  
4.11.2  Set Auto Tune Mode  
4.11.3  Set Auto Broadcast Search Mode  
4.11.4  Set Auto Event Relay Mode  
4.11.5  Set Closed Caption Mode


--- Page 3 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.11.6  Set Audio Mode  
4.12 Set Physical Channel  
4.13 Reception Monitor (Test Mode)  
3.14 Get Version Info  
4.16 Get RMP Manufacturer Id  
V0.4.0  Updated API  
3.4.5  Signal Status Update  
15/11/2022  Deprecated  API 
3.4.5  Signal Status Update  
Added new API  
3.1.11  Display EPG  
3.1.12  Operate BML  
3.1.13  Forced Exit BML  
3.1.14  Broadcast Search   
3.2.7  Set Residential Area  
3.2.8  Set Audio ES  
3.3.6  Get Audio ES  
3.4.9  Dtv EPG Update  
3.4.10  Broadcast Search Update   
3.4.11  EWS Update  
3.4.12  Dtv Event Update  
Added new sequences  
4.17  Get RMP Manufacturer Id  
4.18  EPG 
4.19  BML Data Broadcast  
4.20  Set Residential Area  
4.21  Audio E S 
4.22  EWS  
4.23  Broadcast Search  
v0.4.1  Added new API  
3.3.7  Get Dtv Module Status  
3.4.13  Dtv Module Status Update  09/12/2022  
Added new sequences  
4.24  Dtv Module Status  
v0.4.2  Added new API  
3.3.8 Get Dtv Antenna State  
3.4.1 4 Dtv Antenna  State Update  
3.5.1  Service Connected   
3.5.2  Service Disconnected  01/02/2023  
Added new sequences  
4.25 Dtv Antenna State  
4.1.1  Dtv Service Connection Notification  
4.1.2  Dtv Service Connected – Handling


--- Page 4 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.1.3  Dtv Service Disconnected – Handling  
V0.4.3  4.11  DTV INITIALIZE  
      - Added additional description  
24/04/2023  Added new API  
3.3.9  Get Current Dtv Module Status  
Deprecated API  
3.3.7  Get Dtv Module Status  
Updated  Sequence  
4.1.2  Dtv Service Connected – Handling  
4.24.1  Get Current Module Status  
V0.4.4  Added new API  
3.6.1  Service Suspended  
3.6.2  Service Resume  
02/08/2023  Added new Sequence  
4.1.4  Dtv Service Initialization Sequence  
4.27.1  Resume  
4.27.2  Suspend  
Updated Sequence  
4.1.2  Dtv Service Connected – Handling  
V0.4.5  3.1.2 Channel Seek  
       - Added the important note for Channel Seek  
       - Updated DTV Status Update API  
3.1.7 Direct Channel Select  
       - Added the decription for the threeDigitNumber  
3.4.6 Dtv Status Update  
       - Update d data type for each items of DtvStatus  
       - Added adit ional information as part of DtvStatus  
3.4.11 EWS Update  
       - Added the important note for EWS Update  
       - Added the activity diagram  for EWS  Update  03/04/2024  
V0.4.6  3.4.8 Dtv Firmware Update  
        - Added information for Application after Firmware Update  completion  
Added new Sequence  
4.14 Dtv Firmware Update  
 25/04/24  
V0.4.7  Updated API  
3.3.8 Get Dtv Antenna State  
3.4.14 Dtv Antenna State Update  07/01/ 2025


--- Page 5 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
  
 
Contents  
REVISION HISTORY  ................................ ................................ ................................ ................................ ..................  2 
1 PURPOSE OF THIS DOCUMENT  ................................ ................................ ................................ ......................  8 
1.1 INTRODUCTION TO THE DOCUMENT  ................................ ................................ ................................ ......................  8 
1.2 SCOPE  ................................ ................................ ................................ ................................ .............................  8 
1.3 CONTEXT  ................................ ................................ ................................ ................................ .........................  8 
2 SERVICE INFORMATION  ................................ ................................ ................................ ................................ . 8 
3 API ................................ ................................ ................................ ................................ ................................ . 8 
3.1 DTV  COMMANDS  ................................ ................................ ................................ ................................ .............  9 
3.1.1  Auto Preset  ................................ ................................ ................................ ................................ ..............  9 
3.1.2  Channel Seek  ................................ ................................ ................................ ................................ ..........  10 
3.1.3  Channel Up Down  ................................ ................................ ................................ ................................ .. 12 
3.1.4  Select Preset Channel  ................................ ................................ ................................ .............................  15 
3.1.5  Store Preset Channel  ................................ ................................ ................................ ..............................  16 
3.1.6  Display Banner  ................................ ................................ ................................ ................................ .......  17 
3.1.7  Direct Channel Select  ................................ ................................ ................................ .............................  18 
3.1.8  Dtv Initialize  ................................ ................................ ................................ ................................ ...........  19 
3.1.9  Reception Monitor (Test Mode)  ................................ ................................ ................................ .............  21 
3.1.10  Dtv Firmware Update  ................................ ................................ ................................ .............................  22 
3.1.11  Display EPG  ................................ ................................ ................................ ................................ ............  22 
3.1.12  Operate BML  ................................ ................................ ................................ ................................ ..........  26 
3.1.13  Forced Exit BML  ................................ ................................ ................................ ................................ ..... 28 
3.1.14  Broadcast Search  ................................ ................................ ................................ ................................ ... 29 
3.2 SET COMMAND  ................................ ................................ ................................ ................................ ..............  31 
3.2.1  Set Auto Tune Mode  ................................ ................................ ................................ ..............................  31 
3.2.2  Set Auto Broadcast Search Mode  ................................ ................................ ................................ ..........  32 
3.2.3  Set Auto Event Relay Mode  ................................ ................................ ................................ ....................  33 
3.2.4  Set Closed Caption Mode  ................................ ................................ ................................ .......................  33 
3.2.5  Set Audio Mode  ................................ ................................ ................................ ................................ ...... 34 
3.2.6  Set Physical Channel  ................................ ................................ ................................ ..............................  35 
3.2.7  Set Residential Area  ................................ ................................ ................................ ...............................  36 
3.2.8  Set Audio ES  ................................ ................................ ................................ ................................ ...........  37 
3.3 GET COMMAND  ................................ ................................ ................................ ................................ ..............  38 
3.3.1  Get Preset List  ................................ ................................ ................................ ................................ ........  38 
3.3.2  Get Configure  ................................ ................................ ................................ ................................ .........  39 
3.3.3  Get Version Info  ................................ ................................ ................................ ................................ ..... 40 
3.3.4  Get Program Info  ................................ ................................ ................................ ................................ ... 41 
3.3.5  Get RMP Manufacturer Id  ................................ ................................ ................................ ......................  42


--- Page 6 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.3.6  Get Audio ES  ................................ ................................ ................................ ................................ ...........  43 
3.3.7  Get Dtv Module Status [DEPRECATED]  ................................ ................................ ................................ .. 44 
3.3.8  Get Dtv Antenna State  ................................ ................................ ................................ ...........................  46 
3.3.9  Get Current Dtv Module Status  ................................ ................................ ................................ ..............  46 
3.4 DTV  EVENTS  ................................ ................................ ................................ ................................ ..................  48 
3.4.1  Auto Preset Update  ................................ ................................ ................................ ................................  48 
3.4.2  Channel Seek Update  ................................ ................................ ................................ .............................  49 
3.4.3  Program Infomation Update  ................................ ................................ ................................ ..................  51 
3.4.4  Preset List Update  ................................ ................................ ................................ ................................ .. 52 
3.4.5  Signal Status Update [DEPRICATED]  ................................ ................................ ................................ ...... 53 
3.4.6  Dtv Status Update  ................................ ................................ ................................ ................................ .. 54 
3.4.7  Reception Monitor Update (Test Mode)  ................................ ................................ ................................  56 
3.4.8  Dtv Firmware Update  ................................ ................................ ................................ .............................  59 
3.4.9  Dtv EPG Update  ................................ ................................ ................................ ................................ ..... 60 
3.4.10  Broadcast Search Update  ................................ ................................ ................................ ......................  60 
3.4.11  EWS Update  ................................ ................................ ................................ ................................ ...........  62 
3.4.12  Dtv Event Update  ................................ ................................ ................................ ................................ ... 64 
3.4.13  Dtv Module Status Update  ................................ ................................ ................................ .....................  66 
3.4.14  Dtv Antenna State Update  ................................ ................................ ................................ .....................  67 
3.5 DTV  SERVICE CONNECTION NOITIFICATION  ................................ ................................ ................................ ..........  67 
3.5.1  Service Connected  ................................ ................................ ................................ ................................ .. 67 
3.5.2  Service Disconnected  ................................ ................................ ................................ .............................  68 
3.6 DTV  SERVICE STATUS NOTIFICATION  ................................ ................................ ................................ ..................  69 
3.6.1  Service Suspended  ................................ ................................ ................................ ................................ .. 69 
3.6.2  Service Resume  ................................ ................................ ................................ ................................ ...... 69 
3.7 DTV  RESULTS  ................................ ................................ ................................ ................................ .................  70 
4 SEQUENCES  ................................ ................................ ................................ ................................ .................  71 
4.1 STARTUP COMMUNICATION SEQUENCE  ................................ ................................ ................................ ...............  71 
4.1.1  Dtv Service Connection Notification  ................................ ................................ ................................ .......  71 
4.1.2  Dtv Service Connected – Handling  ................................ ................................ ................................ .........  72 
4.1.3  Dtv Service Disconnected – Handling  ................................ ................................ ................................ ..... 72 
4.1.4  Dtv Service Initialization Sequence  ................................ ................................ ................................ ........  73 
4.2 AUTO PRESET  ................................ ................................ ................................ ................................ .................  74 
4.2.1  Auto Preset Start  ................................ ................................ ................................ ................................ .... 74 
4.2.2  Auto Preset Stop  ................................ ................................ ................................ ................................ .... 75 
4.3 CHANNEL SEEK ................................ ................................ ................................ ................................ ...............  76 
4.3.1  Channel Seek Up  ................................ ................................ ................................ ................................ .... 76 
4.3.2  Channel Seek Stop  ................................ ................................ ................................ ................................ .. 77 
4.4 CHANNEL UP DOWN ................................ ................................ ................................ ................................ ........  77 
4.5 GET PRESET LIST ................................ ................................ ................................ ................................ .............  78 
4.6 SELECT PRESET CHANNEL  ................................ ................................ ................................ ................................ .. 78 
4.7 STORE PRESET CHANNEL  ................................ ................................ ................................ ................................ .. 79 
4.8 DISPLAY BANNER  ................................ ................................ ................................ ................................ ............  79 
4.9 DTV STATUS UPDATE  ................................ ................................ ................................ ................................ .......  80


--- Page 7 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.10 DIRECT CHANNEL SELECT  ................................ ................................ ................................ ................................ .. 80 
4.11 DTV INITIALIZE  ................................ ................................ ................................ ................................ ................  81 
4.12 DTV SETTINGS BASIC................................ ................................ ................................ ................................ ........  81 
4.12.1  Get Configure  ................................ ................................ ................................ ................................ .........  81 
4.12.2  Set Auto Tune Mode  ................................ ................................ ................................ ..............................  82 
4.12.3  Set Auto Broadcast Search Mode  ................................ ................................ ................................ ..........  82 
4.12.4  Set Auto Event Relay Mode  ................................ ................................ ................................ ....................  83 
4.12.5  Set Closed Caption Mode  ................................ ................................ ................................ .......................  83 
4.12.6  Set Audio Mode  ................................ ................................ ................................ ................................ ...... 84 
4.13 SET PHYSICAL CHANNEL ................................ ................................ ................................ ................................ .... 84 
4.14 DTV FIRMWARE UPDATE  ................................ ................................ ................................ ................................ .. 85 
4.15 RECEPTION MONITOR (TEST MODE) ................................ ................................ ................................ ...................  86 
4.16 GET VERSION INFO ................................ ................................ ................................ ................................ ..........  86 
4.17 GET PROGRAM INFO ................................ ................................ ................................ ................................ ........  87 
4.18 GET RMP  MANUFACTURER ID ................................ ................................ ................................ ..........................  87 
4.19 EPG ................................ ................................ ................................ ................................ .............................  88 
4.20 BML  DATA BROADCAST  ................................ ................................ ................................ ................................ ... 89 
4.21 SET RESIDENTIAL AREA ................................ ................................ ................................ ................................ ..... 90 
4.22 AUDIO ES ................................ ................................ ................................ ................................ ......................  91 
4.23 EWS  ................................ ................................ ................................ ................................ ............................  92 
4.24 BROADCAST SEARCH  ................................ ................................ ................................ ................................ ........  93 
4.24.1  Manual Broadcast Search ( Affilaited Search)  ................................ ................................ .......................  93 
4.24.2  Auto Station Search  ................................ ................................ ................................ ...............................  94 
4.24.3  Broadcast Search Stop (Affiliated Search and Auto Station Search)  ................................ ......................  95 
4.25 DTV MODULE STATUS  ................................ ................................ ................................ ................................ ...... 96 
4.25.1  Get Current Module Status  ................................ ................................ ................................ ....................  96 
4.26 DTV ANTENNA STATE ................................ ................................ ................................ ................................ .......  96 
4.27 SUSPEND TO DISK................................ ................................ ................................ ................................ ............  97 
4.27.1  Resume  ................................ ................................ ................................ ................................ ..................  97 
4.27.2  Suspend  ................................ ................................ ................................ ................................ ..................  97


--- Page 8 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
  
 
1 Purpose  of this Document  
1.1 Introduction to the document  
This document is used to provide information related to the APIs provided by DTV Service in CCS2 
project.  
The document can be used by:  
• Feature Owner to verify all the features offered by DTV Service  
• App Developers to understand how to use the APIs to interface and available features offered 
by DTV Service  
 
1.2 Scope  
The scope of this document is to focus on the APIs offered by DTV Service. It also takes into account the 
various pre -conditions, usage and results of the APIs  
 
1.3 Context  
This is a preliminary draft version of the document. Document will be updated for below points during 
next Engineering Cycle documentation phase.  
• Review comments from Feature Owner, Architect & Specialist  
• Robustness (Error Handling, Low Voltage Handling, Configuration Handling)  
• Size & Performance Criteria  
 
2 Service Information  
Service Name:  com.bosch.dtv.service  
Package :  com.bosch.dtv.service  
Persmission :  com.bosch.permission.DTV  
3 API 
This section describes the APIs provided by DTV Service


--- Page 9 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1 DTV Commands  
3.1.1 Auto Preset  
Feature  Auto Preset for TV1/TV2  
Program Epic  CCS2 -3554  
API Method Name  dtvAutoPreset  
Parameters  DtvAutoPresetRequest  request  START_HOME_AREA_UPDATE  
START_TRAVEL_AREA_UPDATE  
STOP  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvAutoPreset Result  
Refer  Dtv Result  table  for information on result  
Events to Follow  (optional) IDtvEventsCallback::onDtvAutoPresetUpdate  
Refer  Auto Preset Update  
(optional) IDtvEventsCallback::  onDtvPresetListUpdate  
Refer  Preset List Update  
Feature Description:  
User can perform Auto Preset to scan entire band and store receivable channels into TV1 or TV2 preset list. Up 
to 12 stations can be stored into each preset list.  
• Result would be provided through onDtvAutoPresetResult . 
•  When Auto Preset is started successfully , Intermediatory and concluding events would be provided, 
through onDtvAutoPresetUpdate , giving information related to each physical channels from 13 to 52 
scanned and reports if any station was found or not.  
• During Auto Preset, if at least one station was found, Preset list would be updated and provided 
through onDtvPresetListUpdate  and the first available stored preset channel (smallest preset number) 
in that preset list would be tuned.  
• If no station was found or cancelled by user, then TV module will retune the formerly tuned last 
channel, if any was tuned before.  Last preset list stays unchanged.  
Usage:


--- Page 10 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 - dtvAutoPreset  with START_HOME_AREA_UPDATE  can be requested when current TV type is TV1, and 
user selects Auto Preset option from Settings  
- dtvAutoPreset with START_ TRAVEL _AREA_UPDATE can be requested when current TV type is TV2, 
and user selects Auto Preset option from Settings  
- dtvAutoPreset  with STOP  can be requested when user selects Cancel from Auto Preset Update popup  
Pre-Condition:  
• TV Module is running, and DTV service is available. There is no automatic station search or seek 
running.  
 Important:  
• During Auto Preset, other requests (except Auto Preset Stop) cannot be handled and would result in 
error response.  
• To ensure user does not perform other operations while Auto Preset is ongoing, Popup can be 
displayed  
Sequence:  
For Complete Feature Sequence, refer Auto Preset  
 
3.1.2 Channel Seek  
Feature  Channel Seek Up/Down  
Program Epic  CCS2 -1617   
API Method Name  dtvChannelSeek  
Parameters  DtvSeekOperation  operation  UP  
DOWN  
 STOP  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvChannelSeekResult  
Refer  Dtv Result  table  for information on result   
Events to Follow  (optional) IDtvEventsCallback::  onDtvChannelSeekUpdate  
Refer Channel Seek Update


--- Page 11 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Feature Description:  
User can perform Channel Seek to search the band, to find other receivable channels.  
• Result would be provided through onDtv Channel SeekResult . 
•  When Channel Seek is started successfully, Intermediatory and concluding events would be provided, 
through onDtv ChannelSeek Update , giving information related to different physical channels searched 
and reports if any channel was found  
• If no channel was found or seek Stopped  by user, then TV module will retune the formerly tuned last 
channel, if any was tuned before.  
• If a channel is found during seek, current seek would be concluded and the found channel would be 
tuned and played.  
• Operation  Up will search band in increasing order from the next physical channel of currently tuned 
physical channel until the one channel before current channel. E.g., when current channel is 36 then 
from 37 to 52 then 13 to 35.  
• Operation  Down  will search band in decreasing order opposite to Seek up.  
Pre-Condition:  
• TV Module is running, and DTV service is available. There is no automatic station search or Auto 
preset in progress.  
 Important:


--- Page 12 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • During Seek, other requests (except Seek) cannot be handled and would result in error response.  
• To ensure user does not perform other operations while seek  is ongoing, Popup can be displayed.  
• TV module has some limitations due to which the Seek should be Aborted \Cancelled in a few Use 
Cases before starting another operation. The below listed  a few possible Use Cases where App should 
first Stop the Seek in Progress before triggering another Request . 
 
Notes:  
Implicit requirements needed due to tv module limitation:  
Precondition : TV1 and TV2 both have presets stored  
 
Use case 1:  
User in TV1, perform seek  
Change source to TV2  
Requirement: TV2 last played preset type should be tuned  
Implicit handling: Seek has to be aborted and then tv2 last preset tune request should be sent.  
 
Use case 2:  
User in TV1, perform seek  
Press HK SWC Next / Prev (short)  
Requirement: ?  
Implicit handling : seek has to be aborted and then channel up /down request need to be sent  
 
Use case 3:  
User in TV1, perform seek Select preset.   
Requirement: ?  
Implicit handling: seek has to be aborted and then preset select request need to be sent.  
 
Use case 4:  
User in TV1, perform seek.  
Change Audio Source from TV1 to AM \FM and quickly changes it back to TV1.  
Requirement:  TV1 last played preset type should be tuned  
Implicit handling: seek has to be aborted when TV is exited, and Source changed to AM \FM. 
Sequence:  
For Complete Feature Sequence, refer Channel Seek  
 
3.1.3 Channel Up Down  
Feature  Channel Up/Down (Next/Previous)


--- Page 13 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Program Epic  CCS2 -4631  
API Method Name  dtvChannelUpDown  
Parameters  DtvChannelUpDown Op
eration  operation  UP 
DOWN  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvChannelUpDownResult  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can perform channel up / down operation to tune to the next / previous presets from the preset list  
• Result would be provided through onDtvChannelUpDownResult . 
• The dtvChannelUpDown request performs  the requested operation on current preset type  only.  
• Different a ctions  that can be performed with DtvChannelUpDownOperation parameter  
- UP: Tune to the next sub service of current preset  if available, else tune to next preset  
- DOWN : Tune to the previous sub service of current preset  if available, else tune to previous preset  
Example:   
Preset 1: 011, 012(unique service), 013(unique service)   
Preset 2: 021(no unique service in sub channels)  
Preset 3: Empty  
Preset 4: 041, 043(unique service)   
Preset 5: 051, 052(unique service)   
Preset 6 – 12: Empty  
Current Tuned Preset: Preset 1, Channel Number: 011  
UP: 012 -> 013 -> 021 -> 041 ->043 -> 051->052->011  
DOWN: 052->051->043->041->021 ->013 ->012 ->011  
If Preset list is empty  or if preset list has no other unique service to Tune to , dtvChannelUpDown request will 
fail and provide Result  as NO_SERVICE . 
Pre-Condition:


--- Page 14 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • TV Module is running, and DTV service is available. There is no automatic station search or Auto 
preset in progress.  
• Program Guide or Program Info are not open.  
Sequence:  
For Complete Feature Sequence, refer Channel Up Down


--- Page 15 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.4 Select Preset Channel  
Feature  Preset Channel Select/Store for TV1/TV2  
Program Epic  CCS2 -3556  
API Method Name  dtvS electPresetChannel  
Parameters  DtvPresetType  presetType  HOME  
DRIVE  
int presetNumber  01-12 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSelectPresetChannel Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can select any preset from the preset list, to tune.  
• Result would be provided through onDtvSelectPresetChannelResult . 
• Any dtvSelectPresetChannel request for any empty preset would lead to error result.  
• If result is OK,  
- requested presetNumber  would be tuned  
Pre-Condition:  
• TV Module is running, and DTV service is available. There is no automatic station search or Auto 
preset in progress.  
Sequence:  
For Complete Feature Sequence, refer Select Preset Channel


--- Page 16 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.5 Store Preset Channel  
Feature  Preset Channel Select/Store for TV1/TV2  
Program Epic  CCS2 -3556  
API Method Name  dtvStorePresetChannel  
Parameters  DtvPresetType  presetType  HOME  
DRIVE   
int presetNumber  01-12 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvStorePresetChannel Result  
Refer  Dtv Result  table  for information on result  
Events to Follow  (optional) IDtvEventsCallback::  onDtvPresetListUpdate  
Refer Preset List Update  
Feature Description:  
User can store the currently playing station in any preset  
• Result would be provided through onDtvStorePresetChannelResult . 
• If the presetNumber  requested to store, already has preset information, it would be overwritten with 
the current playing station information.  
• If result  is OK,  
- Requested presetNumber  would be stored in preset list and tuned  
- Updated preset list would be provided through onDtvPresetListUpdate  
 
Pre-Condition:  
• TV Module is running, and DTV service is available. There is no automatic station search or Auto 
preset in progress.  
Sequence:  
For Complete Feature Sequence, refer Store Preset Channel


--- Page 17 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.6 Display Banner  
Feature  Display Banner (overlaid on TV video)  
Program Epic  CCS2 -3559  
API Method Name  dtvDisplayBanner  
Parameters  DtvBannerOperation  operation  SHOW  
HIDE  
int duration  0 
1-255 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvDisplayBannerResult  
Refer  Dtv Result  table  for information on result  
Feature Description:  
Application can request to show/ hide banner, which shows the current tuned station’s program details.  
• Result would be provided through onDtvDisplayBannerResult . 
• If operation SHOW is requested,  
- If duration  is 0, Banner would be shown till HIDE is requested.  
- If duration  is 1-255, Banner would be shown for that many seconds and hidden automatically.  
• If operation HIDE is requested, Banner would be hidden, if being shown.  
• If banner is being shown and a new dtvDisplayBanner  request is made, the timer would be restarted.  
• Banner would be automatically shown whenever a channel is Tuned . 
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Display Banner


--- Page 18 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.7 Direct Channel Select  
Feature  Direct Channel Input  
Program Epic  CCS2 -5148  
API Method Name  dtvDirectChannelSelect  
Parameters  int threeDigitNumber  000~199  (Full seg)  
 600~799  (One seg)  
int branchId  0-9 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvDirectChannelSelect Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can request to tune to a channel using its threeDigitNumber and its branchId.  
• By default, branchId  should be requested as 1 since branch id would not be stored by application.  
• Result would be provided through onDtvDirectChannelSelectResult.  
• If the requested threeDigitNumber – branchId is not stored in current preset list or not the current tuned 
non-stored preset channel, result would be provided as NO_SERVICE.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer  Direct Channel Select


--- Page 19 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.8 Dtv Initialize  
Feature  TV Settings: Initialization (TV1 / TV2 / Settings / Factory Reset)  
Program Epic  CCS2 -3564  
API Method Name  dtvInitialize  
Parameters  DtvInitializeOperation  operation  ALL_DATA  
CONFIGURED_ SETTINGS  
HOME_PRESET  
DRIVE_PRESET  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvInitialize Result  
Refer  Dtv Result  table  for information on result  
Feature Description:


--- Page 20 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 User can initialize  either Home or Drive or Settings or All Dtv Data  
• Result would be provided through onDtvInitializeResult . 
• Refer below table for the data which would be initialized based on requested operation  
Data  Initial Value  Operation  
Audio Mode  MAIN  ALL_DATA or SETTINGS  
Closed Caption Mode  OFF ALL_DATA or SETTINGS  
Auto Tune Mode  AUTO  ALL_DATA or SETTINGS  
Auto Broadcast Search Mode  RELAY_AFFILIATED_STATION_SEARCH  ALL_DATA or SETTINGS  
Auto Event Relay  ON ALL_DATA or SETTINGS  
Preset List ( Home Preset)  Empty  ALL_DATA or HOME_PRESET  
Region ID (Home Preset)  255 ALL_DATA or HOME_PRESET  
Zip code ( Home Preset)  0 ALL_DATA or HOME_PRESET  
Preset List ( Drive Preset)  Empty  ALL_DATA or DRIVE_PRESET  
Region ID (Drive Preset)  255 ALL_DATA or DRIVE_PRESET  
Zip code ( Drive Preset)  0 ALL_DATA or DRIVE_PRESET  
 
• If current playing channel is from Home Preset and user requests for dtvInitialize  with operation  as 
HOME_PRESET  or ALL_DATA , the current playback would be stopped, and last channel information 
would be cleared.  Same logic is applicable for vice -versa.  
• If current playing channel is from Home Preset and user requests for dtvInitialize  with operation  as 
DRIVE _PRESET , the current playback would be resumed after initialization.  Same logic is applicable for 
vice-versa.  
• Current playing channel or last channel information would not be cleared in case of dtvInitialize  with 
operation  as SETTINGS . 
• If application is storing local data of any of the below types, it must be cleared on receiving the 
onDtvInitializeResult as OK 
DtvIniti
alize  
Operati
on TV1 last 
played 
preset  
number  TV2 last 
played 
preset 
number  TV1 
current 
program 
info TV2 
current 
program 
info Home 
Area 
zipcode & 
prefecture  Travel 
area 
zipcode & 
prefectur
e Audio Mode,  Closed 
caption mode, Auto 
tune mode, Auto 
Broadcast Search 
mode, Auto Event 
relay  
TV1 x  x  x   
TV2  x  x  x  
Settings        x 
ALL x x x x x x x 
 
Pre-Condition:


--- Page 21 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Dtv Initailize  
 
3.1.9 Reception Monitor (Test Mode)  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Method Name  dtvReceptionMonitorSession  
Parameters  DtvReceptionMonitorSt
ate state  STOP,  
START  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvReceptionMonitorSession Result  
Refer  Dtv Result  table  for information on result  
Events to Follow  (optional) IDtvEventsCallback::  onDtvReceptionMonitor Update  
Refer Reception Monitor Update (Test Mode)  
Feature Description:  
Reception Monitoring can be started/stopped using this interface  
• Result would be provided through onDtvReceptionMonitorSessionResult . 
• On request of state as START , onDtvReceptionMonitorUpdate  would be provided every second and 
would continue till STOP state is requested.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Reception Monitor (Test Mode)


--- Page 22 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.10  Dtv Firmware Update  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Method Name  dtvPerformFirmwareUpdate  
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvPerformFirmwareUpdate Result  
Refer  Dtv Result  table  for information on result  
Events to Follow  (optional) IDtvEventsCallback::  onDtv FirmwareUpdate  
Refer  
Feature Description:  
Firmware update of Dtv Module can be initiated using this interface  
• Result would be provided through onDtvPerformFirmwareUpdateResult  
• Progress of firmware update would be provided through onDtvFirmwareUpdate  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Dtv Firmware Update  
 
3.1.11  Display EPG  
Feature  EPG (8 Days Program Schedule for multiple channels) , Program Info (Detailed EPG)  
Program Epic  CCS2 -3552 , CCS2 -3553  
API Method Name  dtvDisplayEpg  
Parameters  DtvEpgOperation  operation   
IDtvMethodCallback  callback   
Return  void


--- Page 23 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Result  IDtvMethodCallback::  onDtvDisplayEPGResult  
DtvResult  result  Refer  Dtv Result  table  for 
information on result  
DtvEpgScreenState  screenState   
DtvEpgButtons  buttonState   
Events to Follow  (optional) IDtvEventsCallback::  onDtvEpgUpdate  
Refer Dtv EPG Update  
Feature Description:


--- Page 24 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 EPG Program Guide and Program Information can be accessed and operated using this interface  
• Result would be provided through onDtvDisplayEPGResult  
DtvEpgOperation  operation  
DISPLAYEPG_LIST  To open EPG List  
DISPLAYEPG_INFORMATION  To open EPG Information  
UP To scroll Up  
DOWN  To scroll Down  
LEFT  To scroll Left  
RIGHT  To scroll Right  
BACK  To go back to previous screen  
ENTER  Refer detailed description below  
SWITCH_SEGMENT  To switch between program information for 1seg and 12seg  
UPDATE  To manually update EPG  
PREVIOUS_DAY   To display program information of previous day  
NEXT_DAY  To display program information of next day  
MULTI_SERVICE  To display program information of sub channels  
CHANGE_SCALE  To adjust the zoom level of EPG Table  
CANCEL_UPDATE  To cancel the manual EPG update  
CLOSE_ALL  Refer detailed description below  
 
• DtvEpgScreenState  describes the current state of EPG  
DtvEpgScreenState  description  
NO_DISPLAY  EPG List or EPG Information is not open (TV Video shown)  
EPG_LIST_FULLSEG  EPG List shown with 12 seg program information  
EPG_INFO_FULLSEG  EPG Info shown with 12 seg program information  
EPG_LIST_ONESEG  EPG List shown with 1 seg program information  
EPG_INFO_ONESEG  EPG Info shown with 1 seg program information  
• All screen  transitions should follow the screen state  
• Transit to Program Guide screen after receiving DtvEpgScreenState  as EPG_LIST_FULLSEG  / 
EPG_LIST_ONESEG  result for the dtvDisplayEpg  DISPLAYEPG_LIST  request  
• Transit to Program Info screen after receiving DtvEpgScreenState  EPG_INFO_FULLSEG  / 
EPG_INFO_ONESEG  result for the dtvDisplayEpg  DISPLAYEPG_ INFO  request  
• If DtvEpgScreenState  is NO_DISPLAY , EPG session is closed  
- Transit to main screen if NO_DISPLAY  received as result for ENTER  DtvEpgOperation  
- Transit to previous screen if NO_DISPLAY  received as a result for other DtvEpgOperation  
• When DtvEpgOperation  UPDATE  is called, intermediatory and conclusive updates would be provided 
through onDtvEpgUpdate  
• DtvEpg Buttons received through result inform if the operation is allowed.


--- Page 25 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 DtvEpg Buttons  description  
isValid_up  
true: valid. Operation allowed. Button can be enabled  
false: invalid. Operation now allowed. Button can be disabled  
 isValid_down  
isValid_left  
isValid_right  
isValid_back  
isValid_enter  
isValid_switchSegment  
isValid_update  
isValid_previousDay  
isValid_nextDay  
isValid_multiService  
isValid_changeScale  
 
 
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Important :


--- Page 26 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • Tuning / Search / Seek / Auto Preset operations are not allowed when EPG is open. Any request would 
result in failure.  
Sequence:  
For Complete Feature Sequence, refer EPG 
 
3.1.12  Operate BML  
Feature  CCS2 -3562  
Program Epic  BML Browser  
API Method Name  dtvOperateBml  
Parameters  DtvBmlButton   button   
DtvBmlButtonState  state  PRESS  
RELEASE  
Return  void    
Result  void  
Feature Description:


--- Page 27 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 User can operate BML using this interface  
• There is no result provided for this interface  
• Possible operations with BML  which can be mapped to various buttons on remote / ‘d’ button  
DtvBmlButton  
NUM_1  
NUM_2  
NUM_3  
NUM_4  
NUM_5  
NUM_6  
NUM_7  
NUM_8  
NUM_9  
NUM_10  
UP 
DOWN  
LEFT  
RIGHT  
ENTER  
BACK  
DATA_BROADCAST  
BLUE  
RED 
GREEN  
YELLOW  
 
• To start data broadcasting (on press of ‘d’ button), dtvOperateBml  with DATA_BROADCAST  should be 
used  
• The successful opening of BML Data  broadcast session can only be judged by the beep sound heard  
• dtvOperateBml  with DATA_BROADCAST  would also toggle between opening BML and closing of BML . 
• To close BML, dtvForcedExitBml  should be used to guarantee the closure of BML Data broadcast 
session  
• On press  action  of the  button, application should use dtvOperateBml  with relevant button  and state  
as PRESS  
• On (short/long) release  action  of the button, dtvOperateBml  with relevant button  and state  as 
RELEASE  should be used  
 
Pre-Condition:


--- Page 28 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer BML Data Broadcast  
 
3.1.13  Forced Exit BML  
Feature  BML Browser  
Program Epic  CCS2 -3562  
API Method Name  dtvForcedExitBml  
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvForcedExitBmlResult  
Refer  Dtv Result  table  for information on result  
Feature Description:  
Application can use this interface to ensured guaranteed closure of BML Data  broadcast session  
• Result would be provided through onDtvForcedExitBmlResult  
• If BML Data  broadcast  session is open and dtvForcedExitBml  sent, BML session would be closed, and 
SUCCESS result would be given  
• If BML Data  broadcast  session is not open and dtvForcedExitBml sent, no action and SUCCESS result  
would be given l 
• This interface can be used on exit of BML screen or on back button press in the BML screen (not the 
back button in remote)  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer BML Data Broadcast


--- Page 29 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.1.14  Broadcast Search  
Feature  Manual Foreground Broadcast Search (Relay/Affiliated Station) / Automatic 
Foreground Broadcast Search (Relay/Affiliated Station)  
Program Epic  CCS2 -3560  / CCS2 -3561  
API Method Name  dtvBroadcastSearch  
Parameters  DtvBroadcastSearchMode  mode  START_RELAY_SEARCH  
START_AFFILIATED_SEARCH  
START_RELAY_AFFILIATED_SEARCH  
STOP_SEARCH  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvBroadcastSearchResult  
Refer  Dtv Result  table  for information on result   
Events to Follow  (optional) IDtvEventsCallback::  onDtv Event Update  
Refer  Dtv Event Update  
(optional) IDtvEventsCallback::  onDtvBroadcastSearchUpdate  
Refer  Broadcast Search Update  
Feature Description:


--- Page 30 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 User can perform Broadcast search  to  
- Find affiliate / relay station  / relay and affiliate / stop broadcast search (manual)  
- stop broadcast search (automatic)  
• Result would be provided through onDtvBroadcastSearchResult . 
•  When Broadcast search  (Manual  – started by using dtvBroadcastSearch ) is started, 
onDtv Event Update  with MANUAL_BROADCASTSEARCH_INPROGRESS  would be provided.  
• When Broadcast search  (Automatic – started by the TV Module during  weak signal) is started, 
onDtv Event Update  with AUTO_BROADCASTSEARCH_INPROGRESS  would be provided.  
• This would be followed with Intermediatory and concluding events, through 
onDtvBroadcastSearchUpdate , giving information related to different physical channels searched and 
reports if any station  was found  
• If no station  was found or Broadcast search  Stopped  by user, then TV module will retune the formerly 
tuned last channel, if any was tuned before.  
• If a channel is found Broadcast search , search would be concluded and the found channel would be 
tuned and played.  
• Concluding  onDtvBroadcastSearchUpdate  would provide information of what kind of station was 
found ( relay or affiliate)  
• Both Manual and Automatic Broadcast search can be stopped using dtvBroadcastSearch  with mode as 
STOP_SEARCH   
Pre-Condition:  
• TV Module is running, and DTV service is available. There is no Auto preset in progress.  
 Important:  
• During Broadcast Search , other requests (except Broadcast Search ) cannot be handled and would 
result in error response.  
Sequence:  
For Complete Feature Sequence, refer Broadcast Search


--- Page 31 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.2 Set Command  
3.2.1 Set Auto Tune Mode  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvSetAutoTuneMode  
Parameters  DtvAutoTuneMode  mode  AUTO  
FULL_SEGMENT  
ONE_SEGMENT  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetAutoTuneModeResult  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can configure the component (1seg/12seg) which the Tv Module would tune to.  
• Result would be provided through onDtvSetAutoT uneModeResult.  
• If mode is set as AUTO , Tv Module would tune to 12 seg if reception quality is good, else would 
switch to 1 seg till the reception improves.  
• If mode  is set as ONE_SEGMENT, Tv Module would tune to 1 seg only, even if 12 seg is available.  
• If mode  is set as FULL_SEGMENT, Tv Module would tune to 12 seg only. If reception is not good, 
black screen would be shown till the reception improves.  
• Set configuration would be persisted.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Auto Tune Mode


--- Page 32 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.2.2 Set Auto Broadcast Search Mode  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvSetAuto Broadcast SearchMode  
Parameters  DtvAutoBroadcastSearc
hMode  mode  OFF 
RELAY_STATION_SEARCH  
RELAY_AFFILIATED_STATION_SEARC
H 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetAuto BroadcastSearchMode Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can configure the type of channels that can be searched for when  the current tuned channel has poor 
reception / is not receivable anymore.  
• Result would be provided through onDtvSetAutoBroadcastSearchModeResult . 
• Set configuration would be persisted.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Auto Broadcast Search Mode


--- Page 33 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.2.3 Set Auto Event Relay Mode  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvSetEventRelayMode  
Parameters  DtvEventRelayMode  mode  OFF 
ON 
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetEventRelayMode Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can configure the Tv Module, to turn on / turn off automatic tuning of event relay station, in case of an 
event relay from the broadcaster.  
• Result would be provided through onDtvSetEventRelayModeResult . 
• Set configuration would be persisted.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Auto Event Relay Mode  
3.2.4 Set Closed Caption Mode  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvSetClosedCaptionMode  
Parameters  DtvClosedCaptionMode  mode  OFF 
CLOSED_CAPTION_1  
CLOSED_CAPTION  _2


--- Page 34 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetClosedCaptionMode Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can configure the Tv Module to turn on or off closed caption (subtitle)  
• Result would be provided through onDtvClosedCaptionModeResult . 
• Set configuration would be persisted.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Closed Caption Mode  
 
3.2.5 Set Audio Mode  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvSetAudioMode  
Parameters  DtvAudioMode  mode  MAIN  
SUB 
MAIN_SUB  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetAudioMode Result  
Refer  Dtv Result  table  for information on result  
Feature Description:


--- Page 35 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 User can configure the audio mode for Dtv Audio  
• Result would be provided through onDtvSetAudioModeResult . 
• Set configuration would be persisted.  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Audio Mode  
 
3.2.6 Set Physical Channel  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Method Name  dtvSetPhysicalChannel  
Parameters  int physicalChannelNumb
er 13 ~ 52  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetPhysicalChannel Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can tune to any physical channel (13 ~ 52) directly  
• Result would be provided through onDtvSetPhysicalChannel Result . 
• Application to ensure that request is sent only for physicalChannelNumber  13 to 52 as other request 
would result in error response.  
• Current physical channel number would be provided as a part of onDtvStatusUpdate  (Refer Dtv Status 
Update ) 
Pre-Condition:  
• TV Module is running, and DTV service is available.


--- Page 36 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Sequence:  
For Complete Feature Sequence, refer Set Physical Channel  
 
3.2.7 Set Residential Area  
Feature  TV Settings:  Prefecture / Zip Code Input  
Program Epic  CCS2 -3566  
API Method Name  dtvSetResidentialArea  
Parameters  DtvPresetType  presetType  HOME  
DRIVE  
int regionId  0 (None)  
1~53 (Prefecture)  
String  zipcode   
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDvSetResidentialArea Result  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can set the Region id (prefecture) and zip code for Home Area and Travel Area  
• Result would be provided through onDvSetResidentialAreaResult  
• It is possible to set either regionId  only or zipcode  only or both regionId  and zipcode  
• If user selects “None” as the prefecture, regionId  can be set as 0  
• If user selects “Skip” for zipcode, zipcode  can be set as empty string  
• If user selects “None” as prefecture and “Skip” for zipcode , dtvSetResidentialArea  should  not be sent  
• Valid zipcode  is of 7 digits  length  
• After receiving onDvSetResidentialAreaResult  as SUCCESS, application should send dtvAutoPreset  
with same preset type to scan and store the preset list based on newly set regionId and zipcode 
information.


--- Page 37 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Set Residential Area  
 
3.2.8 Set Audio ES  
Feature  TV Settings: Audio ES  
Program Epic  CCS2 -3571  
API Method Name  dtvSetAudioES  
Parameters  int audioESTag   
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvSetAudioESResult  
Refer  Dtv Result  table  for information on result  
Feature Description:  
User can select the Voice to be played for the current tuned station  
• Result would be provided through onDtvSetAudioESResult  
• When user selects a voice, the audioESTag  mapped to that voice should be used to send the request  
• Refer to dtvGetAudioES  for info related to mapping audioES Tag to voice  
• Audio ES tags are dynamic and vary between broadcasters  
• If a channel is re-tuned, changed, lost signal then the selected audio  ES would be lost  
• Audio ES would not be persisted by TV Module  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer  Audio ES


--- Page 38 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.3 Get Command  
3.3.1 Get Preset List  
Feature  Preset List Retrieve/Update for TV1/TV2  
Program Epic  CCS2 -3555  
API Method Name  dtvG etPresetList  
Parameters  DtvPresetType  presetType  HOME  
DRIVE  
IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvGetPresetListResult  
DtvResult  result  Refer  Dtv Result  table  for 
information on result  
DtvPresetType  presetType   
List<DtvPresetItem>  preset List  
Feature Description:  
User can fetch the preset list for home or drive preset type.  
• Application needs to request dtvGetPresetList for Home and Drive, once on application start -up. 
• Further updates would be provided through onDtvPresetListUpdate  whenever there is any change in 
the preset list.  
• It is pos sible to fetch preset information for the entire preset list. result , presetType  and presetList  
would be provided through onDtvGetPresetListResult . 
• If result  is OK, 
- presetType : requested preset type  
- presetList : requested preset list information  
• DtvPresetItem  would provide the below information  
int presetNumber   
String  stationName   
• In case no presets were stored, presetList with 12 empty DtvPresetItem  would be provided.  
• In case only a few presets were stored, presetList with 12 DtvPresetItem  would be provided with the 
respective index  of presetList  updated . 
• The data provided through result should be considered only if result is OK


--- Page 39 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
• TV Module is running, and DTV service is available. There is no automatic station search or Auto 
preset in progress.  
Sequence:  
For Complete Feature Sequence, refer  Get Preset List  
 
3.3.2 Get Configure  
Feature  TV Settings: Basics  
Program Epic  CCS2 -3565  
API Method Name  dtvGetConfigure  
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvGetConfigureResult  
DtvResult  result  Refer  Dtv Result  table  for 
information on result  
DtvConfiguration  config   
Feature Description:


--- Page 40 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • Result would be provided through onDtvGetConfigureResult . 
• DtvConfiguration  would provide the below information  
DtvAudioMode  audioMode  MAIN  
SUB 
MAIN_SUB  
DtvClosedCaptionMode  captionMode  OFF 
CLOSED_CAPTION _1 
CLOSED_CAPTION _2 
DtvAutoTuneMode  autoTuneMode  AUTO  
FULL_SEGMENT  
ONE_SEGMENT  
DtvAutoBroadcastSearch
Mode  searchMode  OFF 
RELAY_STATION_SEARCH  
RELAY_AFFILIATED_STATION_SEARCH  
DtvEventRelayMode  relayMode  OFF 
ON 
int homeRegionId   
string  homeZipcode   
int travelRegionId   
string  travelZipcode   
 
• The data provided through result should be considered only if result  is OK  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Get Configure  
 
3.3.3 Get Version Info  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Method Name  dtvGetVersionInfo  
Parameters  IDtvMethodCallback  callback   
Return  void


--- Page 41 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Result  IDtvMethodCallback::  onDtv GetVersion Resul t 
DtvResult  result  Refer  Dtv Result  table  for 
information on result  
DtvVersionInfo  info  
Feature Description:  
• Result would be provided through onDtvGetVersionResult . 
• DtvVersionInfo would provide the below information  
String  hardwareVersion  
String  bootVersion  
String  firmwareVersion  
String  partNumber  
String  diversityMode  
 
• The data provided through result should be considered only if result  is OK  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Get Version Info  
 
3.3.4 Get Program Info  
Feature  Program Information Notification  
Program Epic  CCS2 -3557  
API Method Name  dtvGet Program Info 
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtv GetProgramInfo Resul t 
DtvResult  result  Refer  Dtv Result  table  for 
information on result


--- Page 42 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 DtvProgramInfo  info  
Feature Description:  
• Result would be provided through onDtvGetVersionResult . 
• DtvProgramInfo  would provide the below information  
 
int presetType  00: Home Preset (TV1)  
01: Drive Preset (TV2)  
FF: None  
int presetNumber  00: Non -Stored Preset  
01 ~ 12: Preset Number  
int threeDigitNumber   
int branchId   
String  stationName   
String  programName   
 
• The data provided through result should be considered only if result  is OK  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer Get Program Info  
 
3.3.5 Get RMP Manufacturer Id  
Feature  TV Settings: RMP Manufacturer ID Display  
Program Epic  CCS2 -6560  
API Method Name  dtvGet RmpManufactuereId  
Parameters  DtvRMPType  type  HOME,  
DRIVE,  
DEVICE  
int presetNumber  00 
01-12


--- Page 43 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtv GetRmpManufactuereId Result  
DtvResult  result  Refer  Dtv Result  table  for 
information on result  
String  rmpId   
Feature Description:  
• Result would be provided through onDtvGetRmpManufactuereIdResult  
• RMP Id for Device (RMP Manufacturer Id) and Broadcaster (Generated RMP Manufacturer Id) can be 
fetched  
• To Get Device RMP Manufacturer Id, request dtvGetRmpManufactuereId  with DtvRMPType  as 
DEVICE , presetNumber  as 0 
• To Get Broadcaster RMP Manufacturer Id, request dtvGetRmpManufactuereId  with DtvRMPType  as 
HOME/DRIVE  and presetNumber  as the respective preset index  
• Result  String rmpId  would be of the format X-XXXX -XXXX -XXXX -XXXX -XXXX -XXXX  
• The data provided through result should be considered only if result is OK  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer  Get RMP Manufacturer ID  
 
3.3.6 Get Audio ES  
Feature  TV Settings: Audio ES  
Program Epic  CCS2 -3571  
API Method Name  dtvGetAudioES  
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvGetAudioESResult


--- Page 44 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 DtvResult  result  Refer  Dtv Result  table  for 
information on result  
DtvAudioESInfo  info  
Feature Description:  
• Result would be provided through onDtvGetAudioESResult  
• DtvAudioESInfo contains the below info  
int currentAudioESTag  current selected  audio ES tag  
int []  AudioESTags  list of audio ES tags  
• Each audio ES tag should be mapped to a Voice (in the same order as provided)  
e.g., DtvAudioESInfo  with  currentAudioESTag :12 and AudioESTags : {11,12,13 } 
Voice 1: 11  
Voice 2: 12 (current selected ) 
Voice 3: 13  
• The audio ES tags are dynamic and vary between broadcasters  
• The first ES tag is selected and played by default  (Voice 1) if no setDtvAudioES  is sent  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer   Audio ES  
 
3.3.7 Get Dtv Module Status  [DEPRECATED]  
Feature  TV Module Status and Error Notifications  
Program Epic  CCS2 -7661  
API Method Name  dtvGet ModuleStatus  
Status  DEPRECATED : use dtvGetCurrentModuleStatus  
Parameters  IDtvMethodCallback  callback   
Return  void    
Result  IDtvMethodCallback::  onDtvGet ModuleStatus


--- Page 45 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 DtvModuleStatus  status  LOADING  
READY  
HIGH_TEMPERATURE  
NOT_RESPONSIVE  
INTERNAL_ERROR  
FIRMWARE_UPDATE_INPROGRESS  
FIRMWARE_UPDATE_FAILURE  
Feature Description:  
• Result would be provided through onDtvGet ModuleStatus  
• dtvGetModuleStatus can be requested by Application once on start -up and follow further updates 
based on onDtvModuleStatusUpdate  
 
• Dtv functionality would be available and can be requested only when the DtvModuleStatus  is READY  
• During other states, TV Menu and TV Settings button should be greyed out and Preset List should not 
be visible for user to access  
• Appropriate Advisor ies should be shown when DtvModuleStatus is not READY  and cleared  on receiving 
READY  LOADING  TV Module startup in progress  
READY  TV Module up and ready to process all requests  
HIGH_TEMPERATURE  TV Module has high temperature   
NOT_RESPONSIVE  TV Module not responding   
INTERNAL_ERROR  TV Module has internal error  
FIRMWARE_UPDATE_INPROGRESS  TV Module Firmware Update in progress  
FIRMWARE_UPDATE_FAILURE  TV Module Firmware Update failed  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer   Module Status


--- Page 46 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.3.8 Get Dtv Antenna State  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Method Name  dtvGet AntennaState  
Parameters  DtvAntenna  antenna  DTV_ANTENNA_ 1 
DTV_ANTENNA_ 2 
DTV_ANTENNA_ 3 
DTV_ANTENNA_ 4 
DTV_ANTENNA_ALL  
Return  List<DtvAntennaStatus>    
Feature Description:  
• DtvAntennaStatus  would provide the below information  
 
DtvAntenna  antenna  DTV_ANTENNA_ 1 
DTV_ANTENNA_ 2 
DTV_ANTENNA_ 3 
DTV_ANTENNA_ 4 
DtvAntennaState  antennaS tate DTV_ANTENNA_STATE_ INVALID  
DTV_ANTENNA_STATE_ OK 
DTV_ANTENNA_STATE_OPEN  
DTV_ANTENNA_STATE_SHORT  
DTV_ANTENNA_DEACTIVATED  
DTV_ANTENNA_DEACTIVATED_LOW_VLTG  
DTV_ANTENNA_DEACTIVATED_HIGH_VLTG  
• dtvGetAntennaState  with DTV_ANTENNA_ALL would provide List< DtvAntennaStatus> with state for 
all available Dtv Antenna  
 
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:  
For Complete Feature Sequence, refer   Dtv Antenna State  
3.3.9 Get Current Dtv Module Status  
Feature  TV Module Status and Error Notifications


--- Page 47 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Program Epic  CCS2 -7661  
API Method Name  dtvGet CurrentModuleStatus  
Parameters  void  void   
Return  DtvModuleStatus  status  LOADING  
READY  
HIGH_TEMPERATURE  
NOT_RESPONSIVE  
INTERNAL_ERROR  
FIRMWARE_UPDATE_INPROGRESS  
FIRMWARE_UPDATE_FAILURE  
Feature Description:  
• dtvGet Current ModuleStatus can be requested by Application for 
- onServiceConnected  
and follow further updates based on onDtvModuleStatusUpdate  
 
• Dtv functionality would be available and can be requested only when the DtvModuleStatus  is READY  
• During other states, TV Menu and TV Settings button should be greyed out and Preset List should not 
be visible for user to access  
• Appropriate Advisor ies should be shown when DtvModuleStatus is not READY  and cleared  on receiving 
READY  LOADING  TV Module startup in progress  
READY  TV Module up and ready to process all requests  
HIGH_TEMPERATURE  TV Module has high temperature   
NOT_RESPONSIVE  TV Module not responding   
INTERNAL_ERROR  TV Module has internal error  
FIRMWARE_UPDATE_INPROGRESS  TV Module Firmware Update in progress  
FIRMWARE_UPDATE_FAILURE  TV Module Firmware Update failed  
Pre-Condition:  
• TV Module is running, and DTV service is available.  
Sequence:


--- Page 48 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 For Complete Feature Sequence, refer   Module Status  
 
3.4 DTV Events  
3.4.1 Auto Preset Update  
Feature  Auto Preset for TV1/TV2  
Program Epic  CCS2 -3554  
API Event Name  onDtvAutoPresetUpdate  
Parameters  DtvAutoPresetStatus  status  INPROGRESS  
CHANNEL_FOUND  
NOCHANNEL_FOUND  
boolean  isDetected   
int channelNumber  00 
13~52 (physical channel number)  
Return  void   
Events to Follow  (optional) IDtvEventsCallback::  onDtvPresetListUpdate  
Feature Description:  
User can perform Auto Preset to scan entire band and store receivable channels into TV1 or TV2 preset list. Up 
to 12 stations can be stored into each preset list.  
• When Auto Preset is started successfully , Intermediatory and concluding events would be provided, 
through onDtvAutoPresetUpdate , giving information related to each physical channels from 13 to 52 
scanned and reports if any station  was found or not.  
• When DtvAutoPresetStatus  is INPROGRESS,  
- isDetected  == True : valid signal  was detected on the physical channel number  
- isDetected  == False : no valid signal was detected on the physical channel number  
- channelNumber :  current scanned physical channel number (13~52)  
• When DtvAutoPresetStatus  is not INPROGRESS, ignore isDetected , channelNumber  
• When dtvAutoPreset  STOP  is requested, onDtvAutoPresetUpdate  with DtvAutoPresetStatus  as 
NOCHANNEL_FOUND  would be provided.


--- Page 49 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
• dtvAutoPreset  called and onAutoPreset  Result was OK  
Sequence:  
DtvAutoPresetStatus  Transition Sequence  
 
 
For Complete Feature Sequence, refer Auto Preset  
 
3.4.2 Channel Seek Update  
Feature  Channel Seek Up/Down  
Program Epic  CCS2 -1617  
API Event Name  onDtvChannelSeekUpdate  
Parameters  DtvSeek Status  status  INPROGRESS  
CHANNEL_FOUND  
NOCHANNEL_FOUND


--- Page 50 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 boolean  isDetected   
int channelNumber  00 
13~52 (physical channel number)  
Return  void   
Feature Description:  
User can perform Channel Seek to search the band, to find other receivable channels.  
• When Channel Seek is started successfully, Intermediatory and concluding events would be provided, 
through onDtvChannelSeekUpdate , giving information related to different physical channels searched 
and reports if any channel was found  
• When DtvSeekStatus  is INPROGRESS,  
- isDetected  == True : valid signal was detected for the physical channel number  
- isDetected  == False : no valid signal was detected for the physical channel number  
- channelNumber :  current scanned physical channel number (13~52)  
• When DtvSeekStatus  is not INPROGRESS, ignore isDetected , channelNumber  
When dtvSeekChannel  STOP is requested, onDtvChannelSeekUpdate  with DtvSeekStatus  as 
NOCHANNEL_FOUND  would be provided.  
Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
• dtvS eekChannel  called and onDtvSeekChannel Result  was OK  
Sequence:


--- Page 51 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 DtvSeekStatus  Transition Sequence  
 
For Complete Feature Sequence, refer Channel Seek  
 
3.4.3 Program Infomation Update  
Feature  Program Information Notification  
Program Epic  CCS2 -3557  
API Event Name  onDtvProgramInfoUpdate  
Parameters  DtvProgramInfo  info  
Return  void   
Feature Description:


--- Page 52 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • onDtvProgramInfoUpdate would be provided whenever there is an update in the Program 
Information, related to the current tuned channel  
• DtvProgramInfo  would provide the below information  
 
int presetType  00: Home Preset (TV1)  
01: Drive Preset (TV2)  
FF: None  
int presetNumber  00: Non -Stored Preset  
01 ~ 12: Preset Number  
int threeDigitNumber   
int branchId   
String  stationName   
String  programName   
 
• If current tuned channel is not stored, presetType would be FF and presetNumber would be 00  
• After initialization, onDtvProgramInfoUpdate would be provided with  all fields cleared  
Pre-Condition:  
• TV Module is running, and service is available . Any channel is tuned by TV module.  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
3.4.4 Preset List Update  
Feature  Preset List Retrieve/Update for TV1/TV2  
Program Epic  CCS2 -3555  
API Event Name  onDtvPresetListUpdate  
Parameters  DtvPresetType  presetType   
List<DtvPresetItem>  presetList   
Return  void   
Feature Description:


--- Page 53 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • onDtvPresetListUpdate would be provided in the below use cases  
- startup  (both TV1 and TV2 preset list)  
- after AutoPreset  if new channel was found (preset list for requested preset type during Auto 
Preset)  
- after storePresetChannel  was successful  
• DtvPresetType  would provide info if the preset list is for Home or Drive preset type.  
• The entire preset list would be provided in the update.  
• If no presets were stored, presetList with 12 empty DtvPresetItem  would be provided.  
• In case only a few presets were stored, presetList with 12 DtvPresetItem  would be provided with the 
respective index  of presetList  updated . 
• DtvPresetItem would provide the below information  
int presetNumber   
String  stationName   -  
Pre-Condition:  
• TV Module is running, and service is available . Any channel is tuned by TV module.  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
3.4.5 Signal Status Update  [DEPRICATED]  
Feature  Signal Status (Weak / No signal) / No Service Notification  
Program Epic  CCS2 -3573   
Status  DEPRICATED : use  onDtvEventUpdate instead  
API Event Name  onDtvSignalStatusUpdate  
Parameters  DtvSignalStatus  status  OK 
WEAKSIGNAL  
NOSIGNAL  
NOBROADCAST  
TRMPERROR  
RMPERROR_EC21  
RMPERROR_EC22  
RMPERROR_EC23


--- Page 54 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Return  void   
Feature Description:  
• onDtv SignalStatusUpdate  
•  would be provided whenever there is a change in the reception of currently played channel.  
• Information related to DtvSignalStatus  is as below  
OK Default state, no error  
WEAKSIGNAL  Channel tuned but signal lost  
NOSIGNAL  Channel tuning error, signal not found  
NOBROADCAST  Channel not being broadcasted  
TRMPERROR  TRMP information is invalid  
RMPERROR_EC21   
RMPERROR_EC22   
RMPERROR_EC23   
 
Pre-Condition:  
• TV Module is running, and service is available . Any channel is tuned by TV module.  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
3.4.6 Dtv Status Update  
Feature  Antenna Bars Level (0/1/2/3) Notification  
Program Epic  CCS2 -3558  
API Event Name  onDtvStatusUpdate  
Parameters  DtvStatus  status   
Return  void   
Feature Description:


--- Page 55 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Status of few key parameters would be provided through onDtvStatusUpdate  
• DtvStatus would provide the below information.  
DtvTuningStatus  tuningStatus  Tuning Status  
• IDLE : Idle  
• TUNING : Tuning  
DtvServiceType  serviceType  Service Type (Now  Playing Service Type)  
• ISDB_T_FULLSEG : ISDB -T Fullseg  
• ISDB_T_ONESEG : ISDB -T Oneseg  
• NONE : None (Not Tuning)  
DtvAntenna Level  antennaLevel  Antenna Level  
• DTV_ANTENNA_ LEVEL 0: Antenna Level 0  
• DTV_ANTENNA_ LEVEL 1: Antenna Level 1  
• DTV_ANTENNA_ LEVEL 2: Antenna Level 2  
• DTV_ANTENNA_ LEVEL 3: Antenna Level 3  
int physicalChannelNumber  00, 13 ~ 52  
DtvEpgBmlStatus  epgbmlStatus  EPG/BML Status  
• NO_EPG_BML : No EPG/BML displayed  
• UPDATING : Updating  
• EPG_FULLSEG : EPG List (full seg)  
• EPG_ONESEG : EPG List (one seg) 
• EPG_INFO_FULLSEG : EPG Information (full seg)  
• EPG_INFO_ONESEG : EPG Information (one seg)  
• BML_DISPLAY : BML Display  
 
• tuningStatus  provides information related to the current state of TV Tuner.  
- IDLE:  not tuned to any channel  
- TUNING: tuned to a channel  
• serviceType  shows current Service Type (Now Playing Service Type) – One Seg or Full Seg or Not 
Tuning.  
• antennaLevel  provides information related to the current strength of signal received through the 
antenna. “Antenna Level” indicates the number of antennas on the display.  
- Antenna Level 0 is bad signal.  
- Antenna Level 3 is good signal.  
- If “Tuning Status ( tuningStatus )” is idle, Antenna Level is 0.  
• physicalChannelNumber provides the current physical channel number tuned.  
• epgbmlStatus  provides information related to the status of EPG/BML Screen.  
For Complete  Feature Sequence, refer Dtv Status Update


--- Page 56 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
• TV Module is running, and service is available.  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
3.4.7 Reception Monitor Update (Test Mode)  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Event Name  OnDtvReceptionMonitorUpdate  
Parameters  ReceptionInfo  info  
Return  void   
Feature Description:


--- Page 57 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Status of few key reception parameters  would be provided through OnDtvReceptionMonitorUpdate  
• ReceptionInfo  would provide the below information  
String  ant1_CN  Signal / Noise of Antenna 1 in dB  
String  ant2_CN  Signal / Noise of Antenna 2 in dB  
String  ant3_CN  Signal / Noise of Antenna 3 in dB  
String  ant4_CN  Signal / Noise of Antenna 4 in dB  
String  combined_CN  Signal / Noise of Combined Tuner in dB  
LayerInfo  layerA   
LayerInfo  layerB   
LayerInfo  layerC   
• LayerInfo  would provide the below information  
boolean  isActive  is layer Active or Not  
String  BER Bit Error Rate in %  
String  PER Packet Error Rate in %  
• If a layer is not active, isActive would be set to false and BER, PER would be empty string.  
• When dtvReceptionMonitorSession  with START  state is requested, OnDtvReceptionMonitorUpdate  
would be provided every second . 
• When dtvReceptionMonitorSession with STOP  state is requested, OnDtvReceptionMonitorUpdate 
updates would be stopped.


--- Page 58 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Formula for Calculation REC:  
Reception rate (%) = {1 - (number of data items with PER 1% or more) / (time elapsed)} x 100  
Example:  
User press Start in Reception Monitor Screen  
1st Monitor Status update  
Duration: 1s  PER Calculated REC  
Layer A  0.6 {1 – 0 / 1} * 100 = 100 %  
Layer B  1.1 {1 – 1 / 1} * 100 = 0 %  
Layer C  0 {1 – 0 / 1} * 100 = 100 %  
 
2nd Monitor Status update  
Duration: 2s  PER Calculated REC  
Layer A  1.2 {1 – 1 / 2} * 100 = 50 %  
Layer B  1.3 {1 – 2 / 2} * 100 = 0 %  
Layer C  0 {1 – 0 / 2} * 100 = 100 %  
 
3rd Monitor Status update  
Duration: 3s  PER Calculated REC  Observation  
Layer A  1.8 {1 – 2 / 3} * 100 = 67.33 %  Intermediate reception, some 
packets missed  
Layer B  1.5 {1 – 3 / 3} * 100 = 0 %  Very Poor Reception, all 
packets missed  
Layer C  0 {1 – 0 / 3} * 100 = 100 %  Very Good Reception, no or 
very less packets missed  
 
For Complete  Feature Sequence, refer Reception Monitor (Test Mode)


--- Page 59 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
3.4.8 Dtv Firmware Update  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Event Name  onDtvFirmwareUpdate  
Parameters  DtvFirmwareUpdate Status  status  START  
FILETRANSFER _INPROGRESS  
FLASH _INPROGRESS  
FLASH_ SUCCESS  
COMPLETE  
ABORTED  
FAILURE_INVALID_FILENAME  
FAILURE_INVALID_DATA  
FAILURE_INVALID_FILESIZE  
FAILURE_TIMEOUT  
Return  void   
Feature Description:  
Progress of firmware update would be provided through this interface . 
• Once Firmware Update is complete  (SWUPDATE _COMPLETE ), Application must Get Program Info  and 
Get Preset List  (Home Area, Travel Area) again.  
For Complete  Feature Sequence, refer Dtv Firmware Update  
Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback


--- Page 60 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.4.9 Dtv EPG  Update  
Feature  EPG (8 Days Program Schedule for multiple channels)  
Program Epic  CCS2 -3552  
API Event Name  onDtvEpgUpdate  
Parameters  DtvEpgUpdateStatus  status  INPROGRESS  
SUCCESS  
CANCELLED  
Return  void   
Feature Description:  
Status of EPG Update started by user  would be provided through onDtvEpgUpdate  
• When EPG Update is INPROGRESS  and user wants to exit EPG, first dtvDisplayEpg with 
CANCEL_UPDATE  should be sent, followed with dtvDisplayEpg  with BACK  or CLOSE_AL L 
• After receiving onDtvEpgUpdate as SUCCESS , application should request dtvDisplayEpg  with 
DtvEpgOperation  as DISPLAYEPG_LIST to update the EPG button status  
 
Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
• User has selected Update in EPG Program Guide  
Sequence:  
For Complete Feature Sequence, refer EPG 
 
3.4.10  Broadcast Search Update  
Feature  Manual Foreground Broadcast Search (Relay/Affiliated Station) / Automatic 
Foreground Broadcast Search (Relay/Affiliated Station)  
Program Epic  CCS2 -3560  / CCS2 -3561  
API Event Name  onDtvBroadcastSearchUpdate


--- Page 61 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Parameters  DtvBroadcastSearchStatus  status  INPROGRESS  
COMPLETE_NOSTATION_FOUND  
COMPLETE_RELAYSTATION_FOUND  
COMPLETE_AFFILIATEDSTATION_FO
UND  
boolean  isDetected   
int channelNumber  00 
13~52 (physical channel number)  
Return  void   
Feature Description:  
• When Broadcast Search (Manual / Automatic) is ongoing Intermediatory and concluding events would 
be provided, through DtvBroadcastSearchStatus  
• When DtvBroadcastSearchStatus  is INPROGRESS,  
- isDetected  == True : valid signal was detected for the physical channel number  
- isDetected  == False : no valid signal was detected for the physical channel number  
- channelNumber :  current scanned physical channel number (13~52)  
• When DtvBroadcastSearchStatus  is not INPROGRESS, ignore isDetected , channelNumber  
• If DtvBroadcastSearchStatus   
- COMPLETE_NOSTATION_FOUND : No channel was found during search. TV Module would tune to 
back previous playing channel if any  
- COMPLETE_RELAYSTATION_FOUND : Relay station was found during search and TV Module would 
tune to the relay station.  
- COMPLETE_AFFILIATEDSTATION_FOUND : Affiliate station was found during search and TV Module 
would tune to the affiliated station.   
• When dtvBroadcastSearch STOP_SEARCH is requested, onDtvBroadcastSearchUpdate  with 
DtvBroadcastSearchStatus  as COMPLETE_NOSTATION_FOUND  would be provided  as the conclusive 
event  
Pre-Condition:  
• TV Module is running, and service is available  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
Sequence:  
For Complete Feature Sequence, refer Broadcast Search


--- Page 62 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.4.11  EWS  Update  
Feature  EWS (Emergency Warning Service) Notification  
Program Epic  CCS2 -3563  
API Event Name  onDtvEwsEventUpdate  
Parameters  DtvEwsEventLevel  level  END  
LEVEL_1  
LEVEL_2  
TEST  
int threeDigitNumber  000~199 (Full seg)  
 600~799  (One seg)  
Return  void   
Feature Description:  
Emergency Warning Updates would be provided through this interface  whenever such updates are received 
from the broadcaster.  
• Actions to be performed by application on receiving onDtvEwsEventUpdate  
 
DtvEwsEventLevel   
LEVEL_1  Application should check if provided threeDigitNumber is different from the current 
playing threeDigitNumber  (provided through onDtvProgramInfoUpdate ). If yes, 
Application should tune to the provided threeDigitNumber  using 
dtvDirectChannelSelect  
LEVEL_2  Application should show Emergency Warning popup to user.  
If user selects “Yes”, application should check if provided threeDigitNumber is different 
from the current playing threeDigitNumber  (provided through 
onDtvProgramInfoUpdate ). If yes, Application should tune to the provided 
threeDigitNumber  using dtvDirectChannelSelect  TEST  
END  If Emergency Warning popup shown, application should hide the popup  
 
Pre-Condition:  
• TV Module is running, and service is available.  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
Important:


--- Page 63 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • When displaying EPG/Program Information  or BML, it is necessary to close EPG/Program Information  
or BML before switching to EWS service.  
Sequence:  
The Application should follow the activity diagram below to make sure the EWS feature works as specs : 
 
For Complete Feature Sequence, refer EWS


--- Page 64 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 3.4.12  Dtv Event Update  
Feature  Signal Status (Weak / No signal) / No Service Notification / Manual Foreground 
Broadcast Search (Relay/Affiliated Station) / Automatic Foreground Broadcast Search 
(Relay/Affiliated Station)  
Program Epic  CCS2 -3573  / CCS2 -3560  / CCS2 -3561  
API Event Name  onDtv Event Update  
Parameters  DtvEvent  event  NO_ERROR  
WEAKSIGNAL  
NOSIGNAL  
NOBROADCAST  
TRMP_INVALID  
RMPERROR_EC21  
RMPERROR_EC22  
RMPERROR_EC23  
TUNER_ERROR  
TUNE_INPROGRESS  
TUNE_LASTCHANNEL_INPROGRESS  
SEEK_INPROGRESS  
MANUAL_BROADCASTSEARCH_INP
ROGRESS  
AUTO_BROADCASTSEARCH_INPROG
RESS  
TUNE_COMPLETE  
Return  void   
Feature Description:


--- Page 65 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • onDtvEvent Update  would be provided whenever there is a change in the reception of currently played 
channel  
 
• Application can show “Seek Popup” popup when onDtvEventUpdate  with SEEK_INPROGRESS  is 
received  
• Application can show “Affiliated Station Search” popup when onDtvEventUpdate with 
MANUAL_BROADCASTSEARCH_INPROGRESS is received  
• Application can show “Auto Station Search” popup when onDtvEventUpdate with 
AUTO_BROADCASTSEARCH_INPROGRESS  is received  
• In case of TUNER_ERROR  / TRMP_INVALID , current advisory can be cleared. Appropriate error 
notification would be given through onDtvModuleStatusUpdate  NO_ERROR  Default state, no error  No Advisory  
WEAKSIGNAL  Channel tuned but signal 
lost Weak Signal Advisory  
NOSIGNAL  Channel tuning error, 
signal not found  No Signal Advisory  
NOBROADCAST  Channel not being 
broadcasted  No Broadcast Advisory  
TRMP_INVALID  TRMP information is 
invalid  No Advisory  
RMPERROR_EC21   The reception control data is not set. Please wait for a 
moment. (It may take a maximum of 30 seconds.)  
RMPERROR_EC22   This channel cannot be viewed. Please contact the 
customer center of the channel  
RMPERROR_EC23   This program cannot be viewed with this receiver. 
Please contact the customer center of the channel  
TUNER_ERROR   No Advisory  
TUNE_INPROGRESS  Tuning to new  channel  No Advisory  
TUNE_LASTCHANNEL
_INPROGRESS  Tuning to last channel  No Advisory  
SEEK_INPROGRESS  Channel Seek Started by 
user  Show Seek Popup  
MANUAL_BROADCA
STSEARCH_INPROGR
ESS Broadcast Search started 
by user  Show Affiliated Search Popup  
AUTO_BROADCASTS
EARCH_INPROGRESS  Broadcast Search started 
by TV Module  Show Auto Station Search Popup  
Pre-Condition:


--- Page 66 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 • TV Module is running, and service is available .  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
3.4.13  Dtv Module Status Update  
Feature  TV Module Status and Error Notifications  
Program Epic  CCS2 -7661  
API Event Name  onDtv ModuleStatus Update  
Parameters  DtvModuleStatus  status  LOADING  
READY  
HIGH_TEMPERATURE  
NOT_RESPONSIVE  
INTERNAL_ERROR  
FIRMWARE_UPDATE_INPROGRESS  
FIRMWARE_UPDATE_FAILURE  
Return  void   
Feature Description:  
• onDtvModuleStatusUpdate would be provided whenever there is a change in the state of TV Module  
 
• Dtv functionality would be available and can be requested only when the DtvModuleStatus  is READY  
• During other states, TV Menu and TV Settings button should be greyed out and Preset List should not 
be visible for user to access  
• Appropriate Advisories should be shown when DtvModuleStatus  is not READY  and cleared on receiving 
READY  LOADING  TV Module startup in progress  
READY  TV Module up and ready to process all requests  
HIGH_TEMPERATURE  TV Module has high temperature   
NOT_RESPONSIVE  TV Module not responding   
INTERNAL_ERROR  TV Module has internal error  
FIRMWARE_UPDATE_INPROGRESS  TV Module Firmware Update in progress  
FIRMWARE_UPDATE_FAILURE  TV Module Firmware Update failed  
Pre-Condition:


--- Page 67 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
  
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
3.4.14  Dtv Antenna State Update  
Feature  Developer Test Mode (ENG Menu)  
Program Epic  CCS2 -3575  
API Event Name  onDtv AntennaState Update  
Parameters  List< DtvAntenna Status > antenna Status    
Return  void   
Feature Description:  
• onDtvAntennaStateUpdate  would be provided whenever there is a change in the state of any Dtv 
Antenna  
• DtvAntennaStatus  would provide the below information  
DtvAntenna  antenna  DTV_ANTENNA_ 1 
DTV_ANTENNA_ 2 
DTV_ANTENNA_ 3 
DTV_ANTENNA_ 4 
DtvAntennaState  antennaS tate DTV_ANTENNA_STATE_ INVALID  
DTV_ANTENNA_STATE_ OK 
DTV_ANTENNA_STATE_OPEN  
DTV_ANTENNA_STATE_SHORT  
DTV_ANTENNA_DEACTIVATED  
DTV_ANTENNA_DEACTIVATED_LOW_VLTG  
DTV_ANTENNA_DEACTIVATED_HIGH_VLTG  
 
Pre-Condition:  
 
• Application has registered to receive DTV Events by registering through dtvRegisterCallback  
 
3.5 DTV Service Connection Noitification  
3.5.1 Service Connected  
API Event Name  onServiceConnected


--- Page 68 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Parameters  void  void    
Return  void   
Feature Description:  
• onServiceConnected  would be notified when com.bosch.dtv.service  is available and ready to provide 
service  
• This notification would be provided  
- On start -up after DtvManager instance is created and com.bosch.dtv.service is available  
- Upon recovery after previous onServiceDisconnected  notification  
• On receiving this notification application should  
- Register for dtv events through dtvRegisterCallback  
- Initiate the start -up sequence handling (Refer  Dtv Service Connected – Handling ) 
For sequence, refer Dtv Service Connection Notification  
 
Pre-Condition:  
• Application has passed a valid IDtvServiceConnectionListener  instance while creating the DtvManager 
instance  
 
3.5.2 Service Disconnected  
API Event Name  onService Disconnected  
Parameters  void  void    
Return  void   
Feature Description:  
• onServiceDisconnected  would be notified when com.bosch.dtv.service  is unavailable to provide 
service  
• This notification would be provided  
- When onBinderDied notification is received for com.bosch.dtv.service binder  
• On receiving this notification application should  
- Initiate the disconnected  sequence handling (Refer Dtv Service Disconnected – Handling  ) 
For sequence, refer Dtv Service Connection Notification


--- Page 69 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Pre-Condition:  
 
• Application has passed a valid IDtvServiceConnectionListener  instance while creating the DtvManager 
instance  
 
3.6 DTV Service Status Notification  
3.6.1 Service Suspended  
Feature   
Program Epic   
API Event Name  onSuspendEnter  
Parameters  void  void    
Return  void   
Feature Description:  
• onSuspendEnter would be notified when com.bosch.dtv.service   receives SUSPEND_ENTER state from 
CarPowerManager  
• On receiving this notification application should  
- Initiate the suspendEnter sequence handling (Refer  Suspend  ) 
Pre-Condition:  
 
• Application has registered to receive Dtv Service Notification  by registering through 
dtvRegisterServiceStatusCallback  
 
3.6.2 Service Resume  
Feature   
Program Epic   
API Event Name  onSuspendE xit 
Parameters  void  void


--- Page 70 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 Return  void   
Feature Description:  
• onSuspendE xit would be notified when com.bosch.dtv.service  receives SUSPEND_EXIT state from 
CarPowerManager  
• On receiving this notification application should  
- Initiate the suspendExit sequence handling (Refer Resume  ) 
Pre-Condition:  
 
• Application has registered to receive Dtv Service Notification  by registering through 
dtvRegisterServiceStatusCallback  
 
3.7 DTV Results  
OK  Success  
INVALID_PARAM   
INVALID_DATA   
INVALID_LENGTH   
NO_SERVICE   
NOT_SUPPORT   
WEAK_SIGNAL   
CHANNEL_NOT_RECEIVABLE   
CHANNEL_NOT_BROADCASTED   
INVALID_TRMP   
INVALID_STATUS   
RMP_EC21   
RMP_EC22   
RMP_EC23   
UNKNOWN_ERROR


--- Page 71 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4 Sequences  
4.1 Startup Communication Sequence  
4.1.1 Dtv Service Connection Notification


--- Page 72 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.1.2 Dtv Service Connected – Handling  
 
4.1.3 Dtv Service Disconnected – Handling


--- Page 73 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.1.4 Dtv Service Initialization Sequence


--- Page 74 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.2 Auto Preset  
4.2.1 Auto Preset Start


--- Page 75 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.2.2 Auto Preset Stop


--- Page 76 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.3 Channel Seek  
4.3.1 Channel Seek Up


--- Page 77 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.3.2 Channel Seek Stop  
  
 
4.4 Channel Up Down


--- Page 78 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.5 Get Preset List  
 
 
4.6 Select Preset Channel


--- Page 79 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.7 Store Preset Channel  
 
 
4.8 Display Banner


--- Page 80 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.9 Dtv Status Update  
 
 
 
4.10 Direct Channel Select


--- Page 81 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.11  Dtv Initi alize 
 
4.12 Dtv Settings Basic  
4.12.1  Get Configure


--- Page 82 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.12.2  Set Auto Tune Mode  
 
4.12.3  Set Auto Broadcast Search Mode


--- Page 83 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.12.4  Set Auto Event Relay Mode  
 
4.12.5  Set Closed Caption Mode


--- Page 84 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.12.6  Set Audio Mode  
 
4.13 Set Physical Channel


--- Page 85 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.14 Dtv Firmware Update


--- Page 86 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.15 Reception Monitor (Test  Mode) 
 
4.16 Get Version Info


--- Page 87 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.17 Get Program Info  
 
 
4.18 Get RMP Manufacturer Id


--- Page 88 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.19 EPG


--- Page 89 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.20 BML Data Broadcast


--- Page 90 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.21 Set Residential Area


--- Page 91 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.22 Audio ES


--- Page 92 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.23 EWS


--- Page 93 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.24 Broadcast Search  
4.24.1  Manual Broadcast Search ( Affilaited Search)


--- Page 94 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.24.2  Auto Station Search


--- Page 95 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.24.3  Broadcast Search Stop (Affiliated Search and Auto Station Search)


--- Page 96 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.25 Dtv Module Status  
4.25.1  Get Current Module Status   
 
4.26 Dtv Antenna State


--- Page 97 ---


CCS2 DTV API SPECIFICATION  Status:  
A-IVI 
DRAFT  
RBEI/ECR4 -XC  Version:  Date:  Author:  
v0.4.7 07/01/2025  CCS2 DTV Team   
 
 4.27 Suspend to Disk  
4.27.1  Resume  
 
4.27.2  Suspend