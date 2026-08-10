
--- Page 1 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 1/318  
F039902182  
【TRS231BSxxxx 】 
F039902183  
【TRH231BSxxxx 】 
F039990144  
【FRO232BSyyzz 】 
 
HOST CPU -B/E UART IF  
Specif ication  
Ver.1.0.1 
OKAYA ELECTRONICS CORP.   
M’s STYLE TECHNOLOGY CORP .


--- Page 2 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 2/318 Version  History Date  
0.01 1st Draft Version  (Same as Frontier)  2021/07/22 
0.02 4. DTV Status  
  ・Add 「DTV OFF 」 、 「DTV OFF with EPG SCAN 」 
5.1.1. HOST ⇒B/E Command  
  ・Add 「Get Number of Program info 」 
  ・Add 「Get Audio ES info 」 
  ・Add 「Set DTV Mode 」 
  ・Add 「Set Video Resolution 」 
  ・Add 「Get Video Resolution 」 
5.1.4. B/E ⇒HOST Event  
  ・Add 「Event relay 」 
  ・Add 「Number of Program info 」 
5.2.3. Channel Up/Down  
  ・Add New Parameters in Data 3.  
  ・Add Comment (3) and (4)  
5.2.4. Physical Channel Set  
  ・Delete 「for debug 」 
5.3.1. Set auto tune Mode  
  ・Add New Parameter in Data 2 : 03h Auto with Seamless  
5.3.12. Set DTV Mode  
  ・Add New Command  
5.3.13. Set Video Resolution  
  ・Add New Command  
5.4.1. Get DTV Status  
  ・ Add New Parameter in Data 4 :  
05h : DTV OFF / 06h : DTV OFF with EPG SCAN  
5.4.3. Get Configure  
  ・Add New Parameter in Data 6 : 03h : Auto with Seamless  
5.4.15. Get Number of Program info  
  ・Add New Command  
5.4.16. Get Audio  ES info 
  ・Add New Command  
5.4.17.  Get Video Resolution  
  ・Add New Command  
5.7.1. DTV Status  
  ・Add New Parameter in Data 2 :  
05h : DTV OFF / 06h : DTV OFF with EPG SCAN  
5.7.8. Event relay  
  ・Add New Command  
5.7.9. Number of Program info  
  ・Add New Command  2021/08/23  
0.03 2.2. Communication Format  
  ・Change Response Request number format.  
5.1.1. HOST ⇒B/E Command  
  ・Add 「Set Banner Config 」 
  ・Add 「Get Banner Config 」 
  ・Add 「Set Character Set 」 
  ・Add 「Get Character Set 」 
  ・Add 「Get TS Name with UTF -8」 
  ・Add 「Get Program Information with UTF -8」 
5.1.4. B/E ⇒ HOST Event  2021/09/10


--- Page 3 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 3/318   ・Add 「Program Information with UTF -8」 
5.2.1. Channel Scan  
  ・Add New Parameter in Data 2  
  ・Add comment in Description.  
  ・Change Error Condition in "Invalid Parameter"  
5.2.8. Direct Channel Select (1)  
  ・Add New Optional Parameter.  
  ・Change Error Condition in "Invalid Parameter"  
5.3.1. Set auto tune Mode  
  ・Change Parameter in Data 2 : Auto and Auto with  
Seamless  
5.3.7. Set Baud rate  
  ・Change default value in Data 2.  
5.3.9. Set DTV Parameter  
  ・Add New Parameter in Data 154 – 185 
5.3.12. Set DTV Mode  
  ・Add (3) : Description about scan channel.  
5.3.13. Set Video Resolution  
  ・Typographical correction  (5) Sequence  
5.3.14. Set Banner Config  
  ・Add New Command  
5.3.15. Set Character Set  
  ・Add New Command  
5.4.3. Get Configure (2)  
  ・Change Parameter in Data 2 : Auto and Auto with  
Seamless  
5.4.7. Get Service Information  
  ・Support UTF -8 Character  set 
5.4.8. Get DTV Parameter  
  ・Add New Parameter in Data156 – 187 
5.4.16. Get Audio ES info  
  ・Change to New Format  
5.4.18. Get  Banner Config  
  ・Add New Command  
5.4.19. Get Character Set  
  ・Add New Command  
5.4.20. Get TS Name with UTF -8 
  ・Add New Command  
5.4.21. Get Program Information with UTF -8 
  ・Add New Command  
5.7.10. Program Information with UTF -8 
  ・Add New Event  
0.04 2.1. Communication Configuration  
  ・Change Baud rate  
2.2. Communication Format  
  ・Data Length : Changed the definition of the unit of length  
  ・Correct comment  Request No.  
5.1. Command List  
  ・Delete Comment  
  ・Delete Boot/Loader  
5.1.1. HOST ⇒B/E Command  
  ・Add 「Set DTV Parameter 2 」 
  ・Add 「Get DTV Parameter 2 」 2021/09/28


--- Page 4 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 4/318   ・Add 「Get Service  Information with UTF -8」 
  ・Add 「Get Program Description with UTF -8」 
  ・Add 「Get Program Name with UTF -8」 
  ・Add 「Get Audio ES info with UTF -8」 
  ・Add 「Set User ID 」 
  ・Add 「Get User ID」 
  ・Add 「Set EPG Config 」 013Dh  
  ・Add 「Get EPG Config 」 013Eh  
  ・Add 「Set Video Color 」 013Fh  
  ・Add 「Get Video Color 」 0140h  
  ・Add 「Set Event Mask 」 0141h  
  ・Add 「Get Event Mask 」 0142h  
5.1.4. B/E ⇒HOST Event  
  ・Add 「TS Name Update 」  820E  
  ・Add 「TS Name Update with UTF -8」802F  
5.2.1. Channel Scan  
  ・Add Result OK Send Timing.  
  ・Data 3 : Add Optional Function  that Tune top channel  
5.2.2. Channel Set  
  ・Change No Service Comment.  
5.2.4. Physical Channel Set  
  ・Clerical error correction  in (1)  
  ・Antenna Number Condition Deleted in (4)  
  ・No Service Error Deleted in (4).  
5.2.7. ES Switch  
  ・Correction Invalid Parameter Condition . 
5.2.8. Direct Channel Select  
  ・Update Description.  
  ・Delete unsupported  value from example.  
5.2.11. Watch Dog  
  ・Delete Error Handling  
5.2.14. Display Banner  
  ・Add Invalid Parameter Condition . 
5.2.15. Service  ID Channel Select  
  ・Delete wrong comment . 
  ・Delete Invalid Parameter Condition.  
5.3.1. Set auto tune Mode  
  ・Change Parameter in Data 2 : Auto and Auto with  
Seamless  
Add Description additional  function.  
5.3.2. Set Closed Caption  Mode  
  ・Change to table in (1) Data2.  
5.3.7. Set Baud rate (3)  
  ・Add Comment  
5.3.8. Set DTV System  
  ・Add Fixed 3x1Diver System  
  ・Add New Comment for F039902182 . 
5.3.12. Set DTV Mode  
  ・Update Description.  
5.3.14. Set Banner Config  
  ・Add New Parameter in Data9 -10. 
  ・Add Comment.


--- Page 5 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 5/318 5.3.16. Set DTV Parameter 2  
  ・Add New Command  
5.3.17. Set User ID  
  ・Add New Command  
5.3.18. Set EPG Config (T.B.D.)  
5.3.19. Set Video Color  
  ・Add New Command.  
5.3.20. Set Event Mask  
  ・Add New Command  
5.4.1. Get DTV Status  
  ・Add Fixed 3x1Diver System in (2) Data 14.  
5.4.3. Get Configure  
  ・Change Parameter in Data 2 : Auto and Auto with  
Seamless  
5.4.7. Get Service Information  
  ・Delete UTF -8 Support.  
5.4.10. Get DTV System  
  ・Add Fixed 3x1 Diver System  
5.4.15. Get Number of Program info  
  ・Add New Parameter in Data 2.  
5.4.16. Get Audio ES info  
  ・Delete UTF -8 Support  
5.4.18. Get Banner Config  
  ・Add New Parameter in Data11 -13. 
5.4.22. Get DTV Parameter 2  
  ・Add New Command  
5.4.23. Get Service Information with UTF -8 
  ・Add New Command  
5.4.24. Get Program Description with UTF -8 
  ・Add New Command  
5.4.25. Get Program Name with UTF -8 
  ・Add New Command  
5.4.26. Get Audio ES info with UTF -8 
  ・Add New Command  
5.4.27. Get User ID  
  ・Add New Command  
5.4.28. Get EPG Config  (T.B.D.)  
5.4.29. Get Video Color  
  ・Add New Command  
5.4.30. Get Event Mask  
  ・Add New Command  
5.7.1. DTV Status  
  ・Add Fixed 3x1 Diver System in (1) Data 12.  
5.7.8. Event relay  
  ・Change Command Type to Need Ack  
5.7.9. Number of Program info  
  ・Change Command Type to Need Ack  
5.7.10.  Program Information with UTF -8 
  ・Change Fragment Data Number  
5.7.11. TS Name Update  
  ・Add New Event  
5.7.12. TS Name Update with UTF -8 
  ・Add New Event


--- Page 6 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 6/318 0.05 2.1. Communication Configuration  
  ・Add Comment for Default Baud rate.  
2.2. Communication Format  
  ・Add Model Number  
5.1.1. HOST ⇒B/E Command  
  ・Add 「Get Part  Number 」 
  ・Add 「Get Program Name by 3Digit Number 」 
  ・Add 「Get Program Name with UTF -8 by 3Digit Number 」 
  ・Add 「Get Logo Data by 3Digit Number 」 
5.1.3. B/E ⇒HOST Command  
  ・Boot Mode change Boot to DTV.  
5.1.4. B/E ⇒HOST Event  
  ・Add 「Logo Update 」 
5.1.6. HOST ⇒BE Test  & Debug Command  
  ・Del 「Write F/E Register 」 
  ・Del 「Read F/E Register 」 
  ・Hardware Test change to DTV.  
5.2.4. Physical Channel Set (3)  
  ・Add Description.  
5.2.9. DTV Initialize  
  ・Add New Parameter.  
5.3.1. Set auto tune Mode (3)  
  ・Add description about default value.  
5.3.6.  Set Auto Event Relay  
  ・Add new parameter.  
5.3.7. Set Baud rate (1)  
  ・Delete default.  
5.3.8. Set DTV System (1)  
  ・Add new parameter.  
5.3.9. Set DTV Parameter (1)  
  ・Move new parameter to DTV Parameter  2. 
5.3.13. Set Video Resolution (1)  
  ・Change  720p/480p value.  
5.3.14. Set Banner Config (3)  
  ・Add New Description.  
5.3.15. Set Character Set (3)  
  ・Add New Description.  
5.3.16. Set DTV Parameter (1)  
  ・Video Resolution value changed.  
  ・Move new pa rameter form DTV Parameter  
  ・Add new parameter for EPG  
5.3.17. Set User ID (1) 
  ・Change User ID Max Value  and Definition . 
5.3.17. Set User ID (3)  
  ・Delete reboot.  
5.3.18. Set EPG Config  
  ・Add Parameter  
5.3.19 Set Video Color  
  ・Add Parameter  
  ・Update description  
5.3.20. Set Event Mask (1)  
  ・Add Logo Update Event Mask  2021/10/2 8


--- Page 7 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 7/318 5.4.1. Get DTV Status  
  ・Add BML Status.  
  ・Added new values for Diver Mode  
5.4.3. Get Configure  
  ・Add New Parameter.  
5.4.7. Get Service Information  
  ・Updated description  
5.4.8. Get DTV Parameter (2)  
  ・Move new parameter to  DTV Parameter 2.  
5.4.1 0. Get DTV System  
  ・Added new values for DTV System  
5.4.13. Get  Logo Data (3)  
  ・Add Type 7 Simple Logo with UTF -8 
  ・Add Simple Logo Examples  
5.4.16. Get Audio ES info (3)  
  ・Add language text length.  
5.4.17. Get Video Resolution (2)  
  ・Change  720p/480p value.  
5.4.21. Get Program Information with UTF -8 (2) 
  ・Change Length of Program Name fields.  
  ・Corrected typo in description.  
5.4.22. Get DTV Parameter 2  
  ・Add New Parameter.  
5.4.23. Get Service Information with UTF -8 
  ・Updated description  
5.4.24. Get Program Description with UTF -8 (2) 
  ・Change Length of Program  Description Length fields.  
5.4.25. Get Program Name with UTF -8 (2) 
  ・Change Length of Program Name fields.  
5.4.26. Get Audio ES info with UTF -8 
  ・Add language text length.  
5.4.27. Get User ID (2)  
  ・Change User ID Max Value  and Definition . 
5.4.28. Get EPG Config  (1) 
  ・Add Parameter.  
5.4.30. Get Event Mask (2)  
  ・Add Logo Update Event Mask  
5.4.31. Get Part Number  
  ・Add New Command . 
5.4.32. Get Program Name by 3Digit Number  
  ・Add New Command  
5.4.3 3. Get Program Name with UTF -8 by 3Digit Number  
  ・Add New Command  
5.4.3 4. Get Logo Data by 3Digit Number  
  ・Add New Command  
5.6.1. Wakeup (2)  
  ・Add User ID.  
5.7.1. DTV Status  
  ・Add BML Status.  
  ・Added new values for Diver Mode  
5.7.4. DTV Event  
  ・Add BML Errors  
5.7.8. Event relay (1)


--- Page 8 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 8/318   ・Add Three Digit Number.  
5.7.9. Number of Program info  
  ・Change Home/Travel Both Data  
  ・Updated description  
5.7.10. Program Information with UTF -8 (1) 
  ・Change Length of Program Name fields.  
5.7.13. Logo Update  
  ・Add New Command  
5.9.1. Write F/E Register  
  ・Not Support  
5.9.2. Read F/E Register  
  ・Not Support  
0.06 5.1.4. B/E ⇒ HOST Event  
  ・Add 「EPG Button Status 」(8211h)  
  ・Add 「BML Error 」(8212h)  
5.2.4. Physical Channel Set (3)  
  ・Modify  description.  
5.2.9. DTV Initialize (3)  
  ・Add Initialize Data Table  
5.2.12. Display EPG (3)  
  ・Add New Description  
  ・Deleted EPG update time/ channel . 
5.2.14. Display Banner (3)  
  ・Change Automatically hide time . 
5.3.6. Set Auto Event Relay (1)/(3)  
  ・Change to number of notification and interval  
5.3.8. Set DTV System  (3) 
  ・Delete change sequence . 
  ・Change System configuration  table  
5.3.13. Set Video Resolution  
  ・Delete reboot request  
  ・Delete default  
  ・Add New Parameter 「480i」 
5.3.14. Set Banner Config  
  ・Add New Parameter  
  ・Modify Description  
5.3.16. Set DTV Parameter 2  
  ・Regenerate data content  
5.3.18. Set EPG Config  
  ・Add New Data  
5.3.19. Set Video Color  
  ・Add Default Value  
5.3.20. Set Event Mask  
  ・Add New Event  
5.4.1. Get DTV Status  
  ・Modify Data : 17  
  ・Delete Data : 19  
5.4.3. Get Configure  
  ・Change Data25,26  
5.4.12. Get Program Name (2)  
  ・Correct data length  
5.4.13. Get Logo Data  
  ・Change PNG Data Format(include PLTE).  2021/11/13


--- Page 9 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 9/318   ・Modify  description.  
5.4.17. Get Video Resolution  
  ・Add New Parameter 「480i」 
5.4.18. Get Banner Config (2)  
  ・Add New Parameter  
5.4.22. Get DTV Parameter 2  
  ・Corrected typo  
  ・Regenerate data content  
5.4.25. Get  Program Name with UTF -8 (2) 
  ・Correct data length  
5.4.29. Get EPG Config  
  ・Add New Data  
5.4.29. Get Video Color (2)  
  ・Add Gamma Parameter  
5.4.30. Get Event Mask  
  ・Add New Event  
5.4.32. Get Program Name by 3Digit Number  
  ・Correct data length  
5.4.34. Get Logo Data by 3Digit Number  
  ・Modify  description.  
5.6.1. Wakeup  
  ・Add Current User  
5.7.1. DTV Status  
  ・Modify Data : 15  
  ・Delete Data : 17  
  ・Modify  description.  
5.7.4. DTV Event  
  ・Delete BML Error  
5.7.9. Number of Program Info (1)  
  ・Modify Data number.  
5.7.14. EPG Button Status  
  ・Add New Event  
5.7.15. BML Error  
  ・Add New Event  
5.8.1. SW Update (3)  
  ・Delete NVRAM Data  
 
0.07 2.2. Communication Format  
  ・Add New Format  for 16bit Length Field  
5.2.12. Display EPG  
  ・Modify Description  
5.3.6. Set Auto Event Relay  
  ・Update  description.  
5.3.16. Set DTV Parameter 2  
  ・Add New Parameter  
5.3.18. Set EPG Config  
  ・Update description.  
5.3.19. Set Video Color  
  ・Corrected maximum band default values  of gamma.  
5.3.20. Set Event Mask  
  ・Modify parameter description.  
5.4.22. Get DTV Parameter 2  
  ・Add New Parameter  2021/11/22


--- Page 10 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 10/318 5.4.29. Get Video Color  
  ・Corrected maximum values of gamma.  
5.4.30. Get Event Mask  
  ・Modify parameter description.  
5.6.1.  Wakeup  
  ・Modify Description  
5.7.14. EPG Button Status  
  ・Update description.  
0.08 5.2.12. Display EPG  
  ・Add Display Type Optional Data  
5.3.16. Set DTV Parameter 2  
  ・Add New Parameter  
  ・Delete duplicate definitions . 
5.4.13. Get Logo Data (3)  
  ・UTF -8 Length Support 4byte  UTF -8 code  
5.4.20. Get TS Name with UTF -8 (2) 
  ・Support 4byte UTF -8 code  
5.4.21. Get Program Information with UTF -8 (2) 
  ・Support 4byte UTF -8 code  
5.4.22. Get DTV Parameter 2  
  ・Add New Parameter  
  ・Delete duplicate definitions . 
5.4.23. Get Service Information with UTF -8 (3) 
  ・Support 4byte UTF -8 code  
5.4.26. Get Audio ES info with UTF -8 (3) 
  ・Support 4byte UTF -8 code  
5.7.10. Program Information with UTF -8 (1) 
  ・Support 4byte UTF -8 code  
5.7.12. TS Name Update with UTF -8 (1) 
  ・Support 4byte UTF -8 code  
5.9.6. HW Test  
  ・New Add Operation.  2021/12/15  
0.09 5.1.4. B/E ⇒HOST Event  
  ・Add New Event 「C/N Information 」(8213h)  
5.2.12. Display EPG  
  ・Updated Description  
5.3.16. Set DTV Parameter 2  
  ・Add comment in Receive Logo Type  
  ・Add New Parameter  
5.3.19. Set Video Color  
  ・Updated Description  
5.4.22. Get DTV Parameter 2  
  ・Add comment in Receive Logo Type  
  ・Add New Parameter  
5.7.3. Search Status  
  ・Add New Paramete r 
5.7.15. BML Error  
  ・Correct Data Length . 
5.7.16. C/N Information  
  ・Add New Command   
0.10 5.2.5. Search Up/Down  
・Add New Description  
5.2.6. Broadcast Search  2022/03/11


--- Page 11 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 11/318   ・Add New Description  
5.2.9  DTV initialize  
・Change  Description  content  
5.2.12. Display EPG  
  ・Add New Description  
5.3.9. Set DTV Parameter  
  ・Add New Description  
5.3.13. Set Video  
  ・Add New Description  
5.3.16 . Set DTV Parameter2  
  ・Add New Parameter  
  ・Add New Description  to some data  
5.3.18. Set EPG Config  
・Data length correct  
・Add New Parameter  
5.3.20. Set Event Mask  
  ・Add New Description in Data0,1 and 2.  
  ・Change Data 2 parameter.  
5.4.7. Get Service Information  
  ・Delete Sentence in Description  
5.4.13 . Get Logo Data  
  ・The value inside of Description are changed.  
  ・Change a sentence in Description  
5.7.1. DTV Status  
  ・Data 14, 15 are changed.  
5.7.4. DTV Event  
  ・Add New Description  
5.7.16. C/N Information  
  ・Data description change  
5.9.3. Test Mode  
  ・Added additional Audio Modes for pink noise  
  ・Updated video color table  
  ・Replaced color bar image with actual one.  
0.11 2.2 Communication Format  
  ・Add new description.  
5.2.9. DTV Initialize  
  ・Add  Description content.  
5.2.12. Display EPG  
  ・Add description  on Data 3  
  ・Add new content on Description.  
5.3.12. Set DTV Mode  
  ・Change Data length.  
  ・Add new Data 4.  
  ・Add new contents on Description.  
5.3.14. Set Banner Config  
  ・Banner Width Minimum / Maximum changed.  
  ・Add new data (13), change Data length.  
  ・Add and changed description.  
5.3.16 Set DTV parameter 2  
  ・Add description on data  25~2 7,46,47. 
  ・Add new data (107), (108)  
  ・Add new contents on Error Handling.  
5.3.18. Set EPG Config


--- Page 12 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 12/318   ・EPG Type Image Update.  
  ・Add description about figure.  
  ・Add new description on Data 2.  
  ・Add new data (52).  
5.4.1. Get DTV status  
  ・Add new parameter on Data 17.  
5.4.11. Get Program List  
  ・Delete Sentence in Description . 
5.4.13. Get Logo Data  
  ・Correct Data Length in (2).  
・Delete Sentence in Description . 
5.4.18 Get Banner config  
  ・Add new data(15)  
  ・Change data length  
5.4.22. Get DTV Parameter 2  
  ・Add new data (109),(110) . 
5.4.23. Get Service Information with UTF -8 
  ・Delete Sentence in Description.  
5.4.28 Get EPG Config  
  ・Add new data (51~54).  
5.7.1. DTV status  
  ・Add new parameter on Data 15.  
5.7.3 Search Status  
・Add new description  on Data 2, 4  
・Add new contents on Description.  
5.7.4 DTV Event  
  ・Add new data(20h)  in DTV event.  
  ・Changed description in DTV event code (code 82, 84).  
5.7.15 BML  Status  
  ・Change chapter.  
  ・Add new BML status( B3h,B4h,B5h,B6h ). 
5.9.3 Test mode  
  ・Correct missing data in description.  
0.12 3 Error Code  
  ・Add new error code on the table.  
5.2.10 Shutdown  
  ・Add new description on Sequence . 
5.2.12 Display EPG  
・Add new description about broadcast search behaver.  
5.3.5 Set Residential Area  
・Change  of description method of Data 3 . 
5.3.14 Set Banner Config  
  ・Add new Data 14.  
5.3.16 Set DTV Parameter 2  
・Change  of description method of Data 8 . 
・Change the data contents on Data 46.  
・Change the description of Data name.  
・Change  of description method of Data 47. 
・Add new Data 109.  
5.3.18 Set EPG Config  
・Change  of description method of Data 2. 
・Change the description of Data name.  2022/04/08


--- Page 13 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 13/318 ・EPG Type Image Update.  
5.4.18 Get Banner Config  
・Add new Data 16.  
5.4.22 Get DTV Parameter 2  
・Change  of description method of Data 10 . 
・Change the description of Data name.  
・Change  of description method of Data 49.  
・Add n ew Data 111.  
5.4.28 Get EPG config  
  ・Change  of description method of Data 4. 
・Change the description of Data name.  
5.7.4 DTV Event  
  ・Add new description on Description.  
  ・Add supplement to “20h”.  
  ・Add new flow.  
5.9.3 Test mode  
  ・Change  contents on Data 3  
5.9.5 Monitor Status  
・Change  of description method of Data 3 . 
5.9.7 2nd TS Test  
・Change  of description method of Data 4 . 
5.9.8 2nd TS Test Status  
・Change  of description method of Data 2 . 
0.13 5.2.8. Direct Channel Select  
  ・Add Comment in (1) Data 5.  
5.2.13. Update Preset Table  
  ・Change Data length in (1).  
5.2.14. Display Banner  
  ・Add new description  in (3)  
5.3.5. Set Residential Area  
  ・Add comment in (1) Data 3.  
5.3.6. Set Auto  Event Relay  
  ・Change description in (3)  
5.3.7. Set Baud rate  
  ・Delete parameter 0Bh in (1) Data 2.  
5.3.12. Set DTV Mode  
  ・Add condition in (1) Data 4.  
5.3.15. Set Character Set  
  ・Change Data length in (1)  
5.4.12. Get Program Name  
  ・Change Max Data length in (2)  
5.4.13. Get Logo Data  
  ・Change Data length in (1)  
5.4.25. Get Program Name with UTF -8 
  ・Change description in (3)  
5.4.32. Get Program Name by 3Digit Number  
  ・Change Max Data length in (2)  
5.4.33. Get Program Name with UTF -8 by 3Digit Number  
  ・Change Max Data length in (2)  
5.4.34. Get Logo Data by 3Digit Number  
  ・Change Data length in (1)/(2)  
5.7.2  Scan Status  
  ・Change description of Data 4 in (1)/(2)  2022/4/22


--- Page 14 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 14/318 5.7.4. DTV Event  
  ・Add figure Title.  
5.7.8. Event relay  
  ・Change Sequence  
5.7.9. Number of Program info  
  ・Change Sequence  
5.7.11. TS Name Update  
  ・Change Data length in (1)  
5.7.12. TS Name Update with UTF -8 
  ・Change Data length in (1)  
0.14 5.3.9. Set DTV Parameter  
  ・Add range value to each data  
5.3.14. Set Banner Config  
  ・Add range value to each data  
5.3.16. Set DTV Parameter 2  
  ・Add range value to each data  
5.3.17. Set User ID  
  ・Add New description on Description  
5.3.18. Set EPG Config  
  ・Add range value to each data  
  ・Change data range of Data 46,47  
5.4.22. Get DTV Parameter 2  
  ・Change data range of Data 91,92  
5.7.4. DTV Event  
  ・Change  the description of chart.  
  ・Add new event in state  diagram about Event Code  
5.9.3. Test Mode  
  ・Add new description.  
6.DTV information  
  ・Update  the chapter content.  2022/6/1 
0.15 5.7.4. DTV Event  
  ・Add new event in state diagram about Event Code  
5.9.3. Test Mode  
  ・Change  the description  
6.1. Channel List  
  ・Add note in the table  
6.2. Last Channel  
  ・Add note in the table  
6.3. DTV Configuration  
  ・Add note in the table  2022/6/8  
0.16 5.2.1. Channel Scan  
  ・Remove sentence in Description.  
5.3.6. Set Auto Event Relay  
  ・Add new description on data 2  
5.3.14. Set Banner Config  
  ・Remove sentence in Description.  
  ・Change sentence in Description.  
5.3.16. Set DTV Parameter 2  
  ・Change data name  on EPG related data . 
・Change  data range of data 33 , 87 
  ・Add new description on data 32,33,34  
  ・Change data name on data 10 9 
5.3.18. Set EPG config  2022 /7/6


--- Page 15 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 15/318   ・Change data name.  
  ・Change  image on Description  
5.4.22. Get DTV Parameter 2  
  ・Change data name  on EPG related data  
  ・Change data name on data 111  
5.4.28. Get EPG Config  
  ・Change data name  
6.4. DTV System  
  ・Removed note  
0.16.1 5.3.9. Set DTV parameter  
  ・Correct the BER related data range  
  ・Correct the description of time -related calculation method  2022/8/4  
0.17 This document is integrated with New Frontier project  
 F039990144 【FRO232BSyyzz 】. 
2. UART Communication Specification  
 ・Add New Frontier Baud rate data  
5.2.1 Channel Scan  
 ・Add a new comment in Description  
5.2.12 Display EPG  
 ・Add EPG scale information in Description  
5.3.5 Set Residential Area  
・Change the sentence  in Description  
5.3.16 Set DTV Parameter 2  
 ・Change the description on Data 32,33,34 
 ・Change the description on  Description  
5.3.18 Set EPG Config  
 ・Add New Frontier project image or EPG type  
5.3.19 Set Video Color  
・Change the contents of  the data 4 to 6  
5.7.15 BML Status  
 ・Change the sentence of B5h, B4h in Description.  
5.8.1 SW Update  
 ・Add (6)  Appendix (SW update flow)  
5.9.3 Test Mode  
 ・Add New Frontier project test mode image . 
6.4 DTV System  
 ・Change contents in Note  2022/9/6  
0.18 5.1.1. HOST ⇒ B/E Command  
  ・Add New Command 「0147h Start Background Search 」 
  ・Add New Command 「0148h Start Background Scan 」 
5.1.4. B/E ⇒ HOST Event  
  ・Add New Command 「8214h Manual EPG Scan Result 」 
5.2.16. Start Background Search  
  ・Add New Command  
5.2.17. Start Background Scan  
  ・Add New Comman d 
5.3.6. Set Auto Event Relay  
  ・Updated Description  
5.3.16. Set DTV Parameter 2  
  ・Modified the explanation of Data32  
  ・Removed the table showing Data format  
5.3.19. Set Video Color  
  ・Removed Gamma related line from Description


--- Page 16 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 16/318 5.3.20. Set Event Mask (1) Data4  
  ・Add New Parameter  
5.4.1. Get DTV Status (2) Data16  
  ・Add New Parameter  
5.4.6. Get Program Information  
  ・Corrected Data indices in the response table  
5.4.7. Get Service Information  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.11. Get Program List  
  ・Corrected Data Length in the response table  
  ・Added new table for response with Header Type 2  
  ・Corrected the Number of Events in Description  
  ・Updated Description  
5.4.13. Get Logo Data  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.16. Get Audio ES info  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.20. Get TS Name with UTF -8 
  ・Corrected Data Length and indices in the response table  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.21. Get Program Information with UTF -8 
  ・Corrected Data indices in the response table  
  ・Corrected Data11 value in the response table  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.23. Get Service Information with UTF -8 
  ・Added new table for response with Header Type 2  
  ・Updated Description  
  ・Corrected upper limit of Service Name Length in 
Description  
5.4.24. Get Program Description with UTF -8 
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.25. Get Program Name with UTF -8 
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.26. Get Audio ES info with UTF -8 
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.30. Get Event Mask (2) Data6  
  ・Add New Parameter  
5.4.33. Get Program Name with UTF -8 by 3Digit Number  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.4.34. Get Logo Data by 3Digit Number  
  ・Added new table for response with Header Type 2  
  ・Updated Description  
5.7.1. DTV Status (1) Data14


--- Page 17 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 17/318   ・Add New Parameter  
5.7.10. Program Information with UTF -8 
  ・Corrected Data indices in the event table  
  ・Corrected Data9 value in the event table  
  ・Added new table for event with Header Type 2  
  ・Updated Description  
5.7.11. TS Name Update  
  ・Added new table for event with Header Type 2  
  ・Updated Description  
5.7.12. TS Name Update with UTF -8 
  ・Corrected Data indices in the event table  
  ・Added new table for event with Header Type 2  
  ・Updated Description  
0.19 2.2. Comm unication Format  
  ・Added title to the data format  
  ・Updated Description  
5.2.3. Channel Up/Down  
  ・Updated  Descri ption  
5.3.6. Set Auto Event Relay  
  ・Updated Description  
5.3.13. Set Video Resolution  
  ・Added New Parameter 「1080p@30Hz 」 
5.3.16. Set DTV Parameter 2  
  ・Added 1080p@30Hz resolution to Data 5  
5.3.20. Set Event Mask  
  ・Changed BML Error to BML Status  
5.4.5. Get Audio  ES 
  ・Changed the content s of Data 4  
5.4.7. Get Service Information  
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・Updated Description  
5.4.11. Get Program List  
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・For Header Type 2, Added Data Length value if Result is 
NG 
  ・Updated Description  
5.4.13. Get Logo Data  
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.16. Get Audio ES Info  
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.17. Get Video Resolution  
  ・Added New Parameter 「1080p@30Hz 」 
5.4.20. Get TS Name with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.21. Get Program Information with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.22. Get DTV Parameter 2  
  ・Added 1080p@30Hz resolution to Data 7  
5.4.23. Get Service Information with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・For Header Type 2,  Added Data Length upper limit  
  ・Updated Description  
5.4.24. Get Program Description with UTF -8 2022/11/25


--- Page 18 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 18/318   ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.25. Get Program Name with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.26. Get Audio ES Info with UTF -8 
  ・Corrected table title  
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.4.33. Get Program Name with UTF -8 by 3Digit Number  
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・For Header Type 2, Added Data Length value if Result is 
NG 
  ・For Header Type 2, Start Sync[5Ah]  to [59h] changed . 
5.4.34. Get Logo Data by 3Digit Number  
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・For Header Type 2,  Corrected Data length format  
5.7.10. Program Information with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
  ・For Header Type 2,  Added Data Length maximum.  
5.7.11. TS Name Update  
  ・For Header Type 2, Data Length in 2rows changed to one.  
5.7.12. TS Name Update with UTF -8 
  ・For Header Type 2, Data Length in 2rows changed to one.  
0.20 5.3.16. Set DTV Parameter 2  
・Updated Description  
5.3.18 Set EPG Config  
  ・Updated Description  
  ・Removed unnecessary text  
5.4.22. Get DTV Parameter 2  
・Updated Description  
5.7.1. DTV Status  
  ・Added new parameter in data 2.  
5.8.3. Background SW Update Start  
  ・Added new command  
5.8.4. Background SW Update Cancel  
  ・Added new command  
5.8.5. Background SW Update  
  ・Added new command  
5.8.6. Background SW Update Status  
  ・Added new command  
6.1. Channel List  
  ・Updated store condition  
6.2. Last Channel  
  ・Updated store condition  
6.3. DTV Configuration  
  ・Updated store condition  
6.4. DTV System  
  ・Updated store condition  
6.5. TRMP Information  
  ・Updated store condition  
6.6. Logo  
  ・Updated store condition  
6.7. BML Information  
  ・Updated store condition  
6.8. Channel List


--- Page 19 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 19/318   ・Updated store condition  
7.Background SW Update Sequence  
 ・Add chapters 7.1, 7.2, 7.3.  
0.21 5.1.5. SW Update Command  
  ・Title changed( BE⇒HOST SW Update Command -> SW 
Update Command ) 
  ・Add new command.  
5.3.13. Set Video Resolution  
  ・Updated Description  
5.3.19. Set Video Color  
  ・Brightness range changed.  
5.4.29. Get Video Color  
  ・Brightness range changed.   
0.22 5.1.1. HOST⇒B/E Command  
  ・Added new command “DTV Reset”.  
5.1.4. B/E ⇒ HOST Event  
  ・Changed BML Error to BML Status . 
  ・Added new event “DTV Critical Error”  
5.2.9. DTV Initialize  
  ・Correction of typos in Description.  
5.2.18. DTV Reset  
  ・Added new chapter.  
5.3.8. Set DTV System  
  ・Correction of typos in Description.  
  ・Removed invalid statement.  
  ・Corrected Invalid Parameter condition in Error Handling.  
5.3.9. Set DTV Parameter  
  ・Correction of typos in Description.  
5.4.1. Get DTV Status  
  ・Added value 07h to  Data4 in Get DTV Status Response 
table.  
  ・Updated Description.  
5.4.8. Get DTV Parameter  
  ・Correction of typos in Description.  
5.4.11. Get Program List  
  ・Correction of typos in Description.  
5.7.1. DTV Status  
  ・Updated Description.  
5.7.4. DTV Event  
  ・Removed references to Frontier  
5.7.18. DTV Critical Error  
  ・Added new chapter  
5.9.4. Set Debug Parameter  
  ・Removed references to Frontier  
6.4. DTV System  
  ・Correction of typos  2023/05/17  
0.23 5.1.1. HOST⇒B/E Command  
  ・Changed command “DTV Reset” to “DTV Restart”.  
5.2.18. DTV Restart  
  ・Updated DTV Restart Command format.  
  ・Updated DTV Restart Response format.  
  ・Updated Description.  2023/05/26


--- Page 20 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 20/318   ・Updated Error Handling  
  ・Updated Sequence.  
5.7.18. DTV Critical Error  
  ・Updated Event format.  
  ・Updated Description.  
  ・Updated Sequence.  
0.24 2.3.6. B/E ⇒ Host Sequence [Command(Need ACK) – NAK]  
  ・Updated Description.  
2.3.8. B/E ⇒ Host Sequence [Command(No Need ACK)]  
  ・Updated Description.  
5.3.17. Set User ID 
  ・Corrected the length of Response.  
5.4.1. Get DTV Status  
  ・Updated Description.  
5.4.21. Get Program Information  with UTF -8 
  ・Corrected the length of Response.  
5.4.24. Get Program  Description  with UTF -8 
  ・Corrected the length of Response.  
5.4.25. Get Program  Name  with UTF -8 
  ・Corrected the length of Response.  
5.4.31. Get Part Number  
  ・Corrected the length of Response.  
5.4.33. Get Program Name  with UTF -8 by 3Digit Number  
  ・Corrected the length of Response.  
5.4.34. Get Logo Data  by 3Digit Number  
  ・Corrected the length of Response.  
5.6.1. Wakeup  
  ・Corrected the length of Response.  
5.7.1. DTV Status  
  ・Updated Description.  
5.7.9. Number of Program info  
  ・Updated Description.  
  ・Corrected Data Length.  
5.8.1. SW Update  
  ・Updated Error Handli ng. 
5.8.3. Background SW Update Start  
  ・Updated Error Handling.  
5.9. Test & Debug Command  
  ・Removed chapter “ Write F/E Register (Not Support) ”. 
  ・Removed chapter “ Read F/E Register (Not Support) ”. 2023/0 8/09 
0.25 5.3.7. Set Baud rate. 
  ・Updated (3)Description.  
5.3.8. Set DTV System . 
  ・Updated (3)Description.  
5.3.9. Set DTV Parameter . 
・Remove parameter range information from each data.  
    *These information moves to Chapter 8 . 
・Update (3)Description . 
5.3.14. Set Banner Config . 
・Remove parameter range information from each data.  
    *These information refers to Chapter 8.2 or 8.3 . 
・Update (3)Description . 
5.3.16. Set DTV Parameter 2 . 2023/ 12/08


--- Page 21 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 21/318 ・Update data 3 information.  
・Remove parameter range information from each data.  
    *These information moves to Chapter 8 . 
・Update (3)Descriptio n. 
5.3.18. Set EPG Config . 
・Remove parameter range information from each data.  
    *These information refers to Chapter 8.2 or 8.3  
・Update (3)Description . 
5.4.21. Get Program Information with UTF -8. 
・Correct Data Length . 
5.4.24. Get Program Description  with UTF -8. 
・Correct Data Length . 
5.4.25. Get Program Name with UTF -8. 
・Correct Data Length . 
5.4.33. Get Program Name with UTF -8 by 3Digit Number . 
・Correct Data Length . 
5.4.34. Get Logo Data by 3Digit Number . 
・Correct Data Length . 
5.9.1 Test Mode.  
・Update (3)Description.  
5.9.3. Monitor Status . 
  ・Updated Data 2 : Diver Mode(05h~08h) . 
8. DTV parameter and DTV parameter 2 data range . 
・Add chapters 8.1 to 8.3 . 
0.26 2.2 Communication Format  
・Add applicable  range of Header Type 2  
5.3.9 Set DTV Parameter  
・Correct data supplements  
5.4.7 Get Service Information  
・Change Data Length range  
・Change Description  
5.4.23 Get Service Information with UTF -8 
・Change Data Length range  
・Change Description  
5.7.5 EWS Event  
・Add a Description  
5.9.1 Test & Debug command  
・Change the color value for New Frontier  
8.1 DTV Parameter  
・Change data range  description  
・Add Description  
8.2 DTV Parameter 2 data range for Thrush  
・Change data range description  
・Add Description  
8.3. DTV Parameter 2 data range for New Frontier  
・Change data range description  
・Add Description  
・Change d data that cannot be configure  to gray color  2024/4/ 24 
0.27 5.3.9 Set DTV Parameter  
・Correct description  of data range information  
・Add Time data range information  
5.3.16 Set DTV Parameter 2  
・Correct description of data range information  2024/5/ 29


--- Page 22 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 22/318 5.4.23 Get Service Information with UTF -8 
・Correct description content  
5.7.16 C/N Information  
・Correct description of data range information  
5.9.3 Monitor Status  
・Correct description of data range information  
8.1 DTV Parameter data range  
・Correct description of data range information  
・Add Time data range information  
8.2 DTV Parameter 2 data range for Thrush  
・Correct description of data range information  
8.3. DTV Parameter 2 data range for New Frontier  
・Correct description of data range information  
V0.28 5.2.11 Watch Dog 
・Add error handling  
5.3.6 Set Auto Event Relay  
・Add the unit information  to some data 2024/7/25  
V1.0  The official  release version  
5.2.1 Channel Scan  
・Revised description about Data 3.  
・Add error handling about Data 3 content.  
5.8.5 Background SW Update  
・Revised data length  2024/8/10  
V1.0.1  5.2.1 Channel Scan  
・Changed  description  2024/9/5


--- Page 23 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 23/318 Contents  
1. Introduction  ................................ ................................ ................................ .........................  28 
2. UART Communication Specification  ................................ ................................ .................  28 
2.1. Communication Configuration  ................................ ................................ ....................  28 
2.2. Communication Format  ................................ ................................ ..............................  29 
2.3. Communication Sequence  ................................ ................................ ...........................  30 
2.3.1.  Host ⇒ B/E Sequence [Command(Need ACK) – ACK]  ................................ ...... 30 
2.3.2.  Host ⇒ B/E Sequence [Command(Need ACK) – NAK]  ................................ ..... 31 
2.3.3.  Host ⇒ B/E Sequence [Command(Need ACK) – Timeout]  ................................  32 
2.3.4.  Host ⇒ B/E Sequence [Command(No Need ACK)]  ................................ ............  33 
2.3.5.  B/E ⇒ Host Sequence [Command(Need ACK) – ACK]  ................................ ...... 34 
2.3.6.  B/E ⇒ Host Sequence [Command(Need ACK) – NAK]  ................................ ..... 35 
2.3.7.  B/E ⇒ Host Sequence [Command(Need ACK) – Timeout]  ................................  36 
2.3.8.  B/E ⇒ Host Sequence [Command(No Need ACK)]  ................................ ............  37 
2.4. Communication Specification  ................................ ................................ .....................  38 
2.5. Timeout Value  ................................ ................................ ................................ ..............  38 
3. Error Code  ................................ ................................ ................................ ...........................  39 
4. DTV Status  ................................ ................................ ................................ ..........................  40 
5. Data Detail  ................................ ................................ ................................ ..........................  40 
5.1. Command List  ................................ ................................ ................................ ..............  40 
5.1.1.  HOST⇒B/E Command  ................................ ................................ .........................  40 
5.1.2.  HOST⇒B/E Event  ................................ ................................ ................................  41 
5.1.3.  B/E⇒HOST Command  ................................ ................................ .........................  42 
5.1.4.  B/E⇒HOST Event  ................................ ................................ ................................  42 
5.1.5.  SW Update Command  ................................ ................................ ..........................  42 
5.1.6.  HOST⇒BE Test & Debug Command  ................................ ................................ .. 42 
5.1.7.  B/E⇒HOST Test & Debug Command  ................................ ................................ . 43 
5.2. HOST⇒B/E Command  ................................ ................................ ................................  44 
5.2.1.  Channel Scan  ................................ ................................ ................................ ........  44 
5.2.2.  Channel Set  ................................ ................................ ................................ ...........  46 
5.2.3.  Channel Up/Down  ................................ ................................ ................................  48 
5.2.4.  Physical Channel Set  ................................ ................................ ...........................  50 
5.2.5.  Search Up/Down  ................................ ................................ ................................ ... 52 
5.2.6.  Broadcast Search  ................................ ................................ ................................ .. 54 
5.2.7.  ES Switch  ................................ ................................ ................................ ..............  56 
5.2.8.  Direct Channel Select  ................................ ................................ ...........................  58 
5.2.9.  DTV Initialize  ................................ ................................ ................................ ....... 60 
5.2.10.  Shutdown  ................................ ................................ ................................ ...........  63 
5.2.11.  Watch Dog  ................................ ................................ ................................ ..........  65


--- Page 24 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 24/318 5.2.12.  Display EPG  ................................ ................................ ................................ ...... 67 
5.2.13.  Update Preset Table  ................................ ................................ .........................  71 
5.2.14.  Display Banner  ................................ ................................ ................................ . 73 
5.2.15.  Service ID Channel Select  ................................ ................................ ................  75 
5.2.16.  Start Background Search  ................................ ................................ .................  77 
5.2.17.  Start Background Scan ................................ ................................ .....................  79 
5.2.18.  DTV Restart  ................................ ................................ ................................ ...... 81 
5.3. HOST⇒B/E Set Command  ................................ ................................ .........................  83 
5.3.1.  Set auto tune Mode  ................................ ................................ ...............................  83 
5.3.2.  Set Closed Caption Mode  ................................ ................................ .....................  85 
5.3.3.  Set Auto Broadcast Search Mode  ................................ ................................ ........  87 
5.3.4.  Set Audio Mode  ................................ ................................ ................................ ..... 89 
5.3.5.  Set Residential Area  ................................ ................................ .............................  91 
5.3.6.  Set Auto Event Relay  ................................ ................................ ...........................  95 
5.3.7.  Set Baud rate  ................................ ................................ ................................ ........  97 
5.3.8.  Set DTV System  ................................ ................................ ................................ .... 99 
5.3.9.  Set DTV Parameter  ................................ ................................ ............................  102 
5.3.10.  Set Low Power Mode ................................ ................................ .......................  106 
5.3.11.  BML Forced Exit  ................................ ................................ .............................  108 
5.3.12.  Set DTV Mode  ................................ ................................ ................................ .. 110 
5.3.13.  Set Video Resolution  ................................ ................................ ........................  112 
5.3.14.  Set Banner Config  ................................ ................................ ............................  114 
5.3.15.  Set Character Set  ................................ ................................ .............................  118 
5.3.16.  Set DTV Parameter 2  ................................ ................................ .....................  120 
5.3.17.  Set User ID  ................................ ................................ ................................ ...... 125 
5.3.18.  Set EPG Config  ................................ ................................ ...............................  127 
5.3.19.  Set Video Color  ................................ ................................ ................................  133 
5.3.20.  Set Event Mask  ................................ ................................ ...............................  135 
5.4. HOST⇒B/E Get Command  ................................ ................................ .......................  137 
5.4.1.  Get DTV Status  ................................ ................................ ................................ .. 137 
5.4.2.  Get TS Name  ................................ ................................ ................................ ....... 141 
5.4.3.  Get Configure  ................................ ................................ ................................ ...... 144 
5.4.4.  Get Version  ................................ ................................ ................................ ..........  147 
5.4.5.  Get Audio ES  ................................ ................................ ................................ ....... 149 
5.4.6.  Get Program Information ................................ ................................ ...................  151 
5.4.7.  Get Service Information  ................................ ................................ .....................  153 
5.4.8.  Get DTV Parameter ................................ ................................ ............................  156 
5.4.9.  Get Program Description  ................................ ................................ ...................  159 
5.4.10.  Get DTV System  ................................ ................................ .............................  161


--- Page 25 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 25/318 5.4.11.  Get Program List  ................................ ................................ ............................  163 
5.4.12.  Get Program Name  ................................ ................................ .........................  167 
5.4.13.  Get Logo Data  ................................ ................................ ................................ . 170 
5.4.14.  Get RMP Maker ID  ................................ ................................ .........................  174 
5.4.15.  Get Number of Program info  ................................ ................................ ..........  177 
5.4.16.  Get Audio ES info  ................................ ................................ ............................  180 
5.4.17.  Get Video Resolution  ................................ ................................ ......................  183 
5.4.18.  Get Banner Config  ................................ ................................ ..........................  185 
5.4.19.  Get Character Set  ................................ ................................ ...........................  187 
5.4.20.  Get TS Name with UTF -8 ................................ ................................ ..............  189 
5.4.21.  Get Program Information with UTF -8 ................................ ..........................  192 
5.4.22.  Get DTV Parameter 2  ................................ ................................ .....................  195 
5.4.23.  Get Service Information with UTF -8................................ .............................  199 
5.4.24.  Get Program Description with UTF -8 ................................ ...........................  203 
5.4.25.  Get Program Name with UTF -8 ................................ ................................ .... 206 
5.4.26.  Get Audio ES info with UTF -8 ................................ ................................ ....... 210 
5.4.27.  Get User ID  ................................ ................................ ................................ ..... 213 
5.4.28.  Get EPG Config  ................................ ................................ ...............................  215 
5.4.29.  Get Video Color  ................................ ................................ ...............................  218 
5.4.30.  Get Event Mask  ................................ ................................ ..............................  220 
5.4.31.  Get Part Number  ................................ ................................ ............................  222 
5.4.32.  Get Program Name by 3Digit Number  ................................ ..........................  224 
5.4.33.  Get Program Name with UTF -8 by 3Digit Number  ................................ ..... 226 
5.4.34.  Get Logo Data by 3Digit Number  ................................ ................................ .. 229 
5.5. HOST⇒B/E Event  ................................ ................................ ................................ ..... 232 
5.5.1.  Key Event  ................................ ................................ ................................ ............  232 
5.6. B/E⇒HOST Command  ................................ ................................ ..............................  234 
5.6.1.  Wakeup  ................................ ................................ ................................ ................  234 
5.6.2.  Boot Mode  ................................ ................................ ................................ ............  237 
5.7. B/E⇒HOST Event  ................................ ................................ ................................ ..... 239 
5.7.1.  DTV Status  ................................ ................................ ................................ ..........  239 
5.7.2.  Scan Status  ................................ ................................ ................................ .........  243 
5.7.3.  Search Status  ................................ ................................ ................................ ...... 244 
5.7.4.  DTV Event  ................................ ................................ ................................ ...........  246 
5.7.5.  EWS Event  ................................ ................................ ................................ ..........  250 
5.7.6.  Program Information  ................................ ................................ ..........................  251 
5.7.7.  EPG Status  ................................ ................................ ................................ ..........  253 
5.7.8.  Event relay  ................................ ................................ ................................ ..........  254 
5.7.9.  Number of Program info  ................................ ................................ ....................  255


--- Page 26 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 26/318 5.7.10.  Program Information with UTF -8 ................................ ................................ . 257 
5.7.11.  TS Name Update  ................................ ................................ .............................  260 
5.7.12.  TS Name Update with UTF -8 ................................ ................................ ........  261 
5.7.13.  Logo Update  ................................ ................................ ................................ .... 262 
5.7.14.  EPG Button Status  ................................ ................................ .........................  263 
5.7.15.  BML Status  ................................ ................................ ................................ ..... 264 
5.7.16.  C/N Information  ................................ ................................ ..............................  265 
5.7.17.  EPG Scan Result  ................................ ................................ .............................  266 
5.7.18.  DTV Critical Error  ................................ ................................ ..........................  268 
5.8. SW Update Command  ................................ ................................ ...............................  270 
5.8.1.  SW Update  ................................ ................................ ................................ ..........  270 
5.8.2.  SW Update Status  ................................ ................................ ..............................  275 
5.8.3.  Background SW Update  Start  ................................ ................................ ...........  276 
5.8.4.  Background SW Update  Cancel  ................................ ................................ ........  278 
5.8.5.  Background SW Update  ................................ ................................ .....................  280 
5.8.6.  Background SW Update Status  ................................ ................................ .........  281 
5.9. Test & Debug Command  ................................ ................................ ............................  283 
5.9.1.  Test Mode  ................................ ................................ ................................ ............  283 
5.9.2.  Set Debug Parameter  ................................ ................................ .........................  287 
5.9.3.  Monitor Status  ................................ ................................ ................................ .... 289 
5.9.4.  HW Test  ................................ ................................ ................................ ...............  292 
5.9.5.  2nd TS Test  ................................ ................................ ................................ .........  294 
5.9.6.  2nd TS Test Status  ................................ ................................ .............................  296 
6. DTV Information  ................................ ................................ ................................ ...............  298 
6.1. Channel List  ................................ ................................ ................................ ...............  298 
6.2. Last Channel  ................................ ................................ ................................ ..............  298 
6.3. DTV Configuration  ................................ ................................ ................................ .... 298 
6.4. DTV System ................................ ................................ ................................ ................  299 
6.5. TRMP Information  ................................ ................................ ................................ ..... 299 
6.6. Logo  ................................ ................................ ................................ .............................  299 
6.7. BML Information  ................................ ................................ ................................ ....... 299 
6.8. DTV Parameter2  ................................ ................................ ................................ ........  299 
7. Background SW Update Sequence (Examples)  ................................ ..............................  300 
7.1. Update Success  ................................ ................................ ................................ ..........  300 
7.2. Update Failed – CRC Error  ................................ ................................ ......................  301 
7.3. Update Failed – Invalid Fragment  ................................ ................................ ...........  302 
8. DTV parameter and DTV parameter 2 data range  ................................ ........................  303 
8.1. DTV Parameter data range  ................................ ................................ .......................  303 
8.2. DTV Parameter 2 data range for Thrush ................................ ................................ . 305


--- Page 27 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 27/318 8.3. DTV Parameter 2 data range for New Frontier  ................................ .......................  311


--- Page 28 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 28/318 1. Introduction  
This document is described the communication specification of HOST CPU and B/E.  
 
2. UART Communication Specification  
2.1. Communication Configuration  
 
Baud rate  921600bits  ※1 
Start Bit  1 
Stop Bit  1 
Parity  None  
H/W Flow Control  None  
Baud rate : Default Baud rate is Below  
● TRS231BSxxxx : 9 21600bits  
● TRH231BSxxxx : 9 21600bits  
● FRO232BSyyzz : 19200bits


--- Page 29 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 29/318 2.2. Communication Format  
Header Type 1  
Header Part  Data Part  
Start Flag  Type  Request No  Data Length  Header CRC8  Data  Data CRC8  
 
← 16bit →  
A5 5A   
←  8bit  →  
  
←  8bit  →  
  
←8bit→  
  
← 8bit → 
  
← Xbyte 
→ 
  
← 8bit → 
 
  
 Header Type 2  (Using for TRS231BSxxxx and TRH231BSxxxx)  
Header Part  Data Part  
Start Flag  Type  Request No  Data Length  Header CRC8  Data  Data CRC8  
 
← 16bit → 
A5 59   
←  8bit  → 
  
←  8bit  → 
  
←16bit→ 
  
← 8bit → 
  
← Xbyte 
→ 
  
← 8bit → 
 
 
Start Sync :  A5h,5Ah  : Data Length Field is 8 bit  
A5h,59h : Data Length Field is 16bit  
Type :  Type  
00h : Command(Need Ack)  
01h : Command(No Need Ack)  
80h : ACK  
90h : NAK(Header CRC Error)  
91h : NAK(Data CRC Error)  
Request No. :  Sequential Number  
00h ~ FFh  
Data Length :  Length includes  the following fields.  
Unit : Model dependent  
- Data  
- Data CRC  
In case of ACK/NAK, this field is always 0.  
Header CRC8 :  CRC include the following fields.  
- Start Flag  
- Type  
- Request No  
- Data Length  
8bit CRC Value(Refer to the following Note)  
Data :  Refer to each command.  
Data CRC8 :  CRC include following field.  
- Data  
8bit CRC Value(Refer to the following Note)  
Note: CRC8: g(x) =x8+x5+x4+1  
Request No. :  
● Response from B/E shall use the same request No. from Host so that Host 
can distinguish the correct response.  
● Response from HOST can be incremental request number which is different 
than Request from Module.  
● For Events, B/E uses an incrementing Request No.  
Header Type . 
● Host should always use Header Type 1 for sending commands, 
responses, ACKs.


--- Page 30 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 30/318 2.3. Communication Sequence  
2.3.1.  Host ⇒ B/E Sequence [Command(Need ACK) – ACK]  
 
 
 
 
 
 
 
 
 
 If HOST CPU need ACK for Command, HOST CPU should transmit Command (Need 
ACK).  
 If B/E receive Command (Need ACK), B/E should transmit ACK as the same Request 
No of command.  
 If HOST CPU receive ACK as the same Request No for command, it means that the 
command communication is completed.  
 If HOST CPU receive  ACK as the different Request No for command, the ACK should 
be discarded.  
 HOST CPU shouldn’t transmit the next command until receiving the ACK of the same 
Request No (except retry out).  
 
 
 
 
 
 
 
 
 
 
 
 
 
 If HOST CPU receive the command ([B]) from B/E before receiving the ACK ([A]) for 
the command ([A]), HOST CPU should process the command ([B]) from B/E.  
 
  ACK  Command(Need ACK)  HOST CPU  B/E 
CRC  Check  is 
success  
ACK[A]  Command[A]  HOST CPU  B/E 
CRC Check [A] 
is success  Command[B]  
CRC Check [B] 
is success  
ACK[B]


--- Page 31 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 31/318 2.3.2.  Host ⇒ B/E Sequence [Command(Need ACK) – NAK]  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If Command (Need ACK) is failed, B/E should return NAK.  
 If HOST CPU receive NAK as the same Request No for command, HOST CPU retry 
to transmit the same command.  
 Max of retry count is 3.  
 1st command and retry command should be same Request No.  
 If HOST CPU receive  NAK as the different Request No for command, the NAK should 
be discarded.  
 
  Command(Need ACK)  HOST CPU  B/E 
NAK  Command(Need ACK) Retry 2  
NAK  Command(Need ACK) Retry 1  NAK  
NAK  
Command(Need ACK) Retry 3  CRC Check  
 is failed  CRC Check  
 is failed  
CRC Check  
 is failed  CRC Check  
 is failed


--- Page 32 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 32/318 2.3.3.  Host ⇒ B/E Sequence [Command(Need ACK) – Timeout]  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If HOST CPU transmit Command (Need ACK), HOST CPU should start timer.  
 If HOST CPU don’t receive ACK as the same Request No for command within T1 
sec, HOST CPU retry to transmit the same command. (Refer to “ 2.5.Timeout Value ”) 
 Max of retry count is 3.  
 1st command and retry command should be same Request No.  
  Command(Need ACK) Retry 2  Command(Need ACK) Retry 1  Command(Need ACK)  HOST CPU  B/E 
T1 Timeout  
T1 Timeout  ACK  
ACK  
Command(Need ACK) Retry 3  T1 Timeout  
ACK


--- Page 33 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 33/318 2.3.4.  Host ⇒ B/E Sequence [Command(No Need ACK)]  
 
 
 
 
 
 
 
 
 
 If HOST CPU doesn’t need ACK for Command, HOST CPU should transmit 
Command (No Need ACK).  
 If B/E receive Command (No Need ACK), B/E shouldn’t transmit ACK as the same 
Request No of command.  
  Command(No Need ACK)  HOST CPU  B/E 
CRC Check  
 is success


--- Page 34 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 34/318 2.3.5.  B/E ⇒ Host Sequence [Command(Need ACK) – ACK]  
 
 
 
 
 
 
 
 
 If B/E need ACK for Command, B/E should transmit Command (Need ACK).  
 If HOST CPU receive Command (Need ACK), HOST CPU should transmit ACK as 
the same Request No of command.  
 If B/E receive ACK as the same Request No for command, it means that the 
command communication is completed.  
 If B/E receive  ACK as the different Request No for command, the ACK should be 
discarded.  
 B/E shouldn’t transmit the next command until receiving the ACK of the same 
Request No (except retry out).  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If B/E receive the command ([A]) from HOST CPU before receiving the ACK ([B]) for 
the command ([B]), B/E should process the command ([A]) from HOST CPU , after 
receiving the ACK ([B]) for the command ([B]) . 
 
  ACK  Command(Need ACK)  HOST CPU  B/E 
CRC Check  is success  
ACK[A]  Command[A]  HOST CPU  B/E 
CRC Check [A] 
is success  Command[B]  
CRC Check [B] 
is success  
ACK[B]


--- Page 35 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 35/318 2.3.6.  B/E ⇒ Host Sequence [Command(Need ACK) – NAK]  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If Command (Need ACK) is failed, HOST CPU should ignore the data and return NAK.  
 If B/E receive NAK as the same Request No for command, B/E retry to transmit the 
same command.  
 Max of retry count is 3.  
 1st command and retry command should be same Request No.  
 If B/E receive  NAK as the different Request No for command, the NAK should be 
discarded.  
 
     
  Command(Need ACK) Retry 2  NAK  
NAK  Command(Need ACK) Retry 1  NAK  Command(Need ACK)  HOST CPU  B/E 
CRC Check  is failed  
CRC Check is failed  CRC Check is failed  
Command(Need ACK) Retry 3  
NAK  CRC Check is failed


--- Page 36 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 36/318 2.3.7.  B/E ⇒ Host Sequence [Command(Need ACK) – Timeout]  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If B/E transmit Command (Need ACK), B/E should start timer.  
 If B/E don’t receive ACK as the same Request No for command within T1 sec, B/E 
retry to transmit the same command. (Refer to “ 2.5.Timeout Value ”) 
 Max of retry count is 3.  
 1st command and retry command should be same Request No.  
 HOST CPU  should execute only once with same Request No.  
  Command(Need ACK) Retry 2  ACK  
ACK  Command(Need ACK) Retry 1  Command(Need ACK)  HOST CPU  B/E 
Command(Need ACK) Retry 3  
ACK  T1 Timer  
T1 Timer  
T1 Timer


--- Page 37 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 37/318 2.3.8.  B/E ⇒ Host Sequence [Command(No Need ACK)]  
 
 
 
 
 
 
 
 
 If B/E doesn’t need ACK for Command, B/E should transmit Command (No Need 
ACK).  
 If HOST CPU receive Command (No Need ACK), HOST CPU shouldn’t transmit ACK 
as the same Request No of command.  
 If CRC check is failed Host should ignore the data completely.  
 
 
 
 
 
 
 
 
 
  Command(No Need ACK)  HOST CPU  B/E 
CRC Check is success


--- Page 38 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 38/318 2.4. Communication Specification  
 The UART communication support full duplex.  
 
 
2.5. Timeout Value  
Item Value  Comment  
T1 1sec  Command Retry Timer  
 
  
Command/ACK/NAK  
 Command/ACK/NAK  
Command/ACK/NAK  
HOST  
RX 
TX 
B/E 
RX 
TX


--- Page 39 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 39/318  
3. Error Code  
Error Code  Description  
01h Invalid Parameter  
02h Invalid Data  
03h Invalid Length  
04h No Service  
05h Not Support  
06h Can’t receive this channel, because weak signal.  
07h Can’t receive this channel.  
08h This channel is not being broadcast.  
09h TRMP Information is invalid  
0Ah Invalid Status  
0Bh RMP Error EC21  
0Ch RMP Error EC22  
0Dh RMP Error EC23  
20h Tuner Error(I2C)  
FFh Unknown Error  
  RMP Error EC21 ： 
● Error details:  
This error is displayed when a work key for a transmitted ECM does not exist (when an 
EMM with a valid work key has not yet been received and when the time taken after 
selecting a station is less than twice the maximum value of an EMM resending cycle).  
● Error message example:  
The reception control data is not set. Please wait for a moment. (It may take a 
maximum of 30 seconds.)  
● Code: EC21  
● Others:  
This error can be displayed as the error message above. It is also effective to display 
the error such that viewers can easily understand the current status using the progress 
bar, remaining time display, etc.  
 
 RMP Error EC22 ： 
● Error details:  
This error is displayed when a work key for a transmitted ECM does not exist (when an 
EMM with a valid work key has not yet been received and when the time taken after 
selecting a station exceeds twice the maximum value of an EMM resending cycle).  
● Error message example:  
This channel cannot be viewed. Please contact the customer center of the channel.  
● Code: EC22  
 
 RMP Error EC23 ： 
● Error details:  
This error occurs when an access control descriptor included in the PMT is not 
consistent with CA_system_id as specified in Part 2 of this volume. (See 5.4 in Part 2 
of this volume.)  
● Error message example:  
This program cannot be viewed with this receiver. Please contact the customer center 
of the channel.  
● Code: EC23


--- Page 40 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 40/318 4. DTV Status  
DTV Status  Description  
01h Booting(Power OFF→ON) (Not support)  
02h Shutdown(Power ON→OFF)  
03h In Service  
04h Low Power  
05h DTV OFF  
06h DTV OFF with EPG SCAN  
 
5. Data Detail  
5.1. Command List  
5.1.1.  HOST⇒B/E Command  
Code  
(Data0/1)  Command   DTV  
0001h  Channel Scan   X  
0002h  Channel Set   X  
0003h  Channel Up/Down   X  
0004h  Physical Channel Set   X  
0005h  Search Up/Down   X  
0006h  Broadcast Search   X  
   X  
   X  
0009h  ES Switch   X  
000Ah  Direct Channel Select   X  
0101h  DTV Initialize   X  
   X  
   X  
0104h  Get DTV Status   X  
0105h  Shutdown   X  
0106h  Watch Dog   X  
0107h  Get TS Name   X  
0108h  Set auto tune Mode   X  
     
010Ah  Set Closed Caption Mode   X  
010Bh  Set Auto BC  Search Mode   X  
010Ch  Get Configure   X  
010Dh  Set Audio mode   X  
     
     
0110h  Set Residential Area   X  
0111h  Set Auto Event Relay   X  
0112h  Display EPG   X  
0113h  Get Version   X  
0114h  Get Audio ES   X  
0117h  Update Preset Table   X  
0118h  Get Program Information   X  
0119h  Set Baud rate   X  
     
     
011Ch  Get Service Information   X  
011Dh  Set DTV Parameter   X  
011Eh  Get DTV Parameter   X  
011Fh  Display Banner   X


--- Page 41 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 41/318 0120h  Set DTV System   X  
0121h  Service ID Channel Select   X  
0122h  Get Program Description   X  
0123h  Get DTV System   X  
0124h  Get Program List   X  
0125h  Get Program Name   X  
0126h  Get Logo Data   X  
0127h  Set Low Power Mode   X  
0128h  BML Forced Exit   X  
0129h  Get RMP Maker ID   X  
012Ah  Get Number of Program  info  X  
012Bh  Get Audio ES info   X  
012Ch  Set DTV Mode   X  
012Dh  Set Video Resolution   X  
012Eh  Get Video Resolution   X  
012Fh  Set Banner Config   X  
0130h  Get Banner Config   X  
0131h  Set Character Set   X  
0132h  Get Character Set   X  
0133h  Get TS Name with UTF -8  X  
0134h  Get Program Information with UTF -
8  X  
0135h Set DTV Parameter  2  X  
0136h Get DTV Parameter  2  X  
0137h  Get Service Information with UTF -
8  X  
0138h  Get Program Description with UTF -
8  X  
0139h  Get Program Name with UTF -8  X  
013Ah  Get Audio ES info with UTF -8  X  
013Bh  Set User ID   X  
013Ch  Get User ID   X  
013Dh  Set EPG Config   X  
013Eh  Get EPG Config   X  
013Fh  Set Video Color   X  
0140h  Get Video Color   X  
0141h  Set Event Mask   X  
0142h  Get Event  Mask   X  
0143h  Get Part Number   X  
0144h  Get Program Name by 3Digit 
Number   X  
0145h  Get Program Name with UTF -8 by 
3Digit Number   X  
0146h  Get Logo Data by 3Digit Number   X  
0147h  Start Background Search   X  
0148h  Start Background Scan   X  
01F0h  DTV Res tart  X  
 
5.1.2.  HOST⇒B/E Event  
Code  
(Data0/1)  Command   DTV  
0201h  Key Event   X


--- Page 42 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 42/318 5.1.3.  B/E⇒HOST Command  
Code  
(Data0/1)  Command   DTV  
8001h  Wakeup   X  
8003h  Boot Mode   X  
 
5.1.4.  B/E⇒HOST Event  
Code  
(Data0/1)  Command   DTV  
8201h  DTV Status   X  
8203h  Scan Status   X  
8204h  Search Status   X  
     
8206h  DTV Event   X  
     
8208h  EWS Event   X  
8209h  Program Information   X  
820Ah  EPG Status   X  
820Bh  Event relay   X  
820Ch  Number of Program info   X  
820Dh  Program Information with UTF -8  X  
820Eh  TS Name Update   X  
820Fh  TS N ame Update with UTF -8  X  
8210h  Logo Update   X  
8211h  EPG Button Status   X  
8212h  BML Status   X  
8213h  C/N Information   X  
8214h  Manual EPG Scan Result   X  
8301h  DTV Critical Error   X  
 
5.1.5.  SW Update Command  
Code  
(Data0/1)  Command   DTV  
A001h  SW Update   X  
A002h  SW Update Status   X  
A101 h Background SW Update Start   X  
A102h  Background SW Update Cancel   X  
A103h  Background SW Update   X  
A104h  Background SW Update Status   X  
 
5.1.6.  HOST⇒BE Test  & Debug Command  
Can use these commands for testing purposes only.  
Code  
(Data0/1)  Command   DTV  
     
     
     
     
F005h  Test Mode   X  
F006h  Set Debug Parameter   X  
     
F008h  Hardware Test   X


--- Page 43 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 43/318 F009h  2nd TS Test   X  
     
 
5.1.7.  B/E⇒HOST Test  & Debug Command  
Code  
(Data0/1)  Command   DTV  
F007h  Monitor Status   X  
F00Ah  2nd TS Test Status   X


--- Page 44 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 44/318 5.2. HOST⇒B/E Command  
5.2.1.  Channel Scan  
(1) Channel Scan  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h or 05h  
Header CRC8 :  -- 
Data 0 :  00h Channel Scan(Upper)  
Data 1 :  01h Channel Scan(Lower)  
Data 2 :  Operation  
00h : Start  
10h : Start with Update  Home Preset  
11h : Start with Update Drive Preset  
FFh : Stop  
Data 3 :  Update Operation ( optional ) 
  00h : Update without Tune top channel  
  01h : Update with Tune top channel  
Data CRC8 :  -- 
 
(2) Channel Scan Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Channel Scan(Upper)  
Data 1 :  01h Channel Scan(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 If Operation is 00h, B/E start Channel Scan.  
 If Operation is FFh, B/E stop Channel Scan.  
 When finishing and stopping Channel Scan, B/E doesn’t update automatically , if 
Data2 is 00h . For updating the preset table, HOST have to send “ 5.2.13 .Update 
Preset Table ”. 
Operation in Data 2 with Update Home /Drive  Preset  case , no need "5.2.13. Update 
Preset Table".  
 If you start channel scan during back search or back scan in Dynamic 4Diver System, 
back search or back scan will be canceled immediately.  
 When BE received the scan command, response is sent to Host immediately after 
starting the scan.


--- Page 45 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 45/318  Data 3 : Optional Function  
 
Data  2 Data 3  Operation  
10h or 11h None / 00h Update without Tune top channel (Idle status)  
10h or 11h 01h Update with Tune top channel  
Other than the above  Scan wit hout update  
*If optional data(Data3)is there, it will be invalid 
error.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Channel Scan Command]  
Command(Need ACK)[Channel Scan Response]  
ACK  Processing


--- Page 46 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 46/318 5.2.2.  Channel Set  
(1) Channel Set  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Channel Set(Upper)  
Data 1 :  02h Channel Set(Lower)  
Data 2 :  Preset Number  
00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data 3 :  Preset Channel Number  
01h ~ 0Ch  
Data CRC8 :  -- 
 
(2) Channel Set Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Channel Set(Upper)  
Data 1 :  02h Channel Set(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start tuning Preset Channel Number.  
 Start playback of the first service.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Preset Number is not 00h or 01h or FFh.  
- Preset Channel Number is not 01h~0Ch.  
03h(Invalid Length)  Data Length is invalid.


--- Page 47 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 47/318 04h(No Service)  Desired Service is not found in Preset Table.  
Eg: Auto Tune Mode is Oneseg and the set channel 
doesn’t have an Oneseg service  
FFh( Unknown Error)  Unknown error  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Channel Set Command]  
Command(Need ACK)[Channel Set Response]  
ACK  Processing


--- Page 48 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 48/318 5.2.3.  Channel Up/Down  
(1) Channel Up/Down  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Channel Up/Down(Upper)  
Data 1 :  03h Channel Up/Down(Lower)  
Data 2 :  Preset Number  
FFh : Last Preset  
Data 3 :  Direction  
00h : Up  
01h : Down  
10h : Up (First Service Select)  
11h : Down (First Service Select)  
20h : Up without Channel Change  
21h : Down without Channel Change  
Data CRC8 :  -- 
 
(2) Channel Up/Down Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Channel Up/Down(Upper)  
Data 1 :  03h Channel Up/Down(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start tuning by Up/Down in Preset Table.  
 If different service is there, switch service.  
 Suspend service is skipped.  
 Data 3 : 20h/21h Same  program is skipped.  
e.g., 011->up->012 ->up->013 ->up->011.  
 Select the last channel in the idle state.  
 If there is no last channel, result error and do not select  channel .


--- Page 49 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 49/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Preset Number is not FFh.  
- Direction is o ther than the defined value . 
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Preset table is empty.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Channel Up/Down Command]  
Command(Need ACK)[Channel Up/Down Response]  
ACK  Processing


--- Page 50 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 50/318 5.2.4.  Physical Channel Set  
(1) Physical Channel Set  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Physical Channel Set(Upper)  
Data 1 :  04h Physical Channel Set(Lower)  
Data 2 :  Preset Number  
FFh : Last Preset  
Data 3 :  Physical Channel Number  
0Dh ~ 34h  
Data CRC8 :  -- 
 
(2) Physical Channel Set Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Physical Channel Set(Upper)  
Data 1 :  04h Physical Channel Set(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start tuning by Physical Channel Number.  
 If the tuning is successfully completed, the process of the physical channel set 
command has ended normally, so the search stop command is not necessary.  
 If the tuning is not completed ( e.g., when there is no signal input), the channel 
selecting operation is continued . Host is free to issue other commands like scan 
or tune.


--- Page 51 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 51/318  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Preset Number is not FFh.  
- Physical Channel Number is not 0Dh~34h  
03h(Invalid Length)  Data Length is invalid.   
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Physical Channel Set Command]  
Command(Need ACK)[Physical Channel Set Response]  
ACK  Processing


--- Page 52 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 52/318 5.2.5.  Search  Up/Down  
(1) Search  Up/Down  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Search Up/Down(Upper)  
Data 1 :  05h Search Up/Down(Lower)  
Data 2 :  Preset Number  
FFh : Last Preset  
Data 3 :  Operation  
00h : Start to search up  
01h : Start to search down  
FFh : Stop to search  
Data CRC8 :  -- 
 
(2) Search  Up/Down Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Search Up/Down(Upper)  
Data 1 :  05h Search Up/Down(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E starts to search.  
 If Operation is 00h, B/E start to search up.  
 If Operation is 01h, B/E start to search down.  
 After starting search up/down, “Search Status” starts to notify.  
 If Operation is FFh, B/E stop to search.  
 After finishing or stopping search, “Search Status” stops to notify.  
 When stopping search, B/E tune the last channel. But if B/E doesn’t have valid last 
channel, B/E become idle status.  
 Start next physical channel, and increment (decrement) physical channel number.  
 If channel detected, start playback of the first service.  
 If any channel is not detected, tune the last channel.  
 This will abort background search if it was running.


--- Page 53 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 53/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Preset Number is not FFh.  
- Operation is not 00h or 01h or FFh.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Search Up/Down Command]  
Command(Need ACK)[Search Up/Down Response]  
ACK  Processing


--- Page 54 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 54/318 5.2.6.  Broadcast Search  
(1) Broadcast Search  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  00h Broadcast Search(Upper)  
Data 1 :  06h Broadcast Search (Lower)  
Data 2:  Search Mode  
01h : Relay Search Start  
02h : Affiliated Search Start  
03h : Relay + Affiliated Search Start  
FFh : Search Stop  
Data CRC8 :  -- 
 
(2) Broadcast Search Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Broadcast Search(Upper)  
Data 1 :  06h Broadcast Search (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E starts to search with foreground.  
 If Search mode is 01h, B/E start relay station search.  
 If Search mode is 02h, B/E start affiliated station search.  
 If Search mode is 03h, B/E start relay and affiliated station search.  
 After starting Broadcast search, “Search Status” starts to notify.  
 If search mode is FFh, B/E stop relay/affiliated station search. Then B/E return last 
channel.  
 After finishing or stopping Broadcast search, “Search Status” stops to notify.  
 This will abort background search if it was running.


--- Page 55 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 55/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Search Mode is not 01h or 02h or 03h or FFh.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Broadcast Search Command]  
Command(Need ACK)[Broadcast Search Response]  
ACK  Processing


--- Page 56 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 56/318 5.2.7.  ES Switch  
(1) ES Switch Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h ES Switch(Upper)  
Data 1 :  09h ES Switch(Lower)  
Data 2 :  ES Switch Type  
01h : Video ES Switch(Not support)  
02h : Audio ES Switch  
Data 3 :  Component Tag  
Data CRC8 :  -- 
 
(2) ES Switch Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h ES Switch(Upper)  
Data 1 :  09h ES Switch(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Switch Audio ES.  
 Not support to switching Video ES.  
 Component Tag of Audio ES should be set Component Tag of “ 5.4.5 .Get Audio ES ”. 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- ES Switch Type is not 01h or 02h. 
03h(Invalid Length)  Data Length is invalid.  
05h(Not Support)  The parameter is not supported.


--- Page 57 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 57/318 - ES Switch Type is 01h.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ES Switch Command]  
Command(Need ACK)[ES Switch Response]  
ACK  Processing


--- Page 58 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 58/318 5.2.8.  Direct Channel Select  
(1) Direct Channel  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
07h (Optional)  
Header CRC8 :  -- 
Data 0 :  00h Direct Service(Upper)  
Data 1 :  0Ah Direct Service(Lower)  
Data 2 :  Three Digit Number(Upper) Refer to “(3) Description”  
Data 3 :  Three Digit Number(Lower) Refer to “(3) Description”  
Data 4 :  Branch Identifier Number(0~9)  
Data 5 :  Preset number  (Optional)  
00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data CRC8 :  -- 
 
(2) Direct Channel  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  00h Direct Service(Upper)  
Data 1 :  0Ah Direct Service(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start tuning by the three -digit number and the branch identifier number.  
 Branch Identifier for not -stored channel should be set to 00h.  
 If Data Length is 06h, B/E considers it as Last Preset.  
 Refer to the following about the formant of Three Digit Number.  
three -digit number  Data 2  Data 3  
011 00h 0Bh 
712 02h C8h


--- Page 59 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 59/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Three -digit number is not 000~199, 600~799.  
- Branch Identifier Number is not 00h ~ 09h.  
- Preset number is not 00h/01h/FFh.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  The specified service is not there in Preset table.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Direct Channel Select Command]  
Command(Need ACK)[Direct Channel Select Response]  
ACK  Processing


--- Page 60 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 60/318 5.2.9.  DTV Initialize  
(1) DTV Initialize Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h DTV Initialize(Upper)  
Data 1 :  01h DTV Initialize (Lower)  
Data 2 :   
Target Data  
00h : All Data Initialize  
01h : Configuration Data Initialize  
02h : Home Preset Initialize  
03h : Drive Preset Initialize  
 
8Xh : User Data Initialize (X=User ID)  
Data CRC8 :  -- 
 
(2) DTV Initialize Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h DTV Initialize(Upper)  
Data 1 :  01h DTV Initialize (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Initialize DTV (Channel List/DTV Config/TRMP Information/Logo/BML Information)  
 Refer to the followings about the initial values of DTV Setting. Initialization of each 
item is depend ing on “Data 2”  
Items  Initial Value  Data 2  
Audio Mode  00h : Main  00h or 01h  
Closed Caption Mode  00h : Off  00h or 01h  
Auto Tune Mode  ＊1 00h or 01h  
Auto Broadcast Search Mode  ＊2 00h or 01h  
Auto Event Relay  ＊3 00h or 01h  
Region ID(Home Preset)  FFh 00h or 02h  
Zip code(Home Preset)  All data are 00h  00h or 02h  
Region ID(Drive Preset)  FFh 00h or 03h  
Zip code(Drive Preset)  All data are 00h  00h or 03h  
EPG Scale  00h(Type 1 ) ＊4 00h or 01h  
＊1: The value is DTV Parameter 2  Auto tune mode default


--- Page 61 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 61/318 ＊2: The value is DTV Parameter 2  Default Auto Broadcast Search mode  
＊3: The value is DTV Parameter 2 Event relay Auto Event rely  On/Off  
＊4: If Type  1 is disabled, next available Type  will work.  
 B/E stop to playback and become the black screen during Initialize DTV (Preset Table, 
Last Channel, DTV Setting). If B/E has valid last channel after initialization, B/E tune 
the last channel.  
・ Initialize Data Table  
Content  Config  
BML Home  Drive  Logo  
RMP  Remark  LastCh  LastCh  Data2  
00h All User  All Initialize/Factory Reset  
01h Current 
User  － － － Current User Configuration 
Data Initialize  
02h － Current 
User  － － Current User Home Preset 
Initialize  
03h － － Current 
User  － Current User Drive Preset 
Initialize  
81h User 1  － User 1 All Initialize  
82h User 2  － User 2 All Initialize  
83h User 3  － User 3 All Initialize  
84h User 4  － User 4 All Initialize  
85h User 5  － User 5 All Initialize  
86h User 6  － User 6 All Initialize  
 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 22.5sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Target Data is not 00h ~ 03h.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 62 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 62/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[DTV Initialize Command]  
Command(Need ACK)[DTV Initialize Response]  
ACK  Processing


--- Page 63 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 63/318 5.2.10.  Shutdown  
(1) Shutdown Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h~04h  
Header CRC8 :  -- 
Data 0 :  01h Shutdown(Upper)  
Data 1 :  05h Shutdown(Lower)  
Data 2 :  Shutdown Mode(Option)  
00h : immediately shutdown  
01h : shutdown after storing data  
Data CRC8 :  -- 
 
(2) Shutdown Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Shutdown(Upper)  
Data 1 :  05h Shutdown(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Shutdown B/E  
 If Shutdown Mode is 00h, B/E stop to playback. Then B/E become to idle status.  
 If Shutdown Mode is 01h, B/E stop to playback. Then B/E store DTV Information to 
NVRAM and  become to idle status.  
 If Shutdown Mode is omitted, B/E behavior same as Shutdown Mode=00h.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command 
(Shutdown Mode=00h).  
 Doesn’t receive the response within 10sec after HOST transmit the command 
(Shutdown Mode=01h).  
 The result of response is NG.


--- Page 64 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 64/318  Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Shutdown Mode is not 00h ~ 01h.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 If Shutdown Mode=00h of Shutdown Command, Timeout of Shutdown Response is 
1sec . 
 If Shutdown Mode=01h of Shutdown Command, Timeout of Shutdown Response is 
10sec . 
 After shutdown B/E, issuing UART control command is prohibited, and any 
information output from the UART communication should be ignored  except  Get DTV 
Status command.  
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Shutdown Command]  
Command(Need ACK)[Shutdown Response]  
ACK  Stop to playback  
If Shutdown Mode=01h, 
store last channel to 
NVRAM


--- Page 65 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 65/318 5.2.11.  Watch Dog  
(1) Watch Dog Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh 
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Watch Dog(Upper)  
Data 1 :  06h Watch Dog(Lower)  
Data CRC8 :  -- 
 
(2) Watch Dog Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Watch Dog(Upper)  
Data 1 :  06h Watch Dog(Lower)  
Data 2 :  00h : Reserved  
Data 3 :  00h : Reserved  
Data CRC8 :  -- 
 
(3) Description  
 Watch Dog  
 During SW Update, HOST shouldn’t send this command.  
 
(4) Error Handling  
 Reset mod ule (Refer to sequence)


--- Page 66 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 66/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[Watch Dog Command]  
Command(No Need ACK)[Watch Dog Response]  
Watchdog  Command  Watchdog  Command  HOST CPU  B/E 
Timeout  
Timeout  Watchdog  Response  
～ Reset ～ Watchdog  Command  
Watchdog  Response  
Watchdog  Response


--- Page 67 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 67/318 5.2.12.  Display EPG  
(1) Display EPG  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h or 05h(option)  
Header CRC8 :  -- 
Data 0 :  01h Display EPG (Upper)  
Data 1 :  12h Display EPG (Lower)  
Data 2 :  Operation  
00h : Display EPG List(Current segment)  
01h : Display EPG Information  
02h : Up Arrow  
03h : Down Arrow  
04h : Left Arrow  
05h : Right Arrow  
06h : Back  
07h : Enter  
08h : Switch segment  
09h : Update  
0Ah : Previous Day(Blue Button)  
0Bh : Next Day(Red Button)  
0Ch : Multi service(Green Button)  
0Dh : Change Scale(Yellow Button)  
0Eh : Cancel update  
0Fh：Close All  
Data 3 :  Display EPG Type (Option)  
  Data2 = 00h :  
       00h : Last display type  
01h~04h : EPG Type 1~4  
  Data2 != 00h : Fix 00h  
Data CRC8 :  -- 
 
(2) Display EPG Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 14h  
Result=NG : 05h  
Data 0 :  01h Display EPG (Upper)  
Data 1 :  12h Display EPG (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Screen Status  
00h : No display  
01h : EPG List(Fullseg)  
02h : EPG Information(Fullseg)  
03h : EPG List(Oneseg)  
04h : EPG Information(Oneseg)  
Data 5 :  Display EPG List 0: invalid 1:valid  
Data 6 :  Display EPG Information 0: invalid 1:valid


--- Page 68 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 68/318 Data 7 :  Up Arrow 0: invalid 1:valid  
Data 8 :  Down Arrow 0: invalid 1:valid  
Data 9 :  Left Arrow 0: invalid 1:valid  
Data 10 :  Right Arrow 0: invalid 1:valid  
Data 11 :  Back 0: invalid 1:valid  
Data 12 :  Enter 0: invalid 1:valid  
Data 13 :  Switch segment 0: invalid 1:valid  
Data 14 :  Update 0: invalid 1:valid  
Data 15 :  Previous Day(Blue Button) 0: invalid 1:valid  
Data 16 :  Next Day(Red Button) 0: invalid 1:valid  
Data 17 :  Multi service(Green Button) 0: invalid 1:valid  
Data 18 :  Change Scale(Yellow Button) 0: invalid 1:valid  
Data CRC8 :  -- 
 
(3) Description  
 Display and control EPG.  
 Refer to the following table about each operation  
Screen  
Operation  No EPG  
① EPG List  
② EPG Information  
③ 
Display EPG List  ⇒② ② ⇒② 
Display EPG Information  ⇒③ ⇒③ ③ 
Up Arrow  -(*1) -(*2) -(*3) 
Down Arrow  -(*1) -(*2) -(*3) 
Left Arrow  -(*1) -(*2) -(*1) 
Right Arrow  -(*1) -(*2) -(*1) 
Back  -(*1) ⇒① ⇒① 
⇒② 
(*9) 
Enter  -(*1) ⇒③ -(*1) 
Switch segment  -(*1) -(*4) -(*1) 
Update  -(*1) -(*5) -(*1) 
Previous Day  -(*1) -(*6) -(*1) 
Next Day  -(*1) -(*6) -(*1) 
Multi service  -(*1) -(*7) -(*1) 
Change Scale  -(*1) -(*8) -(*1) 
Close All  -(*1) ⇒① ⇒① 
*1: This operation is ignored.  
*2: This operation moves  the focus.  
*3: This operation scrolls  the screen.  
*4: This operation switch Fullseg EPG List/Oneseg EPG List.  
*5: This operation update EPG List.  
*6: This operation moves  previous day or next day.  
*7: This operation switches  all service and the top service.  
*8: This operation changes  the scale (4Level).  
*9: If moving from EPG List, return to EPG List. If directly display EPG Information, 
close EPG Information.  
 If B/E receive “Cancel update” during updating, B/E display updated EPG Information.  
 During update, it is not possible to playback AV.


--- Page 69 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 69/318 (EPG Scan use foreground antennas.)  
 HOST can know screen status by Data4 of Response.  
 HOST can know valid button by Data5~18 of Response.  
 Notifies HOST about the real time button status via EPG Button Status event.  
 If changing scale (Data2=0Dh), B/E store the last scale to NVRAM. When displaying 
at next, EPG is displayed with last scale.  
 When receiving ack of “Display EPG Response”, B/E update the screen.  
 Change Scale:  It changes as follows each time a command is sent.  
Level1 -> Level2 -> Level3 -> Level4 -> Level1 ・・・  
・ Those Levels ( Types) disabled with Data 2 of Set EPG Config will be skipped 
from the change scale sequence.  
・ When Data Length = 04h and Data 2 = 00h : Display EPG List(Current segment), 
last type of EPG list display.  
・ When Data Length = 05h and Data 2 = 00h  : Display EPG List(Current segment), 
The EPG Type can be select directly by Data 3.  
・ EPG Scale ： 
- TRS231BSxxxx / TRH231BSxxxx  
EPG Scale  Number of Broadcast  Character Size  
Level1  4 Small  
Level2  5 Small  
Level3  4 Middle  
Level4  4 Large  
 
- FRO232B syyzz 
EPG Scale  Number of Broadcast  Character Size  
Level1  3 Small  
Level2  4 Small  
Level3  3 Middle  
Level4  3 Large  
 
 EPG update time per channel can be configured with DTV Parameter 2.  
 The close command cannot be used during updating.  
 When Update  start then background scan will abort . 
 During EPG display, automatic broadcast search does not work.  
 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.


--- Page 70 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 70/318  Regarding the condition that Result of the response is NG, refer the followings:  
Display EPG Response supports the following error codes.  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
-Data Length less than 2.  
- Operation is not 00h ~ 0Eh.  
03h(Invalid Length)  Data Length is invalid.  
0Ah(Invalid Status)  DTV cannot execute.  
Ex) Send when not show EPG.  
FFh( Unknown Error)  Unknown error  
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Display EPG Command]  
Command(Need ACK)[Display EPG Response]  
ACK  
Update Screen


--- Page 71 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 71/318 5.2.13.  Update Preset Table  
(1) Update Preset Table  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  01h Update Preset Table (Upper)  
Data 1 :  17h Update Preset Table (Lower)  
Data 2 :  Preset Number  
00h : Home Preset  
01h : Drive Preset  
Data 3 :  Operation  
00h : Update the result of channel scan  
01h : Entry current channel  
Data 4 :  Operation=00h  
00h : Cancel  
01h : Update  
Operation=01h  
01h~0Ch : One Touch Number  
Data CRC8 :  -- 
 
(2) Update Preset Table Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Update Preset Table (Upper)  
Data 1 :  17h Update Preset Table (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Update Preset Table.  
 If updating the result of channel scan, HOST should send Data3=00h & Data4=01h.  
 If cancel the result of channel scan, HOST should send Data3=00h & Data4=00h. 
B/E discard the result of channel scan.  
・ If entry current playback channel to specified one touch number, HOST should 
send Data3=01h & Data4=01h~0Ch.  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:


--- Page 72 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 72/318  Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  the parameter is invalid.  
- Data2 is not 00h or 01h.  
- Data3 is not 00h or 01h.  
- If Data3 is 00h, Data4 is not 00h or 01h.  
- If Data3 is 01h, Data4 is not 01h~0Ch.  
03h(Invalid Length)  Data Length is invalid.  
0Ah(Invalid Status)  - HOST send Data3=00h without channel scan.  
- HOST send Data3=01h~0Ch without tuning.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Update Preset Table Command]  
Command(Need ACK)[Update Preset Table Response]  
ACK  Processing


--- Page 73 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 73/318 5.2.14.  Display Banner  
(1) Display Banner  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 : 01h Display Banner(Upper)  
Data 1 :  1Fh Display Banner(Lower)  
Data 2 :  Operation  
00h : Display Banner  
01h : Hide Banner  
Data 3 :  Data2=00h(Display Banner)  
00h : No timeout (Continue to display until Hide Banner)  
01h~FFh : Display Time(Second)  
Data2=01h(Hide Banner)  
00h : Fixed Value  
Data CRC8 :  -- 
 
(2) Display Banner  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Display Banner(Upper)  
Data 1 :  1Fh Display Banner(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 This command controls  the display of banner.  
 If Data2=00h (Display Banner) & Data3=00h (No timeout), B/E continue to display 
the banner until receiving Hide Banner.  
 If Data2=00h (Display Banner) & Data3=01h~FFh, Data3 means the timeout value. 
B/E display during the time set by Data3.  
 If Auto Banner Display is enabled, B/E automatically display the banner without this 
command when the channel selecting.  
In this case, B/E automatically hide after Seconds . (X : DTV Parameter 2)  
 When receiving ack of “Display Banner Response”, B/E update the screen.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to


--- Page 74 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 74/318 handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 10 sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  the parameter is invalid.  
- Data2 is not 00h or 01h.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Display Banner Command]  
Command(Need ACK)[Display Banner Response]  
ACK  
Update Screen


--- Page 75 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 75/318 5.2.15.  Service ID Channel Select  
(1) Service ID Channel  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Service ID Channel Select(Upper)  
Data 1 :  21h Service ID Channel Select(Lower)  
Data 2 :  Service ID (Upper)  
Data 3 :  Service ID(Lower)  
Data CRC8 :  -- 
 
(2) Service ID Channel Select  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Service ID Channel Select(Upper)  
Data 1 :  21h Service ID Channel Select(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start tuning by Service ID.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  The specified service is not there in Preset table.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 76 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 76/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Service ID Channel Select Command]  
Command(Need ACK)[Service ID Channel Select Response]  
ACK  Processing


--- Page 77 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 77/318 5.2.16.  Start Background Search  
(1) Start Background Search  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Start Background Search (Upper)  
Data 1 :  47h Start Background Search  (Lower)  
Data 2:  Search Mode  
01h : Relay Search Start  
02h : Affiliated Search Start  
03h : Relay + Affiliated Search Start  
FFh : Search Stop  
Data CRC8 :  -- 
 
(2) Start Background Search Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Start Background Search (Upper)  
Data 1 :  47h Start Background Search  (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E starts to search with back ground.  
 If Search mode is 01h, B/E start relay station search.  
 If Search mode is 02h, B/E start affiliated station search.  
 If Search mode is 03h, B/E start relay and affiliated station search.  
 If search mode is FFh, B/E stop relay/affiliated station search.


--- Page 78 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 78/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Search Mode is not 01h or 02h or 03h or FFh.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)  
[Start Background  Search Command]  
Command(Need ACK)  
[Start Background  Search Response]  
ACK  Processing


--- Page 79 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 79/318 5.2.17.  Start Background Scan  
(1) Start Background Scan  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Start Background Scan (Upper)  
Data 1 :  48h Start Background Scan (Lower)  
Data 2 :  DTV Mode  
00h : Start Background Scan  
FFh : Stop Background Scan  
Data 3 :  Preset Number  
00h : Home  
01h : Drive  
02h : Home & Drive  
Data 4:  EPG Scan time per channel  
01h – FFh 
Data 5 :  Number of days  
1~8days  
Data CRC8 :  -- 
 
(2) Start Background Scan  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Start Background Scan (Upper)  
Data 1 :  48h Start Background Scan (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Scans the preset registered channels for EPG . 
- EPG Scan channel s: Registered channel s in Home and Drive Preset.  
(Excludes duplicate channels .) 
- EPG Scan time per Channel : Data 3 : 1[sec] ～ 255[sec]  
- Start Channel: Last Preset and last channel.  
 
 
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:


--- Page 80 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 80/318 Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Start Background Scan  Command]  
Command(Need ACK)[ Start Background Scan  Response]  
ACK


--- Page 81 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 81/318 5.2.18.  DTV Res tart 
(1) DTV Restart Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h DTV Re start (Upper)  
Data 1 :  F0h DTV  Restart (Lower)  
Data CRC8 :  -- 
 
(2) DTV Res tart Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h DTV Res tart (Upper)  
Data 1 :  F0h DTV  Restart (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 The h ost may use this command to restart the DTV application.  
 This command is valid only after the DTV Critical Error Event (Refer 5.7.18 DTV 
Critical Error ). 
 The BE follows the nor mal startup sequence for a re start with this command.  
 After this command and response , the host should be ready for receiving Wakeup 
Command from  the BE. 
 
(4) Error Handling  
・ If this command is sent without the DTV Critical Error event, BE responds with error 
code 0Ah(Invalid Status).


--- Page 82 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 82/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 ACK  HOST CPU  B/E 
Command(Need ACK)[ DTV Re start  Command]  
Command(Need ACK)[ DTV Res tart Response]  
ACK  
DTV Application 
Restarts


--- Page 83 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 83/318 5.3. HOST⇒B/E Set Command  
5.3.1.  Set auto tune  Mode  
(1) Set auto tune Mode Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set auto tune Mode (Upper)  
Data 1 :  08h Set auto tune Mode (Lower)  
Data 2 :  00h : Auto 
01h : Fullseg  
02h : Oneseg  
03h : Auto with Seamless  
Data CRC8 :  -- 
 
(2) Set auto tune Mode Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set auto tune Mode (Upper)  
Data 1 :  08h Set auto tune Mode (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set auto tune Mode.  
 This setting is saved by NVRAM.  
 It is possible to configure the default value using DTV Parameter 2.


--- Page 84 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 84/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Receiving Mode Command]  
Command(Need ACK)[Set Receiving Mode Response]  
ACK  Processing


--- Page 85 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 85/318 5.3.2.  Set Closed Caption Mode  
(1) Set Closed Caption  Mode  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Closed Caption Mode (Upper)  
Data 1 :  0Ah Set Closed Caption Mode (Lower)  
Data 2 :   
Value  Closed Caption  Superimpose  
00h OFF OFF 
01h ON - 1st ON - 1st 
02h ON - 2nd ON - 2nd 
03h OFF ON - 1st 
04h ON - 1st OFF 
05h ON - 2nd OFF 
 
Initial value : 00h  
Data CRC8 :  -- 
 
(2) Set Closed Caption Mode Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Closed Caption Mode (Upper)  
Data 1 :  0Ah Set Closed Caption Mode (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Closed Caption Mode.  
 This setting is saved by NVRAM.  
 Refer to the following table regarding to the specification of Closed Caption display.  
 
Closed Caption  Description  
OFF Don’t display Closed Caption  
1st If the program has 1st Closed Caption, B/E displays 1st Closed Caption.  
2nd If the program has 2nd Closed Caption, B/E displays 2nd Closed Caption.  
If the program has only 1st Closed Caption, B/E displays 1st Closed 
Caption.  
If the program doesn’t have  Closed Caption, B/E doesn’t display Closed 
Caption.  
 Refer to the following table regarding to the specification of Superimpose display.


--- Page 86 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 86/318 Superimpose  Description  
OFF Don’t display Superimpose.  
1st If the program has 1st Superimpose, B/E displays 1st Superimpose.  
2nd If the program has 2nd Superimpose, B/E displays 2nd Superimpose.  
If the program has only 1st Superimpose, B/E displays 1st Superimpose.  
If the program doesn’t has Superimpose, B/E doesn’t display 
Superimpose.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Closed Caption  Mode Command]  
Command(Need ACK)[Set Closed Caption  Mode Response]  
ACK  Processing


--- Page 87 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 87/318 5.3.3.  Set Auto Broadcast Search Mode  
(1) Set Auto B roadcast Search Mode  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Auto Broadcast Search Mode (Upper)  
Data 1 :  0Bh Set Auto Broadcast Search Mode (Lower)  
Data 2 :  00h : Automatic Broadcast Search Off  
01h : Automatic Relay Station Search On  
02h : Automatic Affiliated Station Search On  
03h : Automatic Relay & Affiliated Station Search On  
Data CRC8 :  -- 
 
(2) Set Auto B roadcast Search Mode Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Auto Broadcast Search Mode (Upper)  
Data 1 :  0Bh Set Auto Broadcast Search Mode (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Automatic Broadcast Search Mode.  
 If Diver Mode is Dynamic 4Diver Mode or Fixed 2x2 Diver Mode, Automatic Broadcast 
Search run via background. If Diver Mode is Fixed 2Diver Mode, Automatic Broadcast 
Search run via foreground (Refer to “ 5.3.8 .Set DTV System ”). 
 This setting is saved by NVRAM.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.


--- Page 88 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 88/318 03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Auto BCSearch Mode Command]  
Command(Need ACK)[Set Auto BCSearch Mode Response]  
ACK  Processing


--- Page 89 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 89/318 5.3.4.  Set Audio Mode  
(1) Set Audio Mode  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Audio Mode (Upper)  
Data 1 :  0Dh Set Audio Mode (Lower)  
Data 2 :  00h : Main  
01h : Sub  
02h : Main(Lch)+Sub(Rch)  
Data CRC8 :  -- 
 
(2) Set Audio Mode Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Audio Mode (Upper)  
Data 1 :  0Dh Set Audio Mode (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Audio Mode.  
 This setting is saved by NVRAM.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 90 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 90/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Audio Mode Command]  
Command(Need ACK)[Set Audio Mode Response]  
ACK  Processing


--- Page 91 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 91/318 5.3.5.  Set Residential Area  
(1) Set Residential Area  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  0Dh 
Header CRC8 :  -- 
Data 0 :  01h Set Residential Area(Upper)  
Data 1 :  10h Set Residential Area(Lower)  
Data 2 :  00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data 3 :  Target  
Bit0 : Set Region ID  
Bit1 : Set Zip -Code  
Bit2~Bit7 : Reserved  (Fix 0)  
Data 4 :  Region ID  
Data 5 :  Zip-Code[0] Ascii Code (In case of “1234567”, ‘1’)  
Data 6 :  Zip-Code[1] Ascii Code (In case of “1234567”, ‘2’)  
Data 7 :  Zip-Code[2] Ascii Code (In case of “1234567”, ‘3’)  
Data 8 :  Zip-Code[3] Ascii Code (In case of “1234567”, ‘4’)  
Data 9 :  Zip-Code[4] Ascii Code (In case of “1234567”, ‘5’)  
Data 10 :  Zip-Code[5] Ascii Code (In case of “1234567”, ‘6’)  
Data 11 :  Zip-Code[6] Ascii Code (In case of “1234567”, ‘7’)  
Data CRC8 :  -- 
 
(2) Set Residential Area Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Residential Area(Upper)  
Data 1 :  10h Set Residential Area(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  --


--- Page 92 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 92/318 (3) Description  
 Set Residential Area (Region ID and Zip code).  
 In case of setting only Region ID, set Data3=01h, Data4=Input Value, Data5~11=00h 
(B/E doesn’t care Data5~11).  
 If case of setting only Zip code, set Data3=02h, Data4=00h (B/E doesn’t care Data4), 
Data5~11=Input Value.  
 If case of Setting Region ID and Zip code, set Data3=03h, Data4=Input Value, 
Data5~11=Input Value.  
 This setting is saved by NVRAM.  
 BML browser will not use zip code anymore if 0000000 used.


--- Page 93 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 93/318  Refer the following about Region ID.  
ID Region  
(English)  Region  
(Japanese)  Wide 
area ID Region  
(English)  Region  
(Japanese)  Wide area  
1 Hokkaido  
(Sapporo)  北海道  
（札幌）  Hokkaido  28 Shizuoka  静岡 － 
2 Hokkaido  
(Hakodate)  北海道  
（函館）  Hokkaido  29 Aichi  愛知 Chukyo  
3 Hokkaido  
(Asahikawa)  北海道  
（旭川）  Hokkaido  30 Mie 三重 Chukyo  
4 Hokkaido  
(Obihiro)  北海道  
（帯広）  Hokkaido  31 Shiga  滋賀 Kinki  
5 Hokkaido  
(Kushiro)  北海道  
（釧路）  Hokkaido  32 Kyoto  京都 Kinki  
6 Hokkaido  
(Kitami)  北海道  
（北見）  Hokkaido  33 Osaka  大阪 Kinki  
7 Hokkaido  
(Muroran)  北海道  
（室蘭）  Hokkaido  34 Hyogo  兵庫 Kinki  
8 Aomori  青森 － 35 Nara  奈良 Kinki  
9 Iwate  岩手 － 36 Wakayama  和歌山  Kinki  
10 Miyagi  宮城 － 37 Tottori  鳥取 Shimane, 
Tottori  
11 Akita  秋田 － 38 Shimane  島根 Shimane, 
Tottori  
12 Yamagata  山形 － 39 Okayama  岡山 Okayama, 
Kagawa  
13 Fukushima  福島 － 40 Hiroshima  広島 － 
14 Ibaraki  茨城 Kanto  41 Yamaguchi  山口 － 
15 Tochigi  栃木 Kanto  42 Tokushima  徳島 － 
16 Gunma  群馬 Kanto  43 Kagawa  香川 Okayama, 
Kagawa  
17 Saitama  埼玉 Kanto  44 Ehime  愛媛 － 
18 Chiba  千葉 Kanto  45 Kochi  高知 － 
19 Tokyo  東京 Kanto  46 Fukuoka  福岡 － 
20 Kanagawa  神奈川  Kanto  47 Saga  佐賀 － 
21 Niigata  新潟 － 48 Nagasaki  長崎 － 
22 Toyama  富山 － 49 Kumamoto  熊本 － 
23 Ishikawa  石川 － 50 Oita 大分 － 
24 Fukui  福井 － 51 Miyazaki  宮崎 － 
25 Yamanashi  山梨 － 52 Kagoshima  鹿児島  － 
26 Nagano  長野 － 53 Okinawa  沖縄 － 
27 Gifu 岐阜 Chukyo


--- Page 94 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 94/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Both Target.b0=0 and Target.b1=0.  
- Target.b0=1 & Region ID is invalid.  
- Target.b1=1 & Zip code is not Ascii Number  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Residential Area Command]  
Command(Need ACK)[Set Residential Area Response]  
ACK  Processing


--- Page 95 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 95/318 5.3.6.  Set Auto Event Relay  
(1) Set Auto Event Relay Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h or 06h(option ) 
Header CRC8 :  -- 
Data 0 :  01h Set Auto Event Relay (Upper)  
Data 1 :  11h Set Auto Event Relay (Lower)  
Data 2 :  00h : Auto Event Relay Off  
01h : Auto Event Relay On  
*When this configured as off, notification will be skipped.  
Data 3 :  Notification interval  before switching  
5 to 30 [s] 
Data 4 :  Number of notifications  before switching  
0 to 6 [times]  
Data CRC8 :  -- 
 
(2) Set Auto Event Relay Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Auto Event Relay (Upper)  
Data 1 :  11h Set Auto Event Relay (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Auto Event Relay.  
 This setting is saved by NVRAM.  
 Data 3 / 4 : Event timing   
 Data 3 is the interval between notifications and the time of switching.  
 Data 4 is the number of notifications before switching.  
Data3 × Data4 : Be equal to or less than 30  
Ex) Data3 = 12 / Data4 = 2  
    Host will be notified 2 times – 12[s] and 24[s] before switching.  
 The host can read the current set values of Data 3, Data 4 using Get Configure 
command.  
 “Event Relay  done ” notification will be sent irrespective of the notification settings 
made by  Data3, Data4  and DTV Parameter 2 Data 33, Data 34.


--- Page 96 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 96/318  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Time(Sec)Switching
Notification (1)Data 3 : t
Data 4 : Ntt
t
Notification (3) Notification (N)Notification (2)
. . . .ACK  HOST CPU  B/E 
Command(Need ACK)[Set Auto Event Relay Command]  
Command(Need ACK)[Set Auto Event Relay Response]  
ACK  Processing


--- Page 97 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 97/318 5.3.7.  Set Baud rate 
(1) Set Baud rate Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Baud rate (Upper)  
Data 1 :  19h Set Baud rate (Lower)  
Data 2 :  Baud rate  
03h : 9600  
04h : 19200  
05h : 38400  
06h : 57600  
07h : 115200  
08h : 230400  
09h : 460800  
0Ah : 921600  
Data CRC8 :  -- 
 
(2) Set Baud rate Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Baud rate (Upper)  
Data 1 :  19h Set Baud rate (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Baud rate.  
 Regarding to the timing of changing baud rate, refer to “(5) Sequence”.  
 Data2 (03h~0 Ah) don’t guarantee the communication.  
 This command setting is not stored to NVRAM.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.


--- Page 98 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 98/318  Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Baud  rate Command]  
Command(Need ACK)[Set Baud rate  Response]  
ACK  
Change Baud rate  Change Baud rate


--- Page 99 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 99/318 5.3.8.  Set DTV System  
(1) Set DTV System Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV System (Upper)  
Data 1 :  20h Set DTV System (Lower)  
Data 2 :  DTV System  
00h : Dynamic 4Diver System  (Fore Br0/1)  
01h : Fixed 2x2Diver System  (Fore Br0/1)  
02h : Fixed 2Diver System(Antenna Br2/3)  
03h : Fixed 4Diver System  
04h：Fixed 2Diver System(Antenna Br0/1)  
05h : Fixed 3x1Diver System  (Fore Br0/1/2)  
06h : Dynamic 4Diver System (Fore Br2/3)  
07h : Fixed 2x2Diver System (Fore Br2/3)  
08h : Fixed 3x1Diver System (Fore Br1/2/3)  
Data CRC8 :  -- 
 
(2) Set DTV System Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV System (Upper)  
Data 1 :  20h Set DTV System (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set DTV System.  
 DTV System shows the following table.  
DTV System  Content  
Dynamic 4Diver System  Automatically switch 4Diver Mode and 2x2Diver 
Mode  
Fixed 2x2Diver System  Always 2x2Diver Mode  
Fixed 2Diver System  Always 2Diver Mode  
Fixed 4Diver System  Always 4Diver Mode  
Fixed 3x1Diver System  Always 3x1Diver Mode  
*: 4Diver Mode is 4 antenna s with foreground (Not use background).  
*: 2x2Diver Mode is 2 antenna s with foreground and 2 antenna s with background.  
*: 2Diver Mode is 2 antenna s with foreground (Not use background).  
*: 3x1Diver Mode is 3 antenna with foreground and 1 antenna with background.


--- Page 100 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 100/318  DTV Program load DTV System (Data2) only once at the booting. If HOST send “Set 
DTV System”, HOST has to reset B/E.  
 If DTV System Read Error happened, Selected Fixed 4Diver System.  
• Set DTV System Response is performed after data of Set DTV System Command  is 
written to NVRAM.  
 
・Antenna input pin assignment  
Depending on the DTV System mode setting and background processing status,  
the function assignment of the antenna Br0 -3 is switched as shown in below Table . 
Here, the DTV system mode setting switches the valid antenna input pins and  
the effectiveness of background processing.  
 
Data 2  System  Background processing status  Br0 Br1 Br2 Br3 
00h 
 Dynamic 4Diver System  Active  F F B B 
Inactive  F F F F 
01h Fixed 2x2Diver System  Active  F F B B 
02h Fixed 2Diver System  Inactive  － － F F 
03h Fixed 4Diver System  Inactive  F F F F 
04h Fixed 2Diver System  Inactive  F F － － 
05h Fixed 3x1Diver System  Active  F F F B 
06h Dynamic 4Diver System  Active  B B F F 
Inactive  F F F F 
07h Fixed 2x2Diver System  Active  B B F F 
08h Fixed 3x1Diver System  Active  B F F F 
F : used for Foreground processing.  
B : used for Background processing.  
－ : not used for either Foreground processing or Background 
processing.  
 
 For F039902182, this setting is irrelevant and so th e response will be OK for any 
values. 04h is the only effective setting.  
 After  change any setting on DTV system, a power cycle on/off is  required to adapt 
the setting . 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 10sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- DTV System is not 00h  ~ 08h.


--- Page 101 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 101/318 03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV System Command]  
Command(Need ACK)[Set DTV System Response]  
ACK  
B/E doesn ’t change behavior . 
B/E will change behavior  
after resetting.


--- Page 102 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 102/318 5.3.9.  Set DTV Parameter  
(1) Set DTV Parameter Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  E3h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Parameter (Upper)  
Data 1 :  1Dh Set DTV Parameter (Lower)  
Data 2~5 :  Enable/Disable  
Data2 : 01h , Data3~5 : 00h : Enable Parameter  
Data2:00h,  Data3~5:  00h: Disable Parameter  
 (In case of Disable, u se Default Parameter)  
Data 6~9 :  C/N for Tuner Unlock Detection.  
Data 10~13 :  BER for Tuner Unlock Detection.     
Data 14~17 :  PER for Tuner Unlock Detection.     
Data 18~21 :  Time for Tuner Unlock Detection.     
Data 22~25 :  C/N for change to Fullseg.     
Data 26~29 :  BER for change to Fullseg.     
Data 30~33 :  PER for change to Fullseg.     
Data 34~37 :  Time for change to Fullseg.     
Data 38~41 :  C/N for change to Oneseg.     
Data 42~45 :  BER for change to Oneseg.     
Data 46~49 :  PER for change to Oneseg.     
Data 50~53 :  Time for change to Oneseg.     
Data 54~57 :  C/N for start Broadcast Search . 
Data 58~61 :  BER for start Broadcast Search.  
Data 62~65 :  PER for start Broadcast Search.   
Data 66~69 :  Time for start Broadcast Search.    
Data 70~73 :  Time (1) for disable Broadcast Search.  
Data 74~77 :  Time (2) for disable Broadcast Search.  
Data 78~81 :  Time for Background Tuner Unlock Detection.  
Data 82~85 :  C/N for start Background Search.     
Data 86~89 :  Time for start Background Search.    
Data 90~93 :  C/N for start Background Scan.     
Data 94~97 :  Time for start Background Scan.     
Data 98~101 :  Time for change to 4Div mode.     
Data 102~105 :  C/N difference for switching to background channel.  
Data 106~109 :  BER for switching to background channel.  
Data 110~113 :  PER for switching to background channel.  
Data 114~117 :  Time for switching to background channel.  
Data 118~121 :  C/N for Receive Error Detection.     
Data 122~125 :  BER for Receive Error Detection.    
Data 126~129 :  PER for Receive Error Detection.    
Data 130~133 :  Time for Receive Error Detection.    
Data 134~137 :  C/N for Fullseg Detection at fixed Fullseg search.  
Data 138~141 :  C/N for Oneseg Detection at fixed or auto switch mode search.  
Data 142~145 :  Detect Time (count) for other  broadcast.  
Data 146~149 :  Detect During Time for Another  broadcast.  
Data 150~153 :  C/N Offset for Fullseg Detection at fixed Fullseg broadcast search.  
Data 154~157 :  Reserved  
Data 158~161 :  Reserved  
Data 162~165 :  Reserved  
Data 166~169 :  Reserved  
Data 170~173 :  Reserved  
Data 174~177 :  Reserved  
Data 178~181 :  Reserved


--- Page 103 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 103/318 Data 182~185 :  Reserved  
Data 186~189 :  Reserved  
Data 190~193 :  Reserved  
Data 194~197 :  Reserved  
Data 198~201 :  Reserved  
Data 202~205 :  Reserved  
Data 206~209 :  Reserved  
Data 210~213 :  Reserved  
Data 214~217 :  Reserved  
Data 218~221 :  Reserved  
Data 222~225 :  Reserved  
Data CRC8 :  -- 
・C/N: signed 4byte data (Divide by 100)  
・BER : unsigned 4byte data  (Divide by 1000000)  
・PER : unsigned 4byte data  (Divide by  10000 )  
・Time ： unsigned 4byte data (Multiply  by 0.2)  
・C/N range 0dB to 4 0.0 dB  
・BER range  0.0 000 (No error) to 0.0441  (Error  4.41%) 
・PER range  0.0(No error) to 1.0  (Error100%)  
・Time  range  200ms  to 2000s (Excluding Data 142 to 145)  
 
 
(2) Set DTV Parameter Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Parameter (Upper)  
Data 1 :  1Dh Set DTV Parameter (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set DTV Parameter.  
 Each parameter is 32bit. Refer to the following table about the format.  
Data   Each Parameter  
Data N   Upper  
↑ 
↓ 
Lower  Data N+1   
Data N+2   
Data N+3   
 
 Determination method


--- Page 104 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 104/318 ● Tuner Unlock Detection  
● Change to Oneseg  
● Start Broadcast Search  
● Receive Error  
    When the following OR condition continues for Time.  
a. C/N < C/N Threshold  
b. BER < BER Threshold  
c. PER < PER Threshold  
 
● Change to Fullseg  
● Switching to background channel  
    When the following AND condition continues for Time.  
a. C/N > C/N Threshold  
b. BER > BER Threshold  
c. PER > PER Threshold  
・If DTV Parameter Read Error happened, The value implemented in the program  
is used.  
・The SET DTV Parameter command can be used during idle status or during tuning  
status.  
・This command stores data in FLASH asynchronously with command response.  
So, if reset of power off immediately after the response, need the shutdown ( shutdown 
after storing data ) command.  
・When changing DTV System / DTV Parameter continuously,  
Execute the command in the following procedure.  
①  Execute Set DTV Parameter  
②  Execute Set DTV System  
③  Execute Shutdown (shutdown after storage data)  
Otherwise, DTV  System will not be changed.  
・Data118~121 is for one/auto segment only , for full segment, it sets with DTV 
Parameter2 Data10 -11. 
・Data 122 -125, 126 -129, 130 -133 :common for all segment.  
・Data 134 -137, 138 -141 are used for Broadcast search and seek together.  
・Even if Data 2 -5 is set to Disable, the parameter read value will read the set value. 
(Value  of parameters set as default cannot be read.)  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.


--- Page 105 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 105/318  The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  Command(Need ACK)[Set DTV Parameter Response]  
ACK  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV Parameter Command]  
Store parameters


--- Page 106 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 106/318 5.3.10.  Set Low Power Mode  
(1) Set Low Power Mode  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Low Power Mode(Upper)  
Data 1 :  27h Set Low Power Mode(Lower)  
Data 2 :  Low Power Mode  
00h : Low Power Mode OFF  
01h : Low Power Mode ON  
Data CRC8 :  -- 
 
(2) Set Low Power Mode  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Low Power Mode(Upper)  
Data 1 :  27h Set Low Power Mode(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Low Power Mode.  
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 107 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 107/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Low Power Mode  Command]  
Command(Need ACK)[Set Low Power Mode  Response]  
ACK


--- Page 108 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 108/318 5.3.11.  BML Forced Exit  
(1) BML Forced Exit  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h BML Forced Exit(Upper)  
Data 1 :  28h BML Forced Exit(Lower)  
Data CRC8 :  -- 
 
(2) BML Forced Exit  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh 
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h BML Forced Exit(Upper)  
Data 1 :  28h BML Forced Exit(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Forced Exit BML.  
 Depending on the content, it may be displayed again. (Auto Start BML content.)  
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 109 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 109/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ BML Forced Exit  Command]  
Command(Need ACK) [BML  Forced Exit  Response]  
ACK


--- Page 110 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 110/318 5.3.12.  Set DTV Mode  
(1) Set DTV Mode  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Mode(Upper)  
Data 1 :  2Ch Set DTV Mode(Lower)  
Data 2 :  DTV Mode  
00h : DTV Mode O N without last channel tune  
01h : DTV Mode ON with last channel tune  
10h : DTV Mode O FF without EPG  Scan  
11h : DTV Mode OFF with EPG Scan  
Data 3 :  EPG Scan time per channel  only Data2=11h  
01h – FFh 
Data 2 != 11h : 00h  
Data 4:  Number of days  only Data2=11h  
1~8days  
Data 2 != 11h : 00h  
Data CRC8 :  -- 
 
(2) Set DTV Mode  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Mode(Upper)  
Data 1 :  2Ch Set DTV Mode(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 DTV Mode  ON without/with last channel tune : Sets DTV Mode to ON and remains 
idle or tune to the last channel . 
 When the DTV mode is OFF, power consumption will be reduced / similar to lower 
power mode but slightly more power consumed.  
 DTV Mode O FF with Scan: Scan s the  preset registered channels  for EPG . 
- EPG Scan channel s: Registered channel s in Home and Drive Preset . 
(Excludes duplicate channels .) 
- EPG Scan time per Channel : Data 3 : 1[sec] ～ 255[sec]  
- Start Channel: Last Preset and last channel.  
- EPG scan completed  status refers to DTV status, Data 2.


--- Page 111 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 111/318 (4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV Mode  Command]  
Command(Need ACK)[Set DTV Mode  Response]  
ACK


--- Page 112 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 112/318 5.3.13.  Set Video  Resolution  
(1) Set Video Resolution  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh 
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Video Resolution (Upper)  
Data 1 :  2Dh Set Video Resolution (Lower)  
Data 2 :  Resolution  
00h : 720p  
01h : 480p 
02h : 1080p  
03h : 480i (NTSC)  
04h : 1080p@30Hz  
Data CRC8 :  -- 
 
(2) Set Video Resolution  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 06h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Set Video Resolution (Upper)  
Data 1 :  2Dh Set Video Resolution (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Reserved Fixx 00h  
 
Data CRC8 :  -- 
 
(3) Description  
 720p is the default  for F03990218x  
 480i : BT656 System only.  
 This Setting change is not stored in NVRAM.  
 Playback will be stopped when changing the resolution and host may start again by 
any of the tune commands.


--- Page 113 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 113/318 (4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Video Resolution  Command]  
Command(Need ACK)[  Set Video Resolution  Response]  
ACK


--- Page 114 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 114/318 5.3.14.  Set Banner Config  
(1) Set Banner Config  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  10h 
Header CRC8 :  -- 
Data 0 :  01h Set Banner Config (Upper)  
Data 1 :  2Fh Set Banner Config (Lower)  
Data 2 :  Banner Position X (Upper)  
Data 3 :  Banner Position X (Lower)  
Data 4 :  Banner Position Y (Upper)  
Data 5 :  Banner Position Y (Lower)  
Data 6 :  Font Size  [px] 
Data 7  : Transparency [%]  
Data 8 :  Logo Position Offset  [px] 
Data 9 :  Margin  of Top and Bottom  [px] 
Data 10 :  Margin  of Left and Right  [px] 
Data 11 :  Line spacing  [px] 
Data 12 :  Max number of characters   
Data 13 :  Segment icon   
00h:enable  
01h:disable  
Data 14 :  Automatic banner display enable   
00h:enable  
01h:disable  
Data CRC8 :  -- 
 
(2) Set Banner Confi g Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Banner Config(Upper)  
Data 1 :  2Fh Set Banner Config (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  --


--- Page 115 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 115/318  
(3) Description  
・ Banner Configuration  Parameter . 
 
・ Broadcast logo size will be change according to the font size , irrespective of the 
logotype set by host.  
・ Banner Height is Font Size × 2 + Top and Bottom Margin × 2 + Line Spacing.  
・ Banner Width Maximum Font Size × [Data : 12]  + Left and Right Margin × 2 + 
Font Size × 6(Time information)  
・ If any value is invalid, returns error and the setting is completely ignored . Banner 
will be displayed using last valid settings.  
・ This command setting is not stored to NVRAM.  
・ All coordinate resolutions are set at 1280x720.  
・ Segment icon  size will be change d according to the font size . 
・ The actual parameter range refer to chapter 8.2 or 8.3, data 37 to 46 ,data 107 
and data 109.  
・ The Maximum Number of Characters of Banner is following content.  
➢ Max number of characters is the max imum number of characters of the 
program name.  
➢ Banner width is calculated based on the set value , Font Size × Max 
number of characters + Left and Right Margin × 2 + Font Size × 6  (showing 
the program  time) 
➢ The above cal culation is based on the second row of the banner.  
➢ The first row contains 3Digit number, Branch ID, Logo and TS Name.  
➢ The effective banner width will be the "Maximum of these 2 row -widths"  
➢ In doing so, if the effective width is more than the calculated second row 
width, more characters of the program name will be displayed.  
 
 
 
Banner Position  Logo position offset


--- Page 116 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 116/318 (4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 117 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 117/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[  Set Banner Confi g] 
Command(Need ACK)[  Set Banner Confi g] 
ACK


--- Page 118 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 118/318 5.3.15.  Set Character Set  
(1) Set Character Set  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set Character Set (Upper)  
Data 1 :  31h Set  Character Set (Lower)  
Data 2 :  Character Set  
00h : ARIB  
01h : UTF -8 
Data CRC8 :  -- 
 
(2) Set Character Set  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Character Set (Upper)  
Data 1 :  31h Set  Character Set (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
・ Change Character set  
・ Affects the following commands.  
T.B.D.  
・ This command setting is not stored to NVRAM.  
 
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 119 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 119/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[  Set Character Set ] 
Command(Need ACK)[  Set Character Set ] 
ACK


--- Page 120 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 120/318 5.3.16.  Set DTV Parameter  2 
(1) Set DTV Parameter  2 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  E3h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Parameter 2 (Upper)  
Data 1 :  35h Set DTV Parameter  2 (Lower)  
Data 2 :  Enable  / Disable  
01h : Enable Parameter  
00h : Disable  Parameter (Use Default Parameter)  
Data 3 :  Auto tune mode default  
00h:Auto  
01h:Fullseg  
02h:Oneseg  
03h:Auto with Seamless  
Data 4:  Default Character Set  
00h : ARIB  
01h : UTF -8 
Data 5 :  Default Video Resolution  
00h :  720p  
01h : 480p  
02h : 1080p  
03h : 480i  
04h : 1080p@30Hz  
Data 6 :  Closed Caption display over BML browser  
00h : Enable Display  
01h : Disable Display  
Data 7 :  BML Error Message  
00h : Enable Display  
01h : Disable Display  
Data 8 :  Receive Logo Type  
Bit0 : Logo Type 0  
Bit1 : Logo Type 1  
Bit2 : Logo Type 2  
Bit3 : Logo Type 3  
Bit4 : Logo Type 4  
Bit5 : Logo Type 5  
Bit6/Bit7 : Fix 0  
 
0 : Receive  
1 : Not Receive  
Data 9 :  Search Detection Timeout  
 *This is using for Broadcast Search and Search up/down.  
Data 10 ~ 11:  C/N for Receive Error Detection for Fix Fullseg mode  
Data 12 ~ 13:  C/N for Preset Scan Detection for Fix Oneseg mode and Auto 
mode  
Data 14 ~ 15:  C/N for Preset Scan Detection for Fix Fullseg mode  
Data 16 :  Timeout for Preset Scan per channel  
Data 17 ~ 18 :  C/N Level 3 threshold for full seg    
Data 19 ~ 20 :  C/N Level 2 threshold for full seg    
Data 21 ~ 22 :  C/N Level 1 threshold for full seg    
Data 23 ~ 24 :  EPG Update scan time / channel  
Data 25 :  EPG Scan Number of Days (Only foreground EPG Scan)  
Data 26 ~ 27 :  EPG Scan Signal Threshold (Only foreground EPG Scan)  
Data 28 ~ 29 :  Audio Const offset for Fullseg


--- Page 121 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 121/318 Data 30 ~ 31 :  Audio Const offset for Oneseg  
Data 32 :  Event relay : Auto Event  relay On/Off   
 *When this configured as off, notification will be skipped.  
Data 3 3 :  Event relay : Notification interval before switching  [s] 
Data 34 :  Event relay : Number of notifications before switching  [times]  
Data 35 ~ 36  Banner: Banner Position X  
Data 37 ~ 38  Banner: Banner Position Y  
Data 39 :  Banner: Font Size [px] 
Data 40 :  Banner: Transparency [%]  
Data 41 :  Banner: Logo Position Offset  [px] 
Data 42 :  Banner: Margin of Top and Bottom [px] 
Data 43 :  Banner: Margin of Left and Right [px] 
Data 44 :  Banner: Line spacing [px] 
Data 45 :  Banner: Max number of characters  
Data 46 :  Banner: Default Timeout [s]  
Data 47 :  EPG List Type Enable  
Bit0 : List Type 1 Enable  
Bit1 : List Type 2 Enable  
Bit2 : List Type 3 Enable  
Bit3 : List Type 4 Enable  
Data 48 :  EPG List: Type1 Program name Font Size  [px] 
Data 49 :  EPG List: Type1 TS Name Font Size  [px] 
Data 50 :  EPG List: Type1 EPG Content Font Size  [px] 
Data 51 :  EPG List: Type2 Program name Font Size  [px] 
Data 52 :  EPG List: Type2 TS Name Font Size  [px] 
Data 53 :  EPG List: Type2 EPG Content Font Size  [px] 
Data 54 :  EPG List: Type3 Program name Font Size  [px] 
Data 55 :  EPG List: Type3 TS Name Font Size  [px] 
Data 56 :  EPG List: Type3 EPG Content Font Size  [px] 
Data 57 :  EPG List: Type4 Program name Font Size  [px] 
Data 58 :  EPG List: Type4 TS Name Font Size  [px] 
Data 59 :  EPG List: Type4 EPG Content Font Size  [px] 
Data 60 :  EPG List: Table Title Color Red    
Data 61 :  EPG List: Table Title Color Green   
Data 62 :  EPG List: Table Title Color Blue    
Data 63 :  EPG List: Table Title Font Color Red    
Data 64 :  EPG List: Table Title Font Color Green    
Data 65 :  EPG List: Table Title Font Color Blue   
Data 66 :  EPG List: Cursor Color Red    
Data 67 :  EPG List: Cursor Color Green    
Data 68 :  EPG List: Cursor Color Blue    
Data 69 :  EPG List: Cursor Font Color Red    
Data 70 :  EPG List: Cursor Font Color Green    
Data 71 :  EPG List: Cursor Font Color Blue    
Data 72 :  EPG List: Current Program Color Red    
Data 73 :  EPG List: Current Program Color Green    
Data 74 :  EPG List: Current Program Color Blue    
Data 75 :  EPG List: Current Program Font Color Red    
Data 76 :  EPG List: Current Program Font Color Green    
Data 77 :  EPG List: Current Program Font Color Blue    
Data 78 :  EPG List: Balloon color Red    
Data 79 :  EPG List: Balloon color Green    
Data 80 :  EPG List: Balloon color Blue    
Data 81 :  EPG List: Balloon Font color Red    
Data 82 :  EPG List: Balloon Font color Green    
Data 83 :  EPG List: Balloon Font color Blue    
Data 84 :  EPG List: Border line color Red    
Data 85 :  EPG List: Border line color Green


--- Page 122 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 122/318 Data 86 :  EPG List: Border line color Blue     
Data 87 :  EPG Information: Font Size  [px] 
Data 88 :  EPG Information: Title Font Color Red    
Data 89 :  EPG Information: Title Font Color Green    
Data 90 :  EPG Information: Title Font Color Blue    
Data 91 :  EPG Information: Line Spacing for Title    
Data 92 :  EPG Information: Line Spacing for Contents     
Data 93 :  EPG Information: Margin   
Data 94 :  Default Auto Broadcast Search mode  
Data 95~96 :  C/N Level 3 threshold for one seg   
Data 97~98 :  C/N Level 2 threshold  for one seg   
Data 99~100 :  C/N Level 1 threshold  for one seg   
Data 101 :  Default event mask 0  
  *Refer to chapter “5.3.20. Set Event Mask”  
Data 102 :  Default event mask 1  
  *Refer to chapter “5.3.20. Set Event Mask”  
Data 103 :  Default event mask 2  
  *Refer to chapter “5.3.20. Set Event Mask”  
Data 104 :  EPG List: Short program border line color Red     
Data 105 :  EPG List: Short program border line color Green    
Data 106 :  EPG List: Short program border line color Blue  
Data 107 :  Banner: segment icon  
Data 108 :  Number of scrolling line on EPG detail  
Data 109 :  Automatic banner display enable.  
00h:Enable  
01h:Disable  
Data 110~225 :  Reserved  
Data CRC8 :  -- 
・C/N: signed 4byte data (Divide by 100)  
・C/N range 0dB to 4 0.0 dB  
 
(2) Set DTV Parameter  2 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set DTV Parameter 2 (Upper)  
Data 1 :  35h Set DTV P arameter  2 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set DTV Parameter.  
 Each parameter  is big endian .  
 Each parameters data range move to Chapter 8.2 or 8.3, please refer to them.  
 For New Frontier(F039990144) case, Data 5 is fixed, cannot be changed.


--- Page 123 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 123/318  For New Frontier(F039990144) case , changing to the following data ate no 
supported , so the display will not be guaranteed if changed.  
 *Data 6 to 7 and 48 to 93, 104 to 105 . 
 C/N: signed 4byte data (Divide by 100)


--- Page 124 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 124/318  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  unknown error  
          For other errors, refer to Chapter [3. Error Code]  
          When 01h (invalid parameter) is happened, all parameter is not effective.  
 
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  Command(Need ACK)[Set DTV Parameter 2 Response]  
ACK  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV Parameter 2 Command]  
Store parameters


--- Page 125 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 125/318 5.3.17.  Set User ID  
(1) Set User ID  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Set User ID (Upper)  
Data 1 :  3Bh Set User ID (Lower)  
Data 2 :  User ID  
01h to 06 h 
FFh : Demo mode User  
Data CRC8 :  -- 
 
(2) Set User ID  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set User ID (Upper)  
Data 1 :  3Bh Set User ID (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
・ During Demo mode User, below Commands are supported.  
 Code  
(Data0/1)  Command  
0104h  Get DTV Status  
0105h  Shutdown  
0106h  Watch dog  
0107h  Get TS Name  
0113h  Get Version  
0118h  Get Program information  
0119h  Set Baud rate  
012Ch  Set Banner Config  
0130h  Get Banner Config  
0133h  Get TS Name with UTF -8 
0134h  Get Program Information with UTF -8 
0135h  Set DTV Parameter 2  
0136h  Get DTV Parameter 2  
013Bh  Set User ID  
013Ch  Get User ID  
0141h  Set Event Mask  
0142h  Get Event Mask  
0143h  Get Part Number


--- Page 126 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 126/318 0145h  Get Program Name with UTF -8 by 3Digit Number  
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set User ID  Command]  
Command(Need ACK)[  Set User ID  Response]  
ACK


--- Page 127 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 127/318 5.3.18.  Set EPG Config  
(1) Set EPG Config  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  36h 
Header CRC8 :  -- 
Data 0 :  01h Set EPG Config (Upper)  
Data 1 :  3Dh Set EPG Config (Lower)  
Data 2 :  EPG List Type Enable  
Bit0 : Type 1 Enable  
Bit1 : Type 2 Enable  
Bit2 : Type 3 Enable  
Bit3 : Type 4 Enable  
 
0 : Enable  
1 : Disable  
Data 3 :  EPG List: Type1 Program name Font Size  [px] 
Data 4 :  EPG List:  Type1 TS Name Font Size  [px] 
Data 5 :  EPG List: Type1 EPG Content Font Size  [px] 
Data 6 :  EPG List: Type2 Program name Font Size  [px] 
Data 7 :  EPG List: Type2 TS Name Font Size [px] 
Data 8 :  EPG List: Type2 EPG Content Font Size  [px] 
Data 9 :  EPG List: Type3 Program name Font Size  [px] 
Data 10 :  EPG List: Type3 TS Name Font Size  [px] 
Data 11 :  EPG List: Type3 EPG Content Font Size  [px] 
Data 12 :  EPG List: Type4 Program name Font Size  [px] 
Data 13 :  EPG List: Type4 TS Name Font Size  [px] 
Data 14 :  EPG List: Type4 EPG Content Font Size  [px] 
Data 15 :  EPG List: Table Title Color Red  
Data 16 :  EPG List: Table Title Color Green  
Data 17 :  EPG List: Table Title Color Blue  
Data 18 :  EPG List: Table Title Font Color Red  
Data 19 :  EPG List: Table Title Font Color Green  
Data 20 :  EPG List: Table Title Font Color Blue  
Data 21 :  EPG List: Cursor Color Red  
Data 22 :  EPG List: Cursor Color Green  
Data 23 :  EPG List: Cursor Color Blue  
Data 24 :  EPG List: Cursor Font Color Red  
Data 25 :  EPG List: Cursor Font Color Green  
Data 26 :  EPG List: Cursor Font Color Blue  
Data 27 :  EPG List: Current Program Color Red  
Data 28 :  EPG List: Current Program Color Green  
Data 29 :  EPG List: Current Program Color Blue  
Data 30 :  EPG List: Current Program Font Color Red  
Data 3 1 :  EPG List: Current Program Font Color Green  
Data 32 :  EPG List: Current Program Font Color Blue  
Data 33 :  EPG List: Balloon color Red  
Data 34 :  EPG List: Balloon color Green  
Data 35 :  EPG List: Balloon color Blue  
Data 36 :  EPG List: Balloon Font color Red  
Data 37 :  EPG List: Balloon Font color Green  
Data 38 :  EPG List: Balloon Font color Blue  
Data 39 :  EPG List: Border line color Red  
Data 40 :  EPG List: Border line color Green  
Data 41 :  EPG List: Border line color Blue  
Data 42 :  EPG  information:  Font Size  [px]


--- Page 128 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 128/318 Data 43 :  EPG information:  Title Font Color Red  
Data 44 :  EPG information:  Title Font Color Green  
Data 45 :  EPG information:  Title Font Color Blue  
Data 46 :  EPG information:  Line Spacing for Title  
Data 47 :  EPG information:  Line Spacing for Contents  
Data 48 :  EPG information:  Margin (Applied to all four sides)  
Data 49 : EPG List: Short program border line color Red  
Data 50 : EPG List: Short program border line color Green  
Data 51 : EPG List: Short program border line color Blue  
Data 52 :  Number of scrolling line on EPG detail  
Data CRC8 :  -- 
 
(2) Set EPG  Confi g Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set EPG Config (Upper)  
Data 1 :  3Dh Set EPG Config (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 EPG Type   for F039902182 【TRS231BSxxxx 】,F03990218
【TRH231BSxxxx 】 
 For New Frontier(F039990144) case, Data 3 to 51 should  not be changed.  
Changing these parameters may corrupt the display.  
           
                        Type1                                                           Type2


--- Page 129 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 129/318           
                        Type3                                                            Type4  
 
 EPG Type   for F039990144 【FRO232BSyyzz 】 
   
                        Type1                                                           Type2  
 
   
                        Type3                                                            Type4


--- Page 130 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 130/318 EPG  Configuration  Parameter . 
 
① Program Name Font Size  
② TS Name Font Size  
③ EPG Content Font Size  
④ Table Title Color  & Font Color  
⑤ Cursor Color  & Font Color  
⑥ Current Program Color  & Font Color  
⑦ Balloon  Color  & Font Color  
⑧ Border Line Color  
⑨ Short  program border line color  
  
① 
② 
③ ④ 
⑤ 
⑧ 00将棋フォーカス  
「破った後に戦  
力アップ」  
⑥ 
⑦ ⑨


--- Page 131 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 131/318  
① Font size  (Title  and Content)  
② Title Font Color  
③ Title Line Spacing  
④ Content Line Spacing  
⑤ EPG Detail Margin  
 
・ The Title Line Spacing will not be applied to first title on the page, to avoid the 
title being displayed too low due to Margin and Line Spacing.  
・ This command setting is not stored to NVRAM.  
・ The actual parameter range refers to chapter 8.2 and 8.3, data 48 to 93, data 
108. 
・ For F039990144 【FRO232BSyyzz 】, the EPG list design is adjusted to meet 
your requests as much as possible, so it is not guaranteed that the display will be 
correct when parameters are changed.  
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
  
① 
② ③ 
④ 
⑤ 
⑤ ⑤ 
⑤


--- Page 132 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 132/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[  Set EPG  Confi g] 
Command(Need ACK)[  Set EPG  Confi g] 
ACK


--- Page 133 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 133/318 5.3.19.  Set Video Color  
(1) Set Video Color  Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  08h 
Header CRC8 :  -- 
Data 0 :  01h Set Video Color (Upper)  
Data 1 :  3Fh Set Video Color (Lower)  
Data 2 :  Brightness   
-127(81h) – 127(7Fh) [Default is 0]  
Data 3  :  Contrast  
0 – 7 [Default is 0]  
Data 4～6 : Reserved  
Data CRC8 :  -- 
 
(2) Set Video Color  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Video Color (Upper)  
Data 1 :  3Fh Set Video Color (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
・ Set Video Color  
・ Brightness: Brightness of the original image can be decreased or increased and 
consists of 25 5 levels.  These values are 2’s complements and can be set 
between -127 and +127 . 
・ Contrast:  Contrast can be adjusted in 8 levels, 0 to 7. 0 represents the contrast 
of original image. The contrast of the original image cannot be reduced.  
・ Set User ID does not affect last color setting.


--- Page 134 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 134/318 (4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Video Color  Command]  
Command(Need ACK)[  Set Video Color  Response]  
ACK


--- Page 135 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 135/318 5.3.20.  Set Event Mask  
(1) Set Event Mas k Command ( HOST  ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  01h Set Event Mask  (Upper)   
Data 1 :  41h Set Event Mask  (Lower)  
Data 2 :  Event mask 0  
bit0 : DTV Status  
bit1 : Scan Status  
bit2 : Search Status  
bit3 : DTV Event  
bit4 : EWS Event  
bit5 : EPG Status  
bit6 : Event relay  
bit7 : Number of Program info  
 
0 : Not Mask  
1 : Mask  - Disables the event notification.  
Data 3 :  Event mask 1  
bit0 : Program Information  
bit1 : Program Information  with UTF -8 
bit2 : TS Name Update  
bit3 : TS Name Update  with UTF -8 
bit4 : Logo Update  
bit5 : EGP Button Status  
bit6 : BML Status  
bit7 : C/N Information  
 
0 : Not Mask  
1 : Mask  - Disables the event notification.  
Data 4 :  Event mask 2  
bit0 :  EPG Scan Result  
bit1 – 7 Reserve  
 
0 : Not Mask  
1 : Mask - Disables the event notification.  
Data CRC8 :  -- 
 
(2) Set Event Mask  Response  (BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Set Event  Mask  (Upper)   
Data 1 :  41h Set Event  Mask (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”)


--- Page 136 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 136/318 Data CRC8 :  -- 
 
(3) Description  
・ Set Event Enable / Disable  
 
(4) Error Handling  
・ Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Event Mask  Command]  
Command(Need ACK)[  Set Event Mask  Response]  
ACK


--- Page 137 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 137/318 5.4. HOST⇒B/E Get Command  
5.4.1.  Get DTV Status  
(1) Get DTV Status  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV Status(Upper)  
Data 1 :  04h Get DTV Status(Lower)  
Data CRC8 :  -- 
 
(2) Get DTV Status Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  14h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV Status(Upper)  
Data 1 :  04h Get DTV Status(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  DTV Status  
00h : Power OFF (Not Support)  
01h : Booting (Not Support)  
02h : Shutdown (After Shutdown  B/E) 
03h : In Service (After Booting  B/E) 
04h : Low Power (Low Power mode)  
05h : DTV OFF  
06h : DTV OFF with EPG SCAN  
07h : Demo mode  
Data 5 :  Tuning Status  
00h : Idle  
01h : Tuning  
Data 6 :  Service Type ( Now Playing Service Type)  
00h : ISDB -T Fullseg  
01h : ISDB -T Oneseg  
FFh : None (Not Tuning)  
Data 7 :  Service Status  
00h : Invalid  
01h : Normal Service  
02h : Special Service  
03h : Emergency Service  
04h : Suspend Service  
Data 8 :  Video Output  
00h : No output (From Tuning to Video Output)  
01h : Outputted  
Data 9 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)


--- Page 138 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 138/318 FFh : None(Not Tuning / Not Stored channel)  
Data 10 :  Preset Channel Number  
00h : tuned by Search/BC  Search/Physical Channel Set  
01h～0Ch : Preset Channel Number  
FFh : None (Not Tuning)  
Data 11 :  Copy Control  
(Refer to “5.7.1 DTV Status (2) Description”)  
Data 12 :  Copy Control  
(Refer to “5.7.1 DTV Status (2) Description”)  
Data 13 :  Event Code  
Refer to “ 5.7.4 .DTV Event ” 
※Event code of "0x80" or more will not occur in this data.  
Data 14 :  Diver Mode  
00h : Dynamic 4Diver System (Fore Br0/1)  
01h : Fixed 2x2Diver System (Fore Br0/1)  
02h : Fixed 2Diver System(Antenna Br2/3)  
03h : Fixed 4Diver System  
04h：Fixed 2Diver System(Antenna Br0/1)  
05h : Fixed 3x1Diver System  (Fore Br0/1/2)  
06h : Dynamic 4Diver System (Fore Br2/3)  
07h : Fixed 2x2Diver System (Fore Br2/3)  
08h : Fixed 3x1Diver System (Fore Br1/2/3)  
Data 15 :  Antenna Level  
00h : Antenna Level 0  
01h : Antenna Level 1  
02h : Antenna Level 2  
03h : Antenna Level 3  
Data 16 :  Background Status  
00h : idle  
01h : Background Search  
02h : Background Scan  
03h : Manual Background Search  
04h : Manual Background Scan  
Data 17 :  EPG/BML Status  
00h : No EPG/BML displayed  
01h : Updating  
02h : EPG List (full seg)  
03h : EPG List (one seg)  
04h : EPG Information (full seg)  
05h : EPG Information (one seg)  
06h : BML Display  
Data18  Tuner0 Physical Channel Number  
Data CRC8  --


--- Page 139 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 139/318 (3) Description  
 Get DTV Status  
 DTV Status information in Data2 will be set to In Service (03h) immediately after 
sending “Wakeup” from B/E. B/E will not wait for Wakeup Response for setting this.  
 If Data4 = “04h: Low Power mode ",  tune commands, Display EPG command, etc., 
are not supported.  
 If Data4 = “07h: Demo mode  ",  Only a few commands are supported. See “ 5.3.17. 
Set User ID ” for the list of supported commands.  
  “Service Status(Data 7)” is :  
Service Status  Description  
Invalid  If Tuning Status (Data5) isn’t “Tuning”, Service Status is 
invalid.  
Normal Service   
Special Service  This service is defined by “ARIB TR -B14 Volume4 23. 
Special Services”.  
Emergency Service  This service is defined by “ARIB TR -B14 Volume4  
26. Use of Emergency Warning Broadcasting 
(Emergency Warning System (EWS))”.  
Suspend Service  This service is “Off service” that defined by “ARIB TR -B14 
Volume4 15. Definition of Service “On service” / “Off 
service””.  
 If “Diver Mode” is 00h or 01h, B/E use both tuner0/tuner1.  
 Tuner0 is used for Foreground processing, and Tuner1 is used for Background 
processing.  
 “Antenna Level” indicates the number of antenna bars on the display. Antenna Level 
0 is bad signal. Antenna Level 3 is good signal. If “Tuning Status (Data5)” is idle, 
Antenna Level is 0.  
 If “EPG Update Status” is 00h, B/E isn’t updating EPG of specified channel. But B/E 
may be updating EPG with back scan.  If 01h, B/E is updating forcibly by 
“5.2.12 .Display EPG ” command. If finishing to update EPG, “EPG Update Status” 
change to 00h.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 140 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 140/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get DTV Status Command]  
Command(Need ACK)[Get DTV Status Response]  
ACK  Processing


--- Page 141 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 141/318 5.4.2.  Get TS Name  
(1) Get TS Name Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Get TS Name (Upper)  
Data 1 :  07h Get TS Name (Lower)  
Data 2 :  01h~0Ch : Preset Channel Number  
FFh : All Preset Channel Number  
00h : Not Stored Channel.  
Data 3 :  00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data CRC8 :  -- 
 
(2) Get TS Name Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK :  
Preset Channel Number = 00h～0Ch: 1Ah  
Preset Channel Number = FFh : F6h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get TS Name (Upper)  
Data 1 :  07h Get TS Name (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value   
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  01h~0Ch : Preset Channel Number  
FFh : All Channels in Preset  
00h : Not Stored Channel.  
Data 5~24 :  TS Name(8bit character code set)  
Data 4 is 00h~0Ch:Specified Preset Channel Number  
Data 4 is FFh : Preset Channel Number = 1  
Data 25~44 :  TS Name(8bit character code set) 
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 2  
Data 45~64 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 3  
Data 65~84 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 4  
Data 85~104 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 5  
Data 105~124 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 6


--- Page 142 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 142/318 Data 125~144 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 7  
Data 145~164 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 8  
Data 165~184 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 9  
Data 185~204 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 10  
Data 205~224 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 11  
Data 225~244 :  TS Name(8bit character code set)  
Data 4 is 00h  ~0Ch : Don’t use  
Data 4 is FFh : Preset Channel Number = 12  
Data CRC8 :  -- 
 
(3) Description  
 Get TS Name.  
 If Preset Channel Number is 01h~0Ch, get TS Name of specified Preset Channel 
and specified Preset Table.  
 If Preset Channel Number is FFh, get All TS Name in specified Preset Table.  
 If Preset Channel Number is 00h, get TS Name of Not Stored Channel.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 143 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 143/318  
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get TS Name Command]  
Command(Need ACK)[Get TS Name Response]  
ACK  Processing


--- Page 144 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 144/318 5.4.3.  Get Configure  
(1) Get Configure  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Configure(Upper)  
Data 1 :  0Ch Get Configure(Lower)  
Data CRC8 :  -- 
 
(2) Get Configure Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 1Ch 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Configure(Upper)  
Data 1 :  0Ch Get Configure(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Audio Mode  
00h : Main  
01h : Sub  
02h : Main  + Sub 
Data 5 :  Closed Caption Mode  
 
00h : closed caption off but superimpose off  
01h : 1st closed caption on and superimpose 1st on  
02h : 2nd closed caption on and superimpose 2nd on  
03h : closed caption off and superimpose 1st on  
04h : 1st closed caption on and superimpose off  
05h : 2nd closed caption on and superimpose off  
   
Initial value : 00h  
Data 6 :  Auto Tune Mode  
00h :  Auto 
01h : Only Fullseg  
02h : Only Oneseg  
03h : Auto with Seamless  
Data 7 :  Auto Broadcast Search Mode  
00h : Automatic Broadcast Search Off  
01h : Automatic Relay Station Search On  
02h : Automatic Affiliated Station Search On  
03h : Automatic Relay & Affiliated Station Search On  
Data 8 :  Auto Event Relay  
 00h : Off  
 01h : On  
Data 9 :  Region ID (Refer to “ 5.3.5 .Set Residential Area ”) 
(Home Preset)


--- Page 145 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 145/318 Data 10 :  Zip-Code[0](Home Preset) Ascii Code  
In case of “1234567”, ‘1’  
Data 11 :  Zip-Code[1](Home Preset) Ascii Code  
In case of “1234567”, ‘2’  
Data 12 :  Zip-Code[2](Home Preset) Ascii Code  
In case of “1234567”, ‘3’  
Data 13 :  Zip-Code[3](Home Preset) Ascii Code  
In case of “1234567”, ‘4’  
Data 14 :  Zip-Code[4](Home Preset) Ascii Code  
In case of “1234567”, ‘5’  
Data 15 :  Zip-Code[5](Home Preset) Ascii Code  
In case of “1234567”, ‘6’  
Data 16 :  Zip-Code[6](Home Preset) Ascii Code  
In case of “1234567”, ‘7’  
Data 17 :  Region ID (Refer to “ 5.3.5 .Set Residential Area ”) 
(Drive Preset)  
Data 18 :  Zip-Code[0](Drive Preset) Ascii Code  
In case of “1234567”, ‘1’  
Data 19 :  Zip-Code[1](Drive Preset) Ascii Code  
In case of “1234567”, ‘2’  
Data 20 :  Zip-Code[2](Drive Preset) Ascii Code  
In case of “1234567”, ‘3’  
Data 21 :  Zip-Code[3](Drive Preset) Ascii Code  
In case of “1234567”, ‘4’  
Data 22 :  Zip-Code[4](Drive Preset) Ascii Code  
In case of “1234567”, ‘5’  
Data 23 :  Zip-Code[5](Drive Preset) Ascii Code  
In case of “1234567”, ‘6’  
Data 24 :  Zip-Code[6](Drive Preset) Ascii Code  
In case of “1234567”, ‘7’  
Data 25 :  Event Relay Notification Interval  before switching  [s] 
Data 26 :  Event Relay Number of Notification  before switching  
[times]  
Data CRC8 :  -- 
 
(3) Description  
 Get Configure  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 146 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 146/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Configure Command]  
Command(Need ACK)[Get Configure Response]  
ACK  Processing


--- Page 147 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 147/318 5.4.4.  Get Version  
(1) Get Version  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Version (Upper)  
Data 1 :  13h Get Version (Lower)  
Data CRC8 :  -- 
 
(2) Get Version Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 15h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Version (Upper)  
Data 1 :  13h Get Version (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Hardware Version 0(Upper)  
Data 5 :  Hardware Version 1  
Data 6 :  Hardware Version 2  
Data 7 :  Hardware Version 3(Lower)  
Data 8 :  Boot Version 0(Upper)  
Data 9 :  Boot Version 1  
Data 10 :  Boot Version 2  
Data 11 :  Boot Version 3(Lower)  
Data 12 :  Software Version 0(Upper)  
Data 13 :  Software Version 1  
Data 14 :  Software Version 2  
Data 15 :  Software Version 3  
Data 16 :  Software Version 4  
Data 17 :  Software Version 5  
Data 18 :  Software Version 6  
Data 19 :  Software Version 7(Lower)  
Data CRC8 :  -- 
 
(3) Description  
 Get Software Version.  
 The format of Hardware Version is ASCII.(Ex. “004A”)  
 The format of Boot Version is ASCII. (Ex. “0102”)  
 The format of Software Version is ASCII. (Ex. “AABB1234”)


--- Page 148 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 148/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Version Command]  
Command(Need ACK)[Get Version Response]  
ACK  Processing


--- Page 149 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 149/318 5.4.5.  Get Audio ES  
(1) Get Audio ES  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES (Upper)  
Data 1 :  14h Get Audio ES (Lower)  
Data CRC8 :  -- 
 
(2) Get Audio ES  Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 06h~26h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES (Upper)  
Data 1 :  14h Get Audio ES (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  ES Num  
0x01~0x0F  : Number of Audio ES  
0xFF : not available yet  
Data 5 :  Component Tag 1  
(Current playing Audio ES component Tag)  
Data 6 :  Component Tag 2  
(Lowest Component Tag(except during playback)  
 … 
Data n :  Component Tag N  
(Highest Component Tag(except during playback)  
Data CRC8 :  -- 
 
(3) Description  
 Get Audio ES.  
 Component Tag is 010h~2Fh (Fullseg), 83h~86h (Oneseg).  
 Component Tag is used by “ 5.2.7 .ES Switch ”. 
 If B/E doesn’t receive  Audio ES Information, Data 4(ES Num) is set to 0xFF.


--- Page 150 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 150/318  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Audio ES Command]  
Command(Need ACK)[Get Audio ES Response]  
ACK  Processing


--- Page 151 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 151/318 5.4.6.  Get Program Information  
(1) Get Program Information  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Information (Upper)  
Data 1 :  18h Get Program Information (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Information Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h~80h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Information (Upper)  
Data 1 :  18h Get Program Information (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 5 :  00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 6 :  Three Digit Number(Upper)  
Data 7 :  Three Digit Number(Lower)  
Data 8 :  Branch Identifier Number  
Data 9 :  Length of Station Name(N1) : 00h~14h  
Data 10~9+N1 :  Station Name(TS Name)  
Data 10+N1 :  Length of Program Name(N2) : 00h~60h  
Data 
11+N1~10+N1+N2:  Program Name  
Data CRC8 :  -- 
 
(3) Description  
 Get the program information in current service.  
 The program information contains Preset Channel Number Station Name / Program 
name).  
 Preset Channel Number (Data5) of Response is current playback channel. If current 
playback channel is not stored, Data5 is 00h and Data4 is FFh.  
 Three Digit Number & Branch Identifier Number of Response are current playback 
service. If current playback channel is not stored, these data are set.


--- Page 152 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 152/318  The length of Station Name is 00h~14h.  
 The format of Station Name is 8bit character code set.  
 The length of Program Name is 00h~60h.  
 The format of Program name is 8bit character code set.  
 If B/E doesn’t have Program name, Length of Program Name is set to 0.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Information Command]  
Command(Need ACK)[Get Program Information Response]  
ACK  Processing


--- Page 153 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 153/318 5.4.7.  Get Service Information  
(1) Get Service Information  Command (HOST ⇒ BE) 
Start Sync :  A5h,5ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Get Service Information (Upper)  
Data 1 :  1Ch Get Service Information (Lower)  
Data 2 :  Preset Table  
00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data 3 :  One Touch Number  
01h ~ 0Ch : Service Information of Specified Channel  
00h : Service Information of Not Stored Channel.  
FFh : Service Information of All Channel.  
Data CRC8 :  -- 
 
(2) Get Service Information Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 08h~  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Service Information (Upper)  
Data 1 :  1Ch Get Service Information (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6~ :  Service_Information_Data  
Refer to “ (4) Description ” 
Data CRC8 :  --


--- Page 154 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 154/318 (3) Get Service Information Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 0008h~0 FFFh 
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Service Information (Upper)  
Data 1 :  1Ch Get Service Information (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6~ :  Service_Information_Data  
Refer to “ (4) Description ” 
Data CRC8 :  -- 
 
(4) Description  
 Get Service Information.  
 If One Touch Number (Data3) of Command is FFh, B/E response the service 
information of all channels.  If One Touch Number (Data3) of Command is  00h, B/E 
response the service information of not -stored channel.  If One Touch Number (Data3) 
is 01h~0Ch, B/E response the service information of specified channel.  
 “Fragment Number” is the order of the fragmented response.  
 For Header Type 1, If the length of Data Part is 255byte and under, “Fragment 
Number” is 0. If the length of Data Part is over 255byte, it is the order number. The 
B/E send s the data in actual order.  
 For Header Type 2, If the length of Data Part is 4095 byte and under, “Fragment 
Number” is 0. If the length of Data Part is over 4095 byte, it is the order number. The 
B/E sends the data in actual order.  
 “Last Fragment Number” is the max number of “Fragment Number”.  
 “Service Information Data” shows the following table.  
Number_of_TS_Information(N1)  
for(i = 0; i < N1 ; i++){  
OneTouchNumber  
Number_of_Service_Information(N2)  
for(j = 0; j < N2; j++){  
        Service_Information()  
} 
} 1byte  
 
1byte  
1byte  
 
n byte  
 “Number_of_TS_Information” is the number of the followings TS Information. The 
range is 00h~0Ch.  
 “OneTouchNumber” is valid one touch number. The range is 00h~0Ch


--- Page 155 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 155/318  “Number_of_Service_Information” is the number of the followings 
Service_Information(). The range of “Number_of_Service_Information” is 00h~17h.  
 The format of “Service_Information()” shows the following table.  
Field  Size Value  
Three Digit Number  2Byte  011~  
Service ID  2Byte  0x0000~0xFFFF  
Branch Identifier Number  1Byte  0~9 
Media Type  1Byte  0 : Full Seg Service  
1 : Data Service(Not Support)  
2 : Data Service(Not Support)  
3 : One Seg Service  
Service Name Length  1Byte  00h ~ 14h  
Service Name  0~20Bytes  8bit character code set   
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 ACK  HOST CPU  B/E 
Command(Need ACK)[Get Service Information Command]  
Command(Need ACK)[Get Service Information Response]  
ACK  Processing


--- Page 156 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 156/318 5.4.8.  Get DTV Parameter  
(1) Get DTV Parameter Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV Parameter (Upper)  
Data 1 :  1Eh Get DTV Parameter (Lower)  
Data CRC8 :  -- 
 
(2) Get DTV Parameter Response (BE ⇒ HOST)  
 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : E5h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get DTV Parameter (Upper)  
Data 1 :  1Eh Get DTV Parameter (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4~7 :  Enable/Disable  
Data4 : 01h , Data5~7 : 00h : Enable Parameter  
Data4 : 00h , Data5~7 : 00h : Disable Parameter  
(In case of Disable, use Default Parameter  
Data 8~11 :  C/N for Tuner Unlock Detection.  
Data 12~15 :  BER for Tuner Unlock Detection.  
Data 16~19 :  PER for Tuner Unlock Detection.  
Data 20~23 :  Time for Tuner Unlock Detection.  
Data 24~27 :  C/N for change to Fullseg.  
Data 28~31 :  BER for change to Fullseg.  
Data 32~35 :  PER for change to Fullseg.  
Data 36~39 :  Time for change to Fullseg.  
Data 40~43 :  C/N for change to Oneseg.  
Data 44~47 :  BER for change to Oneseg.  
Data 48~51 :  PER for change to Oneseg.  
Data 52~55 :  Time for change to Oneseg.  
Data 56~59 :  C/N for start Broadcast Search.  
Data 60~63 :  BER for start Broadcast Search.  
Data 64~67 :  PER for start Broadcast Search.  
Data 68~71 :  Time for start Broadcast Search.  
Data 72~75 :  Time (1) for disable Broadcast Search.  
Data 76~79 :  Time (2) for disable Broadcast Search.  
Data 80~83 :  Time for Background Tuner Unlock Detection.  
Data 84~87 :  C/N for start Background Search.  
Data 88~91 :  Time for start Background Search.  
Data 92~95 :  C/N for start Background Scan.  
Data 96~99 :  Time for start Background Scan.


--- Page 157 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 157/318 Data 100~103 :  Time for change to 4Div mode.  
Data 104~107 :  C/N difference for switching to background channel.  
Data 108~111 :  BER for switching to background channel.  
Data 112~115 :  PER for switching to background channel.  
Data 116~119 :  Time for switching to background channel.  
Data 120~123 :  C/N for Receive Error Detection.  
Data 124~127 :  BER for Receive Error Detection.  
Data 128~131 :  PER for Receive Error Detection.  
Data 132~135 :  Time for Receive Error Detection.  
Data 136~139 :  C/N for Fullseg Detection at fixed Fullseg search.  
Data 140~143 :  C/N for Oneseg Detection at fixed or auto switch mode search.  
Data 144~147 :  Detect Time (count) for other  broadcast.  
Data 148~151 :  Detect During Time for other broadcast.  
Data 152~155 :  C/N Offset for Fullseg Detection at fixed Fullseg broadcast search.  
Data 156~159 :  Reserved  
Data 160~163 :  Reserved  
Data 164~167 :  Reserved  
Data 168~171 :  Reserved  
Data 172~175 :  Reserved  
Data 176~179 :  Reserved  
Data 180~183 :  Reserved  
Data 184~187 :  Reserved  
Data 188~191 :  Reserved  
Data 192~195 :  Reserved  
Data 196~199 :  Reserved  
Data 200~203 :  Reserved  
Data 204~207 :  Reserved  
Data 208~211 :  Reserved  
Data 212~215 :  Reserved  
Data 216~219 :  Reserved  
Data 220~223 :  Reserved  
Data 224~227 :  Reserved  
Data CRC8 :  -- 
※ Parameters  and range : Refer to 5.3.9 Set DTV Parameter.  
 
(3) Description  
 Get DTV Parameter.  
 Even if Data 2 -5 is set to Disable, the parameter read value will read the set value. 
(Value of parameters set as default cannot be read.)  
 Each parameter is 32bit. Refer to the following table about the format.  
 Data  Each Parameter  
Data N  Upper  
↑ 
↓ 
Lower  Data N+1  
Data N+2  
Data N+3  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.


--- Page 158 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 158/318  The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV Parameter Command]  
Command(Need ACK)[Set DTV Parameter Response]  
ACK  
Change Baud rate  Change Baud rate


--- Page 159 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 159/318 5.4.9.  Get Program Description  
(1) Get Program Description  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Description (Upper)  
Data 1 :  22h Get Program Description (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID (Lower)  
Data 4 :  Event ID(Upper)  
Data 5 :  Event ID (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Description Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h~CAh  
Header CRC8 :  -- 
Data 0 :  01h Get Program Description (Upper)  
Data 1 :  22h Get Program Description (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Service ID(Upper)  
Data 5 :  Service ID (Lower)  
Data 6 :  Event ID(Upper)  
Data 7 :  Event ID (Lower)  
Data 8 :  Program Description Length  
Data 9 ~:  Program Description  
Data CRC8 :  -- 
 
(3) Description  
 Get the program description.  
 Service ID identify the service in Broadcaster (0x0000~0xFFFF).Event ID identify the 
program (0x0000~0xFFFF).  
 If Service ID and Event ID are 0xFFFF then Get Current Data.  
(Only [ Tuning Status = Tuning])  
 Program Description Length is the length of Program Description (0~192Byte).  
 Program Description is 8bit character code set Format.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.


--- Page 160 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 160/318  The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Description Command]  
Command(Need ACK)[Get Program Description Response]  
ACK  Processing


--- Page 161 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 161/318 5.4.10.  Get DTV System  
(1) Get DTV System  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV System (Upper)  
Data 1 :  23h Get DTV System (Lower)  
Data CRC8 :  -- 
 
(2) Get DTV System Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV System (Upper)  
Data 1 :  23h Get DTV System (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  DTV System  
00h : Dynamic 4Diver System (Fore Br0/1)  
01h : Fixed 2x2Diver System (Fore Br0/1)  
02h : Fixed 2Diver System(Antenna Br2/3)  
03h : Fixed 4Diver System  
04h：Fixed 2Diver System(Antenna Br0/1)  
05h : Fixed 3x1Diver System (Fore Br0/1/2)  
06h : Dynamic 4Diver System (Fore Br2/3)  
07h : Fixed 2x2Diver System (Fore Br2/3)  
08h : Fixed 3x1Diver System (Fore Br1/2/3)  
Data CRC8 :  -- 
 
(3) Description  
 Get DTV System Parameter.  
 F039902182  : response Data 4 : Always return 04h.


--- Page 162 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 162/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get DTV System Command]  
Command(Need ACK)[Get DTV System Response]  
ACK  Processing


--- Page 163 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 163/318 5.4.11.  Get Program List  
(1) Get Program List Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  08h 
Header CRC8 :  -- 
Data 0 :  01h Get Program List (Upper)  
Data 1 :  24h Get Program List (Lower)  
Data 2 :  Year 
Data 3 :  Month  
Data 4 :  Day 
Data 5 :  Service ID(Upper)  
Data 6 :  Service ID (Lower)  
Data CRC8 :  -- 
 
(2) Get Program List Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh 
Data Length :  05h~ FFh  
Header CRC8 :  -- 
Data 0 :  01h Get Program List (Upper)  
Data 1 :  24h Get Program List (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 :  Year 
Data 7 :  Month  
Data 8 :  Day 
Data 9 :  Service ID(Upper)  
Data 10 :  Service ID (Lower)  
Data 11 :  Number of Event  
Data 12 :  Event ID(0) Information (Event ID (Upper))  
Data 13 :  Event ID(0) Information (Event ID (Lower))  
Data 14 :  Event ID(0) Service ID(Upper)  
Data 15 :  Event ID(0) Service ID (Lower)  
Data 16 :  Event ID(0) Information (Hour)  
Data 17 :  Event ID(0) Information (Minute)  
Data 18 :  Event ID(1) Information (Event ID (Upper))  
Data 19:  Event ID(1) Information (Event ID (Lower))  
Data 20 :  Event ID(1) Service ID(Upper)  
Data 21:  Event ID(1) Service ID (Lower)  
Data 22 :  Event ID(1) Information (Hour)  
Data 23:  Event ID(1) Information (Minute)  
 ~ 
Data N*6+12 :  Event ID(N) Information (Event ID (Upper))  
Data N*6+13 :  Event ID(N) Information (Event ID (Lower))  
Data N*6+14 :  Event ID(N) Service ID(Upper)  
Data N*6+15 :  Event ID(N) Service ID (Lower)


--- Page 164 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 164/318 Data N*6+16 :  Event ID(N) Information (Hour)  
Data N*6+17 :  Event ID(N) Information (Minute)  
Data CRC8 :  -- 
(3) Get Program List Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 00 0Dh~ 0175h  
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Program List (Upper)  
Data 1 :  24h Get Program List (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 :  Year 
Data 7 :  Month  
Data 8 :  Day 
Data 9 :  Service ID(Upper)  
Data 10 :  Service ID (Lower)  
Data 11 :  Number of Event  
Data 12 :  Event ID(0) Information (Event ID (Upper))  
Data 13 :  Event ID(0) Information (Event ID (Lower))  
Data 14 :  Event ID(0) Service ID(Upper)  
Data 15 :  Event ID(0) Service ID (Lower)  
Data 16 :  Event ID(0) Information (Hour)  
Data 17 :  Event ID(0) Information (Minute)  
Data 18 :  Event ID(1) Information (Event ID (Upper))  
Data 19:  Event ID(1) Information (Event ID (Lower))  
Data 20 :  Event ID(1) Service ID(Upper)  
Data 21:  Event ID(1) Service ID (Lower)  
Data 22 :  Event ID(1) Information (Hour)  
Data 23:  Event ID(1) Information (Minute)  
 ~ 
Data N*6+12 :  Event ID(N) Information (Event ID (Upper))  
Data N*6+13 :  Event ID(N) Information (Event ID (Lower))  
Data N*6+14 :  Event ID(N) Service ID(Upper)  
Data N*6+15 :  Event ID(N) Service ID (Lower)  
Data N*6+16 :  Event ID(N) Information (Hour)  
Data N*6+17 :  Event ID(N) Information (Minute)  
Data CRC8 :  -- 
 
(4) Description  
 Get the program list.  
 Header Type 1:  
・  “Fragment Number” is the order of the fragmented response. If the length of Data 
Part is 255byte and under, “Fragment Number” is 0. If the length of Data Part is 
over 255byte, it is the order number. The B/E sends the data in actual order.


--- Page 165 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 165/318 ・ “Last Fragment Number” is the max number of “Fragment Number” (0~2).  
 For Header Type 2, Fragment  Numbers - Data 4, Data 5 are set to 00h.  
 “Year” means the year  of Start Time  for all events.(Only low 2-digits ex.2017 -> 17)  
 “Month” means the month  of Start Time  for all events.(Ex. December -> 12)  
 “Day” means the date  of Start Time  for all events.(Ex. 13th -> 13)  
 “Service ID” identify the service in Broadcaster (0x0000~0xFFFF).  
 “Number of Event” means the number of events.(0~ 96) 
 “Event ID” identify the program (0x0000~0xFFFF).  
 “Hour” means the hour  of Start Time .(0~23)  
 “Minute” means the hour  of Start Time .(0~59)  
 B/E doesn’t save EPG Information to NVRAM. If B/E power off, B/E doesn’t have 
EPG Information.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 166 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 166/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program List Command]  
Command(Need ACK)[Get Program List Response]  
ACK  Processing


--- Page 167 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 167/318 5.4.12.  Get Program Name  
(1) Get Program Name Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name (Upper)  
Data 1 :  25h Get Program Name (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID (Lower)  
Data 4 :  Event ID(Upper)  
Data 5 :  Event ID (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Name Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :   05h~  74h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name (Upper)  
Data 1 :  25h Get Program Name (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Service ID(Upper)  
Data 5 :  Service ID (Lower)  
Data 6 :  Event ID(Upper)  
Data 7 :  Event ID (Lower)  
Data 8 :  Year of Start Time  
Data 9 :  Month of Start Time  
Data 10 :  Day of Start Time  
Data 11 :  Hour of Start Time  
Data 12 :  Minute of Start Time  
Data 13 :  Year of End Time  
Data 14 :  Month of End Time  
Data 15 :  Day of End Time  
Data 16 :  Hour of End Time  
Data 17 :  Minute of End Time  
Data 18 :  Program Name Length  
Data 19 ~:  Program Name  
Data CRC8 :  --


--- Page 168 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 168/318 (3) Description  
 Get the program Name  
 “Service ID” identify the service in Broadcaster (0x0000~0xFFFF).  
 “Event ID” identify the program (0x0000~0xFFFF).  
 If Service ID and Event ID are 0xFFFF then Get Current Data.  
(Only [ Tuning Status = Tuning])  
 “Year of Start Time” means the year  of Start Time .(Only low 2-digit ex.2017 ->17) 
 “Month of Start Time” means the month  of Start Time .(Ex. December -> 12)  
 “Day of Start Time” means the date  of Start Time .(Ex. 13th -> 13)  
  “Hour of Start Time” means the hour  of Start Time .(0~23)  
 “Minute of Start Time” means the hour  of Start Time .(0~59)  
 “Year of End Time” means the year  of End Time .(Only low 2-digit ex.2017 ->17) 
 “Month of End Time” means the month  of End Time .(Ex. December -> 12)  
 “Day of End Time” means the date  of End Time .(Ex. 13th -> 13)  
 “Hour of End Time” means the hour  of End Time .(0~23)  
 “Minute of End Time” means the hour  of End Time .(0~59)  
 If End Time is not yet fixed, “Year”/”Month”/”Day”/”Hour”/”Minute” are 0xFF.  
 “Program Name Length” is the length of Program Name (0~96Byte).  
 “Program Name” is 8bit character code set Format.  
 B/E doesn’t save EPG Information to NVRAM. If B/E power off, B/E doesn’t have 
EPG Information.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 169 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 169/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Name Command]  
Command(Need ACK)[Get Program Name Response]  
ACK  Processing


--- Page 170 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 170/318 5.4.13.  Get Logo Data  
(1) Get Logo Data  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data (Upper)  
Data 1 :  26h Get Logo Data (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID (Lower)  
Data 4 :  Logo Type  
Data CRC8 :  -- 
 
(2) Get Logo Data Response (BE ⇒ HOST  ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 0 8h~ 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data (Upper)  
Data 1 :  26h Get Logo Data (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 ~:  Logo Information  
Refer to “ (4)Description ” 
Data CRC8 :  --


--- Page 171 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 171/318 (3) Get Logo Data Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 000 8h~0734h  
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data (Upper)  
Data 1 :  26h Get Logo Data (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 ~:  Logo Information  
Refer to “ (4)Description ” 
Data CRC8 :  -- 
 
(4) Description  
 Get Logo Data.  
 “Logo Type” is :  
Logo 
Type  Kind Height  
[dot] Width  
[dot] Max Size  
[byte]  Format  
0 SD 4:3 Small  24 48 1400 PNG  
1 SD 16:9 Small  24 36 1184  PNG  
2 HD Small  27 48 1508  PNG  
3 SD 4:3 Large  36 72 1832  PNG  
4 SD 16:9 Large  36 54 1508  PNG  
5 HD Large  36 64 1688  PNG  
6 Simple Logo  - - 10byte  
(5characters)  8bit 
character 
code set  
7 Simple Logo  - - 20byte  
(5characters)  UTF-8 
 Only the Logo Types set in DTV Parameter 2 will be available.  
 This will be used for all screens where a logo is displayed.  
 Result (Data 3) will be NG if host request Logo Type not set in DTV Parameter 2.  
 For Header Type 1  
・ “Fragment Number” is the order of the fragmented response. If the length of Data 
Part is 255byte and under, “Fragment Number” is 0. If the length of Data Part is 
over 255byte, it is the order number.  
・ “Last Fragment Number” is the max number of “Fragment Number” (0~ 6). 
 For Header Type 2, Fragment Numbers - Data 4, Data 5 are set to 00h.


--- Page 172 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 172/318  “Logo Information Data” shows the following table.  
Logo Type  
Length of Logo Data  
Logo Data  1byte  
2byte  
n byte  
 If B/E doesn’t receive Logo Data yet, B/E response that “Length of Logo Data” is zero 
and “Logo Data” is empty.  
 Logo PNG Data will be complete  including the  PLTE Chunk data (536 Byte) . 
 Simple Logo examples  
Broadcast  Simple Logo  
NHK総合大阪  ＮＨＫ－Ｇ  
NHK教育大阪  ＮＨＫ－Ｅ  
毎日放送  ＭＢＳ  
朝日放送  ＡＢＣ  
テレビ大阪  ＴＶＯ  
関西テレビ  ＫＴＶ  
読売テレビ  ＹＴＶ  
 
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Logo Type is not 00h ~ 06h.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 173 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 173/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get DTV System Command]  
Command(Need ACK)[Get DTV System Response]  
ACK  Processing


--- Page 174 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 174/318 5.4.14.  Get RMP Maker ID  
(1) Get RMP Maker ID  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Get RMP Maker ID (Upper)  
Data 1 :  29h Get RMP Maker ID (Lower)  
Data 2 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh : Original RMP Maker ID  
Data 3 :  One touch Number  
 00h : Not stored service  
 01h~0Ch : One touch Number  
 FFh : Original RMP Maker ID  
Data CRC8 :  -- 
 
(2) Get RMP Maker ID Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  13h 
Header CRC8 :  -- 
Data 0 :  01h Get RMP Maker ID (Upper)  
Data 1 :  29h Get RMP Maker ID (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Display0 (Upper)  
Data 5 :  Display0 (Lower)  
Data 6 :  Display1 (Upper)  
Data 7 :  Display1 (Lower)  
Data 8 :  Display2 (Upper)  
Data 9 :  Display2 (Lower)  
Data 10 :  Display3 (Upper)  
Data 11 :  Display3 (Lower)  
Data 12 :  Display4 (Upper)  
Data 13 :  Display4 (Lower)  
Data 14 :  Display5 (Upper)  
Data 15 :  Display5 (Lower)  
Data 16 :  Display6 (Upper)  
Data 17 :  Display6 (Lower)  
Data CRC8 :  --


--- Page 175 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 175/318 (3) Description  
 Get RMP Maker ID  
If “Preset No.” = FFh and “One touch No.” = FFh, Return Original RMP Maker ID.  
 How to Display  
If Response values are below.  
Display0 = 1  
Display1 = 2345  
Display2 = 6789  
Display3 = 0123  
Display4 = 4567  
Display5 = 8901  
Display6 = 2345  
 
「1 – 2345 – 6789 – 0123 – 4567 – 8901 – 2345」 
 
If Response values are All 00h: It indicates that it has not been acquired yet.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  One touch Number is invalid (Not registered channel)  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 176 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 176/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get RMP Maker ID  Command]  
Command(Need ACK)[Get RMP Maker ID  Response]  
ACK  Processing


--- Page 177 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 177/318 5.4.15.  Get Number of Program  info 
(1) Get Number of Program info Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  01h Get Number of Program  info (Upper)  
Data 1 :  2Ah Get Number of Program  info (Lower)  
Data 2 :  00h : Home Preset  
01h : Drive Preset  
FEh: Last Channel  
FFh : Last Preset  
Data CRC8 :  -- 
 
(2) Get Number of Program info  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 1Fh or 07h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Number of Program  info (Upper)  
Data 1 :  2Ah Get Number of Program info  (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value   
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Preset no.0 (Not Stored Channel)  (Fullseg)  : Number of 
Program  info 
00h : Not Active  
01h – 08h : Number of Program  info 
FFh : unknown  
 
Data2=FEh Last channel  
Last Channel Fullseg  : Number of Program  info 
00h : Not Active  
01h – 08h : Number of Program  info 
FFh : unknown  
Data 5 :  Preset no.1 (Fullseg)  : Number of Program  info 
00h : Not Active (Not Stored)  
01h – 08h : Number of Program  info 
FFh : unknown  
 
Data2=FEh Last channel  
Last Channel One seg : Number of Program  info 
00h : Not Active  
01h – 08h : Number of Program  info 
FFh : unknown  
Data 6 : Preset no.2 (Fullseg)  : Number of Program  info 
Data 7 : Preset no.3 (Fullseg)  : Number of Program  info 
Data 8 : Preset no.4 (Fullseg)  : Number of Program  info 
Data 9 : Preset no.5 (Fullseg)  : Number of Program  info


--- Page 178 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 178/318 Data 10 :  Preset no.6 (Fullseg)  : Number of Program  info 
Data 1 1 : Preset no.7 (Fullseg) : Number of Program  info 
Data 1 2 : Preset no.8 (Fullseg)  : Number of Program  info 
Data 13 :  Preset no.9 (Fullseg)  : Number of Program  info 
Data 14 :  Preset no.10 (Fullseg)  : Number of Program  info 
Data 15 :  Preset no.11 (Fullseg)  : Number of Program  info 
Data 16 :  Preset no.12 (Fullseg)  : Number of Program  info 
Data 17 :  Preset no.0(Not Stored Channel)  (Oneseg)  : Number of 
Program  info 
00h : Not Active  
01h – 08h : Number of Program  info 
FFh : unknown  
Data 18 :  Preset no.1 (Oneseg)  : Number of Program  info 
00h : Not Active (Not Stored)  
01h – 08h : Number of Program  info 
FFh : unknown  
Data 19 : Preset no.2(Oneseg)  : Number of Program  info 
Data 20 : Preset no.3 (Oneseg)  : Number of Program  info 
Data 21 : Preset no.4 (Oneseg)  : Number of Program  info 
Data 22 : Preset no.5 (Oneseg)  : Number of Program  info 
Data 23 :  Preset no.6 (Oneseg)  : Number of Program  info 
Data 24 :  Preset no.7 (Oneseg) : Number of Program  info 
Data 25 :  Preset no.8 (Oneseg)  : Number of Program  info 
Data 26 :  Preset no.9 (Oneseg)  : Number of Program  info 
Data 27 :  Preset no.10 (Oneseg)  : Number of Program  info 
Data 28 :  Preset no.11 (Oneseg)  : Number of Program  info 
Data 29 :  Preset no.12 (Oneseg)  : Number of Program  info 
Data CRC8 :  -- 
 
(3) Description  
 Get current time Number of programs  per Channel . 
 Number of Program info = FFh : Haven't got current program info yet  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 179 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 179/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Number of Program info  Command]  
Command(Need ACK)[Get Number of Program info  Response]  
ACK  Processing


--- Page 180 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 180/318 5.4.16.  Get Audio ES info 
(1) Get Audio ES info Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES info(Upper)  
Data 1 :  2Bh Get Audio ES info(Lower)  
Data CRC8 :  -- 
 
(2) Get Audio ES info Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 07h ~ FFh  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 : 01h Get Audio ES info(Upper)  
Data 1 :  2Bh Get Audio ES info(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number   
Data 5 :  Last Fragment Number  
Data 6 ~  Audio ES info Data  
Data CRC8 :  -- 
 
(3) Get Audio ES info Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2Bytes) :  Result=OK : 00 07h ~ 0242 h 
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES info(Upper)  
Data 1 :  2Bh Get Audio ES info(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 ~  Audio ES info Data  
Data CRC8 :  --


--- Page 181 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 181/318 (4) Description  
 Get Audio ES  information.  
 For Header Type 1  
・ “Fragment Number” is the order of the fragmented response. If the length of Data 
Part is 255byte and under, “Fragment Number” is 0. If the length of Data Part is 
over 255byte, it is the order number.  
・ “Last Fragment Number” is the max number of “Fragment Number” (0~2).  
 For Header Type 2, Fragmen t Numbers - Data 4, Data 5 are set to 00h.  
・ "Audio ES Info Data" shows the following table.  
Number_of_AudioES_Information(N1)  
for(i = 0; i < N1 ; i++){  
    CompornetTag  
Number_of_Language(N2)  
for(j = 0; j < N2; j++){ 
        language code  
        language text length (N3)  
        language _text [N3]} 
} 1byte  
 
1byte  
1byte  
1byte  
1byte  
1byte  
N3 byte  
・ N1 max  = 15 / N2 max  = 2 / N3 max = 16  
・ Language code :  
Value  Language  
0 Japanese  
1 English  
2 German  
3 French  
4 Italian  
5 Russian  
6 Chinese  
7 Korean  
8 Spanish  
9 Etc 
Foreign language : Language than the above  
Unknown  : Cannot determine one language because multiple 
language is mixed  
・ language Text : Maximum  16 bytes  for 8bit character code set.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.


--- Page 182 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 182/318  Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
05h(Not Support)  The parameter is not supported.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Audio ES info Command]  
Command(Need ACK)[ Get Audio ES info Response]  
ACK  Processing


--- Page 183 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 183/318 5.4.17.  Get Video Resolution  
(1) Get Video Resolution  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Video Resolution(Upper)  
Data 1 :  2Eh Get Video Resolution (Lower)  
Data CRC8 :  -- 
 
(2) Get Video Resolution Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 06h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Video Resolution(Upper)  
Data 1 :  2Eh Get Video Resolution (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Resolution  
00h : 720p  
01h : 480p  
02h : 1080p  
03h : 480i  
04h : 1080p@30Hz  
Data CRC8 :  -- 
 
(3) Description  
 Get Video Output Resolution  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 184 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 184/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Video Resolution  Command]  
Command(Need ACK)[ Get Video Resolution  Response]  
ACK  Processing


--- Page 185 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 185/318 5.4.18.  Get Banner Config  
(1) Get Banner Config Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Banner Config (Upper)  
Data 1 :  30h Get Banner Config (Lower)  
Data CRC8 :  -- 
 
(2) Get Banner Config  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 12h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Banner Config (Upper)  
Data 1 :  30h Get Banner Config (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 : Banner Position X (Upper)  
Data 5 :  Banner Position X (Lower)  
Data 6 :  Banner Position Y (Upper)  
Data 7 :  Banner Position Y (Lower)  
Data 8 :  Font Size  [px] 
Data 9  : Transparency [%]  
Data 10 :  Logo Position Offset  [px] 
Data 11 :  Margin of Top and Bottom  [px] 
Data 12 :  Margin of Left and Right  [px] 
Data 13 :  Line Spacing  [px] 
Data 14 :  Max number of characters  
Data 15 :  Banner segment icon enable 00h /disable 01h  
Data 16 :  Automatic banner display disables   
 enable 00h /disable 01h  
Data CRC8 :  --


--- Page 186 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 186/318 (3) Description  
 Get Banner Configuration  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Banner Config  Command]  
Command(Need ACK)[ Get Banner Config  Response]  
ACK  Processing


--- Page 187 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 187/318 5.4.19.  Get Character Set  
(1) Get Character Set Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Character Set (Upper)  
Data 1 :  32h Get Character Set (Lower)  
Data CRC8 :  -- 
 
(2) Get Character Set  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 06h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Character Set (Upper)  
Data 1 :  32h Get Character Set (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 : Character Set  
00h : ARIB  
01h : UTF -8 
Data CRC8 :  --


--- Page 188 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 188/318 (3) Description  
 Get Character Set  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Character Set  Command]  
Command(Need ACK)[ Get Character Set  Response]  
ACK  Processing


--- Page 189 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 189/318 5.4.20.  Get TS Name  with UTF-8 
(1) Get TS Name  with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Get TS Name  with UTF -8 (Upper)  
Data 1 :  33h Get TS Name with UTF -8(Lower)  
Data 2 :  01h~0Ch : Preset Channel Number  
FFh : All Preset Channel Number  
00h : Not Stored Channel.  
Data 3 :  00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data CRC8 :  -- 
 
(2) Get TS Name  with UTF -8 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 58h ~ 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get TS Name  with UTF -8 (Upper)  
Data 1 :  33h Get TS Name with UTF -8(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value   
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 : 01h~0Ch : Preset Channel Number  
FFh : All Preset Channel Number   
00h : Not Stored Channel.  
Data 7~86 : TS Name  (UTF-8) 
Data 6 is 00h~0Ch:Specified Preset Channel Number  
Data 6 is FFh : Preset Channel Number = 1  
Data 87~ : TS Name (UTF -8) 
  80bytes per Preset Channel Number  
Data CRC8 :  --


--- Page 190 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 190/318 (3) Get TS Name  with UTF -8 Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 00 56h ~  03C8h  
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get TS Name  with UTF -8 (Upper)  
Data 1 :  33h Get TS Name with UTF -8(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
  00h : Fixed Value   
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed value)  
Data 5 :  Last Fragment Number  (00h : Fixed value)  
Data 6 : 01h~0Ch : Preset Channel Number  
FFh : All Preset Channel Number   
00h : Not Stored Channel.  
Data 7~86 : TS Name  (UTF-8) 
Data 6 is 00h~0Ch:Specified Preset Channel Number  
Data 6 is FFh : Preset Channel Number = 1  
Data 87~ : TS Name (UTF -8) 
  80bytes per Preset Channel Number  
Data CRC8 :  -- 
 
(4) Description  
 Get TS Name  with UTF -8. 
 If Preset Channel Number is 01h~0Ch, get TS Name of specified Preset Channel 
and specified Preset Table.  
 If Preset Channel Number is FFh, get All TS Name in specified Preset Table.  
 If Preset Channel Number is 00h, get TS Name of Not Stored Channel.  
 For Header Type 2, Fragmen t Numbers - Data4, Data5 are set to 00h.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 191 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 191/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get TS Name  with UTF -8 Command]  
Command(Need ACK)[Get TS Name  with UTF -8 Response]  
ACK  Processing


--- Page 192 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 192/318 5.4.21.  Get Program Information  with UTF -8 
(1) Get Program Information  with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Information  with UTF -8 (Upper)  
Data 1 :  34h Get Program Information with UTF -8 (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Information Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result = OK: 08h~FFh  
Result = NG: 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Information  with UTF -8 (Upper)  
Data 1 :  34h Get Program Information with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 : Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 7 : 00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 8 : Three Digit Number(Upper)  
Data 9 : Three Digit Number(Lower)  
Data 10 : Branch Identifier Number  
Data 11 : Length of Station Name(N1) : 00h~ 50h 
Data 12~(11+N1) : Station Name(TS Name  with UTF -8) 
Data 12+N1 :  Length of Program Name(N2)(Upper) : 00h~180h  
Data 13+N1  Length of Program Name(N2)(Lower) : 00h~180h  
Data 
14+N1~13+N1+N2:  Program Name with UTF -8 
Data CRC8 :  --


--- Page 193 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 193/318 (3) Get Program Information Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result = OK: ~01D4h  
Result =  NG: 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Information  with UTF -8 (Upper)  
Data 1 :  34h Get Program Information with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 : Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 7 : 00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 8 : Three Digit Number(Upper)  
Data 9 : Three Digit Number(Lower)  
Data 10 : Branch Identifier Number  
Data 11 : Length of Station Name(N1) : 00h~ 50h 
Data 12~(11+N1) : Station Name(TS Name  with UTF -8) 
Data 12+N1 :  Length of Program Name(N2) (Upper)  : 00h~ 180h 
Data 13+N1  Length of Program Name(N2)(Lower) : 00h~1 80h 
Data 
14+N1~13+N1+N2:  Program Name with UTF -8 
Data CRC8 :  -- 
 
(4) Description  
 Get the program information in current service.  
 The program information contains Preset Channel Number Station Name / Program 
name).  
 Preset Channel Number ( Data7 ) of Response is current playback channel. If current 
playback channel is not stored, Data7 is 00h and Data6 is FFh.  
 Three Digit Number & Branch Identifier Number of Response are current playback 
service. If current playback channel is not stored, these data are set.  
 If B/E doesn’t have Program name, Length of Program Name is set to 0.  
 For Header Type 2, Fragment  Numbers - Data4, Data5 are set to 00h.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.


--- Page 194 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 194/318  The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Information  with 
UTF -8 Command]  
Command(Need ACK)[Get Program Information  with UT
F-8 Response]  
ACK  Processing


--- Page 195 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 195/318 5.4.22.  Get DTV Parameter  2 
(1) Get DTV Parameter  2 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get DTV Parameter  2 (Upper)  
Data 1 :  36h Get DTV Parameter  2 (Lower)  
Data CRC8 :  -- 
 
(2) Get DTV Parameter 2 Response (BE ⇒ HOST)  
 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : E5h  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 : 01h Get DTV Parameter  2 (Upper)  
Data 1 :  36h Get DTV Parameter  2 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Enable  / Disable  
01h : Enable Parameter  
00h : Disable  Parameter (Use Default Parameter)  
Data 5 :  Auto tune mode default  
00h:Auto  
01h:Fullseg  
02h:Oneseg  
03h:Auto with Seamless  
Data 6:  Default Character Set  
00h : ARIB  
01h : UTF -8 
Data 7 :  Default Video Resolution  
00h :720p  
01h : 480p  
02h : 1080p  
03h : 480i  
04h : 1080p@30Hz  
Data 8 :  Closed Caption display over BML browser  
00h : Enable Display  
01h : Disable Display  
Data 9 :  BML Error Message  
00h : Enable Display  
01h : Disable Display  
Data 10 :  Receive Logo Type  
Bit0 : Logo Type 0  
Bit1 : Logo Type 1  
Bit2 : Logo Type 2


--- Page 196 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 196/318 Bit3 : Logo Type 3  
Bit4 : Logo Type 4  
Bit5 : Logo Type 5  
Bit6/Bit7 : Fix 0  
 
0 : Receive  
1 : Not Receive  
Data 11 :  Search Detection Timeout  
Data 12 ~ 13:  C/N for Receive Error Detection for Fix Fullseg mode  
Data 14 ~ 15:  C/N for Preset Scan Detection for Fix Oneseg mode and Auto 
mode  
Data 16 ~ 17:  C/N for Preset Scan Detection for Fix Fullseg mode  
Data 18 :  Timeout for Preset Scan per channel  
Data 19 ~ 20 :  C/N Level 3 threshold     
Data 21 ~ 22 :  C/N Level 2 threshold    
Data 23 ~ 24 :  C/N Level 1 threshold    
Data 25 ~ 26 :  EPG Update scan time / channel 1 to 180[s]  
Data 27 :  EPG Scan Number of Days  
Data 28 ~ 29 :  EPG Scan Signal  Threshold    
Data 30 ~ 31 :  Audio Const offset for Fullseg  
Data 32 ~ 33 :  Audio Const offset for Oneseg  
Data 34 :  Event relay  : Auto Event  relay On/Off  
Data 35 :  Event relay  : Notification interval  before switching  [s] 
Data 36 :  Event relay  : Number of notifications  before switching  [times]  
Data 37 ~ 38  Banner:  Banner Position X  
Data 39 ~ 40  Banner: Banner Position Y  
Data 41 :  Banner:  Font Size [px] 
Data 42 :  Banner:  Transparency [%]  
Data 43 :  Banner:  Logo Position Offset  [px] 
Data 44 :  Banner:  Margin of Top and Bottom [px] 
Data 45 :  Banner:  Margin of Left and Right [px] 
Data 46 :  Banner:  Line spacing  [px] 
Data 47 :  Banner:  Max number of characters  
Data 48 :  Banner:  Default Banner Timeout [s]  
Data 49 :  EPG  List Type Enable  
Bit0 : List Type 1 Enable  
Bit1 : List Type 2 Enable  
Bit2 : List Type 3 Enable  
Bit3 : List Type 4 Enable  
Data 50 :  EPG List: Type1 Program name Font Size  [px] 
Data 51 :  EPG List:  Type1 TS Name Font Size  [px] 
Data 52 :  EPG List: Type1 EPG Content Font Size  [px] 
Data 53 :  EPG List: Type2 Program name Font Size  [px] 
Data 54 :  EPG List:  Type2 TS Name Font Size  [px] 
Data 55 :  EPG List:  Type2 EPG Content Font Size  [px] 
Data 56 :  EPG List:  Type3 Program name Font Size  [px] 
Data 57 :  EPG List:  Type3 TS Name Font Size  [px] 
Data 58 :  EPG List:  Type3 EPG Content Font Size  [px] 
Data 59 :  EPG List:  Type4 Program name Font Size  [px] 
Data 60 :  EPG List:  Type4 TS Name Font Size  [px] 
Data 61 :  EPG List:  Type4 EPG Content Font Size  [px] 
Data 62 :  EPG List:  Table  Title Color Red  
Data 63 :  EPG List:  Table  Title Color Green  
Data 64 :  EPG List:  Table  Title Color Blue  
Data 65 :  EPG List:  Table  Title Font Color Red  
Data 66 :  EPG List:  Table  Title Font Color Green  
Data 67 :  EPG List:  Table  Title Font Color Blue  
Data 68 :  EPG List:  Cursor Color Red


--- Page 197 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 197/318 Data 69 :  EPG List:  Cursor Color Green  
Data 70 :  EPG List:  Cursor Color Blue  
Data 71 :  EPG List:  Cursor Font Color Red  
Data 72 :  EPG List: Cursor Font Color Green  
Data 73 :  EPG List:  Cursor Font Color Blue  
Data 74 :  EPG List:  Current Program Color Red  
Data 75 :  EPG List:  Current Program Color Green  
Data 76 :  EPG List:  Current Program Color Blue  
Data 77 :  EPG List:  Current Program Font Color Red  
Data 78 :  EPG List:  Current Program Font Color Green  
Data 79 :  EPG List:  Current Program Font Color Blue  
Data 80 :  EPG List:  Balloon  color Red  
Data 81 :  EPG List:  Balloon  color Green  
Data 82 :  EPG List:  Balloon  color Blue  
Data 83 :  EPG List:  Balloon  Font color Red  
Data 84 :  EPG List:  Balloon  Font color Green  
Data 85 :  EPG List:  Balloon  Font color Blue  
Data 86 :  EPG List:  Border line color Red  
Data 87 :  EPG List:  Border line color Green  
Data 88 :  EPG List: Border line color Blue 
Data 89 :  EPG Information:  Font Size  [px] 
Data 90 :  EPG Information:  Title Font Color Red  
Data 91 :  EPG Information:  Title Font Color Green  
Data 92 :  EPG Information:  Title Font Color Blue  
Data 93 :  EPG Information: Line Spacing for Title  
Data 94 :  EPG Information:  Line Spacing for Contents  
Data 95 :  EPG Information:  Margin  
Data 96 :  Default Auto Broadcast Search Mode  
Data 97~98 :  C/N Level 3 threshold for one seg    
Data 99~100 :  C/N Level 2 threshold  for one seg   
Data 101~102 : :  C/N Level 1 threshold  for one seg   
Data 103:  Default event mask 0  
Data 104:  Default event mask 1  
Data 105:  Default event mask 2  
Data 106:  EPG List:  Short program border line color Red  
Data 107: EPG List:  Short program border line color Green  
Data 108:  EPG List:  Short program border line color Blue  
Data 109:  Banner: Banner segment icon  
00h:Enable  
01h:D isable  
Data 110:  Number of scrolling line on EPG detail ( 01h~ 
Data 111:  Automatic banner display enable   
 enable 00h /disable 01h  
Data 11 2~ 227 :  Reserved  
Data CRC8 :  -- 
※ Parameters  and range : Refer to 5.3. 16 Set DTV Parameter  2. 
 
(3) Description  
 Get DTV Parameter.  
 Each parameter is big endian.  
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:


--- Page 198 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 198/318  Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set DTV Parameter  2 Command]  
Command(Need ACK)[Set DTV Parameter  2 Response]  
ACK


--- Page 199 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 199/318 5.4.23.  Get Service Information  with UTF -8 
(1) Get Service Information  with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  01h Get Service Information with UTF -8 (Upper)  
Data 1 :  37h Get Service Information with UTF -8 (Lower)  
Data 2 :  Preset Table  
00h : Home Preset  
01h : Drive Preset  
FFh : Last Preset  
Data 3 :  One Touch Number  
01h ~ 0Ch : Service Information of Specified Channel  
00h : Service Information of Not Stored Channel.  
FFh : Service Information of All Channel.  
Data CRC8 :  -- 
 
(2) Get Service Information with UTF -8 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 08h~  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Service Information with UTF -8 (Upper)  
Data 1 :  37h Get Service Information with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6~ :  Service_Information_Data  
Refer to “ (4) Description ” 
Data CRC8 :  --


--- Page 200 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 200/318 (3) Get Service Information with UTF -8 Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 0008h~  0FFFh 
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Service Information with UTF -8 (Upper)  
Data 1 :  37h Get Service Information with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6~ :  Service_Information_Data  
Refer to “ (4) Description ” 
Data CRC8 :  -- 
 
(4) Description  
 Get Service Information.  
 If One Touch Number (Data3) of Command is FFh, B/E response the service 
information of all channels. If One Touch Number (Data3) of Command is  00h, B/E 
response the service information of not -stored channel. If One Touch Number (Data3) 
is 01h~0Ch, B/E response the service information of specified channel.  
 For Header Type 1   
・ “Fragment Number” is the order of the fragmented response. If the length of Data 
Part is 255byte and under, “Fragment Number” is 0. If the length of Data Part is 
over 255byte, it is the order number. The B/E sends the data in actual order.  
・ “Last Fragment Number” is the max number of “Fragment Number”.  
 For Header Type 2  
・ “Fragment Number” is the order of the fragmented response. If the length of Data 
Part is 4095byte and under, “Fragment Number” is 0. If the length of Data Part is 
over 4095byte, it is the order number. The B/E sends the data in actual order.  
・ “Last Fragment Number” is the max number of “Fragment Number”.  
 “Service Information Data” shows the following table.  
Number_of_TS_Information(N1)  
for(i = 0; i < N1 ; i++){  
OneTouchNumber  
Number_of_Service_Information(N2)  
for(j = 0; j < N2; j++){  
        Service_Information()  
} 
} 1byte  
 
1byte  
1byte  
 
n byte  
 “Number_of_TS_Information” is the number of the followings TS Information. The


--- Page 201 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 201/318 range is 00h~0Ch.  
 “OneTouchNumber” is valid one touch number. The range is 00h~0Ch  
 “Number_of_Service_Information” is the number of the followings 
Service_Information(). The range of “Number_of_Service_Information” is 00h~17h.  
 The format of “Service_Information()” shows the following table.  
Field  Size Value  
Three Digit Number  2Byte  011~  
Service ID  2Byte  0x0000~0xFFFF  
Branch Identifier Number  1Byte  0~9 
Media Type  1Byte  0 : Full Seg Service  
1 : Data Service(Not Support)  
2 : Data Service(Not Support)  
3 : One Seg Service  
Service Name Length  1Byte  00h ~ 50h 
Service Name  0~80Bytes  UTF-8 
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 202 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 202/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Service  Information  with UTF -
8 Command]  
Command(Need ACK)[Get Service  Information  with UTF -
8 Response]  
ACK  Processing


--- Page 203 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 203/318 5.4.24.  Get Program Description  with UTF -8 
(1) Get Program Descriptio n with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Description with UTF -8 (Upper)  
Data 1 :  38h Get Program Description with UTF -8 (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID (Lower)  
Data 4 :  Event ID(Upper)  
Data 5 :  Event ID (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Description with UTF -8 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result OK : 08h~FFh  
Result  NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Description with UTF -8 (Upper)  
Data 1 :  38h Get Program Description with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 : Service ID(Upper)  
Data 7 : Service ID (Lower)  
Data 8 : Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Program Description Length (Upper)  
Data 11 :  Program Description Length (Lower)  
Data 12 ~:  Program Description  
Data CRC8 :  --


--- Page 204 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 204/318 (3) Get Program Description with UTF -8 Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result OK : ~030Dh  
Result NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Description with UTF -8 (Upper)  
Data 1 :  38h Get Program Description with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 : Service ID(Upper)  
Data 7 : Service ID (Lower)  
Data 8 : Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Program Description Length (Upper)  
Data 11 :  Program Description Length (Lower)  
Data 12 ~:  Program Description  
Data CRC8 :  -- 
 
(4) Description  
 Get the program description.  
 Service ID identify the service in Broadcaster (0x0000~0xFFFF).Event ID identify the 
program (0x0000~0xFFFF).  
 If Service ID and Event ID are 0xFFFF then Get Current Data.  
(Only [ Tuning Status = Tuning])  
  Program Description Length is the length of Program Description  (Max : 19 2Byte s 
× 4). 
 Program Description is UTF-8 character code set Format.  
 For Header Type 2, Fragment  Numbers - Data4, Data5 are set to 00h.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.


--- Page 205 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 205/318 04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Description  
with  UTF -8 Command]  
Command(Need ACK)[Get Program Description  
with  UTF -8 Response]  
ACK  Processing


--- Page 206 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 206/318 5.4.25.  Get Program Name  with UTF -8 
(1) Get Program Name with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 (Upper)  
Data 1 :  39h Get Program Name with UTF -8 (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID (Lower)  
Data 4 :  Event ID(Upper)  
Data 5 :  Event ID (Lower)  
Data CRC8 :  -- 
 
(2) Get Program Name with UTF -8 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :   Result = OK : 08h~FFh  
 Result = NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 (Upper)  
Data 1 :  39h Get Program Name with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 : Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 :  Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Year of Start Time  
Data 11 :  Month of Start Time  
Data 12 :  Day of Start Time  
Data 13 :  Hour of Start Time  
Data 14 :  Minute of Start Time  
Data 15 :  Year of End Time  
Data 16 :  Month of End Time  
Data 17 :  Day of End Time  
Data 18 :  Hour of End Time  
Data 19 :  Minute of End Time  
Data 20 :  Program Name Length (Upper)  
Data 21 :  Program Name Length (Lower)  
Data 22 ~:  Program Name  
Data CRC8 :  --


--- Page 207 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 207/318 (3) Get Program Name with UTF -8 Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :   Result = OK : ~ 0197h  
 Result = NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 (Upper)  
Data 1 :  39h Get Program Name with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h :  Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 : Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 :  Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Year of Start Time  
Data 11 :  Month of Start Time  
Data 12 :  Day of Start Time  
Data 13 :  Hour of Start Time  
Data 14 :  Minute of Start Time  
Data 15 :  Year of End Time  
Data 16 :  Month of End Time  
Data 17 :  Day of End Time  
Data 18 :  Hour of End Time  
Data 19 :  Minute of End Time  
Data 20 :  Program Name Length (Upper)  
Data 21 :  Program Name Length (Lower)  
Data 22 ~:  Program Name  
Data CRC8 :  --


--- Page 208 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 208/318 (4) Description  
 Get the program description.  
 “Service ID” identify the service in Broadcaster (0x0000~0xFFFF).  
 “Event ID” identify the program (0x0000~0xFFFF).  
 If Service ID and Event ID are 0xFFFF then Get Current Data.  
(Only [ Tuning Status = Tuning])  
 “Year of Start Time” means the year  of Start Time .(Only low 2-digit ex.2017 ->17) 
 “Month of Start Time” means the month  of Start Time .(Ex. December -> 12)  
 “Day of Start Time” means the date  of Start Time .(Ex. 13th -> 13)  
  “Hour of Start Time” means the hour  of Start Time .(0~23)  
 “Minute of Start Time” means the hour  of Start Time .(0~59)  
 “Year of End Time” means the year  of End Time .(Only low 2-digit ex.2017 ->17) 
 “Month of End Time” means the month  of End Time .(Ex. December -> 12)  
 “Day of End Time” means the date  of End Time .(Ex. 13th -> 13)  
 “Hour of End Time” means the hour  of End Time .(0~23)  
 “Minute of End Time” means the hour  of End Time .(0~59)  
 If End Time is not yet fixed, “Year”/”Month”/”Day”/”Hour”/”Minute” are 0xFF.  
 “Program Name Length” is the length of Program Name (0~96Byte  × 3 × 4). 
 “Program Name” is UTF-8 character code set Format.  
 B/E doesn’t save EPG Information to NVRAM. If B/E power off, B/E doesn’t have 
EPG Information.  
 For Header Type 2, Fragment  Numbers - Data 4, Data5 are set to  00h. 
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  Service ID is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 209 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 209/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Name  
with  UTF -8 Command]  
Command(Need ACK)[Get Program Name  
with UTF -8 Response]  
ACK  Processing


--- Page 210 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 210/318 5.4.26.  Get Audio ES info with UTF -8 
(1) Get Audio ES info with UTF -8 Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES info with UTF -8 (Upper)  
Data 1 :  3Ah Get Audio ES info with UTF -8 (Lower)  
Data CRC8 :  -- 
 
(2) Get Audio ES info with UTF -8 Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 07h ~ FFh  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES info with UTF -8 (Upper)  
Data 1 :  3Ah Get Audio ES info with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 ~  Audio ES info Data  
Data CRC8 :  -- 
 
(3) Get Audio ES info with UTF -8 Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 00 07h ~ 07E2 h 
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Audio ES info with UTF -8 (Upper)  
Data 1 :  3Ah Get Audio ES info with UTF -8 (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 ~  Audio ES info Data  
Data CRC8 :  --


--- Page 211 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 211/318 (4) Description  
 Get Audio ES  information.  
・ "Audio ES Info Data" shows the following table.  
Number_of_ AudioES _Information(N1)  
for(i = 0; i < N1 ; i++){  
    CompornetTag  
Number_of_Language(N2)  
for(j = 0; j < N2; j++){  
        language code  
        language text length (N3)  
        language  text[N3] 
} 
} 1byte  
 
1byte  
1byte  
1byte  
1byte  
1byte  
N3 byte  
・ N1 max = 15 / N2 max = 2  / N3 max = 64 
・ Language code :  
Value  Language  
0 Japanese  
1 English  
2 German  
3 French  
4 Italian  
5 Russian  
6 Chinese  
7 Korean  
8 Spanish  
9 Etc 
Foreign language : Language than the above  
Unknown : Cannot determine one language because multiple 
language s are mixed  
・ language Text : Maximum  16*4 bytes  for UTF -8 
・ For Header Type 2, Fragment  Numbers - Data4, Data5 are set to 00h.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
05h(Not Support)  The parameter is not supported.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 212 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 212/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Audio ES info with  UTF -8 
Command]  
Command(Need ACK)[ Get Audio ES info with  UTF -8  
Response]  
ACK  Processing


--- Page 213 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 213/318 5.4.27.  Get User ID  
(1) Get User ID Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get User ID (Upper)  
Data 1 :  3Ch Get User ID (Lower)  
Data CRC8 :  -- 
 
(2) Get User ID  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 06h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get User ID (Upper)  
Data 1 :  3Ch Get User ID (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  User ID  
01h to 06 h or FFh  
Data CRC8 :  -- 
 
(3) Description  
 Get Current User ID  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 214 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 214/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get User ID  Command]  
Command(Need ACK)[ Get User ID  Response]  
ACK  Processing


--- Page 215 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 215/318 5.4.28.  Get EPG Config  
(1) Get EPG Config Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get EPG Config (Upper)  
Data 1 :  3Eh Get EPG Config (Lower)  
Data CRC8 :  -- 
 
(2) Get EPG Config  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 38h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get EPG Config (Upper)  
Data 1 :  3Eh Get EPG Config (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  EPG List Type Enable  
Bit0 : Type 1 Enable  
Bit1 : Type 2 Enable  
Bit2 : Type 3 Enable  
Bit3 : Type 4 Enable  
Data 5 :  EPG List: Type1 Program name Font Size  [px] 
Data 6 :  EPG List:  Type1 TS Name Font Size  [px] 
Data 7 :  EPG List:  Type1 EPG Content Font Size  [px] 
Data 8 :  EPG List:  Type2 Program name Font Size  [px] 
Data 9 :  EPG List:  Type2 TS Name Font Size  [px] 
Data 10 :  EPG List:  Type2 EPG Content Font Size  [px] 
Data 11 :  EPG List:  Type3 Program name Font Size  [px] 
Data 12 :  EPG List:  Type3 TS Name Font Size  [px] 
Data 13 :  EPG List:  Type3 EPG Content Font Size  [px] 
Data 14 :  EPG List:  Type4 Program name Font Size  [px] 
Data 15 :  EPG List:  Type4 TS Name Font Size  [px] 
Data 16 :  EPG List:  Type4 EPG Content Font Size  [px] 
Data 17 :  EPG List:  Table Title Color Red  
Data 18 :  EPG List:  Table Title Color Green  
Data 19 :  EPG List:  Table Title Color Blue  
Data 20 :  EPG List:  Table Title Font Color Red  
Data 21 :  EPG List:  Table Title Font Color Green  
Data 22 :  EPG List:  Table Title Font Color Blue  
Data 23 :  EPG List:  Cursor Color Red  
Data 24 :  EPG List:  Cursor Color Green  
Data 25 :  EPG List:  Cursor Color Blue  
Data 26 :  EPG List:  Cursor Font Color Red  
Data 27 :  EPG List:  Cursor Font Color Green  
Data 28 :  EPG List:  Cursor Font Color Blue


--- Page 216 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 216/318 Data 29 :  EPG List:  Current Program Color Red  
Data 30 :  EPG List:  Current Program Color Green  
Data 31 :  EPG List:  Current Program Color Blue  
Data 32 :  EPG List:  Current Program Font Color Red  
Data 33 :  EPG List: Current Program Font Color Green  
Data 34 :  EPG List: Current Program Font Color Blue  
Data 35 :  EPG List: Balloon color Red  
Data 36 :  EPG List: Balloon color Green  
Data 37 :  EPG List: Balloon color Blue  
Data 38 :  EPG List: Balloon Font color Red  
Data 39 :  EPG List: Balloon Font color Green  
Data 40 :  EPG List: Balloon Font color Blue  
Data 41 :  EPG List: Border line color Red  
Data 42 :  EPG List: Border line color Green  
Data 43 :  EPG List: Border line color Blue  
Data 44 :  EPG Information:  Font Size  [px] 
Data 45 :  EPG Information:  Title Font Color Red  
Data 46 :  EPG Information:  Title Font Color Green  
Data 47 :  EPG Information:  Title Font Color Blue  
Data 48 :  EPG Information:  Line Spacing for Title  
Data 49 :  EPG Information:  Line Spacing for Contents  
Data 50 :  EPG Information:  Margin(Applied to all four sides)  
Data 51 : EPG List: Short program border line color Red  
Data 52 : EPG List: Short program border line color Green  
Data 53 : EPG List: Short program border line color Blue  
Data 54 :  Number of scrolling line on EPG detail ( 01h~ 
Data CRC8 :  -- 
 
 
(3) Description  
 Get EPG Configuration  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 217 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 217/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get EPG Config  Command]  
Command(Need ACK)[ Get EPG Config  Response]  
ACK  Processing


--- Page 218 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 218/318 5.4.29.  Get Video Color  
(1) Get Video Color  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Video Color (Upper)  
Data 1 :  40h Get Video Color  (Lower)  
Data CRC8 :  -- 
 
(2) Get Video Color  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 0Ah 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Video Color (Upper)  
Data 1 :  40h Get Video Color (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Brightness   
-127(81h) – 127(7Fh)  
Data 5 :  Contrast  
0 – 7 
Data 6～8: Reserved   
Data CRC8 :  --


--- Page 219 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 219/318 (3) Description  
 Get Video Color  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Video Color  Command]  
Command(Need ACK)[ Get Video Color  Response]  
ACK  Processing


--- Page 220 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 220/318 5.4.30.  Get Event Mask  
(1) Get Event Mask Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Event Mask (Upper)  
Data 1 :  42h Get Event Mask (Lower)  
Data CRC8 :  -- 
 
(2) Get Ev ent Mask  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 08h 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Event Mask (Upper)  
Data 1 :  42h Get Event Mask (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  bit0 : DTV Status  
bit1 : Scan Status  
bit2 : Search Status  
bit3 : DTV Event  
bit4 : EWS Event  
bit5 : EPG Status  
bit6 : Event relay  
bit7 : Number of Program info  
 
0 : Not Mask  
1 : Mask  - Disables the event notification.  
Data 5 :  bit0 : Program Information  
bit1 : Program Information  with UTF -8 
bit2 : TS Name Update  
bit3 : TS Name Update  with UTF -8 
bit4 : Logo Update  
bit5 : EGP Button Status  
bit6 : BML Error  
bit7 : C/N Information  
 
0 : Not Mask  
1 : Mask  - Disables the event notification.  
Data 6 :  bit0 :  EPG Scan Result  
bit1 – 7 Reserve  
 
0 : Not Mask  
1 : Mask - Disables the event notification.  
Data CRC8 :  --


--- Page 221 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 221/318 (3) Description  
 Get Event Mask  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ Get Event Mask  Command]  
Command(Need ACK)[ Get Event Mask  Response]  
ACK  Processing


--- Page 222 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 222/318 5.4.31.  Get Part Number  
(1) Get Part Number  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  01h Get Part Number (Upper)  
Data 1 :  43h Get Part Number (Lower)  
Data CRC8 :  -- 
 
(2) Get Part Number Response  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 1Dh 
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Part Number (Upper)  
Data 1 :  43h Get Part Number (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  BOSCH PN 1  
Data 5 :  BOSCH PN 2  
Data 6 :  BOSCH PN 3  
Data 7 :  BOSCH PN 4  
Data 8 :  BOSCH PN 5  
Data 9 :  BOSCH PN 6  
Data 10 :  BOSCH PN 7  
Data 11 :  BOSCH PN 8  
Data 12 :  BOSCH PN 9  
Data 13 :  BOSCH PN 10  
Data 14 :  BOSCH PN 11  
Data 15 :  BOSCH PN 12  
Data 16 :  Module PN 1  
Data 17 :  Module PN 2  
Data 18 :  Module PN 3  
Data 19 :  Module PN 4  
Data 20 :  Module PN 5  
Data 21 :  Module PN 6  
Data 22 :  Module PN 7  
Data 23 :  Module PN 8  
Data 24 :  Module PN 9  
Data 25 :  Module PN 10  
Data 26 :  Module PN 11  
Data 27 :  Module PN 12  
Data CRC8 :  --


--- Page 223 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 223/318 (3) Description  
 Get Part Number . 
 The format is ASCII.(Ex. “TRH231BS0000 ”) 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Part Number  Command]  
Command(Need ACK)[Get Part Number  Response]  
ACK  Processing


--- Page 224 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 224/318 5.4.32.  Get Program Name  by 3Digit Number  
(1) Get Program Name by 3Digit Number Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name by 3Digit Number (Upper)  
Data 1 :  44h Get Program Name by 3Digit Number (Lower)  
Data 2 :  Preset  
00h : Home Preset  
01h : Drive Preset  
Data 3 :  Three Digit Number(Upper)  
Data 4 :  Three Digit Number(Lower)  
Data 5 :  Branch Identifier Number  
Data CRC8 :  -- 
 
(2) Get Program Name by 3Digit Number Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :   05h~ 74h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name by 3Digit Number (Upper)  
Data 1 :  44h Get Program Name by 3Digit Number (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Service ID(Upper)  
Data 5 :  Service ID (Lower)  
Data 6 :  Event ID(Upper)  
Data 7 :  Event ID (Lower)  
Data 8 :  Year of Start Time  
Data 9 :  Month of Start Time  
Data 10 :  Day of Start Time  
Data 11 :  Hour of Start Time  
Data 12 :  Minute of Start Time  
Data 13 :  Year of End Time  
Data 14 :  Month of End Time  
Data 15 :  Day of End Time  
Data 16 :  Hour of End Time  
Data 17 :  Minute of End Time  
Data 18 :  Program Name Length  
Data 19 ~: Program Name  
Data CRC8 :  -- 
 
(3) Description  
 Get the Current program Name  
 “Service ID” identify the service in Broadcaster (0x0000~0xFFFF).  
 “Event ID” identify the program (0x0000~0xFFFF).


--- Page 225 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 225/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  3Digit Number is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Name  by 3Digit 
Number  Command]  
Command(Need ACK)[Get Program Name  by 3Digit N
umber  Response]  
ACK  Processing


--- Page 226 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 226/318 5.4.33.  Get Program Name  with UTF -8 by 3Digit Number  
(1) Get Program Name with UTF -8 by 3Digit Number Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  07h 
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 by 3Digit Number 
(Upper)  
Data 1 :  45h Get Program Name with UTF -8 by 3Digit Number 
(Lower)  
Data 2 :  Preset  
00h : Home Preset  
01h : Drive Preset  
Data 3 :  Three Digit Number(Upper)  
Data 4 :  Three Digit Number(Lower)  
Data 5 :  Branch Identifier Number  
Data CRC8 :  -- 
 
(2) Get Program Name with UTF -8 by 3Digit Number Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 08h~FFh  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 by 3Digit Number 
(Upper)  
Data 1 :  45h Get Program Name with UTF -8 by 3Digit Number 
(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 :  Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Year of Start Time  
Data 11 :  Month of Start Time  
Data 12 :  Day of Start Time  
Data 13 :  Hour of Start Time  
Data 14 :  Minute of Start Time  
Data 15 :  Year of End Time  
Data 16 :  Month of End Time  
Data 17 : Day of End Time  
Data 18 :  Hour of End Time  
Data 19 :  Minute of End Time  
Data 20 :  Program Name Length (Upper)  
Data 21 :  Program Name Length (Lower)  
Data 22 ~:  Program Name


--- Page 227 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 227/318 Data CRC8 :  -- 
(3) Get Program Name with UTF -8 by 3Digit Number Response (BE ⇒ HOST  with Header Type 
2) 
Start Sync :  A5h,59h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 0017h ~ 0197h  
Result=NG : 0005h  
Header CRC8 :  -- 
Data 0 :  01h Get Program Name with UTF -8 by 3Digit Number 
(Upper)  
Data 1 :  45h Get Program Name with UTF -8 by 3Digit Number 
(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  (00h : Fixed Value)  
Data 5 :  Last Fragment Number  (00h : Fixed Value)  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 :  Event ID(Upper)  
Data 9 :  Event ID (Lower)  
Data 10 :  Year of Start Time  
Data 11 :  Month of Start Time  
Data 12 :  Day of Start Time  
Data 13 :  Hour of Start Time  
Data 14 :  Minute of Start Time  
Data 15 :  Year of End Time  
Data 16 :  Month of End Time  
Data 17 :  Day of End Time  
Data 18 :  Hour of End Time  
Data 19 :  Minute of End Time  
Data 20 :  Program Name Length  (Upper)  
Data 21 :  Program Name Length (Lower)  
Data 22 ~:  Program Name  
Data CRC8 :  -- 
(4) Description  
 Get the Current program description.  
 “Service ID” identify the service in Broadcaster (0x0000~0xFFFF).  
 “Event ID” identify the program (0x0000~0xFFFF).  
 “Program Name” is UTF -8 character code set Format.  
 For Header Type 2, Fragment  Numbers - Data4, Data5 are set to 00h.  
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:


--- Page 228 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 228/318  Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
02h(Invalid Data)  Event ID is invalid.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  3Digit Number is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Program Name  
with  UTF -8 by 3Digit Number Command]  
Command(Need ACK)[Get Program Name  
with UTF -8 by 3Digit Number  Response]  
ACK  Processing


--- Page 229 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 229/318 5.4.34.  Get Logo Data by 3Digit Number  
(1) Get Logo Data  by 3Digit Number Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  08h 
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data by 3Digit Number (Upper)  
Data 1 :  46h Get Logo Data by 3Digit Number (Lower)  
Data 2 :  Preset  
00h : Home Preset  
01h : Drive Preset  
Data 3 :  Three Digit Number(Upper)  
Data 4 :  Three Digit Number(Lower)  
Data 5 :  Branch Identifier Number  
Data 6 :  Logo Type  
Data CRC8 :  -- 
 
(2) Get Logo Data by 3Digit Number Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result=OK : 08h~FFh  
Result=NG : 05h  
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data by 3Digit Number (Upper)  
Data 1 :  46h Get Logo Data by 3Digit Number (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number  
Data 5 :  Last Fragment Number  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 ~:  Logo Information  
Refer to “ (4)Description ” 
Data CRC8 :  --


--- Page 230 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 230/318 (3) Get Logo Data by 3Digit Number Response (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  Result=OK : 0008h~0734h  
Result=NG : 0005h 
Header CRC8 :  -- 
Data 0 :  01h Get Logo Data by 3Digit Number (Upper)  
Data 1 :  46h Get Logo Data by 3Digit Number (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Fragment Number (00h : Fixed Value)  
Data 5 :  Last Fragment Number (00h : Fixed Value)  
Data 6 :  Service ID(Upper)  
Data 7 :  Service ID (Lower)  
Data 8 ~:  Logo Information  
Refer to “ (4)Description ” 
Data CRC8 :  -- 
 
(4) Description  
 Get Logo Data by 3 Digit number.  
 Logo Data refer to "5.4.13. Get Logo Data".  
 For Header Type 2, Fragment  Numbers – Data 4, Data 5 are set to  00h. 
 
(5) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Logo Type is not 00h ~ 06h.  
03h(Invalid Length)  Data Length is invalid.  
04h(No Service)  3Digit Number  is invalid  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]


--- Page 231 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 231/318 (6) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Get Logo Data by 
3Digit Number  Command]  
Command(Need ACK)[Get Logo Data by 3
Digit Number  Response]  
ACK  Processing


--- Page 232 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 232/318 5.5. HOST⇒B/E Event  
5.5.1.  Key Event  
(1) Key Event (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  02h Key Event(Upper)  
Data 1 :  01h Key Event(Lower)  
Data 2 :  Key Status  
01h : Press  
02h : Release  
 
Data 3 :  Key Code  
01h : No.1  
02h : No.2  
03h : No.3  
04h : No.4  
05h : No.5  
06h : No.6  
07h : No.7  
08h : No.8  
09h : No.9  
0Ah : No.10/0  
0Dh : Up Arrow  
0Eh : Down Arrow  
0Fh : Left Arrow  
10h : Right Arrow  
11h : Enter  
12h : Back  
27h : Data Broadcast  
28h : Blue  
29h : Red  
2Ah : Green  
2Bh : Yellow  
Data CRC8 :  -- 
 
(2) Description  
 Notify Key Event to B/E.  
 Key Event use only BML Browser.  
 When press Remocon button, HOST transmit Key Status=Press  
 If release after N sec, HOST transmit Key Status=Release.


--- Page 233 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 233/318 (3) Error Handling  
 HOST doesn’t need ACK from B/E.  
 If Key Event is CRC Error, B/E doesn’t transmit NAK to HOST.  
 
(4) Sequence  
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[Key Event]  
Processing


--- Page 234 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 234/318 5.6. B/E⇒HOST Command  
5.6.1.  Wakeup  
(1) Wakeup  Command (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  80h Wakeup(Upper)  
Data 1 :  01h Wakeup(Lower)  
Data 2 :  Boot Mode  
00h : Normal Boot  
01h : Software Update  
Data CRC8 :  -- 
 
(2) Wakeup Response  (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  0Bh 
Header CRC8 :  -- 
Data 0 :  80h Wakeup(Upper)  
Data 1 :  01h Wakeup(Lower)  
Data 2 :  00h : Reserved  
Data 3 :  uCom Software Version 0(Upper)  
Data 4 :  uCom Software Version 1  
Data 5 :  uCom Software Version 2  
Data 6 :  uCom Software Version 3(Lower)  
Data 7 :  Action Mode  
00h : Not tuning after booting(Keep idle status)  
FFh : Tuning Last Channel after booting  
 
Data 8 :  In case of Normal Boot:  
00h : Reserved  
In case of Software Update  
00h : SW Update  
01h : HW Test  
Data 9 :  00h : Current User  
01h to 06h : User ID  
FFh : Demo Mode  
Data CRC8 :  -- 
 
(3) Description  
 Inform to HOST that B/E finish to boot.  
 If HOST doesn’t receive this command within 20sec after RESET, HOST should reset 
B/E again.  
 B/E discard all command before receiving Wakeup Response. HOST shouldn’t send 
any commands (except response of Boot Mode) until receiving Wakeup command.  
 If Boot Mode = 01h (Software Update), B/E discard all command from HOST (except 
Supported command (Refer to 5.1. Command List)).  
 If there is no response for more than 20 seconds to UART command issued at the time


--- Page 235 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 235/318 when boot up should have been completed, B/E should be reset.  
 If Action Mode (Data7) is 00h, B/E keeps idle status after booting. If Action Mode 
(Data7) = FFh, B/E tune the last channel after booting. But if B/E doesn’t have the 
last channel, B/E keeps idle status.  
 
- If Last Service  cannot  tune , then Last Channel top Service selected.  
- If Last Channel cannot  tune, TV1's smallest preset number station  selected.  
- If TV1 was empty,  then TV 2's smallest preset number station  selected.  
-  
 When the software comes up in DTV mode, it outputs a Wakeup  command. After that, 
output of DTV Status starts regardless of the response from HOST.  
Therefore, When the response from Host is delayed.  DVT status may be output 
earlier than Wakeup response from HOST.  
 
(4) Error Handling  
 B/E will continue to wait for Wakeup response.


--- Page 236 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 236/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Wakeup Response]  Command(Need ACK)[Wakeup Command]  
ACK  
Wakeup Command  HOST CPU  B/E 
～ Reset ～ 
Timeout  
～ Reset ～ 
Wakeup Response  Wakeup Command


--- Page 237 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 237/318 5.6.2.  Boot Mode  
(1) Boot Mode  Command (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  80h Boot Mode(Upper)  
Data 1 :  03h Boot Mode(Lower)  
Data CRC8 :  -- 
 
(2) Boot Mode  Response  (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Result = OK : 06h  
Result = NG : 05h  
Header CRC8 :  -- 
Data 0 :  80h Boot Mode(Upper)  
Data 1 :  03h Boot Mode(Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  00h : Normal Boot  
01h : SW Update  
Data CRC8 :  -- 
 
(3) Description  
 B/E send this command for confirmation Boot Mode.  
 If B/E receive “Data4=00h (Normal Boot)”, B/E start DTV Program.  
 If B/E receive “Data4=01h (SW Update)”, B/E start to SW Update.  
 If there is no response for more than 20 seconds to UART command issued at the time 
when boot up should have been completed, B/E should be reset.  
 
(4) Error Handling  
 If B/E Result=NG of response, B/E start DTV Program.  
 If B/E didn’t receive Boot Mode Response during 200ms after receiving ACK of 
Wakeup Command, B/E start with Normal Boot.  
 If B/E happen to retry over of Boot Mode Command, B/E start with Normal Boot.


--- Page 238 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 238/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Boot Mode Response]  Command(Need ACK)[Boot Mode Command]  
ACK


--- Page 239 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 239/318 5.7. B/E⇒HOST Event  
5.7.1.  DTV Status  
(1) DTV Status Event (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack))  
Request No. :  00h ~ FFh  
Data Length :  12h 
Header CRC8 :  -- 
Data 0 :  82h DTV Status Event (Upper)  
Data 1 :  01h DTV Status Event (Lower)  
Data 2 :  DTV Status  
00h : Power OFF (Not Support)  
01h : Booting (Not Support)  
02h : Shutdown ( After Shutdown  B/E) 
03h : In Service (After Booting  B/E) 
04h : Low Power (Low Power mode)  
05h : DTV OFF  
06h : DTV OFF with EPG SCAN  
07h : Demo mode 
Data 3 :  Tuning Status  
00h : Idle  
01h : Tuning  
Data 4 :  Service Type ( Now Playing Service Type)  
00h : ISDB -T Fullseg  
01h : ISDB -T Oneseg  
FFh : None (Not Tuning)  
Data 5 :  Service Status  
 00h : Invalid  
01h : Normal Service  
02h : Special Service  
03h : Emergency Service  
04h : Suspend Service  
* Refer to “ 5.4.1(3)  Description ” 
Data 6 :  Video Output  
00h : No output (From Tuning to Video Output)  
01h : Outputted  
Data 7 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh : None(Not Tuning / Not Stored channel)  
Data 8 :  Preset Channel Number  
00h : tuned by Search/BCSearch/Physical Channel Set  
01h～0Ch : Preset Channel Number  
FFh : None (Not Tuning)  
Data 9 :  Copy Control(Refer to “(2) Description”)  
Data 10 :  Copy Control(Refer to “(2) Description”)  
Data 11 :  Event Code  
Refer to “ 5.7.4 .DTV Event ” 
※Event code of "0x80" or more will not occur in this data.  
Data 12 :  Diver Mode  
00h : Dynamic 4Diver System (Fore Br0/1)  
01h : Fixed 2x2Diver System (Fore Br0/1)  
02h : Fixed 2Diver System(Antenna Br2/3)  
03h : Fixed 4Diver System  
04h：Fixed 2Diver System(Antenna Br0/1)  
05h : Fixed 3x1Diver System (Fore Br0/1/2)


--- Page 240 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 240/318 06h : Dynamic 4Diver System (Fore Br2/3)  
07h : Fixed 2x2Diver System (Fore Br2/3)  
08h : Fixed 3x1Diver System (Fore Br1/2/3)  
Data 13 :  Antenna Level  
00h : Antenna Level 0  
01h : Antenna Level 1  
02h : Antenna Level 2  
03h : Antenna Level 3  
Data 14 :  Background Status  
00h : idle  
01h : Background Search  
02h : Background scan  
03h : Manual Background Search  
04h : Manual Background Scan  
Data 15 :  EPG/BML Status 00h : No EPG/BML displayed  
01h : Updating  
02h : EPG List  (full seg)  
03h : EPG List (one seg)  
04h : EPG Information  (full seg)  
05h : EPG Information (one seg)  
06h : BML Display  
Data 16  :  Tuner0 Physical Channel Number  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify DTV Status to HOST.  
 B/E always transfer to HOST CPU in interval of 1s.  
 DTV Status information in Data2 will be set to In Service (03h) immediately after 
sending “Wake up” from B/E. B/E will not wait for Wake up Response for setting this. 
 If Data2 = “04h: Low Power mode ",  tune commands, Display EPG command, etc., 
are not supported.  
 If Data2 = “07h: Demo mode  ",  Only a few commands are supported. See “ 5.3.17. 
Set User ID ” for the list of supported commands.  
 When Audio/Video are outputted, Data6 becomes 01h almost simultaneously with 
DTV event code becoming 90h.  
 Data 6 Video Output:  
- To make host aware that a video output has started after tune/search.  
- From tuning until the start of playback, this will be 00h.  
- If wrong service is found after broadcast station search, then Audio/Video are 
muted, and DTV Event code becomes 00h. In this case, DTV status Data6 
remains 00h.  
- DTV Status Data6 remains 1 during AV mute after DTV Event 90h.  
 Refer to the followings about Copy Control . 
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 
                    
WORD0  WORD1  WORD2  CRCC(*)  
2bit 4bit 8bit 6bit


--- Page 241 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 241/318 b7 b6 b5 b4 b3 b2 b1 b0 b7 b6 b5 b4 b3 b2 b1 b0     
                    
Data 9  Data 10      
Data 9:  
7~6b: 1~2bit (WORD0)  
      00b: Aspect Ratio 4:3  
      01b: Aspect Ratio 4:3 Letterbox  
      10b: Aspect Ratio 16:9  
      11b: Reserved  
5~2b: 3~6bit (WORD1)  
      0000b: CGMS -A Information  
      1111b: Reserved  
1~0b: 7~8bit (WORD2 (CGMS -A)) 
      00b: Copy Freely  
      01b: Not defined  
      10b: Copy One Generation  
      11b: Copy Never  
Data 10:  
7~6b: 9~10bit (WORD2 (Analog Output Copy Control Information))  
      00b: Copy Freely  
      01b: A Pseudo -sync pulse is present  
      10b: A Pseudo -sync pulse + 2 line inverted and split burst insertion  
      11b: A Pseudo -sync pulse + 4 line inverted and split burst insertion  
5~2b: 11~14bit (WORD2)  
      These bits shall be left undefined (Logic 0)  
1~0b: Reserved (Logic 0)  
*: 15~20bit (CRCC) shall be calculated by HOST CPU  
   G(x) = x6+x+1  
 If “Diver Mode” is 00h or 01h, B/E use both tuner0/tuner1.  
 Tuner0 is used for Foreground processing, and Tuner1 is used for Background 
processing.  
 “Antenna Level” indicates the number of antenna bars on the display. Antenna Level 
0 is bad signal. Antenna Level 3 is good signal. If “Tuning Status (Data3)” is idle, 
Antenna Level is 0.  
 If “EPG Update Status” is 00h, B/E isn’t updating EPG of specified channel. But B/E 
may be updating EPG with back scan.  If 01h, B/E is updating forcibly by 
“5.2.12 .Display EPG ” command. If finishing to update EPG, “EPG Update Status” 
change to 00h.  
 In the first DTV status event output immediately after booting up, Data2 to Data16 
may be filled with initial value (00h). However, B/E is not abnormal state. Please 
ignore this DTV status event.


--- Page 242 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 242/318 (3) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 HOST CPU  B/E 
Command(No Need ACK)[DTV Status Event]


--- Page 243 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 243/318 5.7.2.  Scan Status  
(1) Scan Status (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  82h Scan Status(Upper)  
Data 1 :  03h Scan Status (Lower)  
Data 2 :  Status  
01h : notification  
FFh : end  
Data 3 :  Status = 01h  
  0Dh~34h : Physical Channel Number  
Status = FFh  
  00h : Fixed Value  
Data 4 :  Status = 01h  
  00h : No Detection  
  01h : Detection  
Status = FFh  
  00h : No station found or stopped  
  01h : One or more station s found  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify Scan Status to HOST.  
 When changing the physical channel, notify this status (Status=01h).  
 When finishing the scan, notify this status (Data2=FFh, Data3=00h, Data4=00h/01h).  
 When stopping the scan, notify this status (Data2=FFh, Data3=00h, Data4=00h).  
 
(3) Sequence  
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[Scan Status Event]


--- Page 244 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 244/318 5.7.3.  Search Status  
(1) Search Status (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  82h Search Status(Upper)  
Data 1 :  04h Search Status (Lower)  
Data 2 :  Status  
01h : notification(Foreground Search)  
02h : notification(Broadcast Search – Foreground, 
Relay station)  
03h : notification(Broadcast Search – Foreground, 
Affiliated station)  
04h : notification(Broadcast Search – Foreground, 
Relay station + Affiliated station)  
FFh : end (Foreground and Background Search)  
           Background search will be end only when station 
found successful.  
Data 3 :  Status = 01h ~ 04h  
0Dh~34h : Physical Channel Number  
Status = FFh  
00h 
Data 4 :  Status = 01h ~  04h  
00h : No Detection  (Only for foreground search)  
01h : Detection  
Status = FFh  
00h : Not find the new channel and return the last 
channel.  
01h : Find the new channel and select new channel.  
02h : Select Relay Station (Fore)  
03h : Select Affiliated Station (Fore)  
04h : Select Relay Station  (Back)  
05h : Select Affiliated Station  (Back)  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify Search/Broadcast Search Status to HOST.  
 When changing the physical channel for search, notify this status (Status=01h).  
 When changing the physical channel for broadcast search, notify this status 
(Status=02h).  
 When finishing search, notify this status (Data2=FFh, Data3=00h, 
Data4=00h/01h/02h/03h /04h/05h ). 
 When stopping search, notify this status (Data2=FFh, Data3=00h, Data4=00h).  
 If a background search was performed at the start of the foreground search, the 
background search will be stopped , but Data 2, FFh will not occur.


--- Page 245 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 245/318 (3) Sequence  
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[Search Status Event]


--- Page 246 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 246/318 5.7.4.  DTV Event  
(1) DTV Event  Status (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  82h DTV Event(Upper)  
Data 1 :  06h DTV Event (Lower)  
Data 2 :  Event Code  
Refer to “ (2)Description ” 
Data CRC8 :  -- 
 
(2) Description  
 B/E notify DTV Event to HOST.  
 Refer to the following table and state diagram about Event Code.  
Event 
Code  Content(English)  Content(Japanese)  
00h No Error  エラーなし  
06h Can’t receive this channel, because 
weak signal.  信号レベルが低下している為、こ
のチャンネルは受信できません  
07h Can’t receive this channel.  
 このチャンネルは受信できません  
08h This channel is not being broadcast.  このチャンネルは現在放送されて
いません  
09h TRMP Information is invalid  受信機情報が不正です  
0Bh RMP Error EC21  受信制御データが設定されていま
せん。しばらくお待ちください
（最大で 30 秒かかる場合がありま
す）。  
コード： EC21  
0Ch RMP Error EC22  このチャンネルは視聴できませ
ん。ご覧のチャンネルのカスタマ
ーセンターにお問い合わせくださ
い。 
コード： EC22  
0Dh RMP Error EC23  この受信機ではご覧になることが
できません。ご覧のチャンネルの
カスタマーセンターへお問い合わ
せください。  
コード： EC23  
20h Tuner error(I2C  HW error ) － 
80h Start tuning  － 
81h Start tuning(Last Channel)  － 
82h Start search  
 (Search up/down  operation ) － 
83h Start broadcast search(Manually)  － 
84h Start foreground broadcast search  
(Automatic)  － 
90h Tuning is completed first, and 
MPEG TS is decoded, then playing 
audio/video properly.  －


--- Page 247 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 247/318  
 
  
Tuning  
Error  
Tuning  
80h : Start  
Tuning  
81h : Start  
Tuning  
Last CH  
Tuning  
Tuning  
OK 
90h : CH  
Locked and  
MPEG  
decoded  
(Audi/Video  
playing)  
Searching  
Searching  
82h : Start  
Seek 
83h : Start  
Manual  
Broadcast  
Searching  
(Foreground)  
84h : Start  
Automatic  
Broadcast  
Searching  
(Foreground or  
Background)  
Searching  
Tuning Error  
Tuning  
Error  
07h : No  
signal found  
Locked but no  
MPEG Decoded  
(AV Muted)  
Signal Lost or  
Recovered  
06h : CH  
Unlocked  
TRMP Errors  
08h : No  
service  
available  
TRMP  
Errors  
0Bh : TRMP EC21  
0Ch : TRMP EC22  
0Dh : TRMP EC23  
09h : TRMP Info  
not available  
(Device failure)  
Tuning and   
Tuning Error  
Signal Recovered  
or EC Recovered  
00h : Default  
state 
No error  
(CH  
tuned and  
locked) or Idle  
(No CH tuned)  
20h : Tuner error  
Tuning  
NG 
Monitoring  
NG 
20h : Tuner error  
20h : Tuner error  
NG 
Monitoring


--- Page 248 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 248/318  
Non-TRMP/Non -scrambled' TS flow  
  
TS scrambled 
with TRMP?  
Checking received TS  
Already get 
TRMP info ?  
Service 
Y 
Play back Audio & Video  
Y 
N 
PER=0?  
N 
Start measuring time  
N 
Y 
Scrambled?  
Play back Audio & Video  
N 
Y 
Receive Error  
N 
 Y 
Y 
Audio and video are 
played back in case of the 
signal is non-scramble.  
Audio and Video are 
muted in case of the 
signal is scrambled.  
Y 
Y 
Y 
Y 
N 
 Y 
N 
N 
N 
N 
time ≥ 30sec?


--- Page 249 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 249/318  In case of DTV Event code 0b/0c/0dh occurs, B/E change to 1seg if auto segment 
was used. If B/E receives TRMP key from Transport stream then switch back to 
12seg.  
 Start tuning code (80h): It occurs at Foreground Tuning.  
 Start tuning (Last Channel) code (81h): It occurs at Foreground Tuning.  
 Start search (82h): It occurs at Foreground Search.  
 Start broadcast search (Manually) (83h): It occurs at Foreground Search.  
 Start broadcast search (Automatic) (84h): It occurs at Foreground Search and 
Background Search.  
 Complete tuning (90h): It occurs at Foreground Tuning. In this case, DTV status 
Data6 becomes 01h almost simultaneously.  
 No Error or Idle status (00h): If wrong service is found after broadcast station 
search, then Audio/Video are muted, and DTV Event code becomes 00h. In this 
case, DTV status Data6 remains 00h.  
 TRMP Information is invalid (09h): It occurs at after Tuning.  
⑥ Start tuning (80h) or Start tuning (Last Channel) (81h).  
⑦ In case of error: No Error (00h).  
⑧ TRMP Information is invalid (09h).  
 The case of “Locked but no MPEG Decoded  (AV muted)” is only for signal 
generator use case.  
 If an error occurs during I2C communication, it is considered as Monitoring NG.  
 When I2C  error  (20h)  happed, Host needs to reset  (pin assert) the module .  
  
          
(3) Sequence  
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[Error Message Event]  
ACK


--- Page 250 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 250/318 5.7.5.  EWS Event  
(1) EWS  Event  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  82h EWS Event(Upper)  
Data 1 :  08h EWS Event (Lower)  
Data 2 :  Status  
00h : None  
01h : Signal Level1  
02h : Signal Level2  
03h : Test  
Data 3 :  Three Digit Number(Upper) Refer to “(2) Description”  
Data 4 :  Three Digit Number(Lower) Refer to “(2) Description”  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify EWS Event to HOST.  
 If Data 2 is 01h, HU automatically send “ 5.2.8 .Direct Channel Select ”. 
 If Data 2 is 02h or 03h, HU display EWS Confirmation Screen. When user select 
“yes”, HU send “ 5.2.8 .Direct Channel Select ”. 
 Use same branch number that you are currently watching.  
 Even when RMP error code is being output in 12 -seg fixed mode, 'EWS event' can 
be sent if EWS event occurs.  
 When EWS event ended, Data 2 will be 00h and send to Host.  
(3) Sequence  
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[EWS Event]  
ACK


--- Page 251 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 251/318 5.7.6.  Program Information  
(1) Program Information  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  0Ah~7Eh  
Header CRC8 :  -- 
Data 0 :  82h Program Information (Upper)  
Data 1 :  09h Program Information (Lower)  
Data 2 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 3 :  00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 4 :  Three Digit Number(Upper)  
Data 5 :  Three Digit Number(Lower)  
Data 6 :  Branch Identifier Number  
Data 7 :  Length of Station Name(N1) : 00h~14h  
Data 8 ~7+N1 :  Station Name(TS Name)  
Data 8+N1 :  Length of Program Name(N2) : 00h~60h  
Data 9+N1~8+N1+N2:  Program Name  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify the program information.  
 The program information contains Preset Channel Number / Station Name / Program 
name).  
 Preset Channel Number is 01h~0Ch. If current playback channel is not stored, Data3 
is 00h and Data2 is FFh.  
 Three Digit Number & Branch Identifier Number are current playback service. If 
current playback channel is not stored, these data are set.  
 The length of Station Name is 00h~14h.  
 The format of Station Name is 8bit character code set.  
 The length of Program Name is 00h~60h.  
 The format of Program name is 8bit character code set.  
 If B/E doesn’t have Program name, Length of Program Name is set to 0.  
 When any information is updated, B/E will notify this event.


--- Page 252 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 252/318 (3) Sequence  
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[Program Information]  
ACK


--- Page 253 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 253/318 5.7.7.  EPG  Status  
(1) EPG  Status (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  82h EPG Status(Upper)  
Data 1 :  0Ah EPG Status (Lower)  
Data 2 :  Status  
01h : Updating  
FFh : end  
Data 3 :  Status=01h  
00h : Fixed Value  
Status=FFh  
00h : Complete to update EPG  
01h : Cancel by user  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify EPG Status (Data2=01h) to HOST during EPG Updating.  
 When finishing EPG Updating, B/E notify status(Status=FFh)  
 If completing to update EPG for all channel in the preset table, Data3 is 00h.  
 If cancel by user during updating EPG, Data3 is 01h.  
 EPG update will be done at 20s/Ch.  
 
(3) Sequence  
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[EPG Status Event]


--- Page 254 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 254/318 5.7.8.  Event relay  
(1) Event relay  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  09h 
Header CRC8 :  -- 
Data 0 :  82h Event relay (Upper)  
Data 1 :  0Bh Event relay  (Lower)  
Data 2 :  Status  
01h – 1Eh (before 1[s] to 30[s])  
FFh : end  (Event relay done)  
Data 3 :  Relay Three Digit Number(Upper)  
Data 4 :  Relay Three Digit Number(Lower)  
Data 5 :  Relay Branch Identifier Number  
Data : 6  Relay Service ID(Upper)  
Data : 7  Relay Service ID(Lower)  
Data CRC8 :  -- 
 
(2) Description  
 Data 2 : Number of second until s witching service.  
 Data2  = FFh : Event relay done  
 
(3) Sequence  
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command( Need ACK)[  Event relay  Event]  
ACK


--- Page 255 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 255/318 5.7.9.  Number of Program info  
(1) Number of Program info (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  35h 
Header CRC8 :  -- 
Data 0 :  82h Number of Program  info (Upper)  
Data 1 :  0Ch Number of Program info  (Lower)  
Data 2 :  Not Stored Channel (Fullseg) : Number of Program info  
Bit7 : reserved for unknown state  
Bit6-4 : Notification ID  
Bit3-0 : Number of Program  (0:Not Active ) 
※FFh unknown  
Data 3 :  Not Stored Channel (Oneseg) : Number of Program info  
Data 4 :  Home Preset no.1(Fullseg) : Number of Program info  
Data 5 :  Home Preset no.2(Fullseg) : Number of Program info  
Data 6 :  Home Preset no.3(Fullseg) : Number of Program info  
Data 7 :  Home Preset no.4(Fullseg) : Number of Program info  
Data 8 :  Home Preset no.5(Fullseg) : Number of Program info  
Data 9 :  Home Preset no.6(Fullseg) : Number of Program info  
Data 10 :  Home Preset no.7(Fullseg) : Number of Program info  
Data 11 :  Home Preset no.8(Fullseg) : Number of Program info  
Data 12 :  Home Preset no.9(Fullseg) : Number of Program info  
Data 13 :  Home Preset no.10(Fullseg) : Number of Program info  
Data 14 :  Home Preset no.11(Fullseg) : Number of Program info  
Data 15 :  Home Preset no.12(Fullseg) : Number of Program info  
Data 16 :  Home Preset no.1(Oneseg) : Number of Program info  
Data 17 :  Home Preset no.2(Oneseg) : Number of Program info  
Data 18 :  Home Preset no.3(Oneseg) : Number of Program info  
Data 19 :  Home Preset no.4(Oneseg) : Number of Program info  
Data 20 :  Home Preset no.5(Oneseg) : Number of Program info  
Data 21 :  Home Preset no.6(Oneseg) : Number of Program info  
Data 22 :  Home Preset no.7(Oneseg) : Number of Program info  
Data 23 :  Home Preset no.8(Oneseg) : Number of Program info  
Data 24 :  Home Preset no.9(Oneseg) : Number of Program info  
Data 25 :  Home Preset no.10(Oneseg) : Number of Program info  
Data 26 :  Home Preset no.11(Oneseg) : Number of Program info  
Data 27 :  Home Preset no.12(Oneseg) : Number of Program info  
Data 28 :  Travel Preset no.1(Fullseg) : Number of Program info  
Data 29 :  Travel Preset no.2(Fullseg) : Number of Program info  
Data 30 :  Travel Preset no.3(Fullseg) : Number of Program info  
Data 31 :  Travel Preset no.4(Fullseg) : Number of Program info  
Data 32 :  Travel Preset no.5(Fullseg) : Number of Program info  
Data 33 :  Travel Preset no.6(Fullseg) : Number of Program info  
Data 34 :  Travel Preset no.7(Fullseg) : Number of Program info  
Data 35 :  Travel Preset no.8(Fullseg) : Number of Program info  
Data 36 :  Travel Preset no.9(Fullseg) : Number of Program info  
Data 37 :  Travel Preset no.10(Fullseg) : Number of Program info  
Data 38 : Travel Preset no.11(Fullseg) : Number of Program info  
Data 39 :  Travel Preset no.12(Fullseg) : Number of Program info  
Data 40 :  Travel Preset no.1(Oneseg) : Number of Program info  
Data 41 :  Travel Preset no.2(Oneseg) : Number of Program info  
Data 42 : Travel Preset no.3(Oneseg) : Number of Program info  
Data 43 :  Travel Preset no.4(Oneseg) : Number of Program info  
Data 44 :  Travel Preset no.5(Oneseg) : Number of Program info  
Data 45 :  Travel Preset no.6(Oneseg) : Number of Program info


--- Page 256 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 256/318 Data 46 : Travel Preset no.7(Oneseg) : Number of Program info  
Data 47 :  Travel Preset no.8(Oneseg) : Number of Program info  
Data 48 :  Travel Preset no.9(Oneseg) : Number of Program info  
Data 49 :  Travel Preset no.10(Oneseg) : Number of Program info  
Data 50 :  Travel Preset no.11(Oneseg) : Number of Program info  
Data 51 :  Travel Preset no.12(Oneseg) : Number of Program info  
Data CRC8 :  -- 
 
(2) Description  
 Get current time Number of programs per Channel.  
 Number of Program info = FFh : Haven't got current program info yet . 
 Data2 ~ Data51  : 
      Bit3-0 – Number of Program Info  
      Bit6-4 – Notification ID, incremented  (0 to 7) whenever there is an update.  
      Bit7 – Set when information is unavailable.  
 Send only when there is a change in the data  
 
(3) Sequence  
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[  Number of Program  info Event]  
ACK


--- Page 257 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 257/318 5.7.10.  Program Information  with UTF -8 
(1) Program Information  with UTF -8 (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  0Ah~  
Header CRC8 :  -- 
Data 0 :  82h Program Information with UTF -8(Upper)  
Data 1 :  0Dh Program Information with UTF -8(Lower)  
Data 2 :  Fragment Number  
Data 3 :  Last Fragment Number  
Data 4  : Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 5 :  00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 6 : Three Digit Number(Upper)  
Data 7 : Three Digit Number(Lower)  
Data 8 : Branch Identifier Number  
Data 9 : Length of Station Name(N1) : 00h~ 50h 
Data 10~9+N1 :  Station Name(TS Name)  
Data 10+N1 :  Length of Program Name(N2)(Upper) : 00h~1 80h 
Data 11+N1 :  Length of Program Name(N2)(Lower) : 00h~1 80h 
Data 
12+N1~11+N1+N2:  Program Name  
Data CRC8 :  --


--- Page 258 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 258/318 (2) Program Information  with UTF -8 (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes) :  000Ah  ~ 01DDh  
Header CRC8 :  -- 
Data 0 :  82h Program Information with UTF -8(Upper)  
Data 1 :  0Dh Program Information with UTF -8(Lower)  
Data 2 :  Fragment Number  (00h : Fixed Value)  
Data 3 :  Last Fragment Number  (00h : Fixed Value)  
Data 4  : Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
FFh：None  
Data 5 :  00h : Not stored service  
01h~0Ch : Preset Channel Number  
FFh：None  
Data 6 : Three Digit Number(Upper)  
Data 7 : Three Digit Number(Lower)  
Data 8 : Branch Identifier Number  
Data 9 : Length of Station Name(N1) : 00h~ 50h 
Data 10~9+N1 :  Station Name(TS Name)  
Data 10+N1 :  Length of Program Name(N2)(Upper) : 00h~1 80h 
Data 11+N1 :  Length of Program Name(N2)(Lower) : 00h~1 80h 
Data 
12+N1~11+N1+N2:  Program Name  
Data CRC8 :  -- 
 
(3) Description  
 B/E notify the program information.  
 The program information contains Preset Channel Number / Station Name / Program 
name).  
 Preset Channel Number is 01h~0Ch. If current playback channel is not stored, Data3 
is 00h and Data2 is FFh.  
 Three Digit Number & Branch Identifier Number are current playback service. If 
current playback channel is not stored, these data are set.  
 If B/E doesn’t have Program name, Length of Program Name is set to 0.  
 When any information is updated, B/E will notify this event.  
 For Header Type 2, Fragment  Numbers - Data 2, Data 3 are set to 00h.


--- Page 259 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 259/318 (4) Sequence  
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[Program Information  with 
UTF -8] 
ACK


--- Page 260 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 260/318 5.7.11.  TS Name  Update  
(1) TS Name  Update  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h～ 
Header CRC8 :  -- 
Data 0 :  82h TS Name  Update  (Upper)  
Data 1 :  0Eh TS Name Update (Lower)  
Data 2 :  Fragment Number  
Data 3 :  Last Fragment Number  
Data 4 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
Data 5 ~ 24: TS Name Not Stored channel  
Data 25 ~ : TS Name Channel 1 to 12 (20byte per channel)  
Data CRC8 :  -- 
 
(2) TS Name  Update  (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2 Bytes)  010Ah  
Header CRC8 :  -- 
Data 0 :  82h TS Name  Update  (Upper)  
Data 1 :  0Eh TS Name Update (Lower)  
Data 2 :  Fragment Number  (00h : Fixed Value)  
Data 3 :  Last Fragment Number  (00h : Fixed Value)  
Data 4 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
Data 5 ~ 24: TS Name Not Stored channel  
Data 25 ~ : TS Name Channel 1 to 12 (20byte per channel)  
Data CRC8 :  -- 
 
(3) Description  
 TS Name  with ARIB 8bit character code set . 
 TS Name Update  
 For Header Type 2, Fragment  Numbers - Data2, Data3 are set to 00h.  
(4) Sequence  
 
 
 
 
 
 
 HOST CPU  B/E 
Command(Need ACK)[ TS Name Update ] 
ACK


--- Page 261 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 261/318 5.7.12.  TS Name  Update with UTF -8 
(1) TS Name  Update with UTF -8 (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h～ 
Header CRC8 :  -- 
Data 0 :  82h TS Name  Update  with UTF -8 (Upper)  
Data 1 :  0Fh TS Name Update with UTF -8 (Lower)  
Data 2 :  Fragment Number   
Data 3 :  Last Fragment Number   
Data 4 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
Data 5 ~ 84: TS Name Not Stored channel  
Data 85 ~ : TS Name Channel 1 to 12 ( 80byte per channel)  
Data CRC8 :  -- 
 
(2) TS Name  Update with UTF -8 (BE ⇒ HOST  with Header Type 2 ) 
Start Sync :  A5h,5 9h 
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length (2 Bytes ) :  0416h 
Header CRC8 :  -- 
Data 0 :  82h TS Name  Update  with UTF -8 (Upper)  
Data 1 :  0Fh TS Name Update with UTF -8 (Lower)  
Data 2 :  Fragment Number  (00h : Fixed Value)  
Data 3 :  Last Fragment Number  (00h : Fixed Value)  
Data 4 :  Preset Number  
00h : Preset No.1(Home)  
01h : Preset No.2(Drive)  
Data 5 ~ 84: TS Name Not Stored channel  
Data 85 ~ : TS Name Channel 1 to 12 ( 80byte per channel)  
Data CRC8 :  -- 
 
(3) Description  
 TS Name  with UTF -8. 
 TS Name Update  
 For Header Type 2, Fragment  Numbers - Data2, Data3 are set to 00h.  
 
(4) Sequence  
 
 
 
 
 
 
 HOST CPU  B/E 
Command(Need ACK)[ TS Name Update with UTF -8] 
ACK


--- Page 262 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 262/318 5.7.13.  Logo Update  
(1) Logo Update  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  08h 
Header CRC8 :  -- 
Data 0 :  82h Logo Update(Upper)  
Data 1 :  10h Logo Update (Lower)  
Data 2 :  Service ID(Upper)  
Data 3 :  Service ID(Lower)  
Data 4 :  Logo Type  
00h to 05h  
Data 5 :  Logo Version (Upper)  
Data 6 :  Logo Version (Lower)  
Data CRC8 :  -- 
 
(2) Description  
・Logo Type 6 /7 : Not Event Send (Oneseg Logo Include Service Name)  
・If the logo data is shared, the event for the shared service will occur.  
 
(3) Sequence  
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[ Logo Update   Event]  
ACK


--- Page 263 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 263/318 5.7.14.  EPG Button Status  
(1) EPG Button Status  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  0Fh 
Header CRC8 :  -- 
Data 0 :  82h EPG Button Status (Upper)  
Data 1 :  11h EPG Button Status (Lower)  
Data 2 :  Up Arrow 0: invalid 1:valid  
Data 3 :  Down Arrow 0: invalid 1:valid  
Data 4 :  Left Arrow 0: invalid 1:valid  
Data 5 :  Right Arrow 0: invalid 1:valid  
Data 6 :  Back 0: invalid 1:valid  
Data 7 :  Enter 0: invalid 1:valid  
Data 8 :  Switch segment 0: invalid 1:valid  
Data 9 :  Update 0: invalid 1:valid  
Data 10 :  Previous Day(Blue Button) 0: invalid 1:valid  
Data 11 :  Next Day(Red Button) 0: invalid 1:valid  
Data 12 :  Multi service(Green Button) 0: invalid 1:valid  
Data 13 :  Change Scale(Yellow Button) 0: invalid 1:valid  
Data CRC8 :  － 
 
(2) Description  
・EPG Button status  
・Notifies when EPG is displayed and a change in button status is required.  
・This event notification will be started only after B/E receives ACK for Display EPG  
Response.  
 
(3) Sequence  
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command( Need ACK)[ EPG Button Status Event]  
ACK


--- Page 264 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 264/318 5.7.15.  BML Status  
(1) BML Status  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  82h BML Status  (Upper)  
Data 1 :  12h BML Status  (Lower)  
Data 2 :  BML Status  Code  
Data CRC8 :  － 
 
(2) Description  
・Status  Code  
Status  
Code  Content   
B0h The BML document cannot be 
obtained.   
B1h The BML engine of the receiver 
does not  support the version of the 
BML document  obtained.   
B2h During the display of the contents, 
an execution error has occurred,  
and external  reference data cannot 
be obtained.   
B3h BML failed to start or not 
supported.   
B4h BML data not ready.  
This is raised when the BML cannot 
be displayed by pressing the 'd' 
button .   
B5h BML data ready . 
This is raised  when BML started to 
be displayed  by pressing the  ‘d’ 
button .  
B6h BML not available in current 
service.  
This is raised when ‘d’ button 
presses  in case of receiving 
Oneseg or F ullseg without BML 
support.   
 
(3) Sequence  
 
 
 
 
 
 
 HOST CPU  B/E 
Command( Need ACK)[ BML Error Event]  
ACK


--- Page 265 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 265/318 5.7.16.  C/N Information  
(1) C/N Information  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  11h 
Header CRC8 :  -- 
Data 0 :  82h C/N Information  (Upper)  
Data 1 :  13h C/N Information  (Lower)  
Data 2 :  Fore physical channel  
Data 3 -4 :  Fore Diversity  C/N 
Data  5 :  Back physical chan nel 
Data  6-7 : Back Diversity  C/N 
Data 8 -9 : Br0 C/N  
Data 10 -11 : Br1 C/N  
Data 12 -13 : Br2 C/N  
Data 14 -15 : Br3 C/N  
Data CRC8 :  － 
 
(2) Description  
・B/E notifies the C /N Levels to Host . 
・Reports the foreground and background Physical Channel Numbers and C /N levels.  
・Notification interval is 1s.  
・This event can be enabled/ disabled with “Set Event Mask”  
 
 
(3) Sequence  
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[ C/N Information Event]


--- Page 266 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 266/318 5.7.17.  EPG Scan Result  
(1) EPG Scan Result  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  99h 
Header CRC8 :  -- 
Data 0 :  82h EPG Scan Result  (Upper)  
Data 1 :  14h EPG Scan Result  (Lower)  
Data 2 : Not Stored Channel  Fullseg Service 0/1  
XYh :  
X = Service 0 EPG Days  
Y = Service 1 EPG Days  
Data 3 :  Not Stored Channel Fullseg Service 2/3  
XYh :  
X = Service 2 EPG Days  
Y = Service 3 EPG Days  
Data 4 :  Not Stored Channel Fullseg Service 4/5  
XYh :  
X = Service 4 EPG Days  
Y = Service 5 EPG Days  
Data 5 :  Not Stored Channel Fullseg Service 6/7  
XYh :  
X = Service 6 EPG Days  
Y = Service 7 EPG Days  
Data 6 :  Not Stored Channel Oneseg Service 0/1  
XYh :  
X = Service 0 EPG Days  
Y = Service 1 EPG Days  
Data 7 :  Not Stored Channel Oneseg Service 2/Reserve  
XYh :  
X = Service 2 EPG Days  
Y = Reserve  
Data 8 :  Home Channel 1 Fullseg Service 0/1  
Data 9 :  Home Channel 1 Fullseg Service 2/3 
Data 10 :  Home Channel 1 Fullseg Service 4/5 
Data 11 :  Home Channel 1 Fullseg Service 6/7 
Data 12 :  Home Channel 1 Oneseg  Service 0/1 
Data 13 :  Home Channel 1 Oneseg  Service 2/ Reserve  
Data 14 - Data 73 : ・・・ (Home Channel 2 ―＞ Home Channel 11)  
Data 74 : Home Channel 1 2 Fullseg Service 0/1  
Data 75 : Home Channel 1 2 Fullseg Service 2/3 
Data 76 : Home Channel 1 2 Fullseg Service 4/5 
Data 77 : Home Channel 1 2 Fullseg Service 6/7 
Data 78 : Home Channel 1 2 Oneseg Service 0/1 
Data 79 : Home Channel 1 2 Oneseg Service 2/ Reserve  
Data 80 : Driver  Channel 1 Fullseg Service 0/1  
Data 81 : Driver  Channel 1 Fullseg Service 2/3 
Data 82 : Driver  Channel 1 Fullseg Service 4/5 
Data 83 : Driver  Channel 1 Fullseg Service 6/7 
Data 84 : Driver  Channel 1 Oneseg Service 0/1 
Data 85 : Driver  Channel 1 Oneseg Service 2/ Reserve  
Data 86 – Data  145 : ・・・ (Driver  Channel 2 ―＞ Driver Channel 11)  
Data 146 : Driver  Channel 1 2 Fullseg Service 0/1  
Data 147 : Driver  Channel 1 2 Fullseg Service 2/3 
Data 148 : Driver  Channel 1 2 Fullseg Service 4/5 
Data 149 : Driver  Channel 1 2 Fullseg Service 6/7


--- Page 267 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 267/318 Data 150 : Driver  Channel 1 2 Oneseg Service 0/1 
Data 151 : Driver  Channel 1 2 Oneseg Service 2/ Reserve  
Data CRC8 :  － 
 
(2) Description  
 
 
(3) Sequence  
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[  EPG Scan Result ]


--- Page 268 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 268/318 5.7.18.  DTV Critical Error  
(1) DTV Critical Error Event  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  83h DTV Critical Error (Upper)  
Data 1 :  01h DTV Critical Error (Lower)  
Data 2 :  Error Type  
  01h : Hangup  
  02h : Termination  
Data 3 :  Module Information  
  Error Type 01h  
    01h : Audio Decoder  
    02h : Audio Output  
    03h : Video Decoder  
    04h : Video Output  
    05h : Deinterlacer  
    06h : Video Scaler  
    07h : Demux  
    08h : Timer  
Error Type 02h  
    00h : Fixed Value  
Data 4 :  Action Request  
  01h : DTV Restart  
  02h : DTV Module Reset  
Data CRC8 :  － 
 
(2) Description  
 BE notifies the host of any Critical Errors.  
 Critical Error implies application termination or hangup of any DTV threads.  
 Data2 indicates the type of error – Hangup of any threads or Termination.  
 Data3 gives a hint about the module which caused the issue.  
 Data3 is valid only for Hangup.  
 Data4 indicates the action to be taken by the host. 
・ If it is 01h ( DTV Restart), host may send a command (Refer  5.2.18 DTV Res tart) 
to BE to do an application restart.  
・ Alternatively, the host may do the DTV Module Reset.  
 For hangup of threads, the notification will be issued within 3 Seconds of occurrence 
and for unexpected termination, it will be done immediately after the occurrence.  
 Upon receiving this event, host should stop sending other commands to BE.  
・ After this event BE will accept only the DTV Restart  Command ( Refer 5.2.18 DTV 
Restart). 
・ No response will be sent for Watch Dog Command.  
・ Other commands will be responded with 0Ah(Invalid Status).  
 Before sending this event, BE will save the last channel information  and after reset,


--- Page 269 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 269/318 the information will be used to tune to last channel.  
 
(3) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 HOST CPU  B/E 
Command( Need ACK)[ DTV Critical Error Event]  
ACK  
Start Waiting for 
DTV Restart 
Command


--- Page 270 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 270/318 5.8. SW Update Command  
5.8.1.  SW Update  
(1) SW Update Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h~  
Header CRC8 :  -- 
Data 0 :  A0h SW Update (Upper)  
Data 1 :  01h SW Update (Lower)  
Data 2 :  Operation  
00h : SW Update start  
Data CRC8 :  -- 
 
(2) SW Update Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  A0h SW Update (Upper)  
Data 1 :  01h SW Update (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start SW Update.  
 SW updating transfer update files with YMODEM Protocol.  
 B/E wait 100msec after receiving ACK of Response.  
 HOST shouldn’t send any commands during YMODEM Protocol.  
 The new app replaces the older one of two apps in the app partition.  
 Non-application data remains unchanged . 
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.


--- Page 271 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 271/318  
 
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
21h(Disk Full)  There is not enough space in disk.  
FFh( Unknown Error)  unknown error  
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[SW Update Command]  
Command(Need ACK)[SW Update Response]  
ACK  
～YMODEM ～ Wait 100msec


--- Page 272 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 272/318 (6) Appendix   
a. Software Update flow  
Precondition: Keep the RF connections disconnected during the whole update process.  
 
 
 
 
  
START  (Power ON)  
Current  Version Read  
(Get Version ) 
Version ? 
TH010322 (Version 1.0) or older.  
Download  SW 
Ver. REUPDATE (SW Installer)  
Board Power OFF -> ON 
 
TH010347 (Version 1.0.1)  
or later.  
Download  SW 
Ver 1.0.2  
Board Power OFF ->ON  
 
Send “Shutdown”  
Send “Shutdown”  
Wait “Wakeup”  
Response”  Not tuning after booting”  
Wait “Wakeup”  
Response”  Not tuning after booting”  ※ From b.Software Update flow 
[during playback]


--- Page 273 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 273/318  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  Current  Version Read  
(Get Version ) 
Software Version ? 
"REUPDATE" (Update unsuccessful)  "TH010348" (Version 1.0.2)  Wait “Wakeup”  
Response”  Not tuning after booting”  
Download  SW 
Ver 1.0.2 
 
Send “Shutdown”  
Board Power OFF  
Update  Finish


--- Page 274 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 274/318 b.  Software Update flow [during playback]  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  START   
Send  "Set Low Power Mode"  
Low Power Mode ON  
Download  SW 
Follow the post -"Wakeup 
Response"  
sequence in a. (※) 
End


--- Page 275 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 275/318 5.8.2.  SW Update Status  
(1) SW Update Status  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  A0h SW Update Status(Upper)  
Data 1 :  02h SW Update Status (Lower)  
Data 2 :  Status  
00h : Write to NVRAM  
FFh : Finish SW Update  
Data 3 :  Result  
00h : Success  
01h : Invalid file name  
02h : Invalid Data  
03h : Invalid file size  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify SW Update Status to HOST.  
 B/E always transfers to HOST CPU in interval of 1s during SW Update (except 
YMODEM).  
 
 
(3) Sequence  
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[SW Update Status Event]


--- Page 276 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 276/318 5.8.3.  Background SW Update  Start  
(1) Background SW Update Start Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  27h 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update Start (Upper)  
Data 1 :  01h Background SW Update Start (Lower)  
Data 2 ~ 5: SW Size ( 4 Bytes Big Endian ) 
Data 6 ~ 37 :  SW Filename (32 Bytes)  
Data CRC8 :  -- 
 
(2) Background SW Update  Start  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update Start (Upper)  
Data 1 :  01h Background SW Update Start (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “4. Error Handling”)  
Data CRC8 :  -- 
 
(3) Description  
 B/E prepares itself for receiving the SW Update  package.  
 The h ost can send this command even while the B/E is in  a playback state.  
 After this command, i.e., during the Background SW Update, B/E will continue to send 
usual events and can accept  other commands from the host . 
 After receiving the response, the host  can start sending the  SW Update package .  
 (Refer to Section 5.8.5)  
 HOST can cancel the Background SW Update at any time. (Refer to Section 5.8.4)  
 
(4) Error Handling  
 The host should take necessary action in case of failure.  
 The failure can be  the following  types : 
 Doesn’t receive the response within the timeout . 
 The result of response is NG.


--- Page 277 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 277/318  Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter (Size, Filename)  is invalid  
03h(Invalid Length)  Data Length is not 27h . 
0Ah(Invalid Status)  B/E is in invalid status  
 (Ex : Already started BG SW Update)  
21h(Disk Full)  There is not enough space in disk.  
FFh( Unknown Error)  unknown error  
 
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ BG SW Update Start Command]  
Command(Need ACK)[ BG SW Update Start Response]  
ACK


--- Page 278 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 278/318 5.8.4.  Background SW Update  Cancel  
(1) Background SW Update  Cancel  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  03h 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update Cancel (Upper)  
Data 1 :  02h Background SW Update Cancel (Lower)  
Data CRC8 :  -- 
 
(2) Background SW Update Cancel Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh 
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update Cancel (Upper)  
Data 1 :  02h Background SW Update Cancel (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 4.Error Handling ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E stops receiving the SW Update package  for Background SW Update.  
 The host can send this command after Background SW Update Start and before 
sending the last fragment of the package.  
 
(4) Error Handling  
 The host should take necessary action in case of failure.  
 The failure can be the following types:  
 Doesn’t receive the response within the timeout.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
03h(Invalid Length)  Data Length is not 03h.  
0Ah(Invalid Status)  B/E is in invalid status  
 (BG SW Update not started / completed)  
FFh( Unknown Error)  unknown error


--- Page 279 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 279/318 (5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[ BG SW Update Cancel Command]  
Command(Need ACK)[ BG SW Update Cancel Response]  
ACK


--- Page 280 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 280/318 5.8.5.  Background SW Update  
(1) Background SW Update  Command (HOST ⇒ BE) 
Start Sync :  A5h,59h  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length(2Bytes) :  0008h ~  0FFFh 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update (Upper)  
Data 1 :  03h Background SW Update (Lower)  
Data 2 ~ 3 : Fragment Number ( 2 Bytes, Big Endian ) 
Data 4  ~5  : Last Fragment Number ( 2 Bytes, Big Endian ) 
Data 6 ~ :  Data Bytes  
Data CRC8 :  -- 
 
(2) Description  
 With this command, the h ost can send the SW Update Package f or Background SW 
Update . 
 The h ost should divide the SW Update P ackage into fragments and send the 
fragments sequentially.  
 The host  can freely choose the fragment size for each transfer as long as the transfer 
size is within the maximum (0FFFh). 
 The host  is free to send other commands between two fragments.  
 The host  can cancel Background SW Update at any time before sending the last 
fragment of the SW Update Package . 
 When B/E receives the last fragment, it stops receiving the data and proceeds to 
extract the package and copy it to NAND  flash.  
 
(3) Error Handling  
 The host should take necessary action in case of failure.  
 The failure can be the following types:  
 Does not  receive the ACK or receive NAK(CRC Error)  – Host may retry or 
Cancel SW Update . 
 Receives Background SW Update Status with status (Data 2) = F Fh. 
 
(4) Sequence  
 
 
 
 
 
 
 ACK  HOST CPU  B/E 
Command(Need ACK)[ BG SW Update Command]


--- Page 281 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 281/318 5.8.6.  Background SW Update Status  
(1) Background SW Update Status  (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  A1h Background SW Update Status(Upper)  
Data 1 :  04h Background SW Update Status (Lower)  
Data 2 :  Status  
00h : Update  Complete d Successfully  
01h : Received First Fragment  
02h : Received Las t Fragment  
03h : Update Canceled  
FFh : Update Failed  (Refer to Data 3 for details)  
Data 3 :  Status = 00h ~ 03h 
00h : Fixed Value  
 
Status = FFh  
01h : Invalid Fragment  
02h : Invalid Package  
03h : Invalid Contents (Individual files NG)  
04h : Invalid Status  
FFh : Unknown Error  
Data CRC8 :  -- 
 
(2) Description  
 B/E will notify  the host of the Background SW Update Statu s. 
 B/E notifies the below events  
・ 00h : Received all fragments of the SW Update Package  and update process 
completed.  
・ 01h : Successfully completed the SW Update  
・ FFh : SW Update failed  
 In case of SW Update failure, Data 3 will give reason for  the failure  
・ 01h : Invalid Fragment including wrong fragment number.  
・ 02h : Invalid  Package  
・ 03h : Invalid contents – checksum mismatch, required files not present etc.  
・ 04h : Invalid status – BG SW n ot started, Canceled or Already completed  
・ FFh : Unknown Error  
 In case of SW Update failure, B/E will internally cancel the update. Host can restart 
the SW Update.


--- Page 282 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 282/318 (3) Sequence  
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[SW Update Status Event]


--- Page 283 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 283/318 5.9. Test & Debug Command  
5.9.1.  Test Mode  
(1) Test Mode  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h~  
Header CRC8 :  -- 
Data 0 :  F0h Test Mode (Upper)  
Data 1 :  05h Test Mode (Lower)  
Data 2 :  Video Mode  
00h : Normal Mode  
01h : Test Mode(Output Color Bar)  
Data 3 :  Audio Mode  
00h : Normal Mode  
01h: Test Mode(L/R with 1KHz/ 16bit-range sine wave)  
02h: Test Mode(L with 1KHz/ 16bit-range sine wave)  
03h: Test Mode(R with 1KHz/ 16bit-range sine wave)  
04h: Test Mode(L/R with 1KHz/ 15bit-range sine wave)  
05h: Test Mode(L with 1KHz/ 15bit-range sine wave)  
06h: Test Mode(R with 1KHz/ 15bit-range sine wave)  
07h: Pink Noise(Full -scale with L/R)  
08h: Pink Noise(Full -scale with L only)  
09h: Pink Noise(Full -scale with R only)  
Data CRC8 :  -- 
 
(2) Test Mode Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  F0h Test Mode (Upper)  
Data 1 :  05h Test Mode (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 This command is for test mode.  
 This command should be used at Idle Status.  
 If Video Mode (Data2) is 01h, Video output is color bar as the followings . 
 Can use this command for testing purposes only.  
 During test mode, only command 5.2.11. Watch Dog is accepted, and other 
commands are retuned as Invalid.  



--- Page 284 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 284/318  
・F039902182 【TRS231BSxxxx 】, F039902183 【TRH231BSxxxx 】 
 
 
 
No. Color  Signal Level *  
R G B 
① Grey  BFh BFh BFh 
② Yellow  BCh CCh 07h 
③ Cyan  10h D3h BCh 
④ Green  0Dh E0h 05h 
⑤ Magenta  AFh 00h B7h 
⑥ Red AFh 00h 00h 
⑦ Blue 00h 00h B6h 
⑧ -I 05h 43h 67h 
⑨ White  FFh FFh FFh 
⑩ +Q 3Bh 00h 73h 
⑪ Black  00h 00h 00h 
* Comply with ITU -R BT.601 studio encoding parameters.  
 
 If Audio Mode (Data3) is 01h/02h/03h/04h/05h/06h, Audio output is sine wave. It 
repeats that audio  playback for about 20 seconds and stop the short time.  
 If Audio Mode (Data3) is 07h/08h/09h, Audio output is pink noise. There will be a 
short pause every 20seconds.  
 Display resolution of Test mode is based on current  resolution setting.


--- Page 285 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 285/318 ・F039990144 【FRO232BSyyzz 】 
 
 
No. Color  Signal Level *  
Y Cb Cr 
① Grey  BFh BFh BFh 
② Yellow  BCh CCh 07h 
③ Cyan  10h D3h BCh 
④ Green  0Dh E0h 05h 
⑤ Magenta  AFh 00h B7h 
⑥ Red AFh 00h 00h 
⑦ Blue 00h 00h B6h 
⑧ -I 05h 43h 67h 
⑨ White  FFh FFh FFh 
⑩ +Q 3Bh 00h 73h 
⑪ Black  00h 00h 00h 
* Comply with ITU -R BT.601 studio encoding parameters.  
 
 If Audio Mode (Data3) is 01h/02h/03h/04h/05h/06h, Audio output is sine wave. It 
repeats that audio  playback for about 20 seconds and stop the short time.  
 If Audio Mode (Data3) is 07h/08h/09h, Audio output is pink noise. There will be a 
short pause every 20seconds.  
 Display resolution of Test mode is based on current resolution setting.


--- Page 286 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 286/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
- Data2 is not 00h or 01h.  
- Data3 is not 00h or 01h or 02h or 03h.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Test Mode Command]  
Command(Need ACK)[Test Mode Response]  
ACK  Processing


--- Page 287 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 287/318 5.9.2.  Set Debug Parameter  
(1) Set Debug Parameter  Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  04h 
Header CRC8 :  -- 
Data 0 :  F0h Set Debug Parameter (Upper)  
Data 1 :  06h Set Debug Parameter (Lower)  
Data 2 :  Monitor Mode Enable  
00h : disable(default)  
01h : enable  
FFh : Invalid Value  
Data CRC8 :  -- 
 
(2) Set Debug Parameter  Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  F0h Set Debug Parameter (Upper)  
Data 1 :  06h Set Debug Parameter (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 Set Debug Parameter for the DTV Module . 
 Data2 is the parameter for enable/disable of “ 5.9.5 .Monitor Status ”. 
 Can use this command for testing purposes only.


--- Page 288 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 288/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[Set Debug Parameter Command]  
Command(Need ACK)[Set Debug Parameter Response]  
ACK  Processing


--- Page 289 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 289/318 5.9.3.  Monitor Status  
(1) Monitor Status  Event (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  01h : Command(No Need Ack))  
Request No. :  00h ~ FFh  
Data Length :  2Bh 
Header CRC8 :  -- 
Data 0 :  F0h Monitor Status Event (Upper)  
Data 1 :  07h Monitor Status Event (Lower)  
Data 2 :  Diver Mode  
00h : Dynamic 4Diver System  
01h : Fixed 2x2Diver System  
02h : Fixed 2Diver System(Antenna Br2/3)  
03h : Fixed 4Diver System  
04h : Fixed 2Diver System(Antenna Br0/1)  
  05h : Fixed 3x1Diver System (Fore Br0/1/2)  
  06h : Dynamic 4Diver System (Fore Br2/3)  
  07h : Fixed 2x2Diver System (Fore Br2/3)  
08h : Fixed 3x1Diver System (Fore Br1/2/3)  
 
Data 3 :  Layer Status  
Bit0 : Tuner0 A -Layer (0:Invalid 1:Valid)  
Bit1 : Tuner0 B -Layer (0:Invalid 1:Valid)  
Bit2 : Tuner0 C -Layer (0:Invalid 1:Valid)  
Bit3 : Reserved  
Bit4 : Tuner1 A -Layer (0:Invalid 1:Valid)  
Bit5 : Tuner1 B -Layer (0:Invalid 1:Valid)  
Bit6 : Tuner1 C -Layer (0:Invalid 1:Valid)  
Bit7 : Reserved  
Data 4 :  Tuner0 Physical Channel Number(0Ch~34h)  
Data 5 :  Tuner0 C/N(Diver) – Upper  
Data 6 :  Tuner0 C/N(Diver) – Lower  
Data 7 :  Tuner0 A -Layer BER – Upper  
Data 8 :  Tuner0 A -Layer BER – Lower  
Data 9 :  Tuner0 A -Layer PER – Upper  
Data 10 :  Tuner0 A -Layer PER – Lower  
Data 11 :  Tuner0 B -Layer BER – Upper  
Data 12 :  Tuner0 B -Layer BER – Lower  
Data 13 :  Tuner0 B -Layer PER – Upper  
Data 14 :  Tuner0 B -Layer PER – Lower  
Data 15 :  Tuner0 C -Layer BER – Upper  
Data 16 :  Tuner0 C -Layer BER – Lower  
Data 17 :  Tuner0 C -Layer PER – Upper  
Data 18 :  Tuner0 C -Layer PER – Lower  
Data 19 :  Tuner1 Physical Channel Number(0Ch~34h)  
Data 20 :  Tuner1 C/N(Diver) – Upper  
Data 21 :  Tuner1 C/N(Diver) – Lower  
Data 22 :  Tuner1 A -Layer BER – Upper  
Data 23 :  Tuner1 A -Layer BER – Lower  
Data 24 :  Tuner1 A -Layer PER – Upper  
Data 25 :  Tuner1 A -Layer PER – Lower  
Data 26 :  Tuner1 B -Layer BER – Upper  
Data 27 :  Tuner1 B -Layer BER – Lower  
Data 28 :  Tuner1 B -Layer PER – Upper  
Data 29 :  Tuner1 B -Layer PER – Lower  
Data 30 :  Tuner1 C -Layer BER – Upper  
Data 31 :  Tuner1 C -Layer BER – Lower


--- Page 290 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 290/318 Data 32 :  Tuner1 C -Layer PER – Upper  
Data 33 :  Tuner1 C -Layer PER – Lower  
Data 34 :  Antenna0 C/N – Upper  
Data 35 :  Antenna0 C/N – Lower  
Data 36 :  Antenna1 C/N – Upper  
Data 37 :  Antenna1 C/N – Lower  
Data 38 :  Antenna2 C/N – Upper  
Data 39 :  Antenna2 C/N – Lower  
Data 40 :  Antenna3 C/N – Upper  
Data 41 :  Antenna3 C/N – Lower  
Data CRC8 :   
 
(2) Description  
 B/E notify Tuner Monitor Status to HOST in interval of 1s.  
 B/E notify to HOST CPU during Monitor Status Enable of “ 5.9.4 .Set Debug Parameter ” 
is enable.  
 If “Diver Mode (Data2)” is 02h/03h/04h, B/E use only tuner0. So, the information of 
tuner1 (Data 19~33) are all 0.  
 Tuner0 is used for Foreground processing, and Tuner1 is used for Background 
processing.  
  “Layer Status” indicates the status of each tuner and each layer by each bit.  
bit of Layer Status  Description  
Tuner0 A -Layer  0 : Data 7~10 is invalid. HOST can’t refer these data.  
1 : Data 7~10 is valid. HOST can refer these data.  
Tuner0 B -Layer  0 : Data 11~14 is invalid. HOST can’t refer these data.  
1 : Data 11~14 is valid. HOST can refer these data.  
Tuner0 C-Layer  0 : Data 15~18 is invalid. HOST can’t refer these data.  
1 : Data 15~18 is valid. HOST can refer these data.  
Tuner1 A -Layer  0 : Data 22~25 is invalid. HOST can’t refer these data.  
1 : Data 22~25 is valid. HOST can refer these data.  
Tuner1 B -Layer  0 : Data 26~29is invalid. HOST can’t refer these data.  
1 : Data 26~29 is valid. HOST can refer these data.  
Tuner1 C -Layer  0 : Data 30~33 is invalid. HOST can’t refer these data.  
1 : Data 30~33 is valid. HOST can refer these data.  
*:ISDB -T support hierarchical transmission mode include three layers (A/B/C/). Refer 
to ARIB TR -B14 “General Information of the Technical Report 4.Hierarchical 
Configuration for Operation and Available Parameters”  
 
・C/N: signed 2byte data (Divide by 100)  
・BER : unsigned 2byte data  (Divide by 1000000)  
・PER : unsigned 2byte data  (Divide by  10000 )  
・C/N range 0dB to 64.0 dB  
・BER range  0.0(No error) to 1.0 (Error  100%) 
・PER range  0.0(No error) to 1.0  (Error100%)  
・In case of  PER=100% 、 Data=2710H  
・In case of  BER=100% 、 Data=F4240H


--- Page 291 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 291/318 ・but Monitor status display until FFFFH.  This means 6.5%.  
・F/E IC cannot  count BER of 4.41% or more on a structural basis. Therefore, there is 
no problem until 6.5%.   
(3) Sequence  
 
 
 
 
 
 
  HOST CPU  B/E 
Command(No Need ACK)[Monitor Status Event]


--- Page 292 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 292/318 5.9.4.  HW Test  
(1) HW Test Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  Data2!=03h : 04h  
Data2=03h : F4h  
Header CRC8 :  -- 
Data 0 :  F0h HW Test (Upper)  
Data 1 :  08h HW Test (Lower)  
Data 2 :  Operation  
00h : HW Test start  
01h : DDR Check  
02h : Nor Flash Check  
03h : UART Check  
04h : FONT Check  
05h : RMP Check  
06h : HDMI EDID Check  
07h : Tuner I2C Check  
FFh : HW Test finish  
Data 3~242  Only UART Check  
Check Data  
Data CRC8 :  -- 
 
(2) HW Test Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h(except UART Check)  
F6h(UART Check)  
Header CRC8 :  -- 
Data 0 :  F0h HW Test (Upper)  
Data 1 :  08h HW Test (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data 4 :  Check Result  
00h : NG  
01h : OK  
Data 5 ~244  Received data by “HW Test Command”  
Data CRC8 :  -- 
 
(3) Description  
 B/E start Hardware Test.  
 If checking UART Test, HOST has to set Data3~242. F/E send Data5~244 that are 
set received data from HOST. HOST can verify check sending data and receiving 
data 
 Can use this command for testing purposes only.


--- Page 293 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 293/318 (4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.  
 The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[HW Test Command]  
Command(Need ACK)[HW Test Response]  
ACK


--- Page 294 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 294/318 5.9.5.  2nd TS Test   
(1) 2nd TS Test Command (HOST ⇒ BE) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  06h 
Header CRC8 :  -- 
Data 0 :  F0h 2nd TS Test (Upper)  
Data 1 :  09h 2nd TS Test (Lower)  
Data 2 :  Operation  
00h : start  
01h : stop  
Data 3  Physical channel Number  
13~52  
Data 4  Antenna Config  
Bit0 : Antenna 1  
Bit1 : Antenna 2  
Bit2 : Antenna 3  
Bit3 : Antenna 4  
Bit4~ : Reserved  
Data CRC8 :  -- 
 
(2) 2nd TS Test Response (BE ⇒ HOST)  
Start Sync :  A5h,5Ah  
Type :  00h : Command(Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  05h 
Header CRC8 :  -- 
Data 0 :  F0h 2nd TS Test (Upper)  
Data 1 :  09h 2nd TS Test (Lower)  
Data 2 :  Result  
  00h : OK  
  01h : NG  
Data 3 :  Result = OK :  
00h : Fixed Value  
Result = NG :  
  Error Code (Refer to “ 3.Error Code ”) 
Data CRC8 :  -- 
 
(3) Description  
 B/E start 2nd TS Test.  
 If Data2 = 00h, start “ 5.9.8 .2nd TS Test Status ” 
 If Data2 = 01h, stop “ 5.9.8 .2nd TS Test Status ” 
 Can use this command for testing purposes only.  
 
(4) Error Handling  
 In HOST, it is solely up to the product planning policy of each manufacture how to 
handle the failure of response.  
 The failure of response means that the followings:  
 Doesn’t receive the response within 1sec after HOST transmit the command.


--- Page 295 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 295/318  The result of response is NG.  
 Regarding the condition that Result of the response is NG, refer the followings:  
Error Code  Condition  
01h(Invalid Parameter)  The parameter is invalid.  
03h(Invalid Length)  Data Length is invalid.  
FFh( Unknown Error)  Unknown error  
          For other errors, refer to Chapter [3. Error Code]  
 
(5) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  ACK  HOST CPU  B/E 
Command(Need ACK)[2nd Ts Test Command]  
Command(Need ACK)[2nd Ts Test Response]  
ACK


--- Page 296 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 296/318 5.9.6.  2nd TS Test Status  
(1) 2nd TS Test Status Command ( BE ⇒ HOST ) 
Start Sync :  A5h,5Ah  
Type :  00h : Command(No Need Ack)  
Request No. :  00h ~ FFh  
Data Length :  14h 
Header CRC8 :  -- 
Data 0 :  F0h 2nd TS Test Status (Upper)  
Data 1 :  0Ah 2nd TS Test Status (Lower)  
Data 2 :  Layer Status  
Bit0 : Reserved  
Bit1 : Reserved  
Bit2 : Reserved  
Bit3 : Reserved  
Bit4 : Tuner1 A -Layer (0:Invalid 1:Valid)  
Bit5 : Tuner1 B -Layer (0:Invalid 1:Valid)  
Bit6 : Tuner1 C -Layer (0:Invalid 1:Valid)  
Bit7 : Reserved  
Data 3 :  Physical Channel Number(0Ch~34h)  
Data 4 :  C/N(Diver) – Upper  
Data 5 :  C/N(Diver) – Lower  
Data 6 :  A-Layer BER – Upper  
Data 7 :  A-Layer BER – Lower  
Data 8 :  A-Layer PER – Upper  
Data 9 :  A-Layer PER – Lower  
Data 10 :  B-Layer BER – Upper  
Data 11 :  B-Layer BER – Lower  
Data 12 :  B-Layer PER – Upper  
Data 13 :  B-Layer PER – Lower  
Data 14 :  C-Layer BER – Upper  
Data 15 :  C-Layer BER – Lower  
Data 16 :  C-Layer PER – Upper  
Data 17 :  C-Layer PER – Lower  
Data 18 :  TS Count  
Data CRC8 :  -- 
 
(2) Description  
 B/E notify 2nd TS Status to HOST.  
 B/E always transfer to HOST in interval of 1s during 2nd TS Test.


--- Page 297 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 297/318 (3) Sequence  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
  HOST CPU  B/E 
Command(Need ACK)[2nd Ts Test Status]


--- Page 298 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 298/318 6. DTV Information  
6.1. Channel List  
Information  Channel List  
Size 256KByte  
Store Time  
(Erase and Store)  100ms  
Store Condition  When receiving “Update preset table”.  
When receiving “DTV Initialize”.  
When updating Channel Information/Service Information in broadcast 
signal.  
When receiving “Shutdown” with Shutdown Mode = 01h.  
Note This data is stored for each user ID  
 
6.2. Last Channel  
Information  Last Channel  
Size 128K byte 
Store Time  
(Erase and Store)  50ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving “DTV Initialize”  
Note This data is stored for each user ID  
 
6.3. DTV Configuration  
Information  DTV Configuration  
Size 128K byte 
Store Time  
(Erase and Store)  50ms  
Store Condition  When receiving “Set auto tune Mode”.  
When receiving “Set Closed Caption Mode”.  
When receiving “Set Auto Broadcast Search Mode”.  
When receiving “Set Audio Mode”.  
When receiving “Set Residential Area”.  
When receiving “Set Auto Event Relay”.  
When receiving “DTV Initialize”.  
When receiving “Shutdown” with Shutdown Mode = 01h.  
Note This data is stored for each user ID


--- Page 299 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 299/318 6.4. DTV System  
Information  DTV System  
Size 128K byte 
Store Time  
(Erase and Store)  50ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving “Set DTV System”.  
When receiving “Set DTV Parameter”.  
Note Before SW V1.0 (TH010322), If both commands are issued in the 
same power cycle (no reboot in between the commands), the below 
order should be followed.  
 
 
 
 
 
 
 
 
6.5. TRMP Information  
Information  TRMP Information  
Size 128K byte 
Store Time  
(Erase and Store)  50ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving broadcast signal at first.  
When receiving “DTV Initialize”.  
6.6. Logo  
Information  Broadcaster Logo  
Size 256KByte  
Store Time  
(Erase and Store)  100ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving “DTV Initialize”.  
When there is data update during reception.  
 
6.7. BML Information  
Information  BML Information  
Size 512KByte  
Store Time  
(Erase and Store)  200ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving “DTV Initialize”.  
When there is data update during reception.  
 
6.8. DTV Parameter2  
Information  DTV Parameter2  
Size 128K byte 
Store Time  
(Erase and Store)  50ms  
Store Condition  When receiving “Shutdown” with Shutdown Mode = 01h.  
When receiving “Set DTV Parameter 2”. 
 
Set DTV Parameter  
Set DTV System  
Either command oka y 
Either command  okay  Before V1.0 (TH010322)  V1.0 (TH010322)  or later


--- Page 300 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 300/318 7. Background  SW Update Sequence  (Examples)  
7.1. Update Success  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
HOST CPU  
 B/E 
BG SW Update Start Command  
ACK  
BG SW Update Start Response  
ACK  
BG SW Update Command(Fragment 0 / N)  
ACK  
BG SW Update Command(Fragment 1 / N)  
ACK  
BG SW Update Command(Fragment N / N)  
ACK  
SW Update Status Event(01h, 00h)  
SW Update Status Event(02h, 00h)  
Package Extraction  
SW Update Status Event(00h, 00h)


--- Page 301 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 301/318 7.2. Update Failed – CRC Error  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
HOST CPU  
 B/E 
BG SW Update Start Command  
ACK  
BG SW Update Start Response  
ACK  
BG SW Update Command(Fragment 0 / N)  
ACK  
BG SW Update Command(Fragment 1 / N)  
ACK  
BG SW Update Command(Fragment 2 / N)  
NAK  
SW Update Status Event(01h, 00h)  
Detected CRC Error  
Cancel or Retry


--- Page 302 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 302/318 7.3. Update Failed – Invalid Fragment  
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
HOST CPU  
 B/E 
BG SW Update Start Command  
ACK  
BG SW Update Start Response  
ACK  
BG SW Update Command(Fragment 0 / N)  
ACK  
BG SW Update Command(Fragment 1 / N)  
ACK  
BG SW Update Command(Fragment 3 / N)  
ACK  
SW Update Status Event(01h, 00h)  
SW Update Status Event(FFh, 01h)  
Cancels SW Update


--- Page 303 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 303/318 8. DTV parameter and  DTV parameter 2 data range  
8.1. DTV Parameter data range  
The DTV Parameter data range is common  to following three types.  
-F039902182 【TRS231BSxxxx 】 
-F039902183 【TRH231BSxxxx 】 
-F039990144 【FRO232BSyyzz 】 
 
Data  Data name  Data range  
0 Set DTV Parameter (Upper)  01h 
1 Set DTV Parameter (Lower  1Dh 
2~5 DTV Parameter  
Enable /Disable (Use  default Parameter)  01000000h(Enable)  
00000000h(Disable)  
6~9 C/N for Tuner Unlock Detection  
 0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
10~13  BER for Tuner Unlock Detection  
 0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
14~17  PER for Tuner Unlock Detection.  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
18~21 Time for Tuner Unlock Detection  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
22~25  C/N for change to Fullseg.  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
26~29  BER for change to Fullseg  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
30~33  PER for change to Fullseg  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
34~37  Time for change to Fullseg  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
38~41  C/N for change to Oneseg  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
42~45  BER for change to Oneseg  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
46~49  PER for change to Oneseg  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
50~53  Time for change to Oneseg  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
54~57  C/N for start Broadcast Search  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
58~61  BER for start Broadcast Search  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
62~65  PER for start Broadcast Search  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
66~69  Time for start Broadcast Search  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
70~73  Time (1) for disable Broadcast Search  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
74~77  Time (2) for disable Broadcast Search  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
78~81  Time for Background Tuner Unlock 
Detection  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
82~85  C/N for start Background Search  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
86~89  Time for start Background Search  1 - 10000  (200ms -2000s)


--- Page 304 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 304/318 HEX : 00000001h - 00002710 h 
90~93  C/N for start Background Scan  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
94~97  Time for start Background Scan  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
98~101  Time for change to 4Div mode  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
102~105  C/N difference for switching to background 
channel  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
106~109  BER for switching to background channel  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
110~113  PER for switching to background channel  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
114~117  Time for switching to background channel  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
118~121  C/N for Receive Error Detection  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
122~125  BER for Receive Error Detection  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
126~129  PER for Receive Error Detection  0 - 10000  (0 - 100[%]) 
HEX : 00000000h - 00002710 h 
130~133  Time for Receive Error Detection  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
134~137  C/N for Fullseg Detection at fixed Fullseg 
search  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
138~141  C/N for Oneseg Detection at fixed or auto 
switch mode search  0 - 44100  (0 – 4.41[%]) 
HEX : 00000000h - 0000AC44h  
142~145  Detect Time (count) for other broadcast  
(The data value becomes the time as it is ) 1 - 2147483647 [s] 
HEX : 00000001h - 7FFFFFFF h 
146~149  Detect During Time for Another broadcast  1 - 10000  (200ms -2000s)  
HEX : 00000001h - 00002710 h 
150~153  C/N Offset for Fullseg Detection at fixed 
Fullseg broadcast search  0 - 4000 [0 - 40dB] 
HEX : 00000000h - 00000FA0h  
154~157  Reserved   
158~161  Reserved   
162~165  Reserved   
166~169  Reserved   
170~173  Reserved   
174~177  Reserved   
178~181  Reserved   
182~185  Reserved   
186~189  Reserved   
190~193  Reserved   
194~197  Reserved   
198~201  Reserved   
202~205  Reserved   
206~209  Reserved   
210~213  Reserved   
214~217  Reserved   
218~221  Reserved   
222~225  Reserved   
226 CRC8   
・C/N: signed 4byte data (Divide by 100)  
・BER : unsigned 4byte data  (Divide by 1000000)  
・PER : unsigned 4byte data  (Divide by  10000 )


--- Page 305 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 305/318 ・Time ： unsigned 4byte data ( Multiply  by 0.2)  
・C/N range 0dB to 4 0.0 dB  
・BER range  0.0 000 (No error) to 0.0441 (Error  4.41%) 
・PER range  0.0(No error) to 1.0  (Error100%)  
・Time  range  200ms  to 2000s (Excluding Data 142 to 145)  
 
8.2. DTV Parameter 2 data range for Thrush  
The DTV Parameter 2 data range for Thrush is common to following two types.  
-F039902182 【TRS231BSxxxx 】 
-F039902183 【TRH231BSxxxx 】 
Data  Data name  Data range  
0 Set DTV Parameter 2 (Upper)  01h 
1 Set DTV Parameter 2 (Lower  35h 
2 DTV Parameter 2 
Enable/Disable(Use default Parameter)  01h(Enable)  
00h(Disable)  
3 Auto tune mode default  
00h:Auto  
01h:Fullseg  
02h:Oneseg  
03h:Auto with Seamless  0 - 3 
HEX : 00h – 03h 
4 Default Character Set  
 00h:ARIB  
 01h:UTF -8 0 - 1 [%] 
HEX : 00h - 01h 
5 Default Video Resolution  
 00h:720p  
 01h:480p  
 02h:1080p  
 03h:480i  
 04h:1080p@30Hz  0 -4 
HEX : 00h - 04h 
6 Closed Caption display over BML browser  
Enable/Disable  00h(Enable  Display ) 
01h(Disable  Display ) 
7 BML Error Message  
Enable/Disable  00h(Enable Display)  
01h(Disable Display)  
8 Receive Logo Type  
 0 : Receive,   1 : Not Receive  
    Bit7: 0 (Fixed)  
    Bit6: 0 (Fixed)  
    Bit5: Logo Type 5  
    Bit4: Logo Type 4  
    Bit3: Logo Type 3  
    Bit2: Logo Type 2  
    Bit1: Logo Type 1  
    Bit0: Logo Type 0  00XXXXXXb  
9 Search Detection Timeout  1 - 10 [s] 
HEX : 01 – 0Ah 
10~11  C/N for Receive Error Detection for Fix Fullseg 
mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
12~13  C/N for Preset Scan Detection for Fix Oneseg 
mode and Auto mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
14~15  C/N for Preset Scan Detection for Fix Fullseg 
mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
16 Timeout for Preset Scan per channel  0 - 10 [s]


--- Page 306 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 306/318 HEX : 00h - 0Ah 
17~18  C/N Level 3 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
19~20  C/N Level 2 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
21~22  C/N Level 1 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
23~24  EPG Update scan time / channel  1 - 180 [s]  
HEX : 0001h – 00B4h  
25 EPG Scan Number of Days  
(Only foreground EPG Scan)  1 - 8 [day]  
HEX : 01h - 08h 
26~27  EPG Scan Signal Threshold  
(Only foreground EPG Scan)  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
28~29  Audio Const offset for Fullseg  0 - 1000[ms]  
HEX : 0000h - 03E8h  
30~31  Audio Const offset for Oneseg  0 - 1000[ms]  
HEX : 0000h - 03E8h  
32 Event relay : Auto Event relay On/Off  
*When this configured as off, notification will be 
skipped  00h : OFF  
01h : ON  
33 Event relay : Notification interval before 
switching  [s] 0 or 5 - 30 [s] 
HEX : 00h or 05h - 1Eh 
34 Event relay : Number of notifications before 
switching  [times]  0 - 6 [times]  
HEX : 00h - 06h 
35~36  Banner : Banner Position X  0 - 1280  
HEX : 0000h - 0500h  
37~38  Banner : Banner Position Y  0 - 720  
HEX : 0000h – 02D0h  
39 Banner : Font Size [px] 24 - 40 [px] 
HEX : 18h - 28h 
40 Banner : Transparency [%]  0 - 100 [%]  
HEX : 00h - 64h 
41 Banner :  Logo Position Offset  [px] -128 - 127 [px] 
HEX : 80h - 7Fh 
42 Banner : Margin of Top and Bottom [px] 0 – 50 [px] 
HEX : 00h - 32h 
43 Banner : Margin of Left and Right [px] 0 – 50 [px] 
HEX : 00h - 32h 
44 Banner : Line spacing [px] 0 – 50 [px] 
HEX : 00h - 32h 
45 Banner : Max number of characters  1 - 255  
HEX : 01h - FFh 
46 Banner : Default Timeout [s]  
 0 : No timeout (Continue to display until Hide 
Banner)  
 1 – 255 : Display Time  0 or 1 - 255[s]  
HEX : 00h or 01h - FFh 
47 EPG List: Type Enable  
  0 : Enable,  1: Disable  
    Bit7: T.B.D  
    Bit6: T.B.D  
    Bit5: T.B.D  
    Bit4: T.B.D  
    Bit3: Type 4 Enable  
    Bit2: Type 3 Enable  
    Bit1: Type 2 Enable  
    Bit0: Type 1 Enable  
Range : 0 to 14  0 - 15  
HEX : 00h – 0Eh


--- Page 307 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 307/318 48 EPG List: Type1 Program name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
49 EPG List: Type1 TS Name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
50 EPG List: Type1 EPG Content Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
51 EPG List: Type2 Program name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
52 EPG List: Type2 TS Name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
53 EPG List Type2 EPG Content Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
54 EPG List: Type3 Program name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
55 EPG List: Type3 TS Name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
56 EPG List: Type3 EPG Content Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
57 EPG List: Type4 Program name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
58 EPG List: Type4 TS Name Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
59 EPG List: Type4 EPG Content Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
60 EPG List: Table Title Color Red  0 - 255 
HEX : 00h - FFh 
61 EPG List: Table Title Color Green  0 - 255 
HEX : 00h - FFh 
62 EPG List: Table Title Color Blue  0 - 255 
HEX : 00h - FFh 
63 EPG List: Table Title Font Color Red  0 - 255 
HEX : 00h - FFh 
64 EPG List: Table Title Font Color Green  0 - 255 
HEX : 00h - FFh 
65 EPG List: Table Title Font Color Blue  0 - 255 
HEX : 00h - FFh 
66 EPG List: Cursor Color Red  0 - 255 
HEX : 00h - FFh 
67 EPG List: Cursor Color Green  0 - 255 
HEX : 00h - FFh 
68 EPG List: Cursor Color Blue  0 - 255 
HEX : 00h - FFh 
69 EPG List: Cursor Font Color Red  0 - 255 
HEX : 00h - FFh 
70 EPG List: Cursor Font Color Green  0 - 255 
HEX : 00h - FFh 
71 EPG List: Cursor Font Color Blue  0 - 255 
HEX : 00h - FFh 
72 EPG List: Current Program Color Red  0 - 255 
HEX : 00h - FFh 
73 EPG List: Current Program Color Green  0 - 255 
HEX : 00h - FFh 
74 EPG List: Current Program Color Blue  0 - 255 
HEX : 00h - FFh 
75 EPG List: Current Program Font Color Red  0 - 255 
HEX : 00h - FFh 
76 EPG List: Current Program Font Color Green  0 - 255


--- Page 308 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 308/318 HEX : 00h - FFh 
77 EPG List: Current Program Font Color Blue  0 - 255 
HEX : 00h - FFh 
78 EPG List: Balloon color Red  0 - 255 
HEX : 00h - FFh 
79 EPG List: Balloon color Green  0 - 255 
HEX : 00h - FFh 
80 EPG List: Balloon color Blue  0 - 255 
HEX : 00h - FFh 
81 EPG List: Balloon Font color Red  0 - 255 
HEX : 00h - FFh 
82 EPG List: Balloon Font color Green  0 - 255 
HEX : 00h - FFh 
83 EPG List: Balloon Font color Blue  0 - 255 
HEX : 00h - FFh 
84 EPG List: Border line color Red  0 - 255 
HEX : 00h - FFh 
85 EPG List: Border line color Green  0 - 255 
HEX : 00h - FFh 
86 EPG List: Border line color Blue  0 - 255 
HEX : 00h - FFh 
87 EPG Information: Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
88 EPG Information: Title Font Color Red  0 - 255 
HEX : 00h - FFh 
89 EPG Information: Title Font Color Green  0 - 255 
HEX : 00h - FFh 
90 EPG Information: Title Font Color Blue  0 - 255 
HEX : 00h - FFh 
91 EPG Information: Line Spacing for Title  0 - 255 
HEX : 00h - FFh 
92 EPG Information: Line Spacing for Contents  0 - 255 
HEX : 00h - FFh 
93 EPG Information: Margin  0 - 80 
HEX : 00h - 50h 
94 Default Auto Broadcast Search mode  
0:Automatic Broadcast Search Off  
1:Automatic Relay Station Search On  
2:Automatic Affiliated Station Search On  
3:Automatic Relay & Affiliated Station Search 
On 0 - 3 
HEX : 00h -03h 
95~96  C/N Level 3 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
97~98  C/N Level 2 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
99~100  C/N Level 1 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
101 Default event mask 0  
bit0 : DTV Status  
bit1 : Scan Status  
bit2 : Search Status  
bit3 : DTV Event  
bit4 : EWS Event  
bit5 : EPG Status  
bit6 : Event relay  
bit7 : Number of Program info  
0 : Not Mask  0 - 255 
HEX : 00h - FFh


--- Page 309 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 309/318 1 : Mask - Disables the event notification.  
102 Default event mask 1bit0 : Program Information  
bit1 : Program Information with UTF -8 
bit2 : TS Name Update  
bit3 : TS Name Update with UTF -8 
bit4 : Logo Update  
bit5 : EGP Button Status  
bit6 : BML Status  
bit7 : C/N Information  
0 : Not Mask  
1 : Mask - Disables the event notification.  0 - 255 
HEX : 00h - FFh 
103 Default event mask 2  
bit0 : EPG Scan Result  
bit1 - bit7 :Reserved  0 - 255 
HEX : 00h - FFh 
104 EPG List: Short program border line color Red  0 - 255 
HEX : 00h - FFh 
105 EPG List: Short program border line color 
Green  0 - 255 
HEX : 00h - FFh 
106 EPG List: Short program border line color Blue  0 - 255 
HEX : 00h - FFh 
107 Banner segment icon  
Enable/Disable  00h(Enable)  
01h(Disable)  
108 Number of scrolling line on EPG detail  1 - 255 
HEX : 01h - FFh 
109 Automatic banner display  
Enable/Disable  00h(Enable)  
01h(Disable)  
110 Reserved   
111 Reserved   
112 Reserved   
113 Reserved   
114 Reserved   
115 Reserved   
116 Reserved   
117 Reserved   
118 Reserved   
119 Reserved   
120 Reserved   
121 Reserved   
122 Reserved   
123 Reserved   
124 Reserved   
125 Reserved   
126 Reserved   
127 Reserved   
128 Reserved   
129 Reserved   
130 Reserved   
131 Reserved   
132 Reserved   
133 Reserved   
134 Reserved   
135 Reserved   
136 Reserved   
137 Reserved   
138 Reserved   
139 Reserved


--- Page 310 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 310/318 140 Reserved   
141 Reserved   
142 Reserved   
143 Reserved   
144 Reserved   
145 Reserved   
146 Reserved   
147 Reserved   
148 Reserved   
149 Reserved   
150 Reserved   
151 Reserved   
152 Reserved   
153 Reserved   
154 Reserved   
155 Reserved   
156 Reserved   
157 Reserved   
158 Reserved   
159 Reserved   
160 Reserved   
161 Reserved   
162 Reserved   
163 Reserved   
164 Reserved   
165 Reserved   
166 Reserved   
167 Reserved   
168 Reserved   
169 Reserved   
170 Reserved   
171 Reserved   
172 Reserved   
173 Reserved   
174 Reserved   
175 Reserved   
176 Reserved   
177 Reserved   
178 Reserved   
179 Reserved   
180 Reserved   
181 Reserved   
182 Reserved   
183 Reserved   
184 Reserved   
185 Reserved   
186 Reserved   
187 Reserved   
188 Reserved   
189 Reserved   
190 Reserved   
191 Reserved   
192 Reserved   
193 Reserved   
194 Reserved


--- Page 311 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 311/318 195 Reserved   
196 Reserved   
197 Reserved   
198 Reserved   
199 Reserved   
200 Reserved   
201 Reserved   
202 Reserved   
203 Reserved   
204 Reserved   
205 Reserved   
206 Reserved   
207 Reserved   
208 Reserved   
209 Reserved   
210 Reserved   
211 Reserved   
212 Reserved   
213 Reserved   
214 Reserved   
215 Reserved   
216 Reserved   
217 Reserved   
218 Reserved   
219 Reserved   
220 Reserved   
221 Reserved   
222 Reserved   
223 Reserved   
224 Reserved   
225 Reserved   
226 CRC8   
・C/N: signed 4byte data (Divide by 100) 
・C/N range 0dB to 4 0.0 dB  
 
8.3. DTV Parameter 2 data range  for N ew Frontier  
The DTV Parameter 2 data range for New Frontier is  adapted  to following two type.  
-F039990144 【FRO232BSyyzz 】 
Some parameters are not supported.( Not support ones are marked with strikethrough ) 
Data  Data name  Data range  
0 Set DTV Parameter 2 (Upper)  01h 
1 Set DTV Parameter 2 (Lower  35h 
2 DTV Parameter 2  
Enable/Disable(Use default Parameter)  01h(Enable)  
00h(Disable)  
3 Auto tune mode default  
00h:Auto  
01h:Fullseg  
02h:Oneseg  
03h:Auto with Seamless  0 - 3 
HEX : 00h – 03h 
4 Default Character Set  
 00h:ARIB  
 01h:UTF -8 0 - 1 [%]  
HEX : 00h - 01h 
5 Default Video Resolution  0 -4


--- Page 312 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 312/318  00h:720p  
 01h:480p  
 02h:1080p  
 03h:480i  
 04h:1080p@30Hz  HEX : 00h - 04h 
6 Closed Caption display over BML browser  
Enable/Disable  00h(Enable Display)  
01h(Disable Display)  
7 BML Error Message  
Enable/Disable  00h(Enable Display)  
01h(Disable Display)  
8 Receive Logo Type  
 0 : Receive,   1 : Not Receive  
    Bit7: 0 (Fixed)  
    Bit6: 0 (Fixed)  
    Bit5: Logo Type 5  
    Bit4: Logo Type 4  
    Bit3: Logo Type 3  
    Bit2: Logo Type 2  
    Bit1: Logo Type 1  
    Bit0: Logo Type 0  00XXXXXXb  
9 Search Detection Timeout  1 - 10 [s]  
HEX : 01 – 0Ah 
10~11  C/N for Receive Error Detection for Fix Fullseg 
mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
12~13  C/N for Preset Scan Detection for Fix Oneseg 
mode and Auto mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
14~15  C/N for Preset Scan Detection for Fix Fullseg 
mode  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
16 Timeout for Preset Scan per channel  0 - 10 [s]  
HEX : 00h - 0Ah 
17~18  C/N Level 3 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
19~20  C/N Level 2 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
21~22  C/N Level 1 threshold for full seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
23~24  EPG Update scan time / channel  1 - 180 [s]  
HEX : 0001h – 00B4h  
25 EPG Scan Number of Days  
(Only foreground EPG Scan)  1 - 8 [day]  
HEX : 01h - 08h 
26~27  EPG Scan Signal Threshold  
(Only foreground EPG Scan)  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
28~29  Audio Const offset for Fullseg  0 - 1000[ms]  
HEX : 0000h - 03E8h  
30~31  Audio Const offset for Oneseg  0 - 1000[ms]  
HEX : 0000h - 03E8h  
32 Event relay : Auto Event relay On/Off  
*When this configured as off, notification will be 
skipped  00h : OFF  
01h : ON  
33 Event relay : Notification interval before 
switching  [s] 0 or 5 - 30 [s] 
HEX : 00h or 05h - 1Eh 
34 Event relay : Number of notifications before 
switching  [times]  0 - 6 [times]  
HEX : 00h - 06h 
35~36  Banner : Banner Position X  0 - 720  
HEX : 0000h – 02D0h 
37~38  Banner : Banner Position Y  0 - 480  
HEX : 0000h – 01E0h 
39 Banner : Font Size [px] 18 - 24 [px]


--- Page 313 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 313/318 HEX : 1 2h - 18h 
40 Banner : Transparency [%]  0 - 100 [%]  
HEX : 00h - 64h 
41 Banner :  Logo Position Offset  [px] -128 - 127 [px] 
HEX : 80h - 7Fh 
42 Banner : Margin of Top and Bottom  0 – 50 [px] 
HEX : 00h - 32h 
43 Banner : Margin of Left and Right [px] 0 – 50 [px] 
HEX : 00h - 32h 
44 Banner : Line spacing [px] 0 – 50 [px] 
HEX : 00h - 32h 
45 Banner : Max number of characters  1 – 255 
HEX : 01h - FFh 
46 Banner : Default Timeout [s]  
 0 : No timeout (Continue to display until Hide 
Banner)  
 1 – 255 : Display Time  0 or 1 – 255 [s] 
HEX : 00h or 01h - FFh 
47 EPG List: Type Enable  
  0 : Enable,  1: Disable  
    Bit7: T.B.D  
    Bit6: T.B.D  
    Bit5: T.B.D  
    Bit4: T.B.D  
    Bit3: Type 4 Enable  
    Bit2: Type 3 Enable  
    Bit1: Type 2 Enable  
    Bit0: Type 1 Enable  
Range : 0 to 14  0 - 15  
HEX : 00h – 0Eh 
48 EPG List: Type1 Program name Font Size  [px] 18 – 24 [px] 
HEX : 1 2h - 18h 
49 EPG List: Type1 TS Name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
50 EPG List: Type1 EPG Content Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
51 EPG List: Type2 Program name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
52 EPG List: Type2 TS Name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
53 EPG List Type2 EPG Content Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
54 EPG List: Type3 Program name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
55 EPG List: Type3 TS Name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
56 EPG List: Type3 EPG Content Font Size  [px] 24 – 40 [px] 
HEX : 18h - 28h 
57 EPG List: Type4 Program name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
58 EPG List: Type4 TS Name Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
59 EPG List: Type4 EPG Content Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
60 EPG List: Table Title Color Red  0 - 255 
HEX : 00h - FFh 
61 EPG List: Table Title Color Green  0 - 255 
HEX : 00h - FFh 
62 EPG List: Table Title Color Blue  0 - 255


--- Page 314 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 314/318 HEX : 00h - FFh 
63 EPG List: Table Title Font Color Red  0 - 255 
HEX : 00h - FFh 
64 EPG List: Table Title Font Color Green  0 - 255 
HEX : 00h - FFh 
65 EPG List: Table Title Font Color Blue  0 - 255 
HEX : 00h - FFh 
66 EPG List: Cursor Color Red  0 - 255 
HEX : 00h - FFh 
67 EPG List: Cursor Color Green  0 - 255 
HEX : 00h - FFh 
68 EPG List: Cursor Color Blue  0 - 255 
HEX : 00h - FFh 
69 EPG List: Cursor Font Color Red  0 - 255 
HEX : 00h - FFh 
70 EPG List: Cursor Font Color Green  0 - 255 
HEX : 00h - FFh 
71 EPG List: Cursor Font Color Blue  0 - 255 
HEX : 00h - FFh 
72 EPG List: Current Program Color Red  0 - 255 
HEX : 00h - FFh 
73 EPG List: Current Program Color Green  0 - 255 
HEX : 00h - FFh 
74 EPG List: Current Program Color Blue  0 - 255 
HEX : 00h - FFh 
75 EPG List: Current Program Font Color Red  0 - 255 
HEX : 00h - FFh 
76 EPG List: Current Program Font Color Green  0 - 255 
HEX : 00h - FFh 
77 EPG List: Current Program Font Color Blue  0 - 255 
HEX : 00h - FFh 
78 EPG List: Balloon color Red  0 - 255 
HEX : 00h - FFh 
79 EPG List: Balloon color Green  0 - 255 
HEX : 00h - FFh 
80 EPG List: Balloon color Blue  0 - 255 
HEX : 00h - FFh 
81 EPG List: Balloon Font color Red  0 - 255 
HEX : 00h - FFh 
82 EPG List: Balloon Font color Green  0 - 255 
HEX : 00h - FFh 
83 EPG List: Balloon Font color Blue  0 - 255 
HEX : 00h - FFh 
84 EPG List: Border line color Red  0 - 255 
HEX : 00h - FFh 
85 EPG List: Border line color Green  0 - 255 
HEX : 00h - FFh 
86 EPG List: Border line color Blue  0 - 255 
HEX : 00h - FFh 
87 EPG Information:  Font Size  [px] 18 – 24 [px] 
HEX : 12h - 18h 
88 EPG Information: Title Font Color Red  0 - 255 
HEX : 00h - FFh 
89 EPG Information: Title Font Color Green  0 - 255 
HEX : 00h - FFh 
90 EPG Information: Title Font Color Blue  0 - 255 
HEX : 00h - FFh


--- Page 315 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 315/318 91 EPG Information: Line Spacing for Title  0 - 255 
HEX : 00h - FFh 
92 EPG Information: Line Spacing for Contents  0 - 255 
HEX : 00h - FFh 
93 EPG Information: Margin  0 - 80 
HEX : 00h - 50h 
94 Default Auto Broadcast Search mode  
0:Automatic Broadcast Search Off  
1:Automatic Relay Station Search On  
2:Automatic Affiliated Station Search On  
3:Automatic Relay & Affiliated Station Search 
On 0 - 3 
HEX : 00h -03h 
95~96  C/N Level 3 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
97~98  C/N Level 2 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
99~100  C/N Level 1 threshold for one seg  0 - 4000 [0 - 40dB] 
HEX : 0000h - 0FA0h  
101 Default event mask 0  
bit0 : DTV Status  
bit1 : Scan Status  
bit2 : Search Status  
bit3 : DTV Event  
bit4 : EWS Event  
bit5 : EPG Status  
bit6 : Event relay  
bit7 : Number of Program info  
0 : Not Mask  
1 : Mask - Disables the event notification.  0 - 255 
HEX : 00h - FFh 
102 Default event mask 1bit0 : Program Information  
bit1 : Program Information with UTF -8 
bit2 : TS Name Update  
bit3 : TS Name Update with UTF -8 
bit4 : Logo Update  
bit5 : EGP Button Status  
bit6 : BML Status  
bit7 : C/N Information  
0 : Not Mask  
1 : Mask - Disables the event notification.  0 - 255 
HEX : 00h - FFh 
103 Default event mask 2  
bit0 : EPG Scan Result  
bit1 - bit7 :Reserved  0 - 255 
HEX : 00h - FFh 
104 EPG List: Short program border line color Red  0 - 255 
HEX : 00h - FFh 
105 EPG List: Short program border line color 
Green  0 - 255 
HEX : 00h - FFh 
106 EPG List: Short program border line color Blue  0 - 255 
HEX : 00h - FFh 
107 Banner segment icon  
Enable/Disable  00h(Enable)  
01h(Disable)  
108 Number of scrolling line on EPG detail  1 - 255 
HEX : 01h - FFh 
109 Automatic banner display  
Enable/Disable  00h(Enable)  
01h(Disable)  
110 Reserved   
111 Reserved   
112 Reserved


--- Page 316 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 316/318 113 Reserved   
114 Reserved   
115 Reserved   
116 Reserved   
117 Reserved   
118 Reserved   
119 Reserved   
120 Reserved   
121 Reserved   
122 Reserved   
123 Reserved   
124 Reserved   
125 Reserved   
126 Reserved   
127 Reserved   
128 Reserved   
129 Reserved   
130 Reserved   
131 Reserved   
132 Reserved   
133 Reserved   
134 Reserved   
135 Reserved   
136 Reserved   
137 Reserved   
138 Reserved   
139 Reserved   
140 Reserved   
141 Reserved   
142 Reserved   
143 Reserved   
144 Reserved   
145 Reserved   
146 Reserved   
147 Reserved   
148 Reserved   
149 Reserved   
150 Reserved   
151 Reserved   
152 Reserved   
153 Reserved   
154 Reserved   
155 Reserved   
156 Reserved   
157 Reserved   
158 Reserved   
159 Reserved   
160 Reserved   
161 Reserved   
162 Reserved   
163 Reserved   
164 Reserved   
165 Reserved   
166 Reserved   
167 Reserved


--- Page 317 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 317/318 168 Reserved   
169 Reserved   
170 Reserved   
171 Reserved   
172 Reserved   
173 Reserved   
174 Reserved   
175 Reserved   
176 Reserved   
177 Reserved   
178 Reserved   
179 Reserved   
180 Reserved   
181 Reserved   
182 Reserved   
183 Reserved   
184 Reserved   
185 Reserved   
186 Reserved   
187 Reserved   
188 Reserved   
189 Reserved   
190 Reserved   
191 Reserved   
192 Reserved   
193 Reserved   
194 Reserved   
195 Reserved   
196 Reserved   
197 Reserved   
198 Reserved   
199 Reserved   
200 Reserved   
201 Reserved   
202 Reserved   
203 Reserved   
204 Reserved   
205 Reserved   
206 Reserved   
207 Reserved   
208 Reserved   
209 Reserved   
210 Reserved   
211 Reserved   
212 Reserved   
213 Reserved   
214 Reserved   
215 Reserved   
216 Reserved   
217 Reserved   
218 Reserved   
219 Reserved   
220 Reserved   
221 Reserved   
222 Reserved


--- Page 318 ---


Confidential  2024/9/5 
MN:OEC -BT-0007 -E 
ID:P1505 -S01-0009  OKAYA ELECTRONICS  
M’s STYLE TECHNOLOGY  
 
 
 318/318 223 Reserved   
224 Reserved   
225 Reserved   
226 CRC8   
・C/N: signed 4byte data (Divide by 100) 
・C/N range 0dB to 4 0.0 dB  
・Data in gray is where the configuration is not supported.