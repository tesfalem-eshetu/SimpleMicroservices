from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class ExerciseBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Exercise ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    name: str = Field(
        ...,
        description="Exercise name.",
        json_schema_extra={"example": "Push-ups"},
    )
    muscle_group: str = Field(
        ...,
        description="Primary muscle group targeted.",
        json_schema_extra={"example": "Chest"},
    )
    equipment: Optional[str] = Field(
        None,
        description="Required equipment (if any).",
        json_schema_extra={"example": "None"},
    )
    difficulty: str = Field(
        ...,
        description="Difficulty level.",
        json_schema_extra={"example": "Beginner"},
    )
    instructions: str = Field(
        ...,
        description="Step-by-step exercise instructions.",
        json_schema_extra={"example": "Start in plank position, lower body, push up"},
    )
    calories_per_minute: Optional[float] = Field(
        None,
        description="Estimated calories burned per minute.",
        json_schema_extra={"example": 8.5},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Push-ups",
                    "muscle_group": "Chest",
                    "equipment": "None",
                    "difficulty": "Beginner",
                    "instructions": "Start in plank position, lower body, push up",
                    "calories_per_minute": 8.5,
                }
            ]
        }
    }


class ExerciseCreate(ExerciseBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "name": "Bench Press",
                    "muscle_group": "Chest",
                    "equipment": "Barbell",
                    "difficulty": "Intermediate",
                    "instructions": "Lie on bench, grip barbell, lower to chest, press up",
                    "calories_per_minute": 6.0,
                }
            ]
        }
    }


class ExerciseUpdate(BaseModel):
    """Partial update; exercise ID is taken from the path, not the body."""
    name: Optional[str] = Field(
        None, description="Exercise name.", json_schema_extra={"example": "Modified Push-ups"}
    )
    muscle_group: Optional[str] = Field(
        None, description="Primary muscle group targeted.", json_schema_extra={"example": "Arms"}
    )
    equipment: Optional[str] = Field(
        None, description="Required equipment (if any).", json_schema_extra={"example": "Dumbbells"}
    )
    difficulty: Optional[str] = Field(
        None, description="Difficulty level.", json_schema_extra={"example": "Advanced"}
    )
    instructions: Optional[str] = Field(
        None, description="Step-by-step exercise instructions.", json_schema_extra={"example": "Updated instructions"}
    )
    calories_per_minute: Optional[float] = Field(
        None, description="Estimated calories burned per minute.", json_schema_extra={"example": 10.0}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Diamond Push-ups",
                    "muscle_group": "Triceps",
                    "difficulty": "Advanced",
                    "calories_per_minute": 12.0,
                },
                {"difficulty": "Intermediate"},
            ]
        }
    }


class ExerciseRead(ExerciseBase):
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
                    "name": "Push-ups",
                    "muscle_group": "Chest",
                    "equipment": "None",
                    "difficulty": "Beginner",
                    "instructions": "Start in plank position, lower body, push up",
                    "calories_per_minute": 8.5,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
