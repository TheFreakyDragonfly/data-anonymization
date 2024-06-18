# Data anonymisation

##  What is this?
The github-repository for the semester project data-anonymisation.

## What files are there?
The **project** consists of two parts:
+ A VSCode Extension for user interaction
+ A python "backend" for anonmymising data

The folder **data_processing** contains the backend. It consists of:
+ Python source code
+ Python test files

The folder **example_data** contains files with testdata:
+ nothing currently

The folder **data-anon-extension** contains all files related to the VSCode extension:
+ package.json: register commands.
+ src/extension.ts: contains typescript sourcecode
+ src/css/: contains css for webviews

**Other files** in this repository include:
+ README.md: The readme file
+ overview.png: Rough overview of interaction between components in project

## What does the project depend on?
Some dependencies are installed with the project.
Other required dependencies:
+ ollama installed
+ llama3 model installed

## What is the purpose of this project?
+ To provide a clean user-interface
+ To allow users to select what tables to anonymize
+ To perform anonymization based on the contents of a table
	+ Column names
	+ Column contents
+ Utilise LLM to provide flexibility

## How does it work?
1. The user launches the VSCode Extension
2. The user provides Connection details
3. The user selects tables from the menu
4. An order.order file is created
5. Python is launched
6. order_receiver reads the order.order file
7. order_receiver hands over information to anonymizer
8. anonymizer assigns each column in each table a function to anonymize it
9. CSVs with non-anonymized data and anonymized data are written to top level of file structure
