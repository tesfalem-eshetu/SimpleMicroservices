from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.exercise import ExerciseCreate, ExerciseRead, ExerciseUpdate
from models.workout import WorkoutCreate, WorkoutRead, WorkoutUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
exercises: Dict[UUID, ExerciseRead] = {}
workouts: Dict[UUID, WorkoutRead] = {}

app = FastAPI(
    title="Person/Address/Exercise/Workout API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Exercise, and Workout",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Exercise endpoints
# -----------------------------------------------------------------------------
@app.post("/exercises", response_model=ExerciseRead, status_code=201)
def create_exercise(exercise: ExerciseCreate):
    exercise_read = ExerciseRead(**exercise.model_dump())
    exercises[exercise_read.id] = exercise_read
    return exercise_read

@app.get("/exercises", response_model=List[ExerciseRead])
def list_exercises(
    name: Optional[str] = Query(None, description="Filter by exercise name"),
    muscle_group: Optional[str] = Query(None, description="Filter by muscle group"),
    equipment: Optional[str] = Query(None, description="Filter by equipment"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty level"),
):
    results = list(exercises.values())

    if name is not None:
        results = [e for e in results if e.name == name]
    if muscle_group is not None:
        results = [e for e in results if e.muscle_group == muscle_group]
    if equipment is not None:
        results = [e for e in results if e.equipment == equipment]
    if difficulty is not None:
        results = [e for e in results if e.difficulty == difficulty]

    return results

@app.get("/exercises/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: UUID):
    if exercise_id not in exercises:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercises[exercise_id]

@app.put("/exercises/{exercise_id}", response_model=ExerciseRead)
def replace_exercise(exercise_id: UUID, exercise: ExerciseCreate):
    exercises[exercise_id] = ExerciseRead(**exercise.model_dump())
    return exercises[exercise_id]

@app.patch("/exercises/{exercise_id}", response_model=ExerciseRead)
def update_exercise(exercise_id: UUID, update: ExerciseUpdate):
    if exercise_id not in exercises:
        raise HTTPException(status_code=404, detail="Exercise not found")
    stored = exercises[exercise_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    exercises[exercise_id] = ExerciseRead(**stored)
    return exercises[exercise_id]

@app.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: UUID):
    if exercise_id not in exercises:
        raise HTTPException(status_code=404, detail="Exercise not found")
    del exercises[exercise_id]
    return {"message": "Exercise deleted successfully"}

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    # Each person gets its own UUID; stored as PersonRead
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Workout endpoints
# -----------------------------------------------------------------------------
@app.post("/workouts", response_model=WorkoutRead, status_code=201)
def create_workout(workout: WorkoutCreate):
    workout_read = WorkoutRead(**workout.model_dump())
    workouts[workout_read.id] = workout_read
    return workout_read

@app.get("/workouts", response_model=List[WorkoutRead])
def list_workouts(
    user_name: Optional[str] = Query(None, description="Filter by user name"),
    workout_date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    duration_minutes: Optional[int] = Query(None, description="Filter by minimum duration"),
):
    results = list(workouts.values())

    if user_name is not None:
        results = [w for w in results if w.user_name == user_name]
    if workout_date is not None:
        results = [w for w in results if str(w.workout_date) == workout_date]
    if duration_minutes is not None:
        results = [w for w in results if w.duration_minutes and w.duration_minutes >= duration_minutes]

    return results

@app.get("/workouts/{workout_id}", response_model=WorkoutRead)
def get_workout(workout_id: UUID):
    if workout_id not in workouts:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workouts[workout_id]

@app.put("/workouts/{workout_id}", response_model=WorkoutRead)
def replace_workout(workout_id: UUID, workout: WorkoutCreate):
    workouts[workout_id] = WorkoutRead(**workout.model_dump())
    return workouts[workout_id]

@app.patch("/workouts/{workout_id}", response_model=WorkoutRead)
def update_workout(workout_id: UUID, update: WorkoutUpdate):
    if workout_id not in workouts:
        raise HTTPException(status_code=404, detail="Workout not found")
    stored = workouts[workout_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    workouts[workout_id] = WorkoutRead(**stored)
    return workouts[workout_id]

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: UUID):
    if workout_id not in workouts:
        raise HTTPException(status_code=404, detail="Workout not found")
    del workouts[workout_id]
    return {"message": "Workout deleted successfully"}

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/Exercise/Workout API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
