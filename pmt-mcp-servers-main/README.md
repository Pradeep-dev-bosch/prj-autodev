# PMT@XC: Leveraging AI @ BOSCH with MCP, Prompts, Skills and Agents

This repository is a collection of MCP servers, prompts, skills and custom agents. Feel free to use and adapt everything you can find. You are encouraged to share best practices or your project applications with us.

As [PMT@XC](https://inside-docupedia.bosch.com/confluence2/x/1GAYEw) we aim to [leverage AI](https://inside-docupedia.bosch.com/confluence2/x/HMP3Lg) by tuning e.g. your GitHub Copilot.

## Available MCP Servers

**Description**: MCP is an open-source standard for connecting AI applications to tools (Tool integration). An AI application can call tools to retrieve facts and take actions. We aim to provide MCP servers for all tools on the [XC tool heatmap](https://inside-docupedia.bosch.com/confluence2/x/Lq2HF).

![mcp-simple-diagram](img/mcp-simple-diagram.png)

**Usage**: Using the MCP servers is optimized for a local developer setup. Check out the respective README.md. Be aware that MCP servers wrap a tool API. Access is managed by the API owner.

**Goal**: Use the provided MCP servers locally. Please [report bugs](https://github.com/bosch-rbadas/pmt-mcp-servers/issues/new?template=bug_report.md) and [request a new feature](https://github.com/bosch-rbadas/pmt-mcp-servers/issues/new?template=feature_request.md)

**Further info**: [MCP](https://modelcontextprotocol.io/docs/getting-started/intro)

- **[Artifactory](src/artifactory/README.md)** - JFrog Artifactory is artifact repository manager that supports all major package formats and integrates with CI/CD pipelines for binary management and distribution.
- **[Azure Cosmos DB](src/azure/azurecosmosdb/README.md)** - Azure Cosmos DB is a fully managed NoSQL, relational, and vector database.
- **[Azure Infra](src/azure/azureinfra/README.md)** - Azure Infra MCP server enables integration with Microsoft Azure cloud resources and services.
- **[Azure DevOps](src/azure/azuredevops/README.md)** - Azure DevOps MCP server provides access to Azure DevOps pipelines, boards, repos, and artifacts.
- **[Bitbucket](src/bitbucket/README.md)** - Bitbucket is a Git-based source code repository hosting service by Atlassian, supporting collaborative development, code review, and CI/CD integration.
- **[CANoe](src/canoe/README.md)** - Vector CANoe is a comprehensive development and test tool used in automotive engineering to simulate, analyze, and validate ECU communication over networks like CAN, LIN, FlexRay, and Ethernet.
- **[CCM](src/ccm/README.md)** - IBM Engineering Workflow Management is a change and configuration management (CCM) solution that enables teams to manage software development artifacts, track changes, and maintain version control across the development lifecycle.
- **[Codebeamer](src/codebeamer/README.md)** - Codebeamer is an enterprise Application Lifecycle Management (ALM) platform developed by Intland Software (now part of PTC), specifically designed for regulated industries and complex product development.
- **[Conan](src/conan/README.md)** - Conan is a python-based fully decentralized, portable package manager for C and C++ developers which helps in managing binaries and integrates with any build system.
- **[DIA Brain](src/diabrain/README.md)** - DIA Brain MCP server provides seamless integration with Bosch DIA Brain knowledge retrieval system, enabling queries across knowledge bases including SharePoint sites and Docupedia spaces for retrieval-augmented generation.
- **[DNG](src/dng/README.md)** - IBM® Engineering Requirements Management DOORS® Next is a requirements management application that helps you store, categorize, link, and share product requirements with stakeholders such as reviewers, designers, testers, and developers.
- **[Docupedia](src/docupedia/README.md)** - Docupedia is internal knowledge management and documentation platform for sharing technical information, processes, and collaborative content across the organization.
- **[DRIVE Companion](src/drivecompanion/README.md)** - DRIVE Companion is a CR-driven agentic multimodal system for BBM Drive, delivering intelligent assistance via advanced Retrieval-Augmented Generation (RAG). It integrates adaptive data onboarding, multimodal LLM reasoning, Knowledge Graphs, and optimized multi-agent pipelines with robust ranking and hallucination mitigation.
- **[Enterprise Architect](src/enterprisearchitect/README.md)** - Enterprise Architect (EA) is a comprehensive visual modeling and design tool developed by Sparx Systems, widely used for software and systems engineering.
- **[ETM](src/etm/README.md)** - IBM Engineering Test Management (ETM) is a collaborative quality management solution, that provides end-to-end test planning and test asset management, covering everything from requirements to defects.
- **[GitHub Actions](src/gh-actions/README.md)** - GitHub Actions is a powerful CI/CD (Continuous Integration/Continuous Deployment) platform built into GitHub that allows you to automate workflows directly in your repository.
- **[GitHub](src/github/README.md)** - GitHub is a platform used for hosting code and collaborating on software projects.
- **[Jenkins](src/jenkins/README.md)** - Jenkins is an open-source automation server that enables continuous integration and continuous delivery (CI/CD) for building, testing, and deploying software projects.
- **[Jira](src/jira/README.md)** - Jira is a popular project management and issue tracking software developed by Atlassian, widely used for agile software development and project management.
- **[Outlook](src/outlook/README.md)** - Microsoft Outlook is an email, calendar, and contact management application that integrates with Microsoft 365 and Exchange Server for enterprise communication and collaboration.
- **[QAC](src/qac/README.md)** - Perforce QAC is a Source Code Analysis Management framework for managing source code analysis projects and analyzers. It is designed to provide you with an Analysis System that handles several programming languages, using selectable analysis components.
- **[Screenshot](src/screenshot/README.md)** - Screenshot MCP server provides Windows screenshot capture capabilities for AI-assisted visual documentation and debugging workflows.
- **[SharePoint Cloud](src/sharepoint/sharepointcloud/README.md)** - SharePoint Cloud MCP server provides seamless integration with Microsoft SharePoint Online, enabling document management, file sharing, and collaboration.
- **[SharePoint On-Premises](src/sharepoint/sharepointonprem/README.md)** - SharePoint On-Premises MCP server enables integration with Microsoft SharePoint On-Premises sites, supporting NTLM authentication and advanced file and folder management.
- **[Stardog](src/stardog/README.md)** - Stardog is a knowledge graph platform that combines graph database technology with semantic web standards to create intelligent data management solutions.
- **[Splunk](src/splunk/README.md)** - Splunk is a platform for searching, monitoring, and analyzing machine-generated data through a web-style interface, providing real-time insights and operational intelligence with powerful SPL query language and security guardrails.
- **[Zuul CI](src/zuul/README.md)** - Zuul CI is a project gating system that enables continuous integration and delivery pipelines with sophisticated job dependencies, multi-repository testing, and speculative execution of changes.

## Prompts

**Description**: Prompts are the communication with an AI application.

**Usage**: Repeatable prompts can be invoked via / commands in the GitHub Copilot chat window.

**Goal**: Use the below prompts as a template and add and adapt it for your projects. Create your own prompts folder with all useful prompts in your project.

**Further info**: [Slash commands](https://docs.github.com/en/copilot/reference/cheat-sheet#slash-commands-1)

| Prompt | Contributor | Project | Description | Duration Without Prompt | Duration With Prompt | MCP Servers |
| --- | --- | --- | --- |  --- | --- | --- |
| **[Conan_Build_Workflow](.github/prompts/Conan_Build_Workflow-[Akash].prompt.md)** | **Akash** (MS/ESF2-XC) | RADAR 7 | Complete Conan build workflow for DSP and ARM profiles | 10 mins | 5 mins | Conan |
| **[Conan_Editable_Workflow](.github/prompts/Conan_Editable_Workflow-[Akash].prompt.md)** | **Akash** (MS/ESF2-XC) | RADAR 7 | Complete Conan editable package workflow for local development with multi-profile builds using optimized iteration pattern | 25 mins | 15 mins | Conan |
| **[Docupedia_to_Jira](.github/prompts/Docupedia_to_Jira-[Sozhan].prompt.md)** | **Sozhan** Natarajan (MS_ESF2-XC) | Template | Instructions to create Jira issue from Docupedia design page with bidirectional links | 15 mins | 5 mins | Docupedia, Jira |
| **[Jenkins Build Failure Analysis](.github/prompts/Jenkins_Build_Analyzer-[Swaroop].prompt.md)** | **Swaroop M R** (MS/ESF1-XC) | - | Analyze Jenkins build failures, identify root cause, and suggest fixes | 15 mins | 5 mins | Jenkins |

## Skills

**Description**: Skills are a format for extending AI application capabilities with specialized knowledge and workflows. A skill is like documentation on how to do something.

**Usage**: Your agent will have the skill description in its context and chooses the skill based on this. Pick and add the needed skills to your project.

**Goal**: Pick and add the needed skills to your project. Create your own skills and share them.

**Further info**: [Agent Skills](https://agentskills.io/what-are-skills)

| Skill | Contributor | Project | Description | Duration Without Skill | Duration With Skill | MCP Servers |
| --- | --- | --- | --- |  --- | --- | --- |
| **[skill-creator](.github/skills/skill-creator/SKILL.md)** | **Bhargav** K M (MS/EVV1-XC) | - | Skill to create effective skills. |  - | - | - |
| **[vector-canoe](.github/skills/vector-canoe/SKILL.md)**| **Bhargav** K M (MS/EVV1-XC) | - | Skill to use Vector CANoe automotive testing and simulation toolkit. |  - | - | Canoe |

## Agents

**Description**: Custom agents are a way to create distinct identities and with specific tools for a specific task or domain.

**Usage**: Invoke with @ or select the custom agent in the GitHub Copilot chat window.

**Goal**: Use the below custom agents as a template and add and adapt it for your projects. Create your own agents folder with all useful agents in your project.

**Further info**: [Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)

| Agent | Contributor | Project | Description | Duration Without Agent | Duration With Agent | MCP Servers |
| --- | --- | --- | --- | --- | --- | --- |
| **[Conan_Build_Workflow](.github/agents/Conan_Build-[Akash].agent.md)** | **Akash** (MS/ESF2-XC) | RADAR 7 | Execute Conan package manager workflows with profile management and dependency analysis | 10 mins | 5 mins | Conan |
| **[Conan_Editable_Workflow](.github/agents/Conan_Editable-[Akash].agent.md)** | **Akash** (MS/ESF2-XC) | RADAR 7 | Execute complete Conan editable package workflow with multi-profile builds using optimized iteration pattern | 25 mins | 15 mins | Conan |
| **[Continous_Integration_Autonomous_Assist](.github/agents/Continous_Integration_Autonomous_Assist-[Jyothi].agent.md)** | **Jyothi** Lakshmikanth (MS/PJ-AI-CE-XC) | planned: EVC-CE, PK | CIAA Build Orchestrator Agent helps developers to fix build issues in their codebase using the CIAA methodology | 4 hours | 1.5 hours | Planned: Jenkins, Azure DevOps |
| **[Create_Unit_Test](.github/agents/Create_Unit_Test-[Aashik].agent.md)** | Kundukulam **Aashik** (MS_ENE-EAB1-XC) | RA7-Radar PF-BoschAsOEM, RADAR SGU PF, MPC4 COM | Creating unittest file for selected files | 2 days | 0.5 day | - |
| **[Customer_Acquisition_Helper](.github/agents/Customer_Acquisition_Helper-[Christof].agent.md)** | Hammel **Christof** (XC-AS/ESY)<br>**Bhargav** K M (MS/EVV1-XC) | Toyota | Helper agent to provide comprehensive assistance for questions, concerns, and requests regarding acquisition projects, Bosch ADAS products, systems, and all associated artifacts | 1 month | 0.5 month | Sharepoint, Cosmos DB, DRIVE Companion |
| **[Docupedia_To_Jira](.github/agents/Docupedia_to_Jira-[Sozhan].agent.md)** | **Sozhan** Natarajan (MS_ESF2-XC) | Template | Turning Docupedia design pages into concise Jira issues and link them both ways. | 15 mins | 5 mins | Docupedia, Jira |
| **[Jenkins_Build_Analyzer](.github/agents/Jenkins_Build_Analyzer-[Swaroop].agent.md)** | **Swaroop M R** (MS/ESF1-XC) | - | Jenkins CI/CD Expert Agent that analyzes build failures, diagnoses pipeline issues, and suggests actionable fixes | 15 mins | 5 mins | Jenkins |
| **[Feature_integration_Analyst](.github/agents/Feature_Integration_Analyst-[Jyothi].agent.md)** | **Jyothi** Lakshmikanth (MS/PJ-AI-CE-XC) | Perfectly Keyless (PK) | Designs feature integrations as UML sequence diagrams with 5-Why justification with no implement | - | - | - |
| **[Requirements_to_Design](.github/agents/Requirements_to_Design-[Yuvika].agent.md)** | Tech: Dev Sharma **Yuvika** (MS_ENS4-XC),  Prod: Bhatnagar **Medha** (MS_ENS3-XC) | OneParking, RA7-Radar | Master orchestrator agent that coordinates requirements-to-design transformation by delegating specialized tasks to sub-agents for extraction, review, generation, and validation | 5 hours | 4 hours | Codebeamer, DNG |
| **[Scenario_Engineer](https://github.com/bosch-rbadas/core/blob/main/pace/.github/agents/scenario-engineer/README.md)** | Seyboth **Georg** (XC-AS/EAC-ADA-T) | ADA | Transform Codebeamer scenario elements into well-structured scenario specifications in Sphinx-Needs, following ISO 34501/34502/34503 and Pegasus methodology, and maintain traceability | --- | --- | Codebeamer |
| **[System_Requirements_Engineer](https://github.com/bosch-rbadas/core/blob/main/pace/.github/agents/sysreq-engineer/README.md)** | Seyboth **Georg** (XC-AS/EAC-ADA-T) | ADA | Transform agreed stakeholder requirements into high‑quality system requirements in Sphinx‑Needs, maintain traceability to Codebeamer, and enforce human QA gates | --- | --- | Codebeamer |

## ⚠️ Disclaimer ⚠️

**Be aware that any action taken by the LLM via MCP server or agents or prompt or agentic workflow is done with your username**
**Be aware that an LLM is stochastic and not deterministic - results vary each time**
