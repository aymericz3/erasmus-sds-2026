"""
Main application file for the Travel Guide backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import categories, places, transport
from app.api.endpoints import itinerary

# Create FastAPI application instance
app = FastAPI(title="Travel Guide API")

# Configure CORS middleware to allow all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers for categories and places
app.include_router(categories.router)
app.include_router(places.router)
app.include_router(itinerary.router, prefix="/itinerary", tags=["itinerary"])
app.include_router(transport.router, prefix="/transport", tags=["transport"])

# Root endpoint to verify that the API is running
@app.get("/")
def root():
    return {"message": "Travel Guide API is running"}
