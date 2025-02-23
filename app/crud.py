# Contains functions to interact with the database.

import json  
from sqlalchemy.orm import Session
from . import models, schemas
import logging
from typing import Optional
from datetime import datetime
from uuid import uuid4


def create_event(db: Session, event: schemas.EventCreate):
    try:
        db_event = models.Event(
            id=str(uuid4()),  # Unique ID using UUID    #id=str(event.timestamp.timestamp()), 
            type=event.type, 
            timestamp=event.timestamp, 
            # payload=json.dumps(event.payload)  # Correctly serialize payload as JSON string
            payload=event.payload  # Store as a JSON object, not a string
        )
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except Exception as e:
        logging.error(f"Error in create_event: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def get_events(db: Session, event_type: Optional[str], start: Optional[datetime], end: Optional[datetime], skip: int = 0, limit: int = 100):
    try:
        query = db.query(models.Event)
        
        # Apply filtering based on the optional parameters
        if event_type:
            query = query.filter(models.Event.type == event_type)
        if start:
            query = query.filter(models.Event.timestamp >= start)
        if end:
            query = query.filter(models.Event.timestamp <= end)

        # Apply pagination: skip a number of records and limit the results
        events = query.offset(skip).limit(limit).all()
        # events = query.all()  # Retrieve the list of events from the database

        # Ensure that events is not empty
        if not events:
            raise ValueError("No events found for the given filters")

        return events  # Return the list of events

    except Exception as e:
        logging.error(f"Error in get_events: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



def delete_event(db: Session, event_id: str):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        return True
    return False


def update_event(db: Session, event_id: str, updated_event: schemas.EventUpdate):
    # Fetch the event by its ID
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    
    if not event:
        return None
    
    # Update the fields that are provided in the request
    if updated_event.type is not None:
        event.type = updated_event.type
    if updated_event.timestamp is not None:
        event.timestamp = updated_event.timestamp
    if updated_event.payload is not None:
        event.payload = updated_event.payload  # Store as JSON directly
        # event.payload = json.dumps(updated_event.payload)   # Serialize the payload dictionary to a JSON string
    
    # Commit the changes to the database
    db.commit()
    db.refresh(event)  # Refresh to get the updated object
    return event