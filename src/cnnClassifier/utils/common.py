import logging, os
import yaml
from pathlib import Path
from typing import Any
from src.cnnClassifier import logger
import json
import joblib
from box.exceptions import BoxValueError
from ensure import ensure_annotations
import base64
from box import ConfigBox

@ensure_annotations
def read_yaml(path_to_yaml : Path) -> ConfigBox:

    """reads yaml file and returns

    Args:
        path_to_yaml (str): path like input

    Raises 
        ValueError: if yaml file is empty
        e : empty file    

    Returns:
        ConfigBox: ConfigBox type    
    """

    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded suceessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):

    """create list of directories

    Args:
        path_to_directories (list) : list of path of directories
        ignore_log (bool, optional) : ignore if multiple dirs  is to be created. Default to False.
    """

    for path in path_to_directories:
        os.makedirs(path, exist_ok = True)
        if verbose:
            logger.info(f"created directory at: {path}")

@ensure_annotations
def save_json(path: Path, data: dict):
    
    """save json object/data
    Args:
        path(Path) : path to json file
        data(dict) : data to be saved in json file
    """

    with open(path, 'w') as json_file:
        json.dump(data, json_file,)

    logger.info(f"json file saved at {path}")    

@ensure_annotations
def load_json(path : Path):
    
    """load json file

    Args:
        path (Path) : path to json file

    Returns:
        ConfigBox: data as class attributes instead of dict
    """

    with open(path, 'r') as json_file:
        content = json.load(json_file)

    logger.info(f"json file loaded successful from: {path}")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):

    """save binary file

    Args:
        data (Any): data to be saved as binary
        path (Path) : path to binary file
    """

    joblib.dump(value = data, filename = path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path):

    """load binary file

    Args:
        path (Path) : path to binary file

    Returns:
        Any: object stored in the file
    """

    data = joblib.load(path)
    logger.info(f"binary file loaded from: {path}")
    return data

@ensure_annotations
def get_size(path: Path):

    """get size in kb

    Args:
        path(Path) : path of the file

    Return:
        size in kb    
    """

    size_in_kb = round(os.path.getsize(path)/1024)

    return f"~ {size_in_kb} KB"

@ensure_annotations
def decode_image(img_string, filename : str):

    """decode images

    Args:
        image string : path of the file
        filename(str) : name of the file to be decode    
    """

    img_data = base64.b64decode(img_string)
    with open(filename, 'wb') as f:
        f.write(img_data)
        f.close()

@ensure_annotations
def encode_image_into_Base64(croppedImgPath):

    """encode images

    Args:
        croppedImgPath : path of the cropped Image    
    """

    with open(croppedImgPath,'rb')as croppedImageFile:
        return base64.b64encode(croppedImageFile.read())