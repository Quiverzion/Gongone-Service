import yaml

class data:
    def __init__(self):
        self.Data_file_name = "User_data.yaml"
        self.Secrets_file_name = "Secrets.yaml"


    def data_get(self, user:int, data_name:str):
        self.user = user
        self.data_name = data_name
        with open(self.Data_file_name, "r", encoding="UTF8") as a:
            file = yaml.load(a, Loader=yaml.FullLoader)
        if file.get(f"User:{user}") == None:
            return None
        else:
            return file[f"User:{user}"][self.data_name]


    def secrets_get(self, type:str):
        self.type = type
        with open(self.Secrets_file_name, "r", encoding="UTF8") as a:
            file = yaml.load(a, Loader=yaml.FullLoader)
        return file[self.type]
