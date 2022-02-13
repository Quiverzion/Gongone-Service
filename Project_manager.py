import yaml


class data:
    def __init__(self):
        self.Data_file_name = "User_data.yaml"
        self.Secrets_file_name = "Secrets.yaml"

    def data_get(self):
        with open(self.Data_file_name, "r", encoding="UTF8") as a:
            file = yaml.load(a, Loader=yaml.FullLoader)
        return file

    def data_set(self, file):
        self.file = file
        with open(self.Data_file_name, "w", encoding="UTF8") as a:
            yaml.dump(self.file, a)

    def secrets_get(self):
        with open(self.Secrets_file_name, "r", encoding="UTF8") as a:
            file = yaml.load(a, Loader=yaml.FullLoader)
        return file

    def secrets_set(self, file):
        self.file = file
        with open(self.Secrets_file_name, "w", encoding="UTF8") as a:
            yaml.dump(self.file, a)
