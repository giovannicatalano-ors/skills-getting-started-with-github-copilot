import pytest
from httpx import AsyncClient
from fastapi import status
from src.app import app

import asyncio

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_signup_success():
    # Arrange
    activity_name = "Basketball"
    student = {"student": "Alice"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity_name}/signup", json=student)
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert "message" in response.json()

@pytest.mark.asyncio
async def test_signup_duplicate():
    # Arrange
    activity_name = "Basketball"
    student = {"student": "Bob"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        await ac.post(f"/activities/{activity_name}/signup", json=student)  # First signup
        response = await ac.post(f"/activities/{activity_name}/signup", json=student)  # Duplicate
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_signup_activity_not_found():
    # Arrange
    activity_name = "NonexistentActivity"
    student = {"student": "Charlie"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity_name}/signup", json=student)
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()
