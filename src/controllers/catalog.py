import logging
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from repositories import cloud_storage as gcs

from settings import Settings

settings = Settings()

router = APIRouter(
    tags=["Catalog"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get/{catalog_name}")
def get_catalog(catalog_name: str) -> JSONResponse:
    """
    Get a given catalog by its name
    ## Args:
        - catalog_name: [str]: Catalog Name
    ## Returns:
        - Catalog [dict]
    """
    try:

        catalog = gcs.download_catalog(catalog_name, settings.BUCKET_NAME)

        if catalog:
            return JSONResponse(status_code=status.HTTP_200_OK, content=catalog)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": f"Catalog {catalog_name} not found."},
            )

    except Exception as e:
        logging.error(f"Could not get catalog. Error: {e}")
        return JSONResponse(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            content={"message": f"Failed to get {catalog_name} catalog. Error {e}"},
        )
