SW Concept and Design Description

DTV HAL – CCS2.0

Version:        1.7 16.07.2026

Status:          Release

Approval

Date: 16.07.2026

General Approval Form 

[Approval Data / Link]

Distribution list

Name/Department

Role in project

Meda Srikanth Reddy (MS/ECR1-XC)

Component Architect

N.N.

Safety Manager (if applicable)

Nisharani C Paramba (MS/ECR6-XC)

Project Manager

Recipients: add further stakeholders if needed

Reviewer list

Name/Department

Role in project

Reviewer or approver

Kavadapu Narasimhulu

(MS/ECR1-XC)

Component Product Owner

Approver

Meda Srikanth Reddy (MS/ECR1-XC)

Component Architect

Approver

N.N.

Safety Team (if applicable)

Reviewer

Cherishnav Reddy Chittamuru (MS/ECR1-XC) 

SW-Contributor

Reviewer

Pradeep S 

(MS/ERC1-XC)

SW-Contributor

Reviewer

Nguyen Quoc Dat (MS/EMC32-XC)

SW-Contributor

Reviewer

Changes are announced via stages update information, no distribution as printed version, 

provision in the Intranet: see footer.

# Contents

1List of Terms and Abbreviations3

2Purpose of this Document3

3Introduction to the Subsystem4

4Architecture Driving Requirement Groups4

5Use Cases5

5.1Use case view5

6High Level Design6

6.1Static Software Architecture and Deployment to Domains6

6.1.1Analyzed Alternatives6

6.2Provided Interfaces / User Handbook7

6.3Dynamic Design on High Level9

6.3.1DTV HAL Start-up9

6.3.2DTV HAL Shutdown9

6.3.3DTV lib System States9

6.3.4High Temperature Alert.10

6.3.5Suspend to Disk12

6.3.6Sync handler – Blocking call15

6.3.7Software Update16

6.3.8Antenna Monitoring22

6.3.9Diagnostic Trouble Code (DTC) Handling26

6.3.10Low Voltage Handling29

6.3.11DTV Critical Error32

6.3.12Death Recipients Handling33

7Detailed Design37

7.1Static Design on Detail Level37

7.1.1Class interaction diagram37

7.2Analyzed Alternatives37

7.3Mechanisms and Algorithms37

7.4Dynamic Design on Detail Level37

7.5Concurrency / Threading Model37

7.6Data Model View38

7.6.1Storage Mechanism38

7.6.2Data List38

7.6.3Configuration39

7.7Critical Computer Resources (CPU, RAM, Flash)39

7.8Install View39

7.9Security User and Groups40

8Testing & Debugging40

8.1VTS41

8.1.1VTS Test Cases41

8.1.2How to run VTS testcases41

9Requirements to other Components42

10Source Code Reference42

10.1DTV HAL42

10.2DTV Config42

11Open Points42

12References and Related Documents42

13Contacts43

14Amendments44

14.1Revision History44

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

SW

Software

SWAD

Software Architecture Document

Use Case 

A use case is a named capability of a structural entity in a model. Use cases organize requirements into chunks. They help to detect open requirements. It is common for a use case to represent and organize many pages of textual requirements or dozens of usage scenarios.

# Purpose of this Document

This document is used to record results of architecture and design activities for DTV HAL for CCS2.0.

The document contains both the high level as well as the detailed design. It describes the behavior and how the SW interact with the remaining system. The document shows how the SW part will be arranged to satisfy the requirements and guide the developers for the implementation and maintenance phases. It provides also an understanding, which kinds of requirements are related to which design entities (such like SW components or modules).

# Introduction to the Subsystem

DTV HAL is software module which is located in HAL portion of the android software stack in Vendor Partition and

It is configured as a Lazy HAL. 

The more details regarding the interaction between DTV HAL and other modules are explained in the later part of this document.

# Architecture Driving Requirement Groups 

Below are the major requirements full filled in DTV HAL component.

Req No

Scope

Details

R1

TV Module communication

Provides interface to exchange communication between Host and TV Module 

R2

Firmware update

Provides interface and implementation of TV module firmware update

R3

TV Module Diagnosis

Diagnosis handling of TV Module related to uart, temp alert, operation, trmp

R4

TV Module power

R5

Antenna Diagnosis

Handling of Antenna output power and monitoring

# Use Cases

## Use case view

# High Level Design

## Static Software Architecture and Deployment to Domains

The below image illustrates the interaction of DTV HAL with other modules in the Subsystem.

Figure 3

### Analyzed Alternatives

This is yet to be updated.

## Provided Interfaces / User Handbook

The below are the interfaces offered by DTV HAL. 

Service request interface prototypes are defined in IDTV.hal

registerDtvEvents(IDtvEventsCallback callback)

Method to register for events from DTV Hal on module health,HAL statemachine and swupdate 

IDtvEventsCallback  callback:- Callback reference to send events from DTV HAL

Return Result:- result for the request

deregisterDtvEvents(IDtvEventsCallback callback)

Method to de-register for events from DTV Hal on module health,HAL statemachine and swupdate

IDtvEventsCallback  callback:- Callback reference to send events from DTV HAL

Return Result:- result for the request

registerDtvModuleEvents(IDtvModuleEventsCallback callback)

Method to register for events from TV Module

IDtvModuleEventsCallback callback:- Callback reference to send events from TV Module

Return Result:- result for the request

deregisterDtvModuleEvents(IDtvModuleEventsCallback callback)

Method to de-register for events from TV Module

IDtvModuleEventsCallback callback:- Callback reference to send events from TV Module

Return Result:- result for the request

sendCommandToModule(DtvCommandDesc command,IDtvModuleResponseCallback callback) 

Method to send uart commands to TV Module. 

DtvCommandDesc:-  Structure consists of Command ID, IsMultiFragment, CommandType,                                                and Uart data payload

IDtvModuleResponseCallback:- Callback reference to send response from TV Module

Return requestId :- Unique Id assigned for each request sent by client

Return Result :- result for the request

performFirmwareUpdate(string firmwarePath)     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Method to do TV Module firmware update

firmwarePath :- folder path where firmware file "thrHigh_AppPkg.tgz" is available

Return Result :- result for the request

performBlockingFirmwareUpdate (string firmwarePath)     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Method to do TV Module firmware update. This is a blocking call till update is complete

firmwarePath :- folder path where firmware file "thrHigh_AppPkg.tgz" is available

Return Result :- result for the request

getDtvModuleInfo ()     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Method to do get TV Module Information

Return Result :- result for the request

Return DtvModuleInfo :- Module info

getDtvAntennaState (DtvAntennaNumber antenna)     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Method to do get DTV Antenna State

DtvAntennaNumber  antenna :- Antenna Number for which the state is requested

Return Result :- result for the request

Return DtvAntennaStatus :- Antenna State

getDtvModuleStatus ()     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Method to do get DTV Module Status

Return DtvModuleStatus :- TV Module Status

suspend ()     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Service use this interface to suspend hal operation

Return Result :- result for the request

resume ()     * Control audio volume.

@param featureId The audio feature identifier.

@param volume The volume index to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setVolumeIndex(AudioFeatureId featureId, int32_t volume, bool audible) generates(StatusCode status);

/**

Get audio volume index.

@param featureId The audio feature identifier.

@return volume The volume index.

@return status A value from StatusCode enum.

*/

getVolumeIndex(AudioFeatureId featureId) generates(int32_t volume, StatusCode status);

/**

Set the sound collection to use.

@param featureId The audio feature identifier.

@param index The identifier of the sound collection to set.

@param audible The audio feedback to enable or not.

@return status A value from StatusCode enum.

*/

setSoundCollection(AudioFeatureId featureId, int32_t index, bool audible) generates(StatusCode status);

/**

Get the sound collection currently in use.

@param featureId The audio feature identifier.

@return index The identifier corresponding to the sound collection.

@return status A value from StatusCode enum.

*/

getSoundCollection(AudioFeatureId featureId) generates(int32_t index, StatusCode status);

/**

Check if sound generation is muted.

@param featureId The audio feature identifier.

@return muted The mute state.

@return status A value from StatusCode enum.

*/

isMuted(AudioFeatureId featureId) generates(bool muted, StatusCode status);

/**

Control the mute state of sound generation.

@param featureId The audio feature identifier.

@param mute The mute state to set.

@return status A value from StatusCode enum.

*/

mute(AudioFeatureId featureId, bool mute) generates(StatusCode status);

/**

Check if feature is enabled.

@param featureId The audio feature identifier.

@return enabled The activation state.

@return status A value from StatusCode enum.

*/

isEnabled(AudioFeatureId featureId) generates(bool enabled, StatusCode status);

/**

Control the activation state of the feature.

@param featureId The audio feature identifier.

@param enable The activation state to set.

@return status A value from StatusCode enum.

*/

enable(AudioFeatureId featureId, bool enable) generates(StatusCode status);

/**

Subscribe to the events of this HAL.

@param featureId The audio feature identifier.

@param callback This client must be called on appropriate event.

@return status A value from StatusCode enum.

*/

subscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

/**

Unsubscribe from the events of this HAL.

@param featureId The audio feature identifier.

@param callback Identify the client to unsubscribe.

@return status A value from StatusCode enum.

*/

unsubscribe(AudioFeatureId featureId, IAudioFeatureCallback callback) generates(StatusCode status);

Service use this interface to resume hal operation

Return Result :- result for the request

getDtvFirmwareVersion ()

Method to do get Dtv Firmware Version. This is a blocking call

Return Result:- result for the request

Return string firmwareVersion : Firmware Version.

Module Response interface prototypes are defined in IDtvModuleResponseCallback.hal

onDtvModuleResponse(DtvCommandRespDesc response)

Method called by HAL on receiving response from TV Module

DtvCommandRespDesc response : Response form TV Module

Module Events interface prototypes are defined in IDtvModuleEventsCallback.hal

onDtvModuleEvent(DtvEventRespDesc eventDesc)

Method called by HAL on receiving event from TV Module

DtvEventRespDesc eventDesc : event info from module

Status interface prototypes are defined in IDtvEventsCallback.hal

onDtvModuleStatus(DtvModuleStatus status)

Provides status update on current TV Module State

onDtvSwUpdateStatus(DtvSoftwareUpdateStatus status)

Provides status update on current TV Module firmware update status

onDtvAntennaStatus (vec<DtvAntennaStatus> status)

Provides antenna status of TV module  

Status interface prototypes are defined in IDtvModuleInfoResponseCallback.hal

onDtvModuleInfoResponse(DtvModuleInfo info)

Method called by HAL to update TV Module version, partnumber and antennaConfig

DtvModuleInfo info: bootVersion, hardwareVersion, firmwareVersion, boschPartNumber, antennaConfig  

## Dynamic Design on High Level

This section describes the dynamic interactions between components or subsystems. 

### DTV HAL Start-up

### DTV HAL Shutdown

### DTV lib System States

### High Temperature Alert.

# Monitoring

# Recover after error

### Suspend to Disk

As a requirement for Suspend to Disk, DTV Hal would be notified to resume/suspend activity from DTV Service, based on updated from android.car.hardware.power.CarPowerManager

DTV Hal supports two operations:

Suspend: On receiving this request, DTV Hal would 

Stop TV Module

Stop UART communication.

Power off DTV Antenna

Destroy all instances of instantiated libraries and cleanup resources. 

Resume: On receiving this request, DTV Hal would

Configure and power on DTV Antenna

Instantiate required libraries and setup communication.

Start TV Module

Refer to the CarPowerManager state machine below for details.

Currently, the DTV service and DTV HAL monitor four events from the CarPowerManager to manage suspend or resume operation.

SHUTDOWN_ENTER/SUSPEND_ENTER: The suspend operation is triggered

SUSPEND_EXIT: The resume operation is triggered

SHUTDOWN_CANCELLED: The resume operation is triggered when SHUTDOWN_CANCELLED is received from CarPowerManager while the system is in WAIT_FOR_FINISH (after SHUTDOWN_ENTER or SUSPEND_ENTER).

### Sync handler – Blocking call

DTV HAL provides synchronous blocking call support for required interfaces.

This handler will take a request from the caller, process it, and returns the response to the caller as a blocking call.

### Software Update

DTV HAL supports two operations for the Software update feature. The Software update will operate in either background or the foreground, depending on its current version (refer to the SW Update Mode Identification figure in Software Update Validation session).

It also provides synchronous blocking call/ asynchronous call support for required interfaces.

# Software Update Validation

This process will validate the availability of the firmware update operation. 

Based on the data in version.txt file and the current firmware TV module. The DTV HAL will then determine which operation can be initiated.

Currently, DTV HAL supports four operations:

Upgrade Operation

Downgrade Operation

Not perform firmware update operation but DTV HAL will return success as requirement from Software Update component.

No support (It can occur if there is missing data in version.txt file)

Format data of version.txt

Version: TH010XXX

minBgVersion: TH010XXX

minDgVersion: TH010XXX

Note: The current TV firmware can either be a valid or invalid (RPDTRMPS) version. An invalid version can occur if the Software Update operation is interrupted after the SW Loader has been completely downloaded.

RPDTRMPS is the SW Loader version, and it can be downloaded to the TV module to initialize the configuration of NVRAM configuration in TV module. This process is necessary when upgrading the TV firmware from a version older than V1.2 (TH010518)

# Synchronous blocking call

The software update’s synchronous blocking call is invoked when the user initiates it from the USB Update via the SW Update Service.

This handler will take a request from the caller, process it, and returns the response to the caller as a blocking call.

# Asynchronous call 

The software update’s asynchronous call is invoked when the user initiates it from the Test Mode via the DTV Service.

This handler will take a request from the caller, process it, and returns the response immediately to the caller while the SW Update is in progress.

# Background Software Update

The SW Update transfer update files via UART command (V2.1 or newer).

# Foreground Software Update

The SW Update transfer update files with YMODEM Protocol.

# Interrupt Software Update

The software update can be interrupted by certain operations, such as suspending to disk or powering off, among others.

Please note that if an interrupt occurs after the firmware files have been transferred to the TV module, the firmware version will be updated.

In the event that the software update is interrupted, the DTV HAL will revert to an idle state. After resuming, the system will be in a state that allows the software update to proceed.

### Antenna Monitoring 

Antenna is powered using the MAX20084B IC which is mounted on the Sub PCB of silver box.

The MAX20084B is a dual-antenna power supply with an I2C interface for diagnostics and control. The dual 270mA antenna supplies are linear regulators whose output voltage is set individually through I2C interface of IC. Additionally, MAX20084B IC has internal registers which are used to set the current limit, open-load threshold, and other parameters.

For 2-Antenna variants, 1 MAX20084B IC is used, whereas for 4-Antenna variants, 2 MAX20084B IC’s are used.

Antenna Diagnosis communciates with MAX20084B IC through I2C. The registers are read and written using I2C communication.

Antenna Diagnosis supports 3 functionalities:

Initialize Configuration Registers of MAX20084B IC

Power ON/OFF the Antenna 

Periodic Antenna Monitoring

Antenna is powered ON explicitly as part of DTV HAL startup sequence when the TV Module is powered ON.

Once Antenna is powered ON, the Periodic Diagnosis monitoring starts and continues at every 320 milli seconds interval. The EN pin of the IC connected to the same circuit as that of TV module power on. Therefore, EN pin is not controlled by the DTV HAL software separately and is powered on simultaneously when the TV module is powered on. Hence before DTV Hal tries to access MAX20084B IC through I2C, the TV module should be powered on.

During Periodic Antenna Monitoring, if Power On Reset(POR) Flag of Diag Register in MAX20084B is set, we initialize all the Configuration Registers of MAX20084B and enable the Antenna Output.

Project Specific Configuration Values :

Illumination value = 270mA

Over Current Threshold = 40mA

Open Load Threshold = 2mA

Output Voltage = 8V

Warning temperature = 95 deg C

Blanking Time = 50ms

Mask Value is set in a way that reverse current, over current, short to battery interrupts are enabled.

Over Current Wait Time = 15s

# Antenna States 

Antenna State – OPEN :

When Antenna current is less than Open Load Threshold for 3 consecutive cycles of measurement, the Antenna is set to OPEN state.

Antenna State – OK :

When Antenna current is between Open Load Threshold and Over Current Threshold for 3 consecutive cycles of measurement, the Antenna is set to OK state.

Antenna State – SHORT :

When the current in a channel reaches the set current limit, MAX20084B limits the output current of the LDO/switch while the output remains ON until the blanking time elapses. If the channel current is above the overcurrent setting in the OC_OL register at the end of the blanking time the channel is disabled and an overcurrent (OC_) fault is declared by the MAX20084B IC.

When any of the Antenna enters into Short Circuit Error condition (through Over Current Flag, Short to Battery Flag or TShutDown Flag of Diag Registers of MAX20084B), that particular antenna will be powered OFF through MAX20084B IC by disabling the output voltage.DTV HAL waits for a predefined time of 15 seconds before powering ON the antenna again. During this time, Antenna monitoring will be stopped. After the timeout, DTV HAL powers ON the Antenna again and starts monitoring.

Diagnosis requirement is to notify the Antenna State update every 1 second. To ensure consistency of current reading, 3 cycles of current measurement is done in this 1 second interval. Hence Monitor Timer is approx 320 milli seconds (interval) and number of Monitor cycles equals 3.

# Activity Diagram 

Antenna Current is read every 320 milli seconds (interval) for 3 monitor cycles.

The counters are updated based on the current value. If any of the counter value (open, close, short) is same for the 3 consecutive cycles of measurement, the Antenna State is set accordingly and the counters are reset.

If Short circuit condition is detected, the MAX20084B IC powers OFF the Antenna by disabling the output voltage, and the wait time counter in DTV HAL is set to 15 seconds. Once the short circuit wait time is over, the Antenna is powered back ON by the state machine.  

Antenna State Update is send to DTC every 1 second.

### Diagnostic Trouble Code (DTC) Handling 

DTV HAL supports sending the DTC to the Diagnosis service vendor.alliance.hardware.automotive.diagnosis@2.0 whenever an error occurs in DTV.

The DTC code and fault type are defined from the diagnosis service [4] as below:

DTC code

Value

Fault type

Value

DTC Status

DTC_DTV_ANTENNA1

0x938C

FT_SHORT_TO_GROUND

0x11

PASS/ FAIL

FT_OPEN_LOAD

0x13

DTC_DTV_ANTENNA2

0x938D

FT_SHORT_TO_GROUND

0x11

PASS/ FAIL

FT_OPEN_LOAD

0x13

DTC_DTV_ANTENNA3

0x938E

FT_SHORT_TO_GROUND

0x11

PASS/ FAIL

FT_OPEN_LOAD

0x13

DTC_DTV_ANTENNA4

0x938F

FT_SHORT_TO_GROUND

0x11

PASS/ FAIL

FT_OPEN_LOAD

0x13

# Sequence diagram

Connect and updateDTC sequence:

Disconnect sequence:

# Class diagram

### Low Voltage Handling 

HW team recommends that, when system is in Low Voltage conditions, TV antenna output voltage should be turned OFF and when System re-enters normal voltage conditions, we should turn ON the Antenna output voltage again.

This is to ensure the power consumption is kept under check under low voltage conditions.

DTV HAL subscribes to Interface IVhalExtensionVolt and registers for notifications on change in System Voltage.

When IVhalExtensionVolt notifies DTV HAL about Low Voltage (VOLTAGE_MGMT_CRITICAL_LOW ~ 6.2V), Antenna and TV module are powered OFF and when system re-enters into Normal Mode (VOLTAGE_MGMT_LOW ~ 6.7V), Antenna and TV module are powered ON again.

# Sequence diagram

Register and Antenna Power Handling sequence:

Un-Register sequence:

### DTV Critical Error

The DTV HAL supports restarting or resetting the TV module whenever critical errors occur from the TV module sides. It also stored the logs in the persistent memory for tracing.

### Death Recipients Handling

This section contains details of the way the death recipients were handled for DTV clients like DTC, System Voltage and Temperature handling.

This mechanism ensures robustness and resilience. It allows the clients to detect and recover from service failures, maintaining functionality without requiring manual intervention.

# Death Recipient Handling for DTC client:

# Death Recipient Handling for System Voltage client:

# Death Recipient Handling for Thermal Hal client:

# Detailed Design

This section contains details to a level needed that all important architectural decisions are taken and the development can be started. Within this given boundaries, the developer is free to do own decisions. 

## Static Design on Detail Level

### Class interaction diagram

The below diagram depicts the class interaction diagram.

## Analyzed Alternatives

## Mechanisms and Algorithms 

## Dynamic Design on Detail Level

This section describes the dynamic interactions on detail level. This chapter can be skipped if the description in 6.3 Dynamic design on high level is detailed enough. 

## Concurrency / Threading Model

This section describes the threading model for the SW modules. In addition, a distinction is shown which threads are started within the current process space and which processes are started separately (e.g. via fork, spawn), if any.

Thread

Process space

Started by

Description incl. concurrency issues

DTV Hal Main Thread

HwServiceManager

This thread is created at service startup

uartTxHandler

DTV Hal Main Thread

This thread handles sending requests and processing response from TV Module

uartRxHandker

DTV Hal Main Thread

This thread receives data from TV Module via UART port and forms full packet and adds into messageQ

eventObserver

DTV Hal Main Thread

This thread serializes all message and timer events. All callbacks out of dtvlib is posted from this thread context

## Data Model View

This section describes the used storage mechanism (e.g. SQLite DB, datapool, …) as well as the concrete files incl. path used by the SW modules. It also describes how data integrity is secured and data can be set back to factory defaults.

### Storage Mechanism

This section describes the persistence mechanisms used by the subsystem incl. the error handling (e.g. incompatible data found).

SW Module

Used Storage Mechanism

# Migration of Data Structures / Error Handling

When a system is started data structures may be incompatible due to a file system corruption (bit flips) or structure change (SW update). How this expected behavior is handled by the storage mechanism is described here.

# Set to Delivery State

While production test several amounts of data will be written. At the end of production a “Set to delivery” function is called. This chapter describes how the subsystem, or SW module get the trigger of “set to delivery” and which data will be reset.

### Data List

Persistent data that is in ownership of the subsystem is listed here. “Short Description” contains a brief description. “Used persistence mechanism” is a reference to 0. “Max Size” could be a static value or a formula if it is dependent on other values defined in the requirements. The “Max Size” is a prediction at design time and shall be measured after implementation to check the correctness (see chapter 6.60 

Critical Computer Resources (CPU, RAM, Flash)). “When read and written” defines if the data is written on every change or e.g. only while shut down, etc. Default value explains which values are written during creation or Set to Delivery state. File System rights are the minimum needed access rights (e.g. for concurrent usage). ” Deletion while SW update” describes the behavior, when a SW Update is executed (e.g. file is deleted during update or not (if not, data needs to be converted by owner at next startup if needed))

Location in flash

Short description

Used persistence mechanism (see 0)

Max Size

When read and written?

Default data

File system rights

Deletion while SW update? [yes/no] 

### Configuration

DTV HAL should be started based on Module availability/Region based system property, currently there are

no interactions planned with configHub

## Critical Computer Resources (CPU, RAM, Flash)

This section describes the prediction of the CPU needs, Flash and RAM of the Subsystem. 

SW Modul

CPU [% of one ARM 9 core)

Flash (see Data list)

Max RAM[MB]

GPU Memory

[MB]

## Install View

This section describes where the files (executables, libraries, data) of the SW module are stored in the flash file system or at other locations.

File

Directory

Description

vendor.bosch.hardware.dtv@1.0

Binary Path in Source: out/target/product/aivi2_n_full_us/vendor/lib64/ vendor.bosch.hardware.dtv@1.0.so

Binary Path in Target: 

vendor/lib64/vendor.bosch.hardware.dtv@1.0.so

system/lib64/vendor.bosch.hardware.dtv@1.0.so

HIDL library

vendor.bosch.hardware.dtv@1.0-service

Binary Path in Source: out/target/product/aivi2_n_full_us/vendor/bin/hw/ vendor.bosch.hardware.dtv@1.0-service

Binary Path in Target: 

vendor/bin/hw/vendor.bosch.hardware.dtv@1.0-service

DTV HAL

## Security User and Groups

All needed users and groups to implement the Multi-User-Security-Concept are listed here.

Process

User

Needed groups

vendor.bosch.hardware.dtv@1.0-service

system

system

# Testing & Debugging

DTV HAL and framework service is tested using DTV Demo Application.

Traces related to DTV Hal can be checked in logcat by searching for tag dtvhal,dtvlib and log level can be controlled using below command

setprop persist.log.tag.dtvlib DEBUG

setprop persist.log.tag.dtvhal DEBUG

## VTS

VTS (Vendor Test Suite) is a set of test cases and framework designed to test the following components:

Hardware Abstraction Layer (HAL) modules

Vendor native libraries (e.g., Vendor NDK, shortly VNDK)

OS (i.e., Linux kernel)

VTS covers both functional and non-functional.

The test cases are divided into modules and grouped together in plans.

### VTS Test Cases

Test cases in VTS test cases go into modules (files)

A module can contain one or more test cases. All test cases are considered individually for reporting purpose, as long as the right template is used.

Modules can be run individually.

Figure 10

Each module has its own folder, somewhere within the previously shown structure.

The code for the test case/s itself might reside in either of Python, C or C++ file.

Each test case will generally be a function, name prefixed with test/TEST/TEST_F/TEST_P

### How to run VTS testcases

Trade Federation (Tradefed or TF for short) is a continuous test framework designed for running tests on Android devices. For example, Tradefed is used to run the VTS.

Trade Federation is a Java application which runs on a host computer and communicates to one or more Android devices over ADB.

 VTS test Plan can be run via the commands vts-tradefed and run vts

 Default run vts runs all the available vts testcases under every module, you can provide options to the vts run command, to run a specific module or run a specific test case from a module.

# Requirements to other Components

Requirements to other components based on architecture work within this document are listed here.

Component / Generic

Requirement

# Source Code Reference

## DTV HAL

vendor/bosch/hardware/interfaces/dtv/1.0

## DTV Config

vendor/bosch/hardware/interfaces/dtv/dtvconfig

# Open Points

Handling of temp alert from module

Handling shutdown seqeunce

Handling of DTC

Firmware update concept from swupdate team

# References and Related Documents

Link

Link

Scope

Test Specification

Document to record sensible test cases which are created with the test team.

Architecture Roadmap

If available:

RSL Document: https://sites.inside-share2.bosch.com/sites/152810/Documents/0400.Software/04.Work_Products/02.SW_Architecture/F-A14-01_Alliance Android Software Platform Architecture Constraints-v4.7.pdf

Requirement Specification

DTC interface references

The diag resource file defining the DTC interface:

https://rbcm-ccs2-opengrok.de.bosch.com/source/xref/ccs2_qpr3_a12_int/vendor/alliance/hardware/interfaces/automotive/diagnosis/2.0/default/inc/DiagDTV.h

# Contacts

List of persons who maintain this module as well as persons who should be asked for acceptance when the interface or the behavior of the module shall be changed (e.g. if a message format shall be changed) 

No

Name

Comment

# Amendments

## Revision History  

Date

Version

Status

Review-Minutes

Amendments

Author

22/06/2023

0.1

UPDATE

Add “Sync handler - Blocking call” item

Nguyen Quoc Dat 

(MS/EMC23-XC)

03/11/2023

1.0

Release

Review corrections

Chaitra Bharadwaj

01/04/2024

1.1

UPDATE

Add “Software update” item

Nguyen Quoc Dat 

(MS/EMC21-XC)

17/04/2024

1.1

UPDATE

Update the Software update sequence diagrams.

Nguyen Quoc Dat

(MS/EMC21-XC)

02/05/2024

1.1

UPDATE

Add “Diagnostic Trouble Code (DTC) handling” item

Nguyen Quoc Dat

(MS/EMC21-XC)

01/07/2024

1.1

UPDATE

Add “DTV Critical Error” item

Nguyen Quoc Dat 

(MS/EMC21-XC)

18/07/2024

1.2

UPDATE 

Add “Low Voltage Handling” item and “Antenna Monitoring” item

Ajay J Thampy (MS/ECR6-XC)

05/02/2025

1.3

UPDATE

Add “Software Update Validation” item.

Update the Low Voltage Handling content to reflect the change in the range for powering OFF/ON the TV module and Antenna.

Nguyen Quoc Dat

(MS/EMC21-XC)

30/05/2025

1.4

UPDATE

Update the “Software Update Validation” sequence for testing firmware and add the “SW Update Mode Identification” figure in page 15 and 16.

Nguyen Quoc Dat 

(MS/EMC21-XC)

09/06/2025

1.5

UPDATE

Add “Death Recipients Handling” for DTV clients and sequences for DTC, System voltage and Thermal Hal clients in page 32, 33, 34 and 35.

Ganesh Raju Nandi (MS/ECR-XC)

26/09/2025

1.6

UPDATE

Update the “Software Update” sequence and state machine diagrams in page 17, 18, 19 and 20.

Nguyen Quoc Dat (MS/EMC21-XC)

16/07/2026

1.7

UPDATE

Add the CarPowerManager state machine and update SHUTDOWN_CANCELLED handling for the “6.3.5 Suspend to Disk” item

Nguyen Quoc Dat (MS/EMC32-XC)


**Table:**


SW Concept and Design Description

DTV HAL – CCS2.0




**Table:**


Version:        1.7 16.07.2026

Status:          Release

Approval | Date: 16.07.2026 | General Approval Form [Approval Data / Link]

Distribution listName/DepartmentRole in projectMeda Srikanth Reddy (MS/ECR1-XC)Component ArchitectN.N.Safety Manager (if applicable)Nisharani C Paramba (MS/ECR6-XC)Project ManagerRecipients: add further stakeholders if needed | Name/Department | Role in project | Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect | N.N. | Safety Manager (if applicable) | Nisharani C Paramba (MS/ECR6-XC) | Project Manager | Reviewer listName/DepartmentRole in projectReviewer or approverKavadapu Narasimhulu(MS/ECR1-XC)Component Product OwnerApproverMeda Srikanth Reddy (MS/ECR1-XC)Component ArchitectApproverN.N.Safety Team (if applicable)ReviewerCherishnav Reddy Chittamuru (MS/ECR1-XC) SW-ContributorReviewerPradeep S (MS/ERC1-XC)SW-ContributorReviewerNguyen Quoc Dat (MS/EMC32-XC)SW-ContributorReviewerChanges are announced via stages update information, no distribution as printed version, provision in the Intranet: see footer. | Name/Department | Role in project | Reviewer or approver | Kavadapu Narasimhulu(MS/ECR1-XC) | Component Product Owner | Approver | Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect | Approver | N.N. | Safety Team (if applicable) | Reviewer | Cherishnav Reddy Chittamuru (MS/ECR1-XC) | SW-Contributor | Reviewer | Pradeep S (MS/ERC1-XC) | SW-Contributor | Reviewer | Nguyen Quoc Dat (MS/EMC32-XC) | SW-Contributor | Reviewer

Name/Department | Role in project

Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect

N.N. | Safety Manager (if applicable)

Nisharani C Paramba (MS/ECR6-XC) | Project Manager

Name/Department | Role in project | Reviewer or approver

Kavadapu Narasimhulu(MS/ECR1-XC) | Component Product Owner | Approver

Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect | Approver

N.N. | Safety Team (if applicable) | Reviewer

Cherishnav Reddy Chittamuru (MS/ECR1-XC) | SW-Contributor | Reviewer

Pradeep S (MS/ERC1-XC) | SW-Contributor | Reviewer

Nguyen Quoc Dat (MS/EMC32-XC) | SW-Contributor | Reviewer




**Table:**


Name/Department | Role in project

Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect

N.N. | Safety Manager (if applicable)

Nisharani C Paramba (MS/ECR6-XC) | Project Manager




**Table:**


Name/Department | Role in project | Reviewer or approver

Kavadapu Narasimhulu(MS/ECR1-XC) | Component Product Owner | Approver

Meda Srikanth Reddy (MS/ECR1-XC) | Component Architect | Approver

N.N. | Safety Team (if applicable) | Reviewer

Cherishnav Reddy Chittamuru (MS/ECR1-XC) | SW-Contributor | Reviewer

Pradeep S (MS/ERC1-XC) | SW-Contributor | Reviewer

Nguyen Quoc Dat (MS/EMC32-XC) | SW-Contributor | Reviewer




**Table:**


Term or Abbreviation | Description

Component Model | In the IEEE standard 1026-1998 the component model is called the decomposition view and in RUP it is called the logical view.

Design Pattern | General approach to solve a common design problem, e.g. observer pattern. A design pattern consists of a problem statement, a solution and consequences (pros and cons).

Dynamic Model | A set of classes that work together to realize a use case, also called collaboration or mechanistic design. In the IEEE standard 1026-1998 the dynamic model is called the dependency description.

IDL | Interface Definition Language

RM | Requirement Management

State Chart | State charts are a formal behavioral language. State charts are particularly effective when the use case is reactive; that is, it has inherent states (conditions) and remains in those conditions until an event of interest has occurred. A state chart is more precise and less likely to be misinterpreted than text, but it is harder to understand. Therefore it should be used together with text and sequence diagrams.

SW | Software

SWAD | Software Architecture Document

Use Case | A use case is a named capability of a structural entity in a model. Use cases organize requirements into chunks. They help to detect open requirements. It is common for a use case to represent and organize many pages of textual requirements or dozens of usage scenarios.




**Table:**


Req No | Scope | Details

R1 | TV Module communication | Provides interface to exchange communication between Host and TV Module

R2 | Firmware update | Provides interface and implementation of TV module firmware update

R3 | TV Module Diagnosis | Diagnosis handling of TV Module related to uart, temp alert, operation, trmp

R4 | TV Module power | 

R5 | Antenna Diagnosis | Handling of Antenna output power and monitoring




**Table:**


DTC code | Value | Fault type | Value | DTC Status

DTC_DTV_ANTENNA1 | 0x938C | FT_SHORT_TO_GROUND | 0x11 | PASS/ FAIL

 |  | FT_OPEN_LOAD | 0x13 | 

DTC_DTV_ANTENNA2 | 0x938D | FT_SHORT_TO_GROUND | 0x11 | PASS/ FAIL

 |  | FT_OPEN_LOAD | 0x13 | 

DTC_DTV_ANTENNA3 | 0x938E | FT_SHORT_TO_GROUND | 0x11 | PASS/ FAIL

 |  | FT_OPEN_LOAD | 0x13 | 

DTC_DTV_ANTENNA4 | 0x938F | FT_SHORT_TO_GROUND | 0x11 | PASS/ FAIL

 |  | FT_OPEN_LOAD | 0x13 | 




**Table:**


Thread | Process space | Started by | Description incl. concurrency issues

DTV Hal Main Thread |  | HwServiceManager | This thread is created at service startup

uartTxHandler |  | DTV Hal Main Thread | This thread handles sending requests and processing response from TV Module

uartRxHandker |  | DTV Hal Main Thread | This thread receives data from TV Module via UART port and forms full packet and adds into messageQ

eventObserver |  | DTV Hal Main Thread | This thread serializes all message and timer events. All callbacks out of dtvlib is posted from this thread context




**Table:**


SW Module | Used Storage Mechanism




**Table:**


Location in flash | Short description | Used persistence mechanism (see 0) | Max Size | When read and written? | Default data | File system rights | Deletion while SW update? [yes/no]




**Table:**


SW Modul | CPU [% of one ARM 9 core) | Flash (see Data list) | Max RAM[MB] | GPU Memory[MB]




**Table:**


File | Directory | Description

vendor.bosch.hardware.dtv@1.0 | Binary Path in Source: out/target/product/aivi2_n_full_us/vendor/lib64/ vendor.bosch.hardware.dtv@1.0.soBinary Path in Target: vendor/lib64/vendor.bosch.hardware.dtv@1.0.sosystem/lib64/vendor.bosch.hardware.dtv@1.0.so | HIDL library

vendor.bosch.hardware.dtv@1.0-service | Binary Path in Source: out/target/product/aivi2_n_full_us/vendor/bin/hw/ vendor.bosch.hardware.dtv@1.0-serviceBinary Path in Target: vendor/bin/hw/vendor.bosch.hardware.dtv@1.0-service | DTV HAL




**Table:**


Process | User | Needed groups

vendor.bosch.hardware.dtv@1.0-service | system | system




**Table:**


Component / Generic | Requirement




**Table:**


Link | Link | Scope

 | Test Specification | Document to record sensible test cases which are created with the test team.

 | Architecture Roadmap | If available:RSL Document: https://sites.inside-share2.bosch.com/sites/152810/Documents/0400.Software/04.Work_Products/02.SW_Architecture/F-A14-01_Alliance Android Software Platform Architecture Constraints-v4.7.pdf

 | Requirement Specification | 

 | DTC interface references | The diag resource file defining the DTC interface:https://rbcm-ccs2-opengrok.de.bosch.com/source/xref/ccs2_qpr3_a12_int/vendor/alliance/hardware/interfaces/automotive/diagnosis/2.0/default/inc/DiagDTV.h




**Table:**


No | Name | Comment




**Table:**


Date | Version | Status | Review-Minutes | Amendments | Author

22/06/2023 | 0.1 | UPDATE |  | Add “Sync handler - Blocking call” item | Nguyen Quoc Dat (MS/EMC23-XC)

03/11/2023 | 1.0 | Release |  | Review corrections | Chaitra Bharadwaj

01/04/2024 | 1.1 | UPDATE |  | Add “Software update” item | Nguyen Quoc Dat (MS/EMC21-XC)

17/04/2024 | 1.1 | UPDATE |  | Update the Software update sequence diagrams. | Nguyen Quoc Dat(MS/EMC21-XC)

02/05/2024 | 1.1 | UPDATE |  | Add “Diagnostic Trouble Code (DTC) handling” item | Nguyen Quoc Dat(MS/EMC21-XC)

01/07/2024 | 1.1 | UPDATE |  | Add “DTV Critical Error” item | Nguyen Quoc Dat (MS/EMC21-XC)

18/07/2024 | 1.2 | UPDATE |  | Add “Low Voltage Handling” item and “Antenna Monitoring” item | Ajay J Thampy (MS/ECR6-XC)

05/02/2025 | 1.3 | UPDATE |  | Add “Software Update Validation” item.Update the Low Voltage Handling content to reflect the change in the range for powering OFF/ON the TV module and Antenna. | Nguyen Quoc Dat(MS/EMC21-XC)

30/05/2025 | 1.4 | UPDATE |  | Update the “Software Update Validation” sequence for testing firmware and add the “SW Update Mode Identification” figure in page 15 and 16. | Nguyen Quoc Dat (MS/EMC21-XC)

09/06/2025 | 1.5 | UPDATE |  | Add “Death Recipients Handling” for DTV clients and sequences for DTC, System voltage and Thermal Hal clients in page 32, 33, 34 and 35. | Ganesh Raju Nandi (MS/ECR-XC)

26/09/2025 | 1.6 | UPDATE |  | Update the “Software Update” sequence and state machine diagrams in page 17, 18, 19 and 20. | Nguyen Quoc Dat (MS/EMC21-XC)

16/07/2026 | 1.7 | UPDATE |  | Add the CarPowerManager state machine and update SHUTDOWN_CANCELLED handling for the “6.3.5 Suspend to Disk” item | Nguyen Quoc Dat (MS/EMC32-XC)

