from fastapi import WebSocket, WebSocketDisconnect
from typing import List

active_connections: List[WebSocket] = []

async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint to manage real-time updates."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()  # Listening for messages 
            print(f"Message from {user_id}: {data}")
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"User {user_id} disconnected")

async def send_task_update_notification(task_id: str, assigned_user_id: str, status: str):
    """Send real-time updates when a task is updated."""
    message = {"task_id": task_id, "status": status}
    for connection in active_connections:
        try:
            await connection.send_json(message)  # Sending JSON response
        except:
            active_connections.remove(connection)
