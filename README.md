# cms_etl

If you are reading this, there is a good chance my resume brought you in.
Welcome! The main entry point is {root}/src/cms_etl/main.py,
and the AppContext found there is a good thread to pull at to get a quick tour. I appreciate your consideration!

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
- Thoroughly typed throughout
- Interactive mapping of source data to destination columns, outputting .sql scripts ready to load data into production.

## Background

My client wanted to get a data loading project underway but was in the middle of a large back-end transition
directly involving the necessary tables. Not having the final schema locked in, I wanted a way to do all
of the Extract and Transform ahead of time, essentially leaving only SQL query templating to complete once the
schema was finalized.

In addition to a comprehensive table-editing/macro-building environment, there are utilities for fuzzy matching across
columns/tables, setting types, formatting addresses, etc.

The macro export functionality doubles as a human-readable DSL for
examining and editing ETL flows, and allows for fully-processed datasets to easily be used directly in scripts.

I used this project as an opportunity to get some practice with traditional design patterns:
- Adapter Pattern made it easy to support multiple database types.
- A loose State pattern is used in the Menu system, with a central menu stack + loop keeping call stack depth in check.
- Command Pattern allowed me to defer command execution and support macro functionality.
- Factory Pattern is used throughout, often in combination with other patterns.
- Dependency Injection is utilized to decouple modules.

##### SOME PORTIONS OF THE APPLICATION HAVE BEEN REMOVED FOR CLIENT PRIVACY
