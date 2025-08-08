"""
Project models for the AI App Builder
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid
import json

User = get_user_model()

class Project(models.Model):
    """Main project model representing a generated web application"""
    
    STATUS_CHOICES = [
        ('creating', 'Creating'),
        ('created', 'Created'),
        ('building', 'Building'),
        ('deployed', 'Deployed'),
        ('failed', 'Failed'),
        ('archived', 'Archived'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('unlisted', 'Unlisted'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    
    # Basic project information
    name = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    
    # Technical details
    tech_stack = models.JSONField(default=list)  # ['react', 'tailwind', 'typescript']
    framework = models.CharField(max_length=50, default='react')
    
    # AI generation details
    original_prompt = models.TextField()  # The user's original description
    design_preferences = models.TextField(blank=True, null=True)
    ai_model_used = models.CharField(max_length=50, default='gpt-4')
    generation_time_seconds = models.PositiveIntegerField(null=True, blank=True)
    
    # Project status and visibility
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='creating')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='private')
    
    # File system paths
    project_path = models.CharField(max_length=500, blank=True, null=True)
    build_path = models.CharField(max_length=500, blank=True, null=True)
    
    # Deployment information
    deployment_url = models.URLField(blank=True, null=True)
    preview_url = models.URLField(blank=True, null=True)
    custom_domain = models.CharField(max_length=200, blank=True, null=True)
    
    # Analytics and usage
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    fork_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deployed_at = models.DateTimeField(null=True, blank=True)
    last_build_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    class Meta:
        db_table = 'projects'
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['visibility', 'created_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return f"{self.name} by {self.owner.username}"
    
    @property
    def is_public(self):
        return self.visibility == 'public'
    
    @property
    def is_deployed(self):
        return self.status == 'deployed' and self.deployment_url
    
    def increment_view_count(self):
        """Increment the project's view count"""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    def get_file_count(self):
        """Get the number of files in this project"""
        return self.files.count()
    
    def get_total_size_mb(self):
        """Get the total size of all project files in MB"""
        total_size = self.files.aggregate(
            total=models.Sum('size_bytes')
        )['total'] or 0
        return total_size / (1024 * 1024)

class ProjectFile(models.Model):
    """Individual files within a project"""
    
    FILE_TYPE_CHOICES = [
        ('component', 'Component'),
        ('page', 'Page'),
        ('style', 'Style'),
        ('config', 'Configuration'),
        ('asset', 'Asset'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    
    # File information
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1000)  # Relative path within project
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES, default='other')
    language = models.CharField(max_length=50, blank=True, null=True)  # 'javascript', 'css', etc.
    
    # Content
    content = models.TextField()
    content_hash = models.CharField(max_length=64)  # SHA-256 hash for change detection
    size_bytes = models.PositiveIntegerField(default=0)
    
    # Metadata
    description = models.TextField(blank=True, null=True)
    is_generated = models.BooleanField(default=True)  # Was this file AI-generated?
    is_editable = models.BooleanField(default=True)  # Can users edit this file?
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'project_files'
        verbose_name = 'Project File'
        verbose_name_plural = 'Project Files'
        unique_together = ['project', 'file_path']
        indexes = [
            models.Index(fields=['project', 'file_type']),
            models.Index(fields=['project', 'updated_at']),
        ]
    
    def __str__(self):
        return f"{self.filename} in {self.project.name}"
    
    def save(self, *args, **kwargs):
        # Calculate size and hash before saving
        if self.content:
            self.size_bytes = len(self.content.encode('utf-8'))
            import hashlib
            self.content_hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        super().save(*args, **kwargs)

class ProjectCollaborator(models.Model):
    """Users who have been invited to collaborate on a project"""
    
    ROLE_CHOICES = [
        ('viewer', 'Viewer'),
        ('editor', 'Editor'),
        ('admin', 'Admin'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='collaborators')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborated_projects')
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    invited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_invites')
    
    # Status
    is_accepted = models.BooleanField(default=False)
    invitation_token = models.UUIDField(default=uuid.uuid4, editable=False)
    
    # Timestamps
    invited_at = models.DateTimeField(default=timezone.now)
    accepted_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'project_collaborators'
        verbose_name = 'Project Collaborator'
        verbose_name_plural = 'Project Collaborators'
        unique_together = ['project', 'user']
        indexes = [
            models.Index(fields=['user', 'is_accepted']),
            models.Index(fields=['project', 'role']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.role} on {self.project.name}"
    
    def accept_invitation(self):
        """Accept the collaboration invitation"""
        self.is_accepted = True
        self.accepted_at = timezone.now()
        self.save(update_fields=['is_accepted', 'accepted_at'])

class ProjectDeployment(models.Model):
    """Deployment history and configuration for projects"""
    
    DEPLOYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('building', 'Building'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    DEPLOYMENT_TYPE_CHOICES = [
        ('preview', 'Preview'),
        ('production', 'Production'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='deployments')
    
    # Deployment details
    deployment_type = models.CharField(max_length=20, choices=DEPLOYMENT_TYPE_CHOICES, default='preview')
    status = models.CharField(max_length=20, choices=DEPLOYMENT_STATUS_CHOICES, default='pending')
    
    # URLs and configuration
    deployment_url = models.URLField(blank=True, null=True)
    build_logs = models.TextField(blank=True, null=True)
    environment_variables = models.JSONField(default=dict, blank=True)
    
    # Build information
    build_time_seconds = models.PositiveIntegerField(null=True, blank=True)
    commit_hash = models.CharField(max_length=64, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'project_deployments'
        verbose_name = 'Project Deployment'
        verbose_name_plural = 'Project Deployments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'status']),
            models.Index(fields=['deployment_type', 'status']),
        ]
    
    def __str__(self):
        return f"Deployment of {self.project.name} - {self.status}"
    
    @property
    def duration(self):
        """Get the duration of the deployment in seconds"""
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at).total_seconds()
        return None

class ProjectLike(models.Model):
    """User likes for public projects"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_projects')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'project_likes'
        verbose_name = 'Project Like'
        verbose_name_plural = 'Project Likes'
        unique_together = ['project', 'user']
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} likes {self.project.name}"

class ProjectFork(models.Model):
    """Forks of public projects"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='forks')
    forked_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='fork_source')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forked_projects')
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'project_forks'
        verbose_name = 'Project Fork'
        verbose_name_plural = 'Project Forks'
        unique_together = ['original_project', 'user']
    
    def __str__(self):
        return f"{self.user.username} forked {self.original_project.name}"