#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== ShoppingHub Setup ===${NC}\n"

# Check Python version
echo -e "${YELLOW}Checking Python version...${NC}"
python3 --version || {
    echo -e "${RED}Python 3 is required but not installed.${NC}"
    exit 1
}

# Backend setup
echo -e "\n${YELLOW}Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate || . venv/Scripts/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}.env file created. Please update it with your settings.${NC}"
fi

echo -e "\n${GREEN}✓ Backend setup complete!${NC}"
echo -e "${YELLOW}To start the backend server, run:${NC}"
echo -e "${GREEN}cd backend && source venv/bin/activate && uvicorn main:app --reload${NC}"

echo -e "\n${YELLOW}Frontend is ready to serve!${NC}"
echo -e "${YELLOW}To start the frontend, navigate to the frontend directory and use:${NC}"
echo -e "${GREEN}python -m http.server 8080${NC}"
echo -e "${GREEN}or use any HTTP server of your choice${NC}"

echo -e "\n${GREEN}=== Setup Complete ===${NC}"
