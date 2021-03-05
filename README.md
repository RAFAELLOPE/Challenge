# Challenge
Financialforce challenge

# Challenge
Financialforce challenge

Unit tests are implemented with python library "pytest" where I have made some statistical analysis.

It is recommended to create a Python environment that should include (at least):

	Python 3.8.5
	pytest 6.2.2
	numpy 1.20.1
	pandas 1.2.3

Executions times are saved in a log file.


Structure of the project is:

main.py --> main method to call with --output-type

src (Core modules)
    __init__.py
    challenge.py    --> Contains class DatasetConsumption with method get_transformed_dataset() that generates the new dataset
    data_access.py  --> Contains class DatasetAccess with method retrieve_dataset() to get data from API
    data_storage.py --> Contains class DataStorage with method save_to_s3() and others to save in different places

tests (Test modules for unittest with pytest)
    test_data_consumption.py --> Contains method "test_data_consumption()" to statiscally test the transformed dataset

logs (To save execution times in a log)
    execution_times.log

venv (Python environment to activate)



Might be neccessary to export PYTHONPATH to the app folder
export PYTHONPATH="$PYTHONPATH:/path_to_challenge_app/challenge_app"