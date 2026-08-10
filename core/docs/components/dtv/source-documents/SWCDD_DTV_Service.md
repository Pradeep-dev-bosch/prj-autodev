SW Concept and Design Description

DTV Service – CCS2.0

Version:        1.1  ;  01.04.2024

Status:          Release

Date: Klicken Sie hier, um ein Datum einzugeben.

General Approval Form 

[Approval Data / Link]

Distribution list

Name/Department

Role in project

Suma Anand (MS/ECR4-XC)

Project Manager

Bharadwaj Chaitra (MS/ECR4-XC)

Component Architect

N.N.

Safety Manager (if applicable)

Recipients: add further stakeholders if needed

Reviewer list

Name/Department

Role in project

Reviewer or approver

Dasharatha Arunkumar (XC-CT/ERN4-E)

Component Product Owner

Approver

Bharadwaj Chaitra (MS/ECR4-XC)

Component Architect

Approver

N.N.

Safety Team (if applicable)

Reviewer

Akash Bhasker (MS/ECR4-XC) 

SW-Contributor

Reviewer

Han Van Thi (MS/EMC23-XC)

SW-Contributor

Reviewer

Nguyen Quoc Dat (MS/EMC23-XC)

SW-Contributor

Reviewer

Tra Vu Anh (MS/EMC23-XC)

SW-Contributor

Reviewer

Changes are announced via stages update information, no distribution as printed version, 

provision in the Intranet: see footer

Table of content

# Contents

1List of Terms and Abbreviations5

1.1Annotations5

2Purpose of this Document6

3Introduction to the Subsystem6

4Architecture Driving Requirement Groups7

5Use Cases9

5.1Use case view9

6High Level Design9

6.1Static Software Architecture and Deployment to Domains9

6.2Provided Interfaces / User Handbook10

6.3Dynamic Design on High Level10

6.3.1Auto Preset11

6.3.2Dtv Channel Up Down11

6.3.3Dtv Signal Status12

6.3.4Dtv Channel Seek12

6.3.5Dtv Manual Preset Channel Store13

6.3.6DTV Reception Monitor14

6.3.7Set Physical Channel15

6.3.8Get Version16

6.3.9Test Mode Output17

6.3.10Get Preset List18

6.3.11Manual Preset Channel Store19

6.3.12Get Program Info20

6.3.13Get RMP Manufacturer ID Display20

6.3.14Display Banner22

6.3.15DTV Status Event23

6.3.16Get Configure24

6.3.17DTV Initialize24

6.3.18Program Information Update Event25

6.3.19Select Direct Channel25

6.3.20Set Audio Mode26

6.3.21Set Auto Tune Mode26

6.3.22Set Closed Caption Mode27

6.3.23Set Broadcast Search Mode27

6.3.24Set Event Relay Mode27

6.3.25Display EPG28

6.3.26Residential Area30

6.3.27Audio ES31

6.3.28Set Auto Broadcast Search Mode31

6.3.29Broadcast Search32

6.3.30BML Browser35

6.3.31EWS Event37

6.3.32DTV Event Update38

6.3.33DTV Firmware Update39

6.3.34DTV Module Status Notification40

6.4Suspend to Disk40

7Detailed Design42

7.1Static Design on Detail Level42

7.1.1Class interaction diagram42

7.2Analyzed Alternatives42

7.3Dynamic Design on Detail Level42

7.4Concurrency / Threading Model42

7.5Data Model View43

7.5.1Storage Mechanism43

7.5.2Data List44

7.5.3Configuration44

7.6Critical Computer Resources (CPU, RAM, Flash)44

7.7Install View44

7.8Security User and Groups45

8Testing & Debugging45

8.1.1Test Handling Implementation45

8.2CTS45

8.2.1CTS Test Cases46

8.2.2How to run CTS testcases46

9Requirements to other Components46

9.1Audio Requirements46

1.Audio Focus management support46

10Source Code Reference46

11Open Points47

12References and Related Documents47

13Contacts47

14Amendments47

14.1Revision History47

Each chapter has comments to guide the author. 

This hint shall be deleted when the document will be released.

You can use “hidden text” to add information that should not be delivered to a third party. Don’t deliver Word documents, please use pdf export for that issue.

# List of Terms and Abbreviations

Term or Abbreviation

Description

Component Model

In the IEEE standard 1026-1998 the component model is called the decomposition view and in RUP it is called the logical view.

Design Pattern

General approach to solve a common design problem, e.g. observer pattern. A design pattern consists of a problem statement, a solution and consequences (pros and cons). 

Dynamic Model

A set of classes that work together to realize a use case, also called collaboration or mechanistic design. In the IEEE standard 1026-1998 the dynamic model is called the dependency description.

IDL

Interface Definition Language

RM

Requirement Management

State Chart

State charts are a formal behavioral language. State charts are particularly effective when the use case is reactive; that is, it has inherent states (conditions) and remains in those conditions until an event of interest has occurred. A state chart is more precise and less likely to be misinterpreted than text, but it is harder to understand. Therefore it should be used together with text and sequence diagrams.

Subsystem

An assigned area of functional responsibility

SW

Software

SWAD

Software Architecture Document

Use Case 

A use case is a named capability of a structural entity in a model. Use cases organize requirements into chunks. They help to detect open requirements. It is common for a use case to represent and organize many pages of textual requirements or dozens of usage scenarios.

AAOS

Android Automotive Operating System

iAP2

iPod Accessory Protocol version 2

USB

Universal Serial Bus

MD

Mobile Device

HU

Head Unit

SPI

Smartphone Integration

JNI

Java Native Interface

## Annotations

Annotation

Description

@ASSUMPTION

This annotation at the beginning of a sentence, paragraph or statement marks the following description as something that the author assumed as true, although it is not (yet) proven.

@PRELIMANARY

This annotation at the beginning of a sentence, paragraph or statement marks the following description as something that is true at time of writing, but might change in the (near) future or still need clarification.

@TODO

This annotation at the beginning of a sentence, paragraph or statement marks something that needs to be described. Used by the author to mark open topics. 

For functional safety related parts none of the annotations is allowed at time of release.

# Purpose of this Document

This document is used to record results of architecture and design activities for DTV Service component on Android Systems. The document contains both the high level as well as the detailed design. It describes the behavior and how the SW interact with the remaining system. The document shows how the SW part will be arranged to satisfy the requirements and guide the developers for the implementation and maintenance phases. It also provides an understanding, which kinds of requirements are related to which design entities (such like SW components or modules).

# Introduction to the Subsystem

DTV Service is a software module which is a part of the Framework Service in the android software stack. The purpose of this module is to act as a mediator between client Application and DTV HAL to provide DTV related functionalities. The audio and video rendering is not in the scope of DTV service module and is completely handled in MediaInput Service Software module.

The below diagram Figure 1 illustrates DTV Service in the Android Software Stack

Figure 1

DTV Service provides AIDL interface for the Applications to avail DTV related functionalities. DTV Service further interacts with DTV HAL through the HIDL provided by DTV HAL.

DTV Service consists of the following 

com.bosch.service.dtv:  The Service which registers with Service Manager and provides service to clients         

This service hosts the below libraries

libdtv_interface: Java Library providing the AIDL interface and DTV Manager

libdtv_jni: JNI Library for interacting with native DTV HAL

libdtv_modulespec: Native Library for 

Formatting and serializing the AIDL request data to DTV UART required format

Formatting and deserializing the response and events, from DTV UART format to AIDL required format

The below diagram Figure 2 illustrates the subsystem for DTV Service.

                     Figure 2

The more details regarding the interaction between DTV Service and other modules are explained in the later part of this document.

# Architecture Driving Requirement Groups 

There are two major Architecture Driving Requirement Groups for DTV Service

- DTV HAL

- Client DTV Application

Below are the major requirements fulfilled in DTV Service component.

ReqNo

Program Epic

Requirements

Details

R1

CCS2-1617

[DTV] Channel Seek Up/Down

R2

CCS2-3554

[DTV] Auto Preset for TV1/TV2

R3

CCS2-3555

[DTV] Preset List Retrieve/Update for TV1/TV2

R5

CCS2-3557

[DTV] Program Information Notification

R6

CCS2-3556

[DTV] Preset Channel Select/Store for TV1/TV2

R7

CCS2-4631

[DTV] Channel Up/Down (Next/Previous)

R8

CCS2-1613

[DTV] Antenna Phantom voltage enable

R9

CCS2-1612

[DTV] Audio Streaming

R10

CCS2-3573

[DTV] Signal Status (Weak / No signal) / No Service Notification 

R11

CCS2-3558

[DTV] Antenna Bars Level (0/1/2/3) Notification

R12

CCS2-3559

[DTV] Display Banner (overlaid on TV video)

R13

CCS2-3572

[DTV] Direct Channel Input (3 Digits Channel Number)

R14

CCS2-3560

[DTV] Manual Foreground Broadcast Search (Relay/Affiliated Station)

R15

CCS2-3561

[DTV] Automatic Foreground Broadcast Search (Relay/Affiliated Station)

R16

CCS2-3563

[DTV] EWS (Emergency Warning Service) Notification

R17

CCS2-3564

[DTV] Initialization (TV1 / TV2 / Settings / Factory Reset)

R18

CCS2-3565

[DTV] TV Settings: Basics

R19

CCS2-3566

[DTV] TV Settings: Prefecture / Zip Code Input

R20

CCS2-3571

[DTV] TV Settings: Audio ES

R21

CCS2-3567

[DTV] TV Settings: RMP Manufacturer ID Display

R22

CCS2-3552

[DTV] EPG (8 Days Program Schedule for multiple channels)

R23

CCS2-3553

[DTV] Program Info (Detailed EPG)

R24

CCS2-3562

[DTV] BML Browser Remote Key Event

R25

CCS2-3568

[DTV] Antenna Diagnostics

R26

CCS2-3569

[DTV] Production Diagnostics

R27

CCS2-3186

[DTV] High Temperature Protection of DTV module

R28

CCS2-3570

[DTV] TV Module Diagnostics

R29

CCS2-3574

[DTV] TRMP Error Code Notification

R30

CCS2-3575

[DTV] Developer Test Mode (ENG Menu)

# Use Cases

## Use case view

                  Figure 3

# High Level Design

## Static Software Architecture and Deployment to Domains

The below image illustrates the interaction of DTV Service with other modules in the Subsystem.

Figure 4

## Provided Interfaces / User Handbook

Detailed Interface Specification and Usage details are maintained in SharePoint. 

Please refer https://inside-share-hosted-apps.bosch.com/DMS/GetDocumentService/Document.svc/GetDocumentURL?documentID=P12S145423-1180436654-95 

## Dynamic Design on High Level

This section describes the dynamic interactions between components or subsystems. 

### Auto Preset

Figure 4

### Dtv Channel Up Down

Figure 5

### Dtv Signal Status

Figure 6

### Dtv Channel Seek

Figure 7

Search Status Update received from DTV HAL is shared for Channel Seek, Manual Broadcast Search, Automatic Search ( Foreground / Background ). The event would be notified to App through different interfaces based on the current DTV Event.

Figure 8

### Dtv Manual Preset Channel Store

                                                                                     Figure 9

### DTV Reception Monitor

DtvReceptionInfo does not provide the calculated REC value and duration since measurement started.

This has to be handled by client.

Formula for Calculation REC:

Reception rate (%) = {1- (number of data items with PER 1% or more) / (time elapsed)} x 100

Example: 

User press Start in Reception Monitor Screen

1st Monitor Status update

Duration: 1s

PER

Calculated REC

Layer A

0.6

{1 – 0 / 1} * 100 = 100 %

Layer B

1.1

{1 – 1 / 1} * 100 = 0 %

Layer C

0

{1 – 0 / 1} * 100 = 100 %

2nd Monitor Status update

Duration: 2s

PER

Calculated REC

Layer A

1.2

{1 – 1 / 2} * 100 = 50 %

Layer B

1.3

{1 – 2 / 2} * 100 = 0 %

Layer C

0

{1 – 0 / 2} * 100 = 100 %

3rd Monitor Status update

Duration: 3s

PER

Calculated REC

Observation

Layer A

1.8

{1 – 2 / 3} * 100 = 67.33 %

Intermediate reception, some packets missed

Layer B

1.5

{1 – 3 / 3} * 100 = 0 %

Very Poor Reception, all packets missed

Layer C

0

{1 – 0 / 3} * 100 = 100 %

Very Good Reception, no or very less packets missed

### Set Physical Channel

Physical Channel supported: 13 to 52

Application is responsible to send valid physical channel number.

### Get Version 

DtvVersionInfo contains information that is gathered from 3 different UART commands

     String hardwareVersion;     // Get Version

     String bootVersion;             // Get Version

     String softwareVersion;      // Get Version

     String partNumber;            // Get Part Number 

     String diversityMode;         // Get DTV System

### Test Mode Output

### Get Preset List

### Manual Preset Channel Store

### Get Program Info

### Get RMP Manufacturer ID Display

Sequence Diagram: 

Class Diagram: 

### Display Banner

### DTV Status Event

### Get Configure

### DTV Initialize

### Program Information Update Event

### Select Direct Channel

### Set Audio Mode

### Set Auto Tune Mode

### Set Closed Caption Mode

### Set Broadcast Search Mode

### Set Event Relay Mode

### Display EPG

# Current EPG sequence

Current handling for EPG required application has to send Display EPG request again to get current EPG button status

# With EPG Button Status Event

With EPG Button Status Event from TV module, application will be notified when EPG is displayed and a change in button status is required. 

As of now, this event will be disable by Event Mask, expected sequence when EPG Button Status Event enabled will be.

### Residential Area

### Audio ES

### Set Auto Broadcast Search Mode

Set automatic Broadcast Search mode.

### Broadcast Search

User can perform Broadcast search to

Find affiliate / relay station / relay and affiliate / stop broadcast search (manual)

Stop broadcast search (automatic)

# Affiliated Search (Manual)

# Broadcast Search (Auto)

# Broadcast Search Stop (Manual - Auto)

### BML Browser

# Operate BML:

User can operate BML using this interface

There is no result provided for this interface

Possible operations with BML which can be mapped to various buttons on remote / ‘d’ button

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

To start data broadcasting (on press of ‘d’ button), dtvOperateBml with DATA_BROADCAST should be used

The successful opening of BML Data broadcast session can only be judged by the beep sound heard

dtvOperateBml with DATA_BROADCAST would also toggle between opening BML and closing of BML.

To close BML, dtvForcedExitBml should be used to guarantee the closure of BML Data broadcast session

On press action of the button, application should use dtvOperateBml with relevant button and state as PRESS

On (short/long) release action of the button, dtvOperateBml with relevant button and state as RELEASE should be used

# Forced Exit BML:

Application can use this interface to ensured guaranteed closure of BML Data broadcast session

Result would be provided through onDtvForcedExitBmlResult

If BML Data broadcast session is open and dtvForcedExitBml sent, BML session would be closed, and SUCCESS result would be given

If BML Data broadcast session is not open and dtvForcedExitBml sent, no action and SUCCESS result would be givenl

This interface can be used on exit of BML screen or on back button press in the BML screen (not the back button in remote)

### EWS Event

DtvEwsEventLevel

LEVEL_1

Application should check if provided threeDigitNumber is different from the current playing threeDigitNumber (provided through onDtvProgramInfoUpdate). If yes, Application should tune to the provided threeDigitNumber using dtvDirectChannelSelect

LEVEL_2

Application should show Emergency Warning popup to user. 

If user selects “Yes”, application should check if provided threeDigitNumber is different from the current playing threeDigitNumber (provided through onDtvProgramInfoUpdate). If yes, Application should tune to the provided threeDigitNumber using dtvDirectChannelSelect

TEST

END

If Emergency Warning popup shown, application should hide the popup

### DTV Event Update

### DTV Firmware Update

DTV Module Firmware Update sequence and state machine handling would be done in DTV HAL.

Relevant update would be provided from DTV HAL through onDtvSwUpdateStatus and the same would be notified to registered clients through onDtvFirmwareUpdate AIDL interface.

For Information related to Dtv Module Firmware update, please refer SWCDD for DTV HAL.

### DTV Module Status Notification

Logical Handling :

When ModuleStatus or DiagStatus is received, based on below mapping, the AIDL event 

onDtvModuleStatusUpdate with the mapped values would be notified to client application.

AIDL DtvModuleStatus

HIDL DtvModuleStatus DtvDiagStatus

LOADING 

POWEROFF, SHUTDOWN, LOWPOWER_MODE, MODULE_DIAG_ERROR (Without Diag error)

READY

READY

HIGH_TEMPERATURE

Temp Alert

NOT_RESPONSIVE

UART Comm, NO_RESPONSE

INTERNAL_ERROR

Operation In Service Error, TRMP

FIRMWARE_UPDATE_INPROGRESS

DOWNLOAD

FIRMWARE_UPDATE_FAILURE

ToBeUpdated

## Suspend to Disk

Suspend-to-disk (S2D) is a concept to store the a snapshot of the RAM in a mass storage device (typically the eMMC / UFS).  This image is loaded by the bootloader instead of doing a cold boot. The goal is to reduce the start-up time. S2D allows a complete shutdown of the device.

Dtv Service would be responsible to listen to changes in power state from android.car.hardware.power and initiate handling to both Dtv Application and Dtv Hal

Below power states are notified from android.car.hardware.power.CarPowerManager

enum

value

description

INVALID

1

The current power state is unavailable, unknown, or invalid

WAIT_FOR_VHAL

2

Enter suspend state. CPMS is switching to WAIT_FOR_FINISHED state

SUSPEND_ENTER

3

Wake up from suspend

SHUTDOWN_ENTER

5

Enter shutdown state. CPMS is switching to WAIT_FOR_FINISHED state

ON

6

Normal state.

SHUTDOWN_PREPARE

7

State where system is getting ready for shutdown or suspend. Application is expected to cleanup and be ready to suspend

SHUTDOWN_CANCELLED

8

Shutdown is cancelled, returning to normal state

# Detailed Design

This section contains details to a level needed that all important architectural decisions are taken, and the development can be started. Within these given boundaries, the developer is free to do own decisions. 

## Static Design on Detail Level

### Class interaction diagram

The below diagram depicts the class interaction diagram.

Figure 5

## Analyzed Alternatives

DTV Functionality is not supported as part of standard AOSP Android Framework. Hence there were no other alternatives than to introduce a new Service to support DTV functionality. The Service is designed with the intention of supporting major business logic so that the Application can be lean. With lean application, adapting to new customers will be quicker\easier.

## Dynamic Design on Detail Level

This section describes the dynamic interactions on detail level. This chapter can be skipped if the description in 6.3 Dynamic design on high level is detailed enough. 

## Concurrency / Threading Model

This section describes the threading model for the SW modules. In addition, a distinction is shown which threads are started within the current process space and which processes are started separately (e.g., via fork, spawn), if any.

Thread

Process space

Started by

Description incl. concurrency issues

Binder_1

com.bosch.service.dtv

Binder_2

com.bosch.service.dtv

Binder_3

com.bosch.service.dtv

DtvNativeCallbackThread

com.bosch.service.dtv

HwBinder_1

com.bosch.service.dtv

sch.service.dtv

com.bosch.service.dtv

## Data Model View

This section describes the used storage mechanism (e.g., SQLite DB, data pool, …) as well as the concrete files incl. path used by the SW modules. It also describes how data integrity is secured and data can be set back to factory defaults.

### Storage Mechanism

This section describes the persistence mechanisms used by the subsystem incl. the error handling (e.g., incompatible data found).

SW Module

Used Storage Mechanism

# Migration of Data Structures / Error Handling

When a system is started data structures may be incompatible due to a file system corruption (bit flips) or structure change (SW update). How this expected behavior is handled by the storage mechanism is described here.

# Set to Delivery State

While production test several amounts of data will be written. At the end of production, a “Set to delivery” function is called. This chapter describes how the subsystem, or SW module get the trigger of “set to delivery” and which data will be reset.

### Data List

Persistent data that is in ownership of the subsystem is listed here. “Short Description” contains a brief description. “Used persistence mechanism” is a reference to 0. “Max Size” could be a static value or a formula if it is dependent on other values defined in the requirements. The “Max Size” is a prediction at design time and shall be measured after implementation to check the correctness (see chapter 6.60 

Critical Computer Resources (CPU, RAM, Flash)). “When read and written” defines if the data is written on every change or e.g., only while shut down, etc. Default value explains which values are written during creation or Set to Delivery state. File System rights are the minimum needed access rights (e.g., for concurrent usage).” Deletion while SW update” describes the behavior, when a SW Update is executed (e.g., file is deleted during update or not (if not, data needs to be converted by owner at next startup if needed))

Location in flash

Short description

Used persistence mechanism (see 0)

Max Size

When read and written?

Default data

File system rights

Deletion while SW update? [yes/no] 

### Configuration

This section describes the configurable features/functions of the SW modules and explains the standard configuration mechanism used and the concrete values for configuring the variant. In column “Key/Value range” the key (e.g., address of KDS value) and the possible values are documented.

## Critical Computer Resources (CPU, RAM, Flash)

This section describes the prediction of the CPU needs, Flash and RAM of the Subsystem. 

SW Modul

CPU [% of one ARM 9 core)

Flash (see Data list)

Max RAM[MB]

GPU Memory

[MB]

com.bosch.service.dtv

## Install View

This section describes where the files (executables, libraries, data) of the SW module are stored in the flash file system or at other locations.

Component tag

Binary path in source

Binary path in target 

libdtvinterface

out/target/product/aivi2_n_full_us/obj/JAVA_LIBRARIES/libdtvinterface_intermediates

static library

libdtv_modulespec

out/target/product/aivi2_n_full_us/obj/STATIC_LIBRARIES/ libdtv_modulespec

Static library

libdtv_jni

out/target/product/aivi2_n_full_us/system_ext/lib64/ libdtv_jni.so

system_ext/lib64/libdtv_jni.so

com.bosch.service.dtv

out/target/product/aivi2_n_full_us/system_ext/priv-app/com.bosch.service.dtv/*

system_ext/priv-app/com.bosch.service.dtv/

## Security User and Groups

All needed users and groups to implement the Multi-User-Security-Concept are listed here.

Process

User

Needed groups

com.bosch.service.dtv

system

system

# Testing & Debugging

Test features (e.g. automated tests, unit tests, etc.) and special test equipment needed for testing and debugging.

### Test Handling Implementation

## CTS

CTS (Compatibility Test Suite) is a set of test cases and framework designed to test Compatibility

The CTS includes the following types of test cases:

Unit tests test atomic units of code within the Android platform

Functional tests test a combination of APIs together in a higher-level use-case.

### CTS Test Cases

Individual test cases are executed on the DUT. The test cases are written in Java as JUnit tests and packaged Android .apk files to run on the actual device target. 

A module can contain one or more test cases. All test cases are considered individually for reporting purpose if the right template is used

Modules can be run individually

Each module has its own folder, somewhere within the previously shown structure.

Each test case will generally be a function, name prefixed with @Test

### How to run CTS testcases

Trade Federation (Tradefed or TF for short) is a continuous test framework designed for running tests on Android devices. For example, Tradefed is used to run the CTS

Trade Federation is a Java application which runs on a host computer and communicates to one or more Android devices over ADB.

 CTS test Plan can be run via the commands cts-tradefed and run cts

 Default run cts runs all the available cts testcases under every module, you can provide options to the cts run command, to run a specific module or run a specific test case from a module.

# Requirements to other Components

Requirements to other components based on architecture work within this document are listed here.

## Audio Requirements

## Audio Focus management support

Component / Generic

Requirement

# Source Code Reference

Source Directory: vendor/bosch/services/dtv

# Open Points

# References and Related Documents

Link

Link

Scope

SWCDD_MediaInput_Service

Captures Audio and Video Rendering for DTV

CCS2 DTV API Specification

API Spec for Interfaces to App

Requirement Specification

# Contacts

List of persons who maintain this module as well as persons who should be asked for acceptance when the interface or the behavior of the module shall be changed (e.g., if a message format shall be changed) 

No

Name

Comment

1

Dasharatha Arunkumar (XC-CT/ERN4-E)

Product Owner

2

Bharadwaj Chaitra (MS/ECR4-XC)

Architect

3

Akash Bhasker (MS/ECR4-XC)

Team Member

4

Han Van Thi (MS/EMC23-XC)

Team Member

5

Nguyen Quoc Dat (MS/EMC23-XC)

Team Member

6

Tra Vu Anh (MS/EMC23-XC)

Team Member

# Amendments

## Revision History 

History

22.12.2009 08:42:00

 8093

07.12.2007

V0003

DRAFT

asdf

Baier

Date

Version

Status

Review-Minutes

Amendments

Author

25/01/2023

0.1

DRAFT

Initial Version

07/02/2023

0.1

UPDATE

Adds “DTV Module Status Notification” item

Nguyen Quoc Dat

(MS/EMC23-XC)

03/11/2023

1.0

Release

Updated minor correction

Chaitra Bharadwaj

01/04/2023

1.1

UPDATE

Updated DTV Status Event

Pradeep S (MS/ECR4-XC)


**Table:**


SW Concept and Design Description

DTV Service – CCS2.0




**Table:**


Version:        1.1  ;  01.04.2024

Status:          Release

 | Date: Klicken Sie hier, um ein Datum einzugeben. | General Approval Form [Approval Data / Link]

Distribution listName/DepartmentRole in projectSuma Anand (MS/ECR4-XC)Project ManagerBharadwaj Chaitra (MS/ECR4-XC)Component ArchitectN.N.Safety Manager (if applicable)Recipients: add further stakeholders if needed | Name/Department | Role in project | Suma Anand (MS/ECR4-XC) | Project Manager | Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect | N.N. | Safety Manager (if applicable) | Reviewer listName/DepartmentRole in projectReviewer or approverDasharatha Arunkumar (XC-CT/ERN4-E)Component Product OwnerApproverBharadwaj Chaitra (MS/ECR4-XC)Component ArchitectApproverN.N.Safety Team (if applicable)ReviewerAkash Bhasker (MS/ECR4-XC) SW-ContributorReviewerHan Van Thi (MS/EMC23-XC)SW-ContributorReviewerNguyen Quoc Dat (MS/EMC23-XC)SW-ContributorReviewerTra Vu Anh (MS/EMC23-XC)SW-ContributorReviewerChanges are announced via stages update information, no distribution as printed version, provision in the Intranet: see footer | Name/Department | Role in project | Reviewer or approver | Dasharatha Arunkumar (XC-CT/ERN4-E) | Component Product Owner | Approver | Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect | Approver | N.N. | Safety Team (if applicable) | Reviewer | Akash Bhasker (MS/ECR4-XC) | SW-Contributor | Reviewer | Han Van Thi (MS/EMC23-XC) | SW-Contributor | Reviewer | Nguyen Quoc Dat (MS/EMC23-XC) | SW-Contributor | Reviewer | Tra Vu Anh (MS/EMC23-XC) | SW-Contributor | Reviewer

Name/Department | Role in project

Suma Anand (MS/ECR4-XC) | Project Manager

Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect

N.N. | Safety Manager (if applicable)

Name/Department | Role in project | Reviewer or approver

Dasharatha Arunkumar (XC-CT/ERN4-E) | Component Product Owner | Approver

Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect | Approver

N.N. | Safety Team (if applicable) | Reviewer

Akash Bhasker (MS/ECR4-XC) | SW-Contributor | Reviewer

Han Van Thi (MS/EMC23-XC) | SW-Contributor | Reviewer

Nguyen Quoc Dat (MS/EMC23-XC) | SW-Contributor | Reviewer

Tra Vu Anh (MS/EMC23-XC) | SW-Contributor | Reviewer




**Table:**


Name/Department | Role in project

Suma Anand (MS/ECR4-XC) | Project Manager

Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect

N.N. | Safety Manager (if applicable)




**Table:**


Name/Department | Role in project | Reviewer or approver

Dasharatha Arunkumar (XC-CT/ERN4-E) | Component Product Owner | Approver

Bharadwaj Chaitra (MS/ECR4-XC) | Component Architect | Approver

N.N. | Safety Team (if applicable) | Reviewer

Akash Bhasker (MS/ECR4-XC) | SW-Contributor | Reviewer

Han Van Thi (MS/EMC23-XC) | SW-Contributor | Reviewer

Nguyen Quoc Dat (MS/EMC23-XC) | SW-Contributor | Reviewer

Tra Vu Anh (MS/EMC23-XC) | SW-Contributor | Reviewer




**Table:**


Term or Abbreviation | Description

Component Model | In the IEEE standard 1026-1998 the component model is called the decomposition view and in RUP it is called the logical view.

Design Pattern | General approach to solve a common design problem, e.g. observer pattern. A design pattern consists of a problem statement, a solution and consequences (pros and cons).

Dynamic Model | A set of classes that work together to realize a use case, also called collaboration or mechanistic design. In the IEEE standard 1026-1998 the dynamic model is called the dependency description.

IDL | Interface Definition Language

RM | Requirement Management

State Chart | State charts are a formal behavioral language. State charts are particularly effective when the use case is reactive; that is, it has inherent states (conditions) and remains in those conditions until an event of interest has occurred. A state chart is more precise and less likely to be misinterpreted than text, but it is harder to understand. Therefore it should be used together with text and sequence diagrams.

Subsystem | An assigned area of functional responsibility

SW | Software

SWAD | Software Architecture Document

Use Case | A use case is a named capability of a structural entity in a model. Use cases organize requirements into chunks. They help to detect open requirements. It is common for a use case to represent and organize many pages of textual requirements or dozens of usage scenarios.

AAOS | Android Automotive Operating System

iAP2 | iPod Accessory Protocol version 2

USB | Universal Serial Bus

MD | Mobile Device

HU | Head Unit

SPI | Smartphone Integration

JNI | Java Native Interface




**Table:**


Annotation | Description

@ASSUMPTION | This annotation at the beginning of a sentence, paragraph or statement marks the following description as something that the author assumed as true, although it is not (yet) proven.

@PRELIMANARY | This annotation at the beginning of a sentence, paragraph or statement marks the following description as something that is true at time of writing, but might change in the (near) future or still need clarification.

@TODO | This annotation at the beginning of a sentence, paragraph or statement marks something that needs to be described. Used by the author to mark open topics.




**Table:**


ReqNo | Program Epic | Requirements | Details

R1 | CCS2-1617 | CCS2-1617 | [DTV] Channel Seek Up/Down | 

CCS2-1617

R2 | CCS2-3554 | [DTV] Auto Preset for TV1/TV2 | 

R3 | CCS2-3555 | [DTV] Preset List Retrieve/Update for TV1/TV2 | 

R5 | CCS2-3557 | [DTV] Program Information Notification | 

R6 | CCS2-3556 | [DTV] Preset Channel Select/Store for TV1/TV2 | 

R7 | CCS2-4631 | [DTV] Channel Up/Down (Next/Previous) | 

R8 | CCS2-1613 | [DTV] Antenna Phantom voltage enable | 

R9 | CCS2-1612 | [DTV] Audio Streaming | 

R10 | CCS2-3573 | [DTV] Signal Status (Weak / No signal) / No Service Notification | 

R11 | CCS2-3558 | [DTV] Antenna Bars Level (0/1/2/3) Notification | 

R12 | CCS2-3559 | [DTV] Display Banner (overlaid on TV video) | 

R13 | CCS2-3572 | [DTV] Direct Channel Input (3 Digits Channel Number) | 

R14 | CCS2-3560 | [DTV] Manual Foreground Broadcast Search (Relay/Affiliated Station) | 

R15 | CCS2-3561 | [DTV] Automatic Foreground Broadcast Search (Relay/Affiliated Station) | 

R16 | CCS2-3563 | [DTV] EWS (Emergency Warning Service) Notification | 

R17 | CCS2-3564 | [DTV] Initialization (TV1 / TV2 / Settings / Factory Reset) | 

R18 | CCS2-3565 | [DTV] TV Settings: Basics | 

R19 | CCS2-3566 | [DTV] TV Settings: Prefecture / Zip Code Input | 

R20 | CCS2-3571 | [DTV] TV Settings: Audio ES | 

R21 | CCS2-3567 | [DTV] TV Settings: RMP Manufacturer ID Display | 

R22 | CCS2-3552 | [DTV] EPG (8 Days Program Schedule for multiple channels) | 

R23 | CCS2-3553 | [DTV] Program Info (Detailed EPG) | 

R24 | CCS2-3562 | [DTV] BML Browser Remote Key Event | 

R25 | CCS2-3568 | [DTV] Antenna Diagnostics | 

R26 | CCS2-3569 | [DTV] Production Diagnostics | 

R27 | CCS2-3186 | [DTV] High Temperature Protection of DTV module | 

R28 | CCS2-3570 | [DTV] TV Module Diagnostics | 

R29 | CCS2-3574 | [DTV] TRMP Error Code Notification | 

R30 | CCS2-3575 | [DTV] Developer Test Mode (ENG Menu) | 




**Table:**


CCS2-1617




**Table:**


Duration: 1s | PER | Calculated REC

Layer A | 0.6 | {1 – 0 / 1} * 100 = 100 %

Layer B | 1.1 | {1 – 1 / 1} * 100 = 0 %

Layer C | 0 | {1 – 0 / 1} * 100 = 100 %




**Table:**


Duration: 2s | PER | Calculated REC

Layer A | 1.2 | {1 – 1 / 2} * 100 = 50 %

Layer B | 1.3 | {1 – 2 / 2} * 100 = 0 %

Layer C | 0 | {1 – 0 / 2} * 100 = 100 %




**Table:**


Duration: 3s | PER | Calculated REC | Observation

Layer A | 1.8 | {1 – 2 / 3} * 100 = 67.33 % | Intermediate reception, some packets missed

Layer B | 1.5 | {1 – 3 / 3} * 100 = 0 % | Very Poor Reception, all packets missed

Layer C | 0 | {1 – 0 / 3} * 100 = 100 % | Very Good Reception, no or very less packets missed




**Table:**


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




**Table:**


DtvEwsEventLevel | 

LEVEL_1 | Application should check if provided threeDigitNumber is different from the current playing threeDigitNumber (provided through onDtvProgramInfoUpdate). If yes, Application should tune to the provided threeDigitNumber using dtvDirectChannelSelect

LEVEL_2 | Application should show Emergency Warning popup to user. If user selects “Yes”, application should check if provided threeDigitNumber is different from the current playing threeDigitNumber (provided through onDtvProgramInfoUpdate). If yes, Application should tune to the provided threeDigitNumber using dtvDirectChannelSelect

TEST | 

END | If Emergency Warning popup shown, application should hide the popup




**Table:**


AIDL DtvModuleStatus | HIDL DtvModuleStatus DtvDiagStatus

LOADING | POWEROFF, SHUTDOWN, LOWPOWER_MODE, MODULE_DIAG_ERROR (Without Diag error)

READY | READY

HIGH_TEMPERATURE | Temp Alert

NOT_RESPONSIVE | UART Comm, NO_RESPONSE

INTERNAL_ERROR | Operation In Service Error, TRMP

FIRMWARE_UPDATE_INPROGRESS | DOWNLOAD

FIRMWARE_UPDATE_FAILURE | ToBeUpdated




**Table:**


enum | value | description

INVALID | 1 | The current power state is unavailable, unknown, or invalid

WAIT_FOR_VHAL | 2 | Enter suspend state. CPMS is switching to WAIT_FOR_FINISHED state

SUSPEND_ENTER | 3 | Wake up from suspend

SHUTDOWN_ENTER | 5 | Enter shutdown state. CPMS is switching to WAIT_FOR_FINISHED state

ON | 6 | Normal state.

SHUTDOWN_PREPARE | 7 | State where system is getting ready for shutdown or suspend. Application is expected to cleanup and be ready to suspend

SHUTDOWN_CANCELLED | 8 | Shutdown is cancelled, returning to normal state




**Table:**


Thread | Process space | Started by | Description incl. concurrency issues

Binder_1 | com.bosch.service.dtv |  | 

Binder_2 | com.bosch.service.dtv |  | 

Binder_3 | com.bosch.service.dtv |  | 

DtvNativeCallbackThread | com.bosch.service.dtv |  | 

HwBinder_1 | com.bosch.service.dtv |  | 

sch.service.dtv | com.bosch.service.dtv |  | 




**Table:**


SW Module | Used Storage Mechanism




**Table:**


Location in flash | Short description | Used persistence mechanism (see 0) | Max Size | When read and written? | Default data | File system rights | Deletion while SW update? [yes/no]




**Table:**


SW Modul | CPU [% of one ARM 9 core) | Flash (see Data list) | Max RAM[MB] | GPU Memory[MB]

com.bosch.service.dtv |  |  |  | 




**Table:**


Component tag | Binary path in source | Binary path in target

libdtvinterface | out/target/product/aivi2_n_full_us/obj/JAVA_LIBRARIES/libdtvinterface_intermediates | static library

libdtv_modulespec | out/target/product/aivi2_n_full_us/obj/STATIC_LIBRARIES/ libdtv_modulespec | Static library

libdtv_jni | out/target/product/aivi2_n_full_us/system_ext/lib64/ libdtv_jni.so | system_ext/lib64/libdtv_jni.so

com.bosch.service.dtv | out/target/product/aivi2_n_full_us/system_ext/priv-app/com.bosch.service.dtv/* | system_ext/priv-app/com.bosch.service.dtv/




**Table:**


Process | User | Needed groups

com.bosch.service.dtv | system | system




**Table:**


Component / Generic | Requirement




**Table:**


Link | Link | Scope

 | SWCDD_MediaInput_Service | Captures Audio and Video Rendering for DTV

 | CCS2 DTV API Specification | API Spec for Interfaces to App

 | Requirement Specification | 




**Table:**


No | Name | Comment

1 | Dasharatha Arunkumar (XC-CT/ERN4-E) | Product Owner

2 | Bharadwaj Chaitra (MS/ECR4-XC) | Architect

3 | Akash Bhasker (MS/ECR4-XC) | Team Member

4 | Han Van Thi (MS/EMC23-XC) | Team Member

5 | Nguyen Quoc Dat (MS/EMC23-XC) | Team Member

6 | Tra Vu Anh (MS/EMC23-XC) | Team Member




**Table:**


History | 22.12.2009 08:42:00 | 8093 |  |  | 

07.12.2007 |  |  | V0003 | DRAFT | asdf |  |  |  |  | Baier |  | 

Date | Version | Status | Review-Minutes | Amendments | Author

25/01/2023 | 0.1 | DRAFT |  | Initial Version | 

07/02/2023 | 0.1 | UPDATE |  | Adds “DTV Module Status Notification” item | Nguyen Quoc Dat(MS/EMC23-XC)

03/11/2023 | 1.0 | Release |  | Updated minor correction | Chaitra Bharadwaj

01/04/2023 | 1.1 | UPDATE |  | Updated DTV Status Event | Pradeep S (MS/ECR4-XC)

