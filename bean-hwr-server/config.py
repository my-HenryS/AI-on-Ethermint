import yaml


with open('config.yml', 'r') as fr:
    _config = yaml.load(fr)
    _system_config = _config["system"]
    _image_config = _config["image"]
    _database_config = _config["database"]
    _crypto_config = _config["crypto"]


class Config:
    conn_url = _database_config["conn_url"]
    image_save_path = _image_config["save_path"]
    image_format = _image_config["format"]
    websocket_host = _system_config["websocket"]["host"]
    websocket_port = _system_config["websocket"]["port"]
    valid_count = _system_config["valid_count"]
    key = _crypto_config["key"]
    vi = _crypto_config["vi"]
