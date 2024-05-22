import os
import tempfile
import pathlib
from requests.adapters import HTTPAdapter
from requests.sessions import Session
from urllib3.poolmanager import PoolManager

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        self.poolmanager = PoolManager(*args, **kwargs)

def test_cert_pathlike():
    # Create temporary files to act as cert and key
    with tempfile.NamedTemporaryFile(delete=False) as cert_file, tempfile.NamedTemporaryFile(delete=False) as key_file:
        cert_path = cert_file.name
        key_path = key_file.name

    # Case 1: Using string paths
    session = Session()
    adapter = MyAdapter()
    session.mount("https://", adapter)
    try:
        response = session.get("https://example.com", cert=cert_path)
    except Exception as e:
        print(f"Using string paths failed: {e}")

    # Case 2: Using pathlib.Path object
    cert_path_pathlib = pathlib.Path(cert_path)
    try:
        response = session.get("https://example.com", cert=cert_path_pathlib)
    except Exception as e:
        print(f"Using pathlib.Path object failed: {e}")

    # Case 3: Using a tuple of paths (cert and key)
    cert_key_tuple = (cert_path, key_path)
    try:
        response = session.get("https://example.com", cert=cert_key_tuple)
    except Exception as e:
        print(f"Using a tuple of paths failed: {e}")

    # Cleanup temporary files
    os.remove(cert_path)
    os.remove(key_path)

if __name__ == "__main__":
    test_cert_pathlike()
