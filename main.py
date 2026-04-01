from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

import models, schemas, database

app = FastAPI(title="PK Multiserve API")

# CORS configuration for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow any origin for production deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/categories", response_model=List[schemas.Category])
async def get_categories(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Category))
    return result.scalars().all()

@app.get("/products", response_model=List[schemas.Product])
async def get_products(category_slug: str = None, brand: str = None, db: AsyncSession = Depends(database.get_db)):
    query = select(models.Product)
    if category_slug:
        query = query.join(models.Category).where(models.Category.slug == category_slug)
    if brand:
        query = query.where(models.Product.brand == brand)
    
    result = await db.execute(query)
    return result.scalars().all()

@app.get("/products/{slug}", response_model=schemas.Product)
async def get_product_by_slug(slug: str, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(
        select(models.Product).where(models.Product.slug == slug)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.get("/health")
def health_check():
    return {"status": "healthy"}
