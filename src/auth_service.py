"""
Authentication Service - Handles user authentication and JWT tokens
"""

import os
import jwt
import bcrypt
import uuid
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Handles user authentication, registration, and JWT token management"""
    
    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # In-memory user storage (replace with database in production)
        self.users_db = {}
        self.user_sessions = {}
        
        # Create a demo user for testing
        self._create_demo_user()
    
    def _create_demo_user(self):
        """Create a demo user for testing purposes"""
        demo_user = {
            "id": "demo-user-123",
            "email": "demo@example.com",
            "username": "demo",
            "hashed_password": self.get_password_hash("demo123"),
            "is_active": True,
            "created_at": datetime.utcnow(),
            "projects": []
        }
        self.users_db["demo@example.com"] = demo_user
        logger.info("Created demo user: demo@example.com / demo123")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with email and password"""
        user = self.users_db.get(email)
        if not user:
            return None
        
        if not self.verify_password(password, user["hashed_password"]):
            return None
        
        if not user.get("is_active", False):
            return None
        
        return user
    
    async def register_user(
        self,
        email: str,
        password: str,
        username: Optional[str] = None
    ) -> Dict[str, Any]:
        """Register a new user"""
        
        # Check if user already exists
        if email in self.users_db:
            raise ValueError("User already exists")
        
        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = self.get_password_hash(password)
        
        user_data = {
            "id": user_id,
            "email": email,
            "username": username or email.split("@")[0],
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "projects": []
        }
        
        # Store user
        self.users_db[email] = user_data
        
        logger.info(f"Registered new user: {email}")
        return user_data
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    async def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id: str = payload.get("sub")
            
            if user_id is None:
                raise ValueError("Invalid token")
            
            # Find user by ID
            user = None
            for user_data in self.users_db.values():
                if user_data["id"] == user_id:
                    user = user_data
                    break
            
            if user is None:
                raise ValueError("User not found")
            
            return user
            
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.JWTError:
            raise ValueError("Invalid token")
    
    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login a user and return access token"""
        user = await self.authenticate_user(email, password)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Create access token
        access_token = self.create_access_token(
            data={"sub": user["id"], "email": user["email"]}
        )
        
        # Store session
        self.user_sessions[user["id"]] = {
            "token": access_token,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        }
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": self.access_token_expire_minutes * 60,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "username": user["username"]
            }
        }
    
    async def logout(self, user_id: str) -> bool:
        """Logout a user and invalidate their session"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
            logger.info(f"User {user_id} logged out")
            return True
        return False
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        for user_data in self.users_db.values():
            if user_data["id"] == user_id:
                return user_data
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        return self.users_db.get(email)
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user information"""
        user = await self.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        # Update user data
        for key, value in updates.items():
            if key in ["email", "username"]:
                user[key] = value
            elif key == "password":
                user["hashed_password"] = self.get_password_hash(value)
        
        user["updated_at"] = datetime.utcnow()
        
        # Update in storage (find by current email)
        for email, stored_user in self.users_db.items():
            if stored_user["id"] == user_id:
                self.users_db[email] = user
                break
        
        logger.info(f"Updated user {user_id}")
        return user
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete a user account"""
        user = await self.get_user_by_id(user_id)
        if not user:
            return False
        
        # Remove from storage
        email_to_remove = None
        for email, stored_user in self.users_db.items():
            if stored_user["id"] == user_id:
                email_to_remove = email
                break
        
        if email_to_remove:
            del self.users_db[email_to_remove]
        
        # Remove session
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        
        logger.info(f"Deleted user {user_id}")
        return True
    
    async def is_token_valid(self, token: str) -> bool:
        """Check if a token is valid without raising exceptions"""
        try:
            await self.verify_token(token)
            return True
        except Exception:
            return False
    
    def get_user_stats(self) -> Dict[str, Any]:
        """Get user statistics"""
        return {
            "total_users": len(self.users_db),
            "active_sessions": len(self.user_sessions),
            "created_today": sum(
                1 for user in self.users_db.values()
                if user["created_at"].date() == datetime.utcnow().date()
            )
        }