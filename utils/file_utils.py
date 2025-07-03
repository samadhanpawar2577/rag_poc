import uuid
import os
from config import UNITY_VOLUME_PATH

def upload_to_unity_catalog(file):
    file_id = str(uuid.uuid4())
    stored_path = f"{UNITY_VOLUME_PATH}/{file_id}_{file.name}"
    with open(stored_path, "wb") as f:
        f.write(file.read())
    return file_id, stored_path