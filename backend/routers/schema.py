from fastapi import APIRouter, HTTPException
from models.schemas import SchemaResponse
from services.db_service import get_schema_metadata

router = APIRouter()


@router.get("/schema", response_model=SchemaResponse)
async def get_schema():
    """
    Returns the database schema (tables and columns).
    Used by the frontend to show users what data is available.
    """
    try:
        tables = get_schema_metadata()
        return SchemaResponse(tables=tables)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch schema: {str(e)}")
