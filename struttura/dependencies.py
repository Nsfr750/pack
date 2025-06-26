"""
Dependency resolution for Python Package Manager.
Handles dependency resolution and conflict detection.
"""
import re
import sys
import subprocess
import logging
from typing import Dict, List, Set, Tuple, Optional, NamedTuple
from pathlib import Path

logger = logging.getLogger(__name__)

class PackageSpec(NamedTuple):
    """Represents a package specification with name and version constraints."""
    name: str
    specifiers: List[Tuple[str, str]]  # List of (operator, version) tuples
    extras: List[str] = []
    
    def __str__(self) -> str:
        """Convert to pip-compatible requirement string."""
        parts = [self.name]
        if self.extras:
            parts.append(f"[{','.join(self.extras)}]")
        if self.specifiers:
            parts.append(','.join(f"{op}{ver}" for op, ver in self.specifiers))
        return ''.join(parts)

class DependencyResolver:
    """Handles dependency resolution for Python packages."""
    
    # Regular expressions for parsing package specifications
    NAME_RE = re.compile(r'^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$', re.IGNORECASE)
    VERSION_SPECIFIER_RE = re.compile(r'^(~=|==|!=|<=|>=|<|>|===|!==)\s*([^,;\s]+)')
    EXTRA_RE = re.compile(r'^\s*\[(.*?)\]')
    
    def __init__(self, python_executable: str = None):
        """Initialize the dependency resolver.
        
        Args:
            python_executable: Path to Python executable (default: sys.executable)
        """
        self.python = python_executable or sys.executable
    
    def parse_requirement(self, requirement: str) -> PackageSpec:
        """Parse a requirement string into a PackageSpec.
        
        Args:
            requirement: Requirement string (e.g., "package>=1.0,<2.0")
            
        Returns:
            PackageSpec: Parsed package specification
            
        Raises:
            ValueError: If the requirement string is invalid
        """
        requirement = requirement.strip()
        if not requirement:
            raise ValueError("Empty requirement string")
            
        # Extract extras if present
        extras = []
        extra_match = self.EXTRA_RE.search(requirement)
        if extra_match:
            extras = [e.strip() for e in extra_match.group(1).split(',') if e.strip()]
            requirement = self.EXTRA_RE.sub('', requirement, 1)
        
        # Extract version specifiers
        specifiers = []
        while True:
            # Find the first version specifier
            match = self.VERSION_SPECIFIER_RE.search(requirement)
            if not match:
                break
                
            op = match.group(1)
            version = match.group(2)
            specifiers.append((op, version))
            
            # Remove the matched part
            requirement = requirement[:match.start()] + requirement[match.end():]
        
        # The remaining part is the package name
        name = requirement.strip()
        if not name or not self.NAME_RE.match(name):
            raise ValueError(f"Invalid package name: {name}")
        
        return PackageSpec(name=name, specifiers=specifiers, extras=extras)
    
    def get_installed_packages(self) -> Dict[str, str]:
        """Get a dictionary of installed packages and their versions.
        
        Returns:
            Dict[str, str]: Mapping of package names to versions
        """
        try:
            result = subprocess.run(
                [self.python, '-m', 'pip', 'list', '--format=json'],
                capture_output=True,
                text=True,
                check=True
            )
            
            packages = {}
            for pkg in json.loads(result.stdout):
                packages[pkg['name'].lower()] = pkg['version']
            return packages
            
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.error(f"Error getting installed packages: {e}")
            return {}
    
    def get_package_dependencies(self, package_spec: str) -> List[PackageSpec]:
        """Get the dependencies of a package.
        
        Args:
            package_spec: Package specification (e.g., "package>=1.0")
            
        Returns:
            List[PackageSpec]: List of dependencies as PackageSpec objects
        """
        try:
            # Use pip to get package metadata
            result = subprocess.run(
                [self.python, '-m', 'pip', 'show', package_spec],
                capture_output=True,
                text=True,
                check=True
            )
            
            dependencies = []
            requires_dist = False
            
            for line in result.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                    
                if line.lower().startswith('requires:'):
                    requires_dist = True
                    deps = line[9:].strip()
                    if deps:
                        for dep in deps.split(','):
                            try:
                                dependencies.append(self.parse_requirement(dep))
                            except ValueError as e:
                                logger.warning(f"Skipping invalid dependency: {dep} - {e}")
                elif requires_dist:
                    # Handle multi-line requirements
                    if ':' in line:  # Next section started
                        break
                    for dep in line.split(','):
                        try:
                            dependencies.append(self.parse_requirement(dep))
                        except ValueError as e:
                            logger.warning(f"Skipping invalid dependency: {dep} - {e}")
            
            return dependencies
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Error getting package dependencies: {e}")
            return []
    
    def resolve_dependencies(self, requirements: List[str]) -> Dict[str, str]:
        """Resolve dependencies for a list of requirements.
        
        Args:
            requirements: List of requirement strings
            
        Returns:
            Dict[str, str]: Mapping of package names to resolved versions
            
        Raises:
            ValueError: If dependencies cannot be resolved
        """
        try:
            # Use pip's resolver to handle the heavy lifting
            temp_req_file = Path('temp_requirements.txt')
            with temp_req_file.open('w') as f:
                for req in requirements:
                    f.write(f"{req}\n")
            
            # Create a temporary virtual environment for resolution
            venv_dir = Path('temp_venv')
            subprocess.run(
                [sys.executable, '-m', 'venv', str(venv_dir)],
                check=True
            )
            
            # Use the virtual environment's pip to resolve dependencies
            pip_path = venv_dir / 'bin' / 'pip'
            if sys.platform == 'win32':
                pip_path = venv_dir / 'Scripts' / 'pip.exe'
            
            # Install the requirements
            result = subprocess.run(
                [str(pip_path), 'install', '-r', str(temp_req_file)],
                capture_output=True,
                text=True
            )
            
            # Clean up
            temp_req_file.unlink()
            shutil.rmtree(venv_dir, ignore_errors=True)
            
            if result.returncode != 0:
                raise ValueError(f"Failed to resolve dependencies: {result.stderr}")
            
            # Get the installed packages
            return self.get_installed_packages()
            
        except Exception as e:
            # Clean up on error
            if 'temp_req_file' in locals() and temp_req_file.exists():
                temp_req_file.unlink()
            if 'venv_dir' in locals() and venv_dir.exists():
                shutil.rmtree(venv_dir, ignore_errors=True)
            raise ValueError(f"Dependency resolution failed: {e}")
    
    def check_conflicts(self, requirements: List[str]) -> List[Tuple[str, str, str]]:
        """Check for version conflicts in requirements.
        
        Args:
            requirements: List of requirement strings
            
        Returns:
            List[Tuple[str, str, str]]: List of conflicts as (package, required_by, conflict) tuples
        """
        try:
            resolved = self.resolve_dependencies(requirements)
            return []  # No conflicts if resolution succeeds
        except ValueError as e:
            # Extract conflict information from the error message
            conflicts = []
            error_msg = str(e)
            
            # This is a simplified approach - in a real implementation, you'd want to parse
            # the actual conflict information from the error message
            conflict_match = re.search(r"Cannot install ([^\s]+) because these package versions have conflicting dependencies", error_msg)
            if conflict_match:
                package = conflict_match.group(1)
                conflicts.append((package, "multiple", f"Version conflict for {package}"))
            
            return conflicts
