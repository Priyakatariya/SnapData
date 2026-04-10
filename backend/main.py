from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import query, schema

app = FastAPI(
    title="Talk2Data AI",
    description="Natural Language to SQL API powered by Gemini AI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api")
app.include_router(schema.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Talk2Data AI Backend is running 🚀"}
