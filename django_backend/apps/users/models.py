"""
User models for the AI App Builder
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid

class User(AbstractUser):
    """Extended user model with additional fields for the AI App Builder"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    github_username = models.CharField(max_length=100, blank=True, null=True)
    
    # Subscription and usage tracking
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('free', 'Free'),
            ('pro', 'Pro'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    
    # Usage limits and tracking
    projects_created = models.PositiveIntegerField(default=0)
    ai_requests_this_month = models.PositiveIntegerField(default=0)
    storage_used_mb = models.PositiveIntegerField(default=0)
    
    # Preferences
    preferred_tech_stack = models.JSONField(default=list, blank=True)
    default_design_style = models.CharField(
        max_length=50,
        choices=[
            ('modern', 'Modern'),
            ('minimal', 'Minimal'),
            ('colorful', 'Colorful'),
            ('dark', 'Dark'),
            ('light', 'Light'),
        ],
        default='modern'
    )
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(default=timezone.now)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.email} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    def can_create_project(self):
        """Check if user can create more projects based on their subscription"""
        limits = {
            'free': 3,
            'pro': 50,
            'enterprise': 1000
        }
        return self.projects_created < limits.get(self.subscription_tier, 3)
    
    def can_make_ai_request(self):
        """Check if user can make more AI requests this month"""
        limits = {
            'free': 100,
            'pro': 2000,
            'enterprise': 10000
        }
        return self.ai_requests_this_month < limits.get(self.subscription_tier, 100)
    
    def increment_project_count(self):
        """Increment the user's project count"""
        self.projects_created += 1
        self.save(update_fields=['projects_created'])
    
    def increment_ai_request_count(self):
        """Increment the user's AI request count"""
        self.ai_requests_this_month += 1
        self.save(update_fields=['ai_requests_this_month'])
    
    def reset_monthly_usage(self):
        """Reset monthly usage counters (called by a scheduled task)"""
        self.ai_requests_this_month = 0
        self.save(update_fields=['ai_requests_this_month'])

class UserProfile(models.Model):
    """Extended profile information for users"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Professional information
    job_title = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Skills and interests
    skills = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    
    # Social links
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    project_updates = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile for {self.user.username}"

class APIKey(models.Model):
    """API keys for programmatic access"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')
    
    name = models.CharField(max_length=100)
    key_prefix = models.CharField(max_length=10)  # First few characters for identification
    key_hash = models.CharField(max_length=255)  # Hashed version of the full key
    
    # Permissions
    can_create_projects = models.BooleanField(default=True)
    can_edit_projects = models.BooleanField(default=True)
    can_delete_projects = models.BooleanField(default=False)
    can_deploy_projects = models.BooleanField(default=True)
    
    # Usage tracking
    last_used = models.DateTimeField(null=True, blank=True)
    requests_count = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'api_keys'
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.key_prefix}...)"
    
    def is_expired(self):
        """Check if the API key has expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False