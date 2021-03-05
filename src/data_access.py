class DatasetAccess:
    def __init__(self, endpoint:str):
        self.endpoint = endpoint
    
    def retrieve_dataset(self, page):
        """
        We assume this method makes an API call for a given page and returns
        the JSON response. We do not need to implement the request
            args: page
            returns: json object
        """
        pass
