#!/usr/bin/env bash

# Deployment Git Commit Script

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║      ChamaNexus Deployment Commit Script       ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════╝${NC}"

# Generate timestamp
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Default commit message for our specific fixes
COMMIT_MESSAGE="Deploy: Fix backend-frontend connectivity for Render deployment

## Deployment Summary
Date: $TIMESTAMP
Service: ChamaNexus Backend (Render)
Frontend: chamanexus.onrender.com
Backend: chamanexus-backend.onrender.com

## Issues Resolved
1. Fixed 404 errors on API endpoints
2. Added missing root-level routes for frontend
3. Configured CORS for production domains
4. Fixed CSRF token handling
5. Updated middleware for API endpoints

## Technical Changes
- Added /csrf-token/ endpoint at root level
- Added /accounts/ routes without /api/v1/ prefix
- Updated CORS_ALLOWED_ORIGINS with frontend domain
- Fixed CSRF_TRUSTED_ORIGINS configuration
- Updated REST_FRAMEWORK permissions
- Improved build.sh with migration support

## Testing Endpoints
- GET / - API root ✓
- GET /csrf-token/ - CSRF token ✓
- POST /accounts/auth/register/ - Registration ✓
- POST /accounts/auth/login/ - Login ✓

## Environment Variables Required
- FRONTEND_URL=https://chamanexus.onrender.com
- CORS_ALLOWED_ORIGINS includes frontend domain
- CSRF_TRUSTED_ORIGINS includes both domains

This deployment enables successful connection between React frontend
and Django backend on Render platform."

# Show what will be committed
echo -e "\n${YELLOW}Files to commit:${NC}"
git status --porcelain

echo -e "\n${BLUE}Commit message:${NC}"
echo "================================================================================"
echo -e "$COMMIT_MESSAGE"
echo "================================================================================"

# Ask for confirmation
echo ""
read -p "Proceed with commit? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Commit cancelled.${NC}"
    exit 0
fi

# Execute
echo -e "${GREEN}Staging changes...${NC}"
git add .

echo -e "${GREEN}Committing...${NC}"
git commit -m "$COMMIT_MESSAGE"

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Deployment commit created!${NC}"
    
    # Get current branch
    BRANCH=$(git branch --show-current)
    echo -e "\n${BLUE}Next steps:${NC}"
    echo "1. Review commit: ${GREEN}git show${NC}"
    echo "2. Push to remote: ${GREEN}git push origin $BRANCH${NC}"
    echo "3. Monitor deployment on Render dashboard"
else
    echo -e "\n${RED}✗ Commit failed!${NC}"
fi
