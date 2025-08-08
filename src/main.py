"""
AI-Powered App Builder - FastAPI Service
Similar to Lovable.dev - generates web applications from natural language descriptions
"""

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
import logging
from datetime import datetime

from ai_service import AICodeGenerator, ChatManager
from project_manager import ProjectManager
from auth_service import AuthService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI App Builder API",
    description="Generate web applications from natural language descriptions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
auth_service = AuthService()
ai_generator = AICodeGenerator()
chat_manager = ChatManager()
project_manager = ProjectManager()

# Pydantic models
class ProjectRequest(BaseModel):
    name: str
    description: str
    tech_stack: List[str] = ["react", "tailwind", "typescript"]
    design_preferences: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    project_id: str
    context: Optional[Dict[str, Any]] = None

class CodeEditRequest(BaseModel):
    project_id: str
    file_path: str
    changes: str
    description: str

class ProjectResponse(BaseModel):
    project_id: str
    name: str
    description: str
    status: str
    created_at: datetime
    files: List[Dict[str, Any]]
    preview_url: Optional[str] = None

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        user = await auth_service.verify_token(credentials.credentials)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@app.get("/")
async def root():
    return {"message": "AI App Builder API - Ready to create amazing applications!"}

@app.post("/api/projects", response_model=ProjectResponse)
async def create_project(
    request: ProjectRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new project from natural language description"""
    try:
        logger.info(f"Creating project: {request.name} for user: {current_user['id']}")
        
        # Generate project structure and initial code
        project_data = await ai_generator.generate_project(
            name=request.name,
            description=request.description,
            tech_stack=request.tech_stack,
            design_preferences=request.design_preferences
        )
        
        # Save project to database
        project = await project_manager.create_project(
            user_id=current_user["id"],
            name=request.name,
            description=request.description,
            generated_data=project_data
        )
        
        return ProjectResponse(
            project_id=project["id"],
            name=project["name"],
            description=project["description"],
            status=project["status"],
            created_at=project["created_at"],
            files=project_data.get("files", []),
            preview_url=project.get("preview_url")
        )
        
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/api/projects", response_model=List[ProjectResponse])
async def get_projects(current_user: dict = Depends(get_current_user)):
    """Get all projects for the current user"""
    try:
        projects = await project_manager.get_user_projects(current_user["id"])
        return [
            ProjectResponse(
                project_id=p["id"],
                name=p["name"],
                description=p["description"],
                status=p["status"],
                created_at=p["created_at"],
                files=p.get("files", []),
                preview_url=p.get("preview_url")
            )
            for p in projects
        ]
    except Exception as e:
        logger.error(f"Error fetching projects: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch projects")

@app.get("/api/projects/{project_id}")
async def get_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get project details including generated files"""
    try:
        project = await project_manager.get_project(project_id, current_user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return project
    except Exception as e:
        logger.error(f"Error fetching project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch project")

@app.post("/api/projects/{project_id}/edit")
async def edit_project_code(
    project_id: str,
    request: CodeEditRequest,
    current_user: dict = Depends(get_current_user)
):
    """Edit project code using AI assistance"""
    try:
        # Verify project ownership
        project = await project_manager.get_project(project_id, current_user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Generate code changes
        updated_code = await ai_generator.edit_code(
            project_context=project,
            file_path=request.file_path,
            changes_description=request.changes,
            current_code=request.description
        )
        
        # Update project files
        updated_project = await project_manager.update_project_file(
            project_id=project_id,
            file_path=request.file_path,
            new_content=updated_code
        )
        
        return {"success": True, "updated_code": updated_code}
        
    except Exception as e:
        logger.error(f"Error editing project code: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to edit code: {str(e)}")

@app.post("/api/projects/{project_id}/chat")
async def chat_with_ai(
    project_id: str,
    message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """Chat with AI about the project without making edits"""
    try:
        # Verify project ownership
        project = await project_manager.get_project(project_id, current_user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Get AI response
        response = await chat_manager.chat(
            message=message.message,
            project_context=project,
            user_context=message.context
        )
        
        return {"response": response, "timestamp": datetime.utcnow()}
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

@app.post("/api/projects/{project_id}/publish")
async def publish_project(
    project_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Publish project to make it accessible via URL"""
    try:
        # Verify project ownership
        project = await project_manager.get_project(project_id, current_user["id"])
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Deploy project and get URL
        deployment_url = await project_manager.deploy_project(project_id)
        
        return {
            "success": True,
            "url": deployment_url,
            "message": "Project published successfully!"
        }
        
    except Exception as e:
        logger.error(f"Error publishing project: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to publish project")

@app.websocket("/ws/projects/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket for real-time collaboration and updates"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "code_update":
                # Broadcast code changes to other collaborators
                await chat_manager.broadcast_update(project_id, message)
            elif message["type"] == "cursor_position":
                # Broadcast cursor position for collaborative editing
                await chat_manager.broadcast_cursor(project_id, message)
            
            # Echo back for now (implement proper collaboration logic)
            await websocket.send_text(json.dumps({
                "type": "ack",
                "message": "Update received",
                "timestamp": datetime.utcnow().isoformat()
            }))
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for project {project_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)