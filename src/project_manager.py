"""
Project Manager - Handles project CRUD operations and deployment
"""

import os
import uuid
import json
import asyncio
import shutil
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiofiles
import logging

logger = logging.getLogger(__name__)

class ProjectManager:
    """Manages project lifecycle including creation, storage, and deployment"""
    
    def __init__(self):
        self.projects_dir = os.getenv("PROJECTS_DIR", "/tmp/projects")
        self.deployments_dir = os.getenv("DEPLOYMENTS_DIR", "/tmp/deployments")
        self.base_url = os.getenv("BASE_URL", "http://localhost:3000")
        
        # Ensure directories exist
        os.makedirs(self.projects_dir, exist_ok=True)
        os.makedirs(self.deployments_dir, exist_ok=True)
        
        # In-memory storage for demo (replace with database in production)
        self.projects_db = {}
        self.user_projects = {}
    
    async def create_project(
        self,
        user_id: str,
        name: str,
        description: str,
        generated_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new project with generated code"""
        
        project_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Create project directory
        project_path = os.path.join(self.projects_dir, project_id)
        os.makedirs(project_path, exist_ok=True)
        
        # Save generated files
        files_created = []
        for file_info in generated_data.get("files", []):
            file_path = os.path.join(project_path, file_info["path"])
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Write file content
            async with aiofiles.open(file_path, 'w') as f:
                await f.write(file_info["content"])
            
            files_created.append({
                "path": file_info["path"],
                "description": file_info.get("description", ""),
                "size": len(file_info["content"])
            })
        
        # Create package.json if it doesn't exist (for Node.js projects)
        await self._ensure_package_json(project_path, name, generated_data.get("dependencies", []))
        
        # Store project metadata
        project_data = {
            "id": project_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "status": "created",
            "created_at": timestamp,
            "updated_at": timestamp,
            "path": project_path,
            "files": files_created,
            "generated_data": generated_data,
            "preview_url": None,
            "deployment_url": None
        }
        
        # Store in memory (replace with database)
        self.projects_db[project_id] = project_data
        
        if user_id not in self.user_projects:
            self.user_projects[user_id] = []
        self.user_projects[user_id].append(project_id)
        
        logger.info(f"Created project {project_id} for user {user_id}")
        return project_data
    
    async def get_project(self, project_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID if user has access"""
        
        project = self.projects_db.get(project_id)
        if not project or project["user_id"] != user_id:
            return None
        
        return project
    
    async def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all projects for a user"""
        
        project_ids = self.user_projects.get(user_id, [])
        projects = []
        
        for project_id in project_ids:
            project = self.projects_db.get(project_id)
            if project:
                projects.append(project)
        
        return sorted(projects, key=lambda x: x["created_at"], reverse=True)
    
    async def update_project_file(
        self,
        project_id: str,
        file_path: str,
        new_content: str
    ) -> Dict[str, Any]:
        """Update a specific file in the project"""
        
        project = self.projects_db.get(project_id)
        if not project:
            raise ValueError("Project not found")
        
        # Update file on disk
        full_file_path = os.path.join(project["path"], file_path)
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
        
        async with aiofiles.open(full_file_path, 'w') as f:
            await f.write(new_content)
        
        # Update project metadata
        project["updated_at"] = datetime.utcnow()
        
        # Update file info in project data
        for file_info in project["files"]:
            if file_info["path"] == file_path:
                file_info["size"] = len(new_content)
                break
        else:
            # Add new file if it doesn't exist
            project["files"].append({
                "path": file_path,
                "description": "Updated file",
                "size": len(new_content)
            })
        
        logger.info(f"Updated file {file_path} in project {project_id}")
        return project
    
    async def delete_project(self, project_id: str, user_id: str) -> bool:
        """Delete a project"""
        
        project = await self.get_project(project_id, user_id)
        if not project:
            return False
        
        # Remove from file system
        project_path = project["path"]
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
        
        # Remove from memory storage
        del self.projects_db[project_id]
        if user_id in self.user_projects:
            self.user_projects[user_id].remove(project_id)
        
        logger.info(f"Deleted project {project_id}")
        return True
    
    async def deploy_project(self, project_id: str) -> str:
        """Deploy project and return accessible URL"""
        
        project = self.projects_db.get(project_id)
        if not project:
            raise ValueError("Project not found")
        
        try:
            # Create deployment directory
            deployment_id = f"{project_id}_{int(datetime.utcnow().timestamp())}"
            deployment_path = os.path.join(self.deployments_dir, deployment_id)
            
            # Copy project files to deployment directory
            shutil.copytree(project["path"], deployment_path)
            
            # Install dependencies if package.json exists
            package_json_path = os.path.join(deployment_path, "package.json")
            if os.path.exists(package_json_path):
                await self._install_dependencies(deployment_path)
            
            # Build the project if build script exists
            await self._build_project(deployment_path)
            
            # Start the development server (in production, use proper deployment)
            port = await self._get_available_port()
            deployment_url = f"{self.base_url}:{port}"
            
            # Start server in background
            await self._start_dev_server(deployment_path, port)
            
            # Update project with deployment info
            project["deployment_url"] = deployment_url
            project["status"] = "deployed"
            project["updated_at"] = datetime.utcnow()
            
            logger.info(f"Deployed project {project_id} to {deployment_url}")
            return deployment_url
            
        except Exception as e:
            logger.error(f"Error deploying project {project_id}: {str(e)}")
            raise Exception(f"Deployment failed: {str(e)}")
    
    async def get_project_files(self, project_id: str, user_id: str) -> Dict[str, str]:
        """Get all file contents for a project"""
        
        project = await self.get_project(project_id, user_id)
        if not project:
            return {}
        
        files_content = {}
        project_path = project["path"]
        
        for file_info in project["files"]:
            file_path = os.path.join(project_path, file_info["path"])
            if os.path.exists(file_path):
                async with aiofiles.open(file_path, 'r') as f:
                    content = await f.read()
                    files_content[file_info["path"]] = content
        
        return files_content
    
    async def _ensure_package_json(
        self,
        project_path: str,
        project_name: str,
        dependencies: List[str]
    ):
        """Create package.json if it doesn't exist"""
        
        package_json_path = os.path.join(project_path, "package.json")
        
        if not os.path.exists(package_json_path):
            # Check if this looks like a Node.js project
            has_js_files = any(
                f.endswith(('.js', '.jsx', '.ts', '.tsx'))
                for f in os.listdir(project_path)
                if os.path.isfile(os.path.join(project_path, f))
            )
            
            if has_js_files:
                package_json = {
                    "name": project_name.lower().replace(" ", "-"),
                    "version": "1.0.0",
                    "description": "Generated by AI App Builder",
                    "main": "index.js",
                    "scripts": {
                        "start": "react-scripts start",
                        "build": "react-scripts build",
                        "dev": "next dev",
                        "serve": "serve -s build"
                    },
                    "dependencies": {
                        "react": "^18.2.0",
                        "react-dom": "^18.2.0",
                        "react-scripts": "^5.0.1"
                    },
                    "devDependencies": {
                        "@types/react": "^18.2.0",
                        "@types/react-dom": "^18.2.0",
                        "typescript": "^4.9.0"
                    }
                }
                
                # Add specified dependencies
                for dep in dependencies:
                    if ":" in dep:
                        name, version = dep.split(":")
                        package_json["dependencies"][name] = version
                    else:
                        package_json["dependencies"][dep] = "latest"
                
                async with aiofiles.open(package_json_path, 'w') as f:
                    await f.write(json.dumps(package_json, indent=2))
    
    async def _install_dependencies(self, project_path: str):
        """Install project dependencies"""
        
        try:
            # Use npm install
            process = await asyncio.create_subprocess_exec(
                "npm", "install",
                cwd=project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                logger.warning(f"npm install failed: {stderr.decode()}")
            else:
                logger.info("Dependencies installed successfully")
                
        except Exception as e:
            logger.error(f"Error installing dependencies: {str(e)}")
    
    async def _build_project(self, project_path: str):
        """Build the project if build script exists"""
        
        package_json_path = os.path.join(project_path, "package.json")
        if not os.path.exists(package_json_path):
            return
        
        try:
            # Check if build script exists
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            if "build" in package_data.get("scripts", {}):
                process = await asyncio.create_subprocess_exec(
                    "npm", "run", "build",
                    cwd=project_path,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await process.communicate()
                
                if process.returncode == 0:
                    logger.info("Project built successfully")
                else:
                    logger.warning(f"Build failed: {stderr.decode()}")
                    
        except Exception as e:
            logger.error(f"Error building project: {str(e)}")
    
    async def _get_available_port(self) -> int:
        """Get an available port for deployment"""
        import socket
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        
        return port
    
    async def _start_dev_server(self, project_path: str, port: int):
        """Start development server for the project"""
        
        try:
            # Try different server commands based on project type
            package_json_path = os.path.join(project_path, "package.json")
            
            if os.path.exists(package_json_path):
                # Node.js project
                process = await asyncio.create_subprocess_exec(
                    "npm", "start",
                    cwd=project_path,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                    env={**os.environ, "PORT": str(port)}
                )
            else:
                # Static files - use Python's http.server
                process = await asyncio.create_subprocess_exec(
                    "python", "-m", "http.server", str(port),
                    cwd=project_path,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
            
            logger.info(f"Started dev server on port {port}")
            
        except Exception as e:
            logger.error(f"Error starting dev server: {str(e)}")