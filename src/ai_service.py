"""
AI Service for Code Generation and Chat
Handles interaction with AI models to generate and modify code
"""

import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import openai
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import tiktoken
import logging

logger = logging.getLogger(__name__)

class AICodeGenerator:
    """Generates code using AI models based on natural language descriptions"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = "gpt-4-turbo-preview"
        self.encoding = tiktoken.get_encoding("cl100k_base")
        
    async def generate_project(
        self,
        name: str,
        description: str,
        tech_stack: List[str],
        design_preferences: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate a complete project structure from description"""
        
        # Create system prompt for project generation
        system_prompt = self._create_project_generation_prompt(tech_stack)
        
        # Create user prompt with project details
        user_prompt = self._create_user_prompt(name, description, design_preferences)
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content
            project_data = self._parse_project_response(ai_response)
            
            return {
                "project_plan": project_data.get("plan", ""),
                "files": project_data.get("files", []),
                "dependencies": project_data.get("dependencies", []),
                "setup_instructions": project_data.get("setup", ""),
                "features": project_data.get("features", []),
                "ai_response": ai_response
            }
            
        except Exception as e:
            logger.error(f"Error generating project: {str(e)}")
            raise Exception(f"Failed to generate project: {str(e)}")
    
    async def edit_code(
        self,
        project_context: Dict[str, Any],
        file_path: str,
        changes_description: str,
        current_code: str
    ) -> str:
        """Edit existing code based on natural language instructions"""
        
        system_prompt = """You are an expert software developer. You will be given:
        1. Current code from a file
        2. Description of changes needed
        3. Project context
        
        Your task is to modify the code according to the instructions while:
        - Maintaining code quality and best practices
        - Preserving existing functionality unless explicitly asked to change it
        - Following the project's coding style and patterns
        - Adding appropriate comments for new functionality
        
        Return ONLY the updated code, no explanations or markdown formatting."""
        
        user_prompt = f"""
        Project Context: {json.dumps(project_context.get('description', ''), indent=2)}
        File Path: {file_path}
        
        Current Code:
        ```
        {current_code}
        ```
        
        Changes Requested:
        {changes_description}
        
        Please provide the updated code:
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=3000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error editing code: {str(e)}")
            raise Exception(f"Failed to edit code: {str(e)}")
    
    def _create_project_generation_prompt(self, tech_stack: List[str]) -> str:
        """Create system prompt for project generation"""
        
        tech_stack_str = ", ".join(tech_stack)
        
        return f"""You are an expert full-stack developer and architect. You specialize in creating modern web applications using {tech_stack_str}.

Your task is to generate a complete project structure and initial code based on user requirements. You should:

1. Create a comprehensive project plan
2. Generate all necessary files with complete, functional code
3. Include proper project structure and organization
4. Add appropriate dependencies and configuration files
5. Implement modern UI/UX patterns and responsive design
6. Include proper error handling and validation
7. Follow best practices for the chosen technology stack

For React projects, use:
- Functional components with hooks
- TypeScript for type safety
- Tailwind CSS for styling
- Modern folder structure (components, pages, hooks, utils)
- Proper state management

For backend APIs, include:
- RESTful API design
- Input validation
- Error handling
- Authentication setup
- Database integration patterns

Return your response in JSON format with these fields:
{
  "plan": "Detailed project plan and architecture",
  "files": [
    {
      "path": "relative/path/to/file",
      "content": "Complete file content",
      "description": "What this file does"
    }
  ],
  "dependencies": ["package1", "package2"],
  "setup": "Setup and installation instructions",
  "features": ["Feature 1", "Feature 2"]
}"""

    def _create_user_prompt(self, name: str, description: str, design_preferences: Optional[str]) -> str:
        """Create user prompt with project details"""
        
        prompt = f"""
Project Name: {name}

Description: {description}

Please create a complete, functional web application based on this description.
"""
        
        if design_preferences:
            prompt += f"\nDesign Preferences: {design_preferences}"
        
        prompt += """

Make sure the application is:
- Fully functional with all core features working
- Responsive and mobile-friendly
- Modern and visually appealing
- Well-structured and maintainable
- Ready to run with minimal setup

Generate all necessary files including components, styles, configuration, and documentation."""

        return prompt
    
    def _parse_project_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response and extract project data"""
        
        try:
            # Try to extract JSON from the response
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback: create basic structure from text response
                return {
                    "plan": response,
                    "files": [],
                    "dependencies": [],
                    "setup": "Please check the generated files for setup instructions",
                    "features": []
                }
                
        except json.JSONDecodeError:
            logger.warning("Failed to parse JSON response, using fallback")
            return {
                "plan": response,
                "files": [],
                "dependencies": [],
                "setup": "Please check the generated files for setup instructions",
                "features": []
            }

class ChatManager:
    """Manages AI chat conversations for project assistance"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = "gpt-4-turbo-preview"
        self.conversations = {}  # Store conversation history
    
    async def chat(
        self,
        message: str,
        project_context: Dict[str, Any],
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Chat with AI about the project"""
        
        system_prompt = f"""You are an expert software development assistant helping with a web application project.

Project Details:
- Name: {project_context.get('name', 'Unknown')}
- Description: {project_context.get('description', 'No description')}
- Status: {project_context.get('status', 'Unknown')}

You can help with:
- Code explanations and improvements
- Debugging issues
- Architecture decisions
- Feature planning
- Best practices
- Technology recommendations

Be helpful, concise, and provide actionable advice. If asked about specific code, reference the project context."""

        try:
            response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in chat: {str(e)}")
            return f"I'm sorry, I encountered an error: {str(e)}"
    
    async def broadcast_update(self, project_id: str, message: Dict[str, Any]):
        """Broadcast code updates to collaborators (placeholder)"""
        # TODO: Implement real-time collaboration
        logger.info(f"Broadcasting update for project {project_id}: {message}")
    
    async def broadcast_cursor(self, project_id: str, message: Dict[str, Any]):
        """Broadcast cursor position to collaborators (placeholder)"""
        # TODO: Implement cursor sharing
        logger.info(f"Broadcasting cursor for project {project_id}: {message}")

class CodeAnalyzer:
    """Analyzes and validates generated code"""
    
    def __init__(self):
        pass
    
    async def analyze_code_quality(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code quality and suggest improvements"""
        # TODO: Implement code analysis
        return {
            "quality_score": 85,
            "issues": [],
            "suggestions": []
        }
    
    async def validate_syntax(self, code: str, language: str) -> Dict[str, Any]:
        """Validate code syntax"""
        # TODO: Implement syntax validation
        return {
            "valid": True,
            "errors": []
        }