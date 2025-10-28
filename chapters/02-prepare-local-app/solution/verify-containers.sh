#!/bin/bash

# Container Verification Script for Chapter 2
# This script verifies that your application containers are working correctly

echo "=== Chapter 2 Container Verification ==="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
echo -e "\n${YELLOW}Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker Desktop.${NC}"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo -e "${RED}❌ Docker daemon not running. Please start Docker Desktop.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed and running${NC}"

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local url=$1
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$url" > /dev/null 2>&1; then
            return 0
        fi
        sleep 1
        ((attempt++))
    done
    return 1
}

# Verify frontend container
echo -e "\n${YELLOW}Testing Frontend Container...${NC}"

# Check if frontend Dockerfile exists
if [ ! -f "Dockerfile.frontend" ] && [ ! -f "../Dockerfile" ]; then
    echo -e "${RED}❌ Frontend Dockerfile not found${NC}"
    echo "Please create a Dockerfile for your frontend application"
else
    echo -e "${GREEN}✅ Frontend Dockerfile found${NC}"
    
    # Build frontend container
    echo "Building frontend container..."
    if docker build -f Dockerfile.frontend -t chapter2-frontend-test . > /dev/null 2>&1 || \
       docker build -t chapter2-frontend-test . > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend container builds successfully${NC}"
        
        # Check if port 3000 is available
        if ! check_port 3000; then
            echo -e "${YELLOW}⚠️  Port 3000 is in use, using port 3001 instead${NC}"
            FRONTEND_PORT=3001
        else
            FRONTEND_PORT=3000
        fi
        
        # Run frontend container
        echo "Testing frontend container..."
        FRONTEND_CONTAINER=$(docker run -d -p ${FRONTEND_PORT}:3000 chapter2-frontend-test 2>/dev/null)
        
        if [ -n "$FRONTEND_CONTAINER" ]; then
            # Wait for service to be ready
            if wait_for_service "http://localhost:${FRONTEND_PORT}"; then
                echo -e "${GREEN}✅ Frontend container runs and responds correctly${NC}"
                echo -e "${GREEN}   Accessible at: http://localhost:${FRONTEND_PORT}${NC}"
            else
                echo -e "${YELLOW}⚠️  Frontend container running but not responding to HTTP requests${NC}"
                echo "Check your frontend application configuration"
            fi
            
            # Cleanup frontend container
            docker stop $FRONTEND_CONTAINER > /dev/null 2>&1
            docker rm $FRONTEND_CONTAINER > /dev/null 2>&1
        else
            echo -e "${RED}❌ Frontend container failed to start${NC}"
        fi
        
        # Cleanup frontend image
        docker rmi chapter2-frontend-test > /dev/null 2>&1
    else
        echo -e "${RED}❌ Frontend container build failed${NC}"
        echo "Check your Dockerfile and application dependencies"
    fi
fi

# Verify backend container
echo -e "\n${YELLOW}Testing Backend Container...${NC}"

# Check if backend Dockerfile exists
if [ ! -f "Dockerfile.backend" ] && [ ! -f "../backend/Dockerfile" ]; then
    echo -e "${RED}❌ Backend Dockerfile not found${NC}"
    echo "Please create a Dockerfile for your backend application"
else
    echo -e "${GREEN}✅ Backend Dockerfile found${NC}"
    
    # Build backend container
    echo "Building backend container..."
    if docker build -f Dockerfile.backend -t chapter2-backend-test . > /dev/null 2>&1 || \
       docker build -t chapter2-backend-test ../backend > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend container builds successfully${NC}"
        
        # Check if port 8000 is available
        if ! check_port 8000; then
            echo -e "${YELLOW}⚠️  Port 8000 is in use, using port 8001 instead${NC}"
            BACKEND_PORT=8001
        else
            BACKEND_PORT=8000
        fi
        
        # Run backend container
        echo "Testing backend container..."
        BACKEND_CONTAINER=$(docker run -d -p ${BACKEND_PORT}:8000 chapter2-backend-test 2>/dev/null)
        
        if [ -n "$BACKEND_CONTAINER" ]; then
            # Wait for service to be ready
            if wait_for_service "http://localhost:${BACKEND_PORT}" || \
               wait_for_service "http://localhost:${BACKEND_PORT}/health" || \
               wait_for_service "http://localhost:${BACKEND_PORT}/api/health"; then
                echo -e "${GREEN}✅ Backend container runs and responds correctly${NC}"
                echo -e "${GREEN}   Accessible at: http://localhost:${BACKEND_PORT}${NC}"
            else
                echo -e "${YELLOW}⚠️  Backend container running but not responding to HTTP requests${NC}"
                echo "Check your backend application configuration and health endpoints"
            fi
            
            # Cleanup backend container
            docker stop $BACKEND_CONTAINER > /dev/null 2>&1
            docker rm $BACKEND_CONTAINER > /dev/null 2>&1
        else
            echo -e "${RED}❌ Backend container failed to start${NC}"
        fi
        
        # Cleanup backend image
        docker rmi chapter2-backend-test > /dev/null 2>&1
    else
        echo -e "${RED}❌ Backend container build failed${NC}"
        echo "Check your Dockerfile and application dependencies"
    fi
fi

# Check for architecture documentation
echo -e "\n${YELLOW}Checking Documentation...${NC}"

if [ -f "ARCHITECTURE.md" ] || [ -f "../ARCHITECTURE.md" ] || [ -f "README.md" ]; then
    echo -e "${GREEN}✅ Architecture documentation found${NC}"
else
    echo -e "${YELLOW}⚠️  Architecture documentation not found${NC}"
    echo "Consider creating ARCHITECTURE.md to document your application"
fi

# Final summary
echo -e "\n${GREEN}=== Verification Complete ===${NC}"
echo -e "\nNext steps:"
echo -e "${YELLOW}1.${NC} If containers are working, you're ready for Chapter 3!"
echo -e "${YELLOW}2.${NC} If there are issues, review the Dockerfile examples in the solution directory"
echo -e "${YELLOW}3.${NC} Make sure your application code listens on 0.0.0.0, not just localhost"
echo -e "${YELLOW}4.${NC} Verify all dependencies are included in your container images"

echo -e "\n${GREEN}Great work on Chapter 2! Your application is ready for Azure deployment.${NC}"