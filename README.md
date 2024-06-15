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
+ nothing currently

**Other files** in this repository include:
+ .gitignore: For everyone in the project
+ README.md: The readme file

## What does the project depend on?
Some dependencies are installed with the project.
Other required dependencies:
+ virtualenv (python package)
	+ pip install virtualenv

## What is the purpose of this project?
+ To provide a clean user-interface
+ To allow users to select what tables to anonymize
+ To perform anonymization based on the contents of a table
	+ Column names
	+ Column contents
+ Utilise LLM to provide flexibility
