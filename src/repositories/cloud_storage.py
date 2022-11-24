import json
import logging
from google.cloud import storage
from dotenv import load_dotenv
from cachetools import cached, TTLCache
from datetime import datetime, timedelta

load_dotenv()
gcs_client = storage.Client()
ctl_cache = TTLCache(maxsize=1024, ttl=timedelta(hours=24), timer=datetime.now)
list_cache = TTLCache(maxsize=10, ttl=timedelta(hours=24), timer=datetime.now)


# Here recent 32 functions
# will we stored for 1 minutes
@cached(cache=ctl_cache)
def download_catalog(blob_name: str, bucket_name: str) -> dict:
    """
    Download a file from a bucket. The results from this function will be cached for 60 seconds.
    ## Args:
        - blob_name: [str] File to be downloaded
        - bucket_name: [str] GCS Bucket where date will be downloaded from
    ## Returns:
        - Catalog [dict]
    """
    catalog = {}
    try:
        bucket = gcs_client.get_bucket(bucket_name)
        # Download catalog as byte string
        contents = bucket.blob(blob_name).download_as_string()
        logging.info("Catalog Downloaded")
        # Decode and trim the catalog to parse it as json
        catalog = json.loads(contents.decode("utf-8").strip())
        return catalog
    except Exception as e:
        logging.error(e)
        return catalog
