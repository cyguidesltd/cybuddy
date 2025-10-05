#!/bin/bash
# Setup script for CyBuddy PyPI deployment

echo "🚀 CyBuddy Deployment Setup"
echo "============================"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a git repository. Please run this from your project root."
    exit 1
fi

# Check if GitHub remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No GitHub remote found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/secbuddy.git"
    exit 1
fi

echo "✅ Git repository detected"
echo "✅ GitHub remote configured"
echo ""

# Check if pyproject.toml exists
if [ ! -f "pyproject.toml" ]; then
    echo "❌ pyproject.toml not found. Please ensure you're in the project root."
    exit 1
fi

echo "✅ pyproject.toml found"
echo ""

# Check if GitHub Actions workflows exist
if [ ! -d ".github/workflows" ]; then
    echo "❌ GitHub Actions workflows not found. Please ensure .github/workflows/ exists."
    exit 1
fi

echo "✅ GitHub Actions workflows configured"
echo ""

echo "📋 Next Steps:"
echo "=============="
echo ""
echo "1. 🔑 Configure PyPI API Token:"
echo "   - Go to: https://pypi.org/manage/account/"
echo "   - Create API token (scope: entire account or project)"
echo "   - Copy the token (starts with 'pypi-')"
echo ""
echo "2. 🔐 Add GitHub Secret:"
echo "   - Go to: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1\/\2/')/settings/secrets/actions"
echo "   - Click 'New repository secret'"
echo "   - Name: PYPI_API_TOKEN"
echo "   - Value: Your PyPI token"
echo ""
echo "3. 🚀 Test Deployment:"
echo "   # Make a small change and test release"
echo "   python scripts/release.py patch"
echo ""
echo "4. 📊 Monitor Deployment:"
echo "   - Check GitHub Actions: https://github.com/$(git remote get-url origin | sed 's/.*github.com[:/]\([^/]*\)\/\([^.]*\).*/\1\/\2/')/actions"
echo "   - Verify PyPI: https://pypi.org/project/cybuddy/"
echo ""
echo "🎉 Setup complete! Your repository is ready for automatic PyPI deployment."
echo ""
echo "📖 For detailed instructions, see: docs/DEPLOYMENT.md"
