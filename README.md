# cms_etl

**cms_etl** is a lightweight ETL framework and CLI toolkit for building repeatable, scriptable data ingestion and transformation workflows.

> **Note:** This application was originally developed for a private client and is published with permission. Domain-specific functionality has been removed, and some features may not function fully in this public version.

---

## Overview

cms_etl was designed to make complex, real-world data workflows easier to inspect, modify, and automate. It provides both a command-line interface and a scripting-friendly environment for working with structured data across multiple databases.

The project emphasizes:

- Reusability over one-off scripts  
- Human-readable workflows  
- Practical tools for messy, inconsistent datasets  

---

## Key Features

### **Workflow DSL / Macro System**
ETL flows can be exported as a human-readable macro format that doubles as a lightweight DSL. This makes transformations easy to:

- Review  
- Edit  
- Version  
- Reuse in scripts  

---

### **Interactive Table & Data Tooling**
Includes a table-editing and macro-building environment designed for exploratory data work and repeatable processing tasks.

---

### **Multi-Database Support**
Supports multiple concurrent database connections, allowing workflows that operate across heterogeneous data sources.

---

### **Data Normalization & Reconciliation Utilities**
Provides utilities for handling common real-world data challenges, including:

- Fuzzy matching across columns and tables  
- Type setting and normalization  
- Address formatting and cleanup  

These tools were built to support reconciliation of inconsistent external data with structured internal schemas.

---

## Design Philosophy

cms_etl is structured as a reusable tooling layer rather than a collection of ad-hoc scripts. The focus is on:

- Composability  
- Repeatability  
- Clear abstraction boundaries  
- Making complex data transformations easier to reason about  

---

## Technology

- **Python**
- **SQLAlchemy** — database interaction  
- **Pandas** — data transformation  
- **Rich** — CLI interface and terminal output  

---

## Use Cases

cms_etl is suited for:

- Data migration and cleanup  
- Reconciliation between external and internal datasets  
- Repeatable ETL workflows  
- Scriptable data processing tasks  
