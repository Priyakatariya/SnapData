from pydantic import BaseModel, Field
from typing import Any, Optional


class QueryRequest(BaseModel):
    question: str = Field(..., description="Natural language question from the user")
    confidence_threshold: float = Field(
        default=0.5, ge=0.0, le=1.0,
        description="Minimum confidence score to execute the query"
    )


class QueryResponse(BaseModel):
    question: str
    sql: str
    explanation: str
    confidence: float
    columns: list[str]
    results: list[dict[str, Any]]
    row_count: int


class ColumnInfo(BaseModel):
    name: str
    type: str
    nullable: bool


class TableInfo(BaseModel):
    table_name: str
    columns: list[ColumnInfo]


class SchemaResponse(BaseModel):
    tables: list[TableInfo]


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
