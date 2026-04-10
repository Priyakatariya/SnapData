from fastapi import APIRouter, HTTPException
from models.schemas import QueryRequest, QueryResponse, ErrorResponse
from services.gemini_service import generate_sql
from services.db_service import get_schema_string, execute_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    """
    Accepts a natural language question, converts it to SQL via Gemini,
    executes it on the database, and returns structured results.
    """
    try:
        # Step 1: Get DB schema for context
        schema = get_schema_string()

        # Step 2: Generate SQL + explanation via Gemini
        ai_result = await generate_sql(request.question, schema)
        sql = ai_result["sql"]
        explanation = ai_result["explanation"]
        confidence = ai_result["confidence"]

        # Step 3: Block low-confidence results
        if confidence < request.confidence_threshold:
            raise HTTPException(
                status_code=422,
                detail=f"Confidence score {confidence:.0%} is below threshold "
                       f"{request.confidence_threshold:.0%}. Please rephrase your question.",
            )

        # Step 4: Execute query
        columns, results = execute_query(sql)

        return QueryResponse(
            question=request.question,
            sql=sql,
            explanation=explanation,
            confidence=confidence,
            columns=columns,
            results=results,
            row_count=len(results),
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
