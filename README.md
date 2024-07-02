##### DISCLAIMER: Developed for personal use on a client's project. Some portions of the application have been removed for client privacy.
##### Not designed with general public consumption in mind.

# cms_etl

cms_etl is an ETL library featuring an interactive console environment and scripting tools used to expedite
the ETL process for data provided by CMS.gov. Written in Python, primarily leveraging libraries:
- pandas
- sqlalchemy
- rich
- rapidfuzz

Notables:
- \>50% codebase test coverage representing 100% of data mutations.
- Loads latest datasets from CMS and maintains metadata throughout the process.
- Macro exports allow the use of processed datasets directly in scripts, allowing for flexible, non-linear flows when necessary
- Menu stack + loop keeps call stack shallow
- Thoroughly typed
- Interactive mapping of source data to destination columns, outputting .sql scripts ready to load data into production.

## Background

Client wanted to get a data loading project underway but was in the middle of a large back-end transition. Not having the final schema locked in, I needed a way to do all
of the Extract and Transform ahead of time, leaving only some simple interactive mapping to complete the process.

In addition to a comprehensive table-editing/macro-building environment, there are utilities for fuzzy matching across
columns/tables, setting types, formatting addresses, etc.

The macro export functionality doubles as a human-readable DSL for
examining and editing ETL flows, and allows for fully-processed datasets to easily be used directly in scripts.
