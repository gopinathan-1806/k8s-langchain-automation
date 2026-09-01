# ⚡ K8s AI Doctor

AI-powered Kubernetes incident diagnosis using **IBM Cloud IKS,
Kubernetes API, LangChain, OpenAI, LangSmith, and Streamlit**.

## Overview

K8s AI Doctor is a **read-only Kubernetes troubleshooting assistant**.

It connects to a Kubernetes cluster, discovers unhealthy workloads,
collects Kubernetes evidence, sends the evidence to an OpenAI model
through LangChain, and presents an evidence-based root-cause analysis
through a Streamlit web interface.

``` text
Kubernetes Cluster
       │
       ▼
Kubernetes API
       │
       ▼
Evidence Collection
       │
       ▼
Diagnostic Engine
       │
       ▼
LangChain
       │
       ▼
OpenAI
       │
       ▼
Structured RCA
       │
       ▼
Streamlit UI
```

## Goal

The project is designed to provide hands-on learning with:

-   Python and virtual environments
-   Kubernetes API integration
-   IBM Cloud IKS
-   Kubernetes troubleshooting
-   Evidence collection
-   LangChain
-   OpenAI LLM integration
-   Structured AI responses
-   LangSmith observability
-   Streamlit application development
-   AI-assisted DevOps/SRE workflows

## Architecture

``` text
                         ┌──────────────────────┐
                         │      Engineer        │
                         │ Selects Incident     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         │    K8s AI Doctor     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Kubernetes Analyzer  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Kubernetes Client   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     IBM Cloud IKS    │
                         └──────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
                  Pods            Events           Nodes
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │ Evidence Collection  │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │  Diagnostic Engine   │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │      LangChain       │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │       OpenAI         │
                         │         LLM          │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │   Structured RCA     │
                         │ Root Cause           │
                         │ Evidence             │
                         │ Confidence           │
                         │ Recommendations      │
                         │ Safe Commands        │
                         └──────────┬───────────┘
                                    ▼
                         ┌──────────────────────┐
                         │     Streamlit UI     │
                         └──────────────────────┘

                         ┌──────────────────────┐
                         │      LangSmith       │
                         │ Prompt / Input /     │
                         │ Output / Latency /   │
                         │ Token Usage / Trace  │
                         └──────────▲───────────┘
                                    │
                              LangChain Run
```

## Components Used

  Component                  Purpose
  -------------------------- -----------------------------------
  Python                     Application language
  Kubernetes Python Client   Kubernetes API communication
  IBM Cloud IKS              Kubernetes environment
  kubectl                    Kubernetes CLI and authentication
  kubeconfig                 Cluster configuration
  LangChain                  LLM application framework
  OpenAI                     LLM for incident analysis
  LangSmith                  LLM tracing and observability
  Pydantic                   Structured response validation
  Streamlit                  Web frontend

## Project Structure

``` text
langchain-openai-assignment/
│
├── apps/
│   ├── __init__.py
│   ├── main.py
│   ├── analyzer.py
│   ├── diagnostic_engine.py
│   ├── kubernetes_client.py
│   ├── llm.py
│   ├── prompts.py
│   ├── config.py
│   └── test_diagnostics.py
│
├── frontend/
│   └── app.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Environment Variables

Create `.env` in the project root:

``` env
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=k8s-ai-doctor
OPENAI_MODEL=gpt-4o-mini
```

Never hard-code or commit API keys.

Recommended `.gitignore`:

``` gitignore
.env
.venv/
__pycache__/
*.pyc
.DS_Store
```

## Prerequisites

Install/configure:

-   Python 3.10+
-   kubectl
-   Access to an IBM Cloud IKS cluster
-   OpenAI API key
-   LangSmith API key

Verify Python:

``` bash
python3 --version
```

Verify kubectl:

``` bash
kubectl version --client
```

Verify the cluster:

``` bash
kubectl cluster-info
```

Check the active context:

``` bash
kubectl config current-context
```

Verify the namespace:

``` bash
kubectl get pods -n monitoring
```

## Installation

### 1. Enter the project

``` bash
cd langchain-openai-assignment
```

### 2. Create a virtual environment

``` bash
python3 -m venv .venv
```

Activate it:

``` bash
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Add your OpenAI and LangSmith credentials.

## Kubernetes Connectivity

The application uses the Kubernetes configuration available to the local
machine.

Verify:

``` bash
kubectl config current-context
```

``` bash
kubectl cluster-info
```

``` bash
kubectl get pods -n monitoring
```

Test the Python Kubernetes client:

``` bash
python -c "from kubernetes import client, config; config.load_kube_config(); print('Kubernetes client configuration loaded successfully')"
```

## Run Diagnostics

Run from the project root:

``` bash
python apps/test_diagnostics.py
```

or:

``` bash
python -m apps.test_diagnostics
```

Run commands from the project root because the project uses the `apps`
Python package.

## Run the Frontend

Start Streamlit:

``` bash
streamlit run frontend/app.py
```

Open:

``` text
http://localhost:8501
```

## How the Application Works

``` text
1. Engineer opens the Streamlit application
             │
             ▼
2. Application connects to IKS
             │
             ▼
3. Kubernetes API retrieves workloads
             │
             ▼
4. Unhealthy workloads are identified
             │
             ▼
5. Engineer selects an incident
             │
             ▼
6. Kubernetes evidence is collected
             │
             ├── Pod status
             ├── Container state
             ├── Container image
             ├── Kubernetes events
             ├── Scheduling information
             ├── Volume information
             └── Node information
             │
             ▼
7. Evidence is passed to LangChain
             │
             ▼
8. OpenAI analyzes the evidence
             │
             ▼
9. Structured RCA is generated
             │
             ├── Root cause
             ├── Evidence
             ├── Confidence
             ├── Explanation
             ├── Recommendations
             └── Safe kubectl commands
             │
             ▼
10. RCA is displayed in Streamlit
             │
             ▼
11. LangSmith records the LLM execution
```

## Example Incident

A Kubernetes workload may report:

``` text
Pod:
prometheus-alertmanager-0

Status:
Pending

Container:
alertmanager

Image:
quay.io/prometheus/alertmanager:v0.34.0
```

Kubernetes events may contain:

``` text
Failed to pull image

dial tcp ...:443: i/o timeout
```

The application can correlate the evidence and produce a diagnosis such
as:

``` text
Root Cause:
The Kubernetes node is unable to establish a connection
to the container registry.

Confidence:
HIGH
```

The important difference is that the AI diagnosis is based on **actual
Kubernetes evidence**, rather than generic troubleshooting advice.

## LangSmith Observability

LangSmith provides visibility into the LLM execution:

``` text
Streamlit
    │
    ▼
Diagnostic Engine
    │
    ▼
LangChain
    │
    ├──────────────► LangSmith
    │                 ├── Prompt
    │                 ├── Input
    │                 ├── Output
    │                 ├── Latency
    │                 └── Token Usage
    │
    ▼
OpenAI
```

This makes it possible to inspect and debug the AI workflow.

## Safety Model

The application currently follows a **read-only diagnostic model**.

AI may recommend commands such as:

``` bash
kubectl describe pod ...
```

or:

``` bash
kubectl get events ...
```

but it does not automatically execute destructive Kubernetes operations.

``` text
Kubernetes
     │
     ▼
Read-only Evidence
     │
     ▼
     AI
     │
     ▼
Recommendations
     │
     ▼
  Engineer
```

The engineer remains responsible for approving remediation.

## Current Capabilities

-   [x] Python virtual environment
-   [x] Kubernetes Python client
-   [x] IBM Cloud IKS integration
-   [x] Kubernetes pod discovery
-   [x] Kubernetes event collection
-   [x] Evidence collection
-   [x] Incident diagnosis
-   [x] LangChain integration
-   [x] OpenAI integration
-   [x] Structured AI response
-   [x] LangSmith tracing
-   [x] Streamlit frontend
-   [x] Incident selection
-   [x] Root-cause analysis
-   [x] Evidence display
-   [x] Recommended investigation steps
-   [x] Safe kubectl commands
-   [x] Read-only architecture

## Future Enhancements

### V2 --- Multi-resource Investigation

Extend investigation beyond Pods:

``` text
Pod
 │
 ├── Deployment
 ├── ReplicaSet
 ├── Service
 ├── Endpoints
 ├── Node
 ├── PVC / PV
 └── ConfigMap
```

### V3 --- LangChain Tool Calling

``` text
                  AI Agent
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    get_pod()    get_events()  get_logs()
        │            │            │
        ▼            ▼            ▼
     K8s API       K8s API       K8s API
        │            │            │
        └────────────┼────────────┘
                     ▼
                  Evidence
                     │
                     ▼
                    LLM
                     │
                     ▼
                    RCA
```

### V4 --- Incident Correlation

Potential additions:

-   Incident timeline
-   Log analysis
-   Prometheus metrics
-   Service/network troubleshooting
-   Node health correlation
-   Historical incident comparison

### V5 --- AI SRE Assistant

Future capabilities:

``` text
RCA
 +
Incident Chat
 +
Historical Incidents
 +
Metrics
 +
RAG
 +
AI Agents
 +
MCP
 +
Remediation Suggestions
```

## Learning Outcomes

### Python

-   Virtual environments
-   Modules and packages
-   Environment variables
-   API clients
-   Exception handling

### Kubernetes

-   Pods
-   Containers
-   Events
-   Nodes
-   Volumes
-   Namespaces
-   Kubernetes API
-   kubectl
-   IBM Cloud IKS

### GenAI

-   LLM integration
-   Prompt engineering
-   Structured output
-   Evidence-based reasoning
-   LLM application architecture

### LangChain

-   Chat models
-   Prompt templates
-   Chains
-   Structured output
-   Tracing
-   Tool-calling concepts

### OpenAI

-   Chat models
-   API authentication
-   Model configuration
-   Token usage

### LangSmith

-   LLM tracing
-   Observability
-   Prompt inspection
-   Latency analysis
-   Token usage

### Streamlit

-   Interactive UI
-   Session state
-   Dashboard design
-   Dynamic components
-   User input

## Key Architecture Lesson

The most important architectural principle demonstrated by this project
is:

> **Do not send an LLM directly into your infrastructure and ask it to
> figure everything out.**

Instead:

``` text
Infrastructure
      ↓
Evidence
      ↓
Context
      ↓
LLM
      ↓
Structured Decision Support
      ↓
Human
```

Kubernetes remains the **source of truth**.

The LLM acts as an **intelligence layer over operational data**.

## Quick Start

``` bash
cd langchain-openai-assignment
source .venv/bin/activate
kubectl config current-context
kubectl get pods -n monitoring
streamlit run frontend/app.py
```

Open:

``` text
http://localhost:8501
```

## Project Status

  Item            Status
  --------------- -----------------------
  Version         V1.0
  Status          Functional
  Kubernetes      IBM Cloud IKS
  Frontend        Streamlit
  AI Framework    LangChain
  LLM             OpenAI
  Observability   LangSmith
  Mode            Read-only diagnostics

## ⭐ Final Summary

``` text
        Kubernetes
             +
           Python
             +
         LangChain
             +
           OpenAI
             +
        LangSmith
             +
         Streamlit
             =
   AI-Assisted Kubernetes
     Incident Diagnosis
```

K8s AI Doctor demonstrates how cloud-native infrastructure and
Generative AI can be combined to build an AI-assisted Kubernetes
troubleshooting platform.

The current V1 focuses on **evidence-driven, read-only incident
diagnosis** and provides a foundation for future capabilities such as
agents, RAG, tool calling, metrics analysis, MCP, and automated
remediation.
