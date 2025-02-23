
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, schemas

router = APIRouter()

@router.post("/events")
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    return crud.create_event(db, event)


@router.get("/events")
def get_events(
    event_type: str = Query(None, description="Filter by event type"),              # Optional filter for event type 
    start: str = Query(None, description="Start timestamp (YYYY-MM-DD HH:MM:SS)"),  # Optional filter for event type 
    end: str = Query(None, description="End timestamp (YYYY-MM-DD HH:MM:SS)"),      # Optional filter for event type 
    skip: int = Query(0, ge=0, description="Number of records to skip (must be non-negative)"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return (between 1 and 1000)"),
    db: Session = Depends(get_db),
):
    return crud.get_events(db, event_type, start, end, skip, limit)  # include pagination
    # return crud.get_events(db, event_type, start, end)

@router.delete("/events/{event_id}")
def delete_event(event_id: str, db: Session = Depends(get_db)):
    success = crud.delete_event(db, event_id)
    if success:
        return {"message": "Event deleted successfully"}
    raise HTTPException(status_code=404, detail="Event not found")


@router.put("/events/{event_id}")
def update_event(event_id: str, updated_event: schemas.EventUpdate, db: Session = Depends(get_db)):
    # Call the CRUD function to update the event
    event = crud.update_event(db, event_id, updated_event)
    if event:
        return event
    raise HTTPException(status_code=404, detail="Event not found")