# Challenge
Financialforce challenge

Structure:

main.py --> main method to call with --output-type

src (Core modules)
    __init__.py
    challenge.py    --> Contains class DatasetConsumption with method get_transformed_dataset() that generates the new dataset
    data_access.py  --> Contains class DatasetAccess with method retrieve_dataset() to get data from API
    data_storage.py --> Contains class DataStorage with method save_to_s3() and others to save in different places

tests (Test modules for unittest with pytest)
    test_data_consumption.py --> Contains method "test_data_consumption()" to statiscally test the transformed dataset


export PYTHONPATH="$PYTHONPATH:/path_to_challenge_app/challenge_app"
