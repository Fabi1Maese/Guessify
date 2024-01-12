import configparser

class Config():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf.ini')
        self.config = config
        self.client_id = config['CREDS']['client_id']
        self.client_secret = config['CREDS']['client_secret']
        self.redirect_uri = config['CREDS']['redirect_uri']
        self.tempfiles_path = config['tempfiles']['path']
        self.game_code_size = config['settings']['game_code_size']
        self.minimum_points_threshold = config['settings']['minimum_points_threshold']