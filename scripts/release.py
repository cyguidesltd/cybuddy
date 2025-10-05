#!/usr/bin/env python3
"""
Release script for CyBuddy
Automatically bumps version and creates git tags for PyPI deployment
"""

import re
import sys
import subprocess
from pathlib import Path

def get_current_version():
    """Get current version from pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    if not pyproject_path.exists():
        raise FileNotFoundError("pyproject.toml not found")
    
    content = pyproject_path.read_text()
    match = re.search(r'version = "([^"]+)"', content)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    
    return match.group(1)

def update_version(new_version):
    """Update version in pyproject.toml"""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    
    # Replace version line
    new_content = re.sub(
        r'version = "[^"]+"',
        f'version = "{new_version}"',
        content
    )
    
    pyproject_path.write_text(new_content)
    print(f"✅ Updated version to {new_version} in pyproject.toml")

def bump_version(current_version, bump_type):
    """Bump version based on type (major, minor, patch)"""
    parts = current_version.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {current_version}")
    
    major, minor, patch = map(int, parts)
    
    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}. Use major, minor, or patch")
    
    return f"{major}.{minor}.{patch}"

def create_git_tag(version):
    """Create git tag and push to remote"""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    result = subprocess.run(
        ["git", "tag", "-l", tag_name],
        capture_output=True,
        text=True
    )
    
    if tag_name in result.stdout:
        print(f"⚠️  Tag {tag_name} already exists")
        return False
    
    # Create and push tag
    subprocess.run(["git", "add", "pyproject.toml"], check=True)
    subprocess.run(["git", "commit", "-m", f"Bump version to {version}"], check=True)
    subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release {version}"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    subprocess.run(["git", "push", "origin", tag_name], check=True)
    
    print(f"✅ Created and pushed tag {tag_name}")
    return True

def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/release.py <bump_type>")
        print("Bump types: major, minor, patch")
        print("Examples:")
        print("  python scripts/release.py patch    # 1.0.0 -> 1.0.1")
        print("  python scripts/release.py minor    # 1.0.0 -> 1.1.0")
        print("  python scripts/release.py major    # 1.0.0 -> 2.0.0")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    if bump_type not in ["major", "minor", "patch"]:
        print(f"❌ Invalid bump type: {bump_type}")
        print("Use: major, minor, or patch")
        sys.exit(1)
    
    try:
        current_version = get_current_version()
        print(f"📦 Current version: {current_version}")
        
        new_version = bump_version(current_version, bump_type)
        print(f"🚀 New version: {new_version}")
        
        # Confirm before proceeding
        confirm = input(f"Proceed with release {new_version}? [y/N]: ")
        if confirm.lower() != 'y':
            print("❌ Release cancelled")
            sys.exit(1)
        
        update_version(new_version)
        create_git_tag(new_version)
        
        print(f"\n🎉 Release {new_version} created successfully!")
        print("GitHub Actions will automatically build and publish to PyPI")
        print(f"Monitor progress at: https://github.com/YOUR_USERNAME/secbuddy/actions")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
