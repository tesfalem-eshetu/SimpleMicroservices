from __future__ import annotations

from typing import Optional, List
from uuid import UUID, uuid4
from datetime import datetime, date
from pydantic import BaseModel, Field


class WorkoutBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Workout ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    user_name: str = Field(
        ...,
        description="Name of the person doing the workout.",
        json_schema_extra={"example": "John Doe"},
    )
    workout_date: date = Field(
        ...,
        description="Date of the workout (YYYY-MM-DD).",
        json_schema_extra={"example": "2025-09-14"},
    )
    exercises: List[str] = Field(
        default_factory=list,
        description="List of exercises performed.",
        json_schema_extra={"example": ["Push-ups", "Squats", "Planks"]},
    )
    duration_minutes: Optional[int] = Field(
        None,
        description="Total workout duration in minutes.",
        json_schema_extra={"example": 45},
    )
    calories_burned: Optional[float] = Field(
        None,
        description="Total calories burned during workout.",
        json_schema_extra={"example": 320.5},
    )
    notes: Optional[str] = Field(
        None,
        description="Additional notes about the workout.",
        json_schema_extra={"example": "Felt great, increased weights"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "user_name": "John Doe",
                    "workout_date": "2025-09-14",
                    "exercises": ["Push-ups", "Squats", "Planks"],
                    "duration_minutes": 45,
                    "calories_burned": 320.5,
                    "notes": "Felt great, increased weights",
                }
            ]
        }
    }


class WorkoutCreate(WorkoutBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "user_name": "Jane Smith",
                    "workout_date": "2025-09-15",
                    "exercises": ["Bench Press", "Deadlifts", "Pull-ups"],
                    "duration_minutes": 60,
                    "calories_burned": 450.0,
                    "notes": "New personal record on deadlifts",
                }
            ]
        }
    }


class WorkoutUpdate(BaseModel):
    """Partial update; workout ID is taken from the path, not the body."""
    user_name: Optional[str] = Field(
        None, description="Name of the person doing the workout.", json_schema_extra={"example": "Jane Doe"}
    )
    workout_date: Optional[date] = Field(
        None, description="Date of the workout (YYYY-MM-DD).", json_schema_extra={"example": "2025-09-15"}
    )
    exercises: Optional[List[str]] = Field(
        None, description="List of exercises performed.", json_schema_extra={"example": ["Burpees", "Mountain Climbers"]}
    )
    duration_minutes: Optional[int] = Field(
        None, description="Total workout duration in minutes.", json_schema_extra={"example": 30}
    )
    calories_burned: Optional[float] = Field(
        None, description="Total calories burned during workout.", json_schema_extra={"example": 280.0}
    )
    notes: Optional[str] = Field(
        None, description="Additional notes about the workout.", json_schema_extra={"example": "Short but intense session"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "duration_minutes": 30,
                    "calories_burned": 280.0,
                    "notes": "Short but intense session",
                },
                {"exercises": ["Yoga", "Stretching"]},
            ]
        }
    }


class WorkoutRead(WorkoutBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "user_name": "John Doe",
                    "workout_date": "2025-09-14",
                    "exercises": ["Push-ups", "Squats", "Planks"],
                    "duration_minutes": 45,
                    "calories_burned": 320.5,
                    "notes": "Felt great, increased weights",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
