import main


class Commandline:
    def __init__(self, params):
        self.params = params



if __name__ == "__main__":
    params = main.Config()
    Commandline(params.parameters)