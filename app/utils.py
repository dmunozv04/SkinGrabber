from uuid import UUID
import app.nbt as nbt
from base64 import b64decode
import json
import requests
import app.constants as constants
from functools import lru_cache
from os import environ
def string_to_uuid(uuid_str: str):
    uuid = UUID(uuid_str)
    return uuid

def get_tailor_skin_value_from_uuid(uuid: UUID):
    nbt_file = nbt.NBTFile(get_playerdata_path() + str(uuid) + ".dat", 'rb')
    skin_base64 = str(nbt_file["fabrictailor:skin_data"]["value"])
    skin_json = b64decode(skin_base64)
    skin_url = json.loads(skin_json)["textures"]["SKIN"]["url"]
    skin_value = skin_url.split("/")[-1]
    return skin_value

def get_bedrock_skin_value_from_uuid(uuid: UUID):
    uuid_bedrock_str = str(uuid)[19:].replace("-", "")
    uuid_bedrock = int(uuid_bedrock_str, 16)
    r = requests.get(constants.geyser_skin_api + str(uuid_bedrock))
    skin_value = r.json()["texture_id"]
    return skin_value

@lru_cache(maxsize=100)
def get_head_from_value(value):
    api_url = constants.heads_api + value
    r = requests.get(api_url)
    return r.content

def get_skin_from_uuid(uuid_str: str):
    skin_value = None
    try:
        uuid = string_to_uuid(uuid_str)
        skin_value = get_tailor_skin_value_from_uuid(uuid)
    except Exception as e:
        print(e)
        if uuid_str.startswith("00000000-0000-0000-"):
            skin_value = get_bedrock_skin_value_from_uuid(uuid_str)
    if skin_value is None:
        skin_value = uuid_str
    return get_head_from_value(skin_value)
@lru_cache(maxsize=1)
def get_playerdata_path():
    path = environ.get("PLAYERDATA_PATH", "playerdata/")
    if path[:-1] != "/":
        path = path + "/"
    return path