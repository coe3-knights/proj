# PROJECT MANAGEMENT SOFTWARE

## **Software Requirements Specification**

**_Version:_** _1.0_

**_Status:_** _Draft_

**_Prepared by:_** _Quansah Anthony J.K.J_

**_Developed by:_** _THE KNIGHTS_

**_Date:_** _16th April, 2019_
___

## Table of Contents

### 1. [Introduction](#Introduction)

* [Purpose](#Propose)
* [Intended Audience and Reading Suggestion](#Intended-Audience-and-Reading-Suggestion)
* [Product Scope](#Product-Scope)
* [References](#References)

### 2. [Overall Description](#Overall-Description)

* [Product Perspective](#Product-Perspective)
* [Product Functions](#Product-Functions)
* [User Classes and Characteristics](#User-Classes-and-Characteristics)
* [Operating Environment](#Operating-Environment)
* [Design and Implementation Constraints](#Design-and-Implementation-Constraints)
* [User Documentation](#User-Documentation)
* [Assumptions and Dependencies](#Assumptions-and-Dependencies)

### 3. [External Interface Requirements](#External-Interface-Requirements)

* [User Interfaces](#User-Interfaces)
* [Hardware Interfaces](#Hardware-Interfaces)
* [Software Interfaces](#Software-Interfaces)
* [Communications Interfaces](#Communications-Interfaces)

### 4. [Domain Model](#Domain-Model)

___

## Revision History

| Name | Date | Reason for changes | Version | Date of Approval |
|------|------|--------------------|---------|------------------|
|Blessed Boakye Britwum | May 25, 2019 | Ported the document into markdown | 1.0 | May 27,2019 |
|      |      |                    |         |                  |
|      |      |                    |         |                  |
___

## Introduction

### Purpose

This Software Requirement Documentation is exclusively for the Project Management Software under development by the The Knights. This SRS is intended to provide the scope of the aforementioned software, from customer level to developer level. This SRS focuses on the entire software project as a whole and will thus contain all necessary information associated to it.

### Intended Audience and Reading Suggestions

Below is a table that describes the various stakeholders or audience directly associated to the aforementioned software.
|ID|Stakeholder|Description|
|----|----|----|
|S-1|Customer|Checking correspondence of business goals and functionality requirements to the expectations from implementing the product.|
|S-2|Development team|Forming the accurate vision of the project, detailed functional and nonfunctional requirements.|
|S-3|QA team|Making test-plans and test-cases.|
|S-4|PM/BA|Estimating the quote of the project, planning resources and the timeline of work.|
|S-5|User|Basing on this document the Terms of Service and the Privacy Policy are created.|

### Product Scope

The Project Management Software is a web based software program that:

* Serves as a project repository for approved projects of varying fields.
* Allows stakeholders to access uploaded projects or upload projects based on different levels of access rights.
* Stakeholders may decide to register an account or not; stakeholder (users) with accounts will have more access to some features of the software than free roaming users.

The aforementioned software will go a long way in helping users make their research work more easier and relatively faster due to the availability of different reference materials that will help users to increase their options of approach for projects they may be working on. Targeted users are students, tertiary level ones to be precise.

### References

The hyperlink below leads directly to the Version control site for the SRS
<https://github.com/the-Knights>

List any other documents or Web addresses to which this SRS refers. These may include user interface style guides, contracts, standards, system requirements specifications, use case documents, or a vision and scope document. Provide enough information, so that the reader could access a copy of each reference, including title, author, version number, date, and source or location (if applicable)
___

## Overall Description

This section:

* contains general view of the project
* environment where it will be used
* description of expected user audience and constraints
* assumptions and dependencies which can be identified

### Product Perspective

The Project Management System is a self-contained product jeered towards helping users improve the quality of their work (projects). Though there may be other similar products in market, this product is not in any way a follow-on member of another product family or a replacement for existing systems. It is new and as specified earlier, self-contained.

#### Product Functions

Summarize the major functions the product must perform or must let the user perform. Details will be provided in Section 3.
A picture of the major groups of related requirements and their interactions, such as a top level data flow diagram or object class diagram, is often effective.

The PMS has the following functions:

* Users can Sign up for an account
* Users can upload projects
* Users can search for available projects
* Users can download some parts of projects, ie. project reports but not source code or full content of project scope.
* Other stakeholders (administrator .ie lecturer) can rate supervised projects.
* Users without accounts  cannot upload projects, however they can search and download some projects.

### User Classes and Characteristics

|ID|User classes|Description|
|--|--|--|
|U-1|Administrator|A signed up user who has completed the account activation. He owns expanded rights inside the portal. He performs the content pre moderation.|
|U-2|Signed up user|A user of the portal who has completed the sign up on the portal and the account activation.|
|U-3|Not signed up user|A user of the portal who has completed neither the sign up on the portal, nor the account activation. He owns limited rights inside the portal.|

### Operating Environment

The operating environment for the Project Management System:

* The PMS will run on the web
* Suitable operating systems:
  * Windows
  * IOS
  * Linux OS distros
* The PMS will require a hardware; personal computer, to be able to run

### Design and Implementation Constraints

The bullets below enlists the various implementation constraints needed to implement the PMS:

* SPECIFIC TECHNOLOGIES, TOOLS AND DATABASES TO BE USED
  * python programming language
  * flask
  * react
  * SQLite
* HARDWARE LIMITATIONS
  * Internet-In order
  * Access to relatively fast internet
  * IDE
* BINDING AGREEMENTS  
  * Work agreement between customer and the_Knight
* STANDARD DATA EXCHANGE FORMAT
  * JSON
* DESIGN CONVENTIONS/ PROGRAMMING STANDARDS
  * The_Knights will be in charge of maintainance
* LANGUAGE REQUIREMENTS
  * English
* COMMUNICATION PROTOCOLS
  * HTTP
  * SMTP
* SECURITY CONSIDERATIONS
  * N/A
  
### User Documentation

User documentation formats that will be delivered along with the software:

* Online help
* Tutorials
* User documents

### Assumptions and Dependencies

#### ASSUMPTIONS

Information was not given.  
The development Team; The_Knights will base on their thoughts and assumptions while developing  the required application, however prioritizing clients interests in the chain of decision making.

#### DEPENDENCIES
