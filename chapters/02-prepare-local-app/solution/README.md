# Chapter 2 Solution: Application Preparation and Containerization

This directory contains the complete solution and verification resources for Chapter 2: "Prepare for Success by Understanding Your Local Application."

## What You Should Have Accomplished

By completing Chapter 2, you should have:

✅ **Application Architecture Mapped**: Complete understanding of your application components and their relationships  
✅ **Containers Created**: Working Docker containers for your frontend and backend applications  
✅ **Documentation Built**: Comprehensive architecture documentation and migration plan  
✅ **Migration Strategy**: Clear roadmap for moving each component to Azure  
✅ **Container Testing**: Verified that containers run correctly and communicate properly  
✅ **Azure Readiness**: Everything prepared for successful Azure deployment

## Verification Checklist

### Application Understanding
- [ ] Component architecture documented with relationships
- [ ] Data flow patterns identified and documented  
- [ ] Dependencies clearly understood and listed
- [ ] Communication patterns between components mapped
- [ ] Current application baseline established

### Containerization Success
- [ ] Frontend container builds successfully
- [ ] Backend container builds successfully
- [ ] Containers run without errors locally
- [ ] Application functions correctly in containers
- [ ] Container networking verified and working

### Documentation Quality
- [ ] Architecture diagram created and comprehensive
- [ ] Migration plan documented with phases
- [ ] Cost estimates calculated for Azure services
- [ ] Resource requirements identified
- [ ] Pre-migration checklist completed

## Container Verification Scripts

### Frontend Container Verification
```bash
#!/bin/bash

echo "=== Frontend Container Verification ==="

# Check if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile found"
else
    echo "❌ Dockerfile not found"
    exit 1
fi

# Build frontend container
echo "Building frontend container..."
if docker build -t my-frontend-verification . > /dev/null 2>&1; then
    echo "✅ Frontend container builds successfully"
else
    echo "❌ Frontend container build failed"
    exit 1
fi

# Test container run
echo "Testing frontend container..."
CONTAINER_ID=$(docker run -d -p 3001:3000 my-frontend-verification)

# Wait for container to start
sleep 5

# Check if container is running
if docker ps | grep -q $CONTAINER_ID; then
    echo "✅ Frontend container runs successfully"
    
    # Test HTTP response
    if curl -f http://localhost:3001 > /dev/null 2>&1; then
        echo "✅ Frontend responds to HTTP requests"
    else
        echo "⚠️  Frontend container running but not responding to HTTP"
    fi
else
    echo "❌ Frontend container failed to start"
fi

# Cleanup
docker stop $CONTAINER_ID > /dev/null 2>&1
docker rm $CONTAINER_ID > /dev/null 2>&1
docker rmi my-frontend-verification > /dev/null 2>&1

echo "Frontend verification complete"
```

### Backend Container Verification
```bash
#!/bin/bash

echo "=== Backend Container Verification ==="

# Check if Dockerfile exists
if [ -f "Dockerfile" ]; then
    echo "✅ Dockerfile found"
else
    echo "❌ Dockerfile not found"
    exit 1
fi

# Build backend container
echo "Building backend container..."
if docker build -t my-backend-verification . > /dev/null 2>&1; then
    echo "✅ Backend container builds successfully"
else
    echo "❌ Backend container build failed"
    exit 1
fi

# Test container run
echo "Testing backend container..."
CONTAINER_ID=$(docker run -d -p 8001:8000 my-backend-verification)

# Wait for container to start
sleep 5

# Check if container is running
if docker ps | grep -q $CONTAINER_ID; then
    echo "✅ Backend container runs successfully"
    
    # Test HTTP response (assuming health endpoint)
    if curl -f http://localhost:8001/health > /dev/null 2>&1 || curl -f http://localhost:8001 > /dev/null 2>&1; then
        echo "✅ Backend responds to HTTP requests"
    else
        echo "⚠️  Backend container running but not responding to HTTP"
    fi
else
    echo "❌ Backend container failed to start"
fi

# Cleanup
docker stop $CONTAINER_ID > /dev/null 2>&1
docker rm $CONTAINER_ID > /dev/null 2>&1
docker rmi my-backend-verification > /dev/null 2>&1

echo "Backend verification complete"
```

### PowerShell Container Verification (Windows)
```powershell
# Frontend Container Verification Script
Write-Host "=== Frontend Container Verification ===" -ForegroundColor Green

# Check if Dockerfile exists
if (Test-Path "Dockerfile") {
    Write-Host "✅ Dockerfile found" -ForegroundColor Green
} else {
    Write-Host "❌ Dockerfile not found" -ForegroundColor Red
    exit 1
}

# Build frontend container
Write-Host "Building frontend container..." -ForegroundColor Yellow
try {
    docker build -t my-frontend-verification . 2>$null | Out-Null
    Write-Host "✅ Frontend container builds successfully" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend container build failed" -ForegroundColor Red
    exit 1
}

# Test container run
Write-Host "Testing frontend container..." -ForegroundColor Yellow
$containerId = docker run -d -p 3001:3000 my-frontend-verification

# Wait for container to start
Start-Sleep -Seconds 5

# Check if container is running
$runningContainers = docker ps
if ($runningContainers -match $containerId) {
    Write-Host "✅ Frontend container runs successfully" -ForegroundColor Green
    
    # Test HTTP response
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:3001" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ Frontend responds to HTTP requests" -ForegroundColor Green
    } catch {
        Write-Host "⚠️  Frontend container running but not responding to HTTP" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Frontend container failed to start" -ForegroundColor Red
}

# Cleanup
docker stop $containerId 2>$null | Out-Null
docker rm $containerId 2>$null | Out-Null
docker rmi my-frontend-verification 2>$null | Out-Null

Write-Host "Frontend verification complete" -ForegroundColor Green
```

## Sample Dockerfiles

### React Frontend Dockerfile
```dockerfile
# Use official Node.js runtime as base image
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source code
COPY . .

# Build the React application
RUN npm run build

# Install serve to serve static files
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", "build", "-l", "3000"]
```

### Node.js Backend Dockerfile
```dockerfile
# Use official Node.js runtime as base image
FROM node:18-alpine

# Set working directory inside container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy application source code
COPY . .

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["npm", "start"]
```

### Vue.js Frontend Dockerfile
```dockerfile
# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine as production-stage

# Copy built application
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
```

## Architecture Documentation Template

### Application Architecture Document
```markdown
# My Application Architecture Documentation

## Application Overview
- **Name**: [Your Application Name]
- **Purpose**: [Brief description of what your app does]
- **Technology Stack**: [Frontend tech], [Backend tech], [Database tech]
- **Current Status**: Containerized and ready for Azure migration

## Component Architecture

### Frontend Application
- **Technology**: [React/Vue/Angular] [version]
- **Development Server**: [Create React App/Vite/etc.]
- **Build Output**: Static files (HTML, CSS, JS)
- **Local URL**: http://localhost:[port]
- **Container Port**: [port]
- **Container Name**: [container-name]

### Backend API
- **Technology**: [Node.js/Python/C#] [version] with [Express/Django/ASP.NET]
- **Local URL**: http://localhost:[port]
- **Container Port**: [port]
- **Container Name**: [container-name]
- **Main Routes**: 
  - [List your main API endpoints]
- **Dependencies**: [List external dependencies]

### Database
- **Technology**: [PostgreSQL/MySQL/MongoDB] [version]
- **Local Connection**: localhost:[port]
- **Database Name**: [database_name]
- **Main Tables/Collections**: [List main data structures]
- **Current Data Size**: [Approximate size]

### File Storage
- **Current Method**: [Local filesystem/cloud storage]
- **File Types**: [Image formats, document types, etc.]
- **Current Usage**: [Approximate size]
- **Access Pattern**: [How files are accessed]

## Container Configuration

### Frontend Container
- **Base Image**: node:18-alpine
- **Build Process**: npm install → npm run build → serve static files
- **Exposed Port**: [port]
- **Health Check**: GET / returns 200
- **Container Size**: [Approximate size]

### Backend Container
- **Base Image**: node:18-alpine
- **Build Process**: npm install → start server
- **Exposed Port**: [port]
- **Health Check**: GET /health returns 200 (if available)
- **External Dependencies**: Database connection, environment variables

## Communication Patterns

### User Registration Flow
1. [Step 1 description]
2. [Step 2 description]
3. [etc.]

### File Upload Flow
1. [Step 1 description]
2. [Step 2 description]
3. [etc.]

## Azure Migration Plan

### Phase 1: Frontend Deployment
- **Target Service**: Azure App Service or Static Web Apps
- **Estimated Time**: 1-2 hours
- **Dependencies**: None
- **Success Criteria**: Frontend accessible via Azure URL

### Phase 2: Backend Deployment
- **Target Service**: Azure App Service (Container)
- **Estimated Time**: 2-3 hours
- **Dependencies**: Database connection configuration
- **Success Criteria**: API endpoints responding correctly

### Phase 3: Database Migration
- **Target Service**: Azure SQL Database or Azure Database for PostgreSQL
- **Estimated Time**: 3-4 hours
- **Dependencies**: Data export/import, connection string updates
- **Success Criteria**: All data migrated, applications connected

### Phase 4: Storage Migration
- **Target Service**: Azure Blob Storage
- **Estimated Time**: 2-3 hours
- **Dependencies**: File migration, API updates
- **Success Criteria**: File upload/download working correctly

## Resource Requirements

### Azure Services Needed
- App Service Plan (Basic B1 or higher for containers)
- App Service (Frontend)
- App Service (Backend)
- SQL Database (Basic tier for learning)
- Storage Account (Standard tier)

### Estimated Monthly Costs
- App Service Plan: ~$13
- SQL Database: ~$5
- Storage Account: ~$2
- **Total: ~$20/month**

## Pre-Migration Checklist
- [ ] All containers build successfully
- [ ] Containers run correctly locally
- [ ] Application functionality verified in containers
- [ ] Database schema documented
- [ ] Environment variables identified
- [ ] File storage requirements understood
- [ ] Cost estimates reviewed and approved
- [ ] Azure environment prepared (from Chapter 1)
```

## Common Issues and Solutions

### Container Build Issues

**Problem**: "npm install" fails during container build
**Solution**: 
1. Check that package.json is valid JSON
2. Ensure package-lock.json is included in container
3. Try clearing npm cache: `RUN npm cache clean --force`

**Problem**: Container builds but application doesn't start
**Solution**:
1. Check that your start script exists in package.json
2. Verify the application listens on 0.0.0.0, not just localhost
3. Ensure the EXPOSE port matches your application port

### Container Networking Issues

**Problem**: Frontend can't connect to backend container
**Solution**:
1. Use `docker network create` to create a custom network
2. Run both containers on the same network
3. Reference backend by container name instead of localhost

**Problem**: Port conflicts when running containers
**Solution**:
1. Use different host ports: `-p 3001:3000` and `-p 8001:8000`
2. Stop other applications using the same ports
3. Check what's running with `netstat -tulpn` (Linux) or `netstat -an` (Windows)

### Application Issues in Containers

**Problem**: Environment variables not working in container
**Solution**:
1. Pass variables with `-e`: `docker run -e NODE_ENV=production`
2. Use a .env file with `--env-file`
3. Set default values in your application code

**Problem**: File uploads don't work in containers
**Solution**:
1. Use volume mounts for persistent storage: `-v $(pwd)/uploads:/app/uploads`
2. Configure writable directories in container
3. Plan to migrate to Azure Blob Storage for production

## Next Steps

With your application containerized and documented, you're ready for Chapter 3: "Go Live Instantly by Deploying Your Frontend to the Cloud."

### Recommended Follow-up Actions:
1. **Test Container Communication**: Ensure containers can communicate properly
2. **Optimize Container Images**: Learn about multi-stage builds and image optimization  
3. **Set Up Container Registry**: Prepare for Azure Container Registry usage
4. **Review Azure Documentation**: Familiarize yourself with Azure App Service container deployment

### Additional Resources:
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Azure App Service Container Documentation](https://docs.microsoft.com/en-us/azure/app-service/configure-custom-container)
- [Azure Container Instances Tutorial](https://docs.microsoft.com/en-us/azure/container-instances/)

## Support

If you encounter issues with containerization or application preparation:
1. Run the verification scripts to identify specific problems
2. Check the common issues section for solutions
3. Refer to Docker documentation for containerization issues
4. Review your application architecture documentation for clarity

Remember: Proper application preparation and containerization are crucial for successful cloud deployment. Take time to ensure containers work correctly before proceeding to Azure deployment.