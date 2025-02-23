# /app/tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app
from app import crud, schemas
from datetime import datetime
from uuid import uuid4  # Import UUID for unique IDs


client = TestClient(app)

# Test Create Event
def test_create_event():
    event_data = {
        "id": str(uuid4()),  # Generate a unique ID
        "type": "test_type",
        "timestamp": "2025-02-10T12:00:00Z",
        "payload": {"key": "value"}
    }
    response = client.post("/events", json=event_data)
    
    assert response.status_code == 200
    assert response.json()["type"] == event_data["type"]
    assert response.json()["payload"] == event_data["payload"]  # No need to load JSON anymore


# Test Get Events (without filters)
def test_get_events():
    response = client.get("/events")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Assuming the response is a list

# Test Get Events (with filters)
def test_get_events_with_filters():
    response = client.get("/events?event_type=test_type&start=2025-02-10T00:00:00Z&end=2025-02-11T00:00:00Z")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Delete Event
def test_delete_event():
    # First create an event to delete
    event_data = {
        "type": "delete_test",
        "timestamp": "2025-02-10T12:00:00Z",
        "payload": {"key": "delete_value"}
    }
    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]
    
    # Now delete the event
    delete_response = client.delete(f"/events/{event_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "Event deleted successfully"}

    # Try deleting again to ensure it doesn't exist
    delete_response_again = client.delete(f"/events/{event_id}")
    assert delete_response_again.status_code == 404

# Test Update Event
def test_update_event():
    # First create an event to update
    event_data = {
        "type": "update_test",
        "timestamp": "2025-02-10T12:00:00Z",
        "payload": {"key": "update_value"}
    }
    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]
    
    # Update the event
    updated_event_data = {
        "type": "updated_type",
        "payload": {"key": "updated_value"}
    }
    update_response = client.put(f"/events/{event_id}", json=updated_event_data)
    
    assert update_response.status_code == 200
    updated_event = update_response.json()
    assert updated_event["type"] == updated_event_data["type"]
    assert updated_event["payload"] == updated_event_data["payload"]
