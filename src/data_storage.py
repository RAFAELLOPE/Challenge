class DataStorage:
    def __init__(self, **connection_params):
        self.params = connection_params

    def save_to_s3(self, file_key:str) -> bool:
        """
        We assume this method handles writing into s3 key.
        We do not need to implement the logic.
        It returns True if written operation has been carried out successfully
            args: file_key
            returns: boolean indicating success in the operation
        """
        return True

    def save_to_postgres(self):
        pass

    def save_to_csv(self):
        pass