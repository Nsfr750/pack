"""
Repository management for Python Package Manager.
Handles both public and private package repositories.
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Union
import subprocess
import logging

logger = logging.getLogger(__name__)

class PackageRepository:
    """Represents a package repository (public or private)."""
    
    def __init__(self, name: str, url: str, username: str = None, password: str = None, 
                 is_default: bool = False):
        """Initialize a package repository.
        
        Args:
            name: Repository name
            url: Repository URL
            username: Optional username for authentication
            password: Optional password/token for authentication
            is_default: Whether this is the default repository
        """
        self.name = name
        self.url = url
        self.username = username
        self.password = password
        self.is_default = is_default
    
    def get_auth_url(self) -> str:
        """Get the URL with authentication if credentials are provided."""
        if self.username and self.password:
            # Handle both http and https URLs
            if self.url.startswith('http://'):
                return self.url.replace('http://', f'http://{self.username}:{self.password}@', 1)
            elif self.url.startswith('https://'):
                return self.url.replace('https://', f'https://{self.username}:{self.password}@', 1)
        return self.url
    
    def to_dict(self) -> dict:
        """Convert repository to dictionary for serialization."""
        return {
            'name': self.name,
            'url': self.url,
            'username': self.username,
            'is_default': self.is_default,
            # Note: Password is not included in serialization for security
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PackageRepository':
        """Create a PackageRepository from a dictionary."""
        return cls(
            name=data['name'],
            url=data['url'],
            username=data.get('username'),
            password=None,  # Password is not stored in serialized data
            is_default=data.get('is_default', False)
        )


class RepositoryManager:
    """Manages package repositories."""
    
    CONFIG_FILE = 'repositories.json'
    
    def __init__(self, config_dir: str = None):
        """Initialize the repository manager.
        
        Args:
            config_dir: Directory to store repository configuration
        """
        self.config_dir = config_dir or os.path.join(os.path.expanduser('~'), '.python_package_manager')
        self.config_file = os.path.join(self.config_dir, self.CONFIG_FILE)
        self.repositories: Dict[str, PackageRepository] = {}
        self._load_repositories()
    
    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)
    
    def _load_repositories(self) -> None:
        """Load repositories from the configuration file."""
        self._ensure_config_dir()
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.repositories = {
                        name: PackageRepository.from_dict(repo_data)
                        for name, repo_data in data.items()
                    }
            except Exception as e:
                logger.error(f"Error loading repositories: {e}")
                self.repositories = {}
        
        # Ensure PyPI is always available
        if 'pypi' not in self.repositories:
            self.add_repository(
                PackageRepository('pypi', 'https://pypi.org/simple', is_default=True)
            )
    
    def save_repositories(self) -> None:
        """Save repositories to the configuration file."""
        self._ensure_config_dir()
        try:
            data = {
                name: repo.to_dict()
                for name, repo in self.repositories.items()
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving repositories: {e}")
    
    def add_repository(self, repo: PackageRepository) -> None:
        """Add or update a repository.
        
        Args:
            repo: The repository to add or update
        """
        self.repositories[repo.name] = repo
        self.save_repositories()
    
    def remove_repository(self, name: str) -> bool:
        """Remove a repository by name.
        
        Args:
            name: Name of the repository to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        if name in self.repositories and name != 'pypi':  # Prevent removing PyPI
            del self.repositories[name]
            self.save_repositories()
            return True
        return False
    
    def get_repository(self, name: str) -> Optional[PackageRepository]:
        """Get a repository by name.
        
        Args:
            name: Name of the repository
            
        Returns:
            Optional[PackageRepository]: The repository or None if not found
        """
        return self.repositories.get(name)
    
    def get_default_repository(self) -> Optional[PackageRepository]:
        """Get the default repository.
        
        Returns:
            Optional[PackageRepository]: The default repository or None if not set
        """
        for repo in self.repositories.values():
            if repo.is_default:
                return repo
        return self.get_repository('pypi')  # Fall back to PyPI
    
    def list_repositories(self) -> List[PackageRepository]:
        """Get a list of all repositories.
        
        Returns:
            List[PackageRepository]: List of all repositories
        """
        return list(self.repositories.values())
    
    def set_default_repository(self, name: str) -> bool:
        """Set the default repository.
        
        Args:
            name: Name of the repository to set as default
            
        Returns:
            bool: True if successful, False if repository not found
        """
        if name not in self.repositories:
            return False
            
        # Clear default flag from all repositories
        for repo in self.repositories.values():
            repo.is_default = False
            
        # Set the new default
        self.repositories[name].is_default = True
        self.save_repositories()
        return True
