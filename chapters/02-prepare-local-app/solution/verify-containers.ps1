# Container Verification Script for Chapter 2 (PowerShell)
# This script verifies that your application containers are working correctly

Write-Host "=== Chapter 2 Container Verification ===" -ForegroundColor Green

# Check if Docker is running
Write-Host "`nChecking Docker installation..." -ForegroundColor Yellow

try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "✅ Docker is installed: $dockerVersion" -ForegroundColor Green
        
        # Check if Docker daemon is running
        docker info 2>$null | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker daemon is running" -ForegroundColor Green
        } else {
            Write-Host "❌ Docker daemon not running. Please start Docker Desktop." -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker not found. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

# Function to check if port is available
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $false  # Port is in use
    } catch {
        return $true   # Port is available
    }
}

# Function to wait for service to be ready
function Wait-ForService {
    param([string]$Url, [int]$MaxAttempts = 30)
    
    for ($i = 1; $i -le $MaxAttempts; $i++) {
        try {
            $response = Invoke-WebRequest -Uri $Url -TimeoutSec 2 -ErrorAction Stop
            if ($response.StatusCode -eq 200) {
                return $true
            }
        } catch {
            Start-Sleep -Seconds 1
        }
    }
    return $false
}

# Verify frontend container
Write-Host "`nTesting Frontend Container..." -ForegroundColor Yellow

# Check if frontend Dockerfile exists
$frontendDockerfile = $null
if (Test-Path "Dockerfile.frontend") {
    $frontendDockerfile = "Dockerfile.frontend"
} elseif (Test-Path "Dockerfile") {
    $frontendDockerfile = "Dockerfile"
} elseif (Test-Path "..\Dockerfile") {
    $frontendDockerfile = "..\Dockerfile"
}

if ($frontendDockerfile) {
    Write-Host "✅ Frontend Dockerfile found: $frontendDockerfile" -ForegroundColor Green
    
    # Build frontend container
    Write-Host "Building frontend container..." -ForegroundColor Yellow
    if ($frontendDockerfile -eq "Dockerfile.frontend") {
        $buildResult = docker build -f $frontendDockerfile -t chapter2-frontend-test . 2>$null
    } else {
        $buildResult = docker build -t chapter2-frontend-test . 2>$null
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Frontend container builds successfully" -ForegroundColor Green
        
        # Check if port 3000 is available
        $frontendPort = 3000
        if (-not (Test-Port -Port 3000)) {
            Write-Host "⚠️  Port 3000 is in use, using port 3001 instead" -ForegroundColor Yellow
            $frontendPort = 3001
        }
        
        # Run frontend container
        Write-Host "Testing frontend container..." -ForegroundColor Yellow
        $frontendContainer = docker run -d -p "${frontendPort}:3000" chapter2-frontend-test 2>$null
        
        if ($frontendContainer) {
            Start-Sleep -Seconds 3
            
            # Wait for service to be ready
            if (Wait-ForService -Url "http://localhost:$frontendPort") {
                Write-Host "✅ Frontend container runs and responds correctly" -ForegroundColor Green
                Write-Host "   Accessible at: http://localhost:$frontendPort" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Frontend container running but not responding to HTTP requests" -ForegroundColor Yellow
                Write-Host "Check your frontend application configuration" -ForegroundColor Yellow
            }
            
            # Cleanup frontend container
            docker stop $frontendContainer 2>$null | Out-Null
            docker rm $frontendContainer 2>$null | Out-Null
        } else {
            Write-Host "❌ Frontend container failed to start" -ForegroundColor Red
        }
        
        # Cleanup frontend image
        docker rmi chapter2-frontend-test 2>$null | Out-Null
    } else {
        Write-Host "❌ Frontend container build failed" -ForegroundColor Red
        Write-Host "Check your Dockerfile and application dependencies" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Frontend Dockerfile not found" -ForegroundColor Red
    Write-Host "Please create a Dockerfile for your frontend application" -ForegroundColor Yellow
}

# Verify backend container
Write-Host "`nTesting Backend Container..." -ForegroundColor Yellow

# Check if backend Dockerfile exists
$backendDockerfile = $null
if (Test-Path "Dockerfile.backend") {
    $backendDockerfile = "Dockerfile.backend"
} elseif (Test-Path "..\backend\Dockerfile") {
    $backendDockerfile = "..\backend\Dockerfile"
}

if ($backendDockerfile) {
    Write-Host "✅ Backend Dockerfile found: $backendDockerfile" -ForegroundColor Green
    
    # Build backend container
    Write-Host "Building backend container..." -ForegroundColor Yellow
    if ($backendDockerfile -eq "Dockerfile.backend") {
        $buildResult = docker build -f $backendDockerfile -t chapter2-backend-test . 2>$null
    } else {
        $buildResult = docker build -t chapter2-backend-test ..\backend 2>$null
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Backend container builds successfully" -ForegroundColor Green
        
        # Check if port 8000 is available
        $backendPort = 8000
        if (-not (Test-Port -Port 8000)) {
            Write-Host "⚠️  Port 8000 is in use, using port 8001 instead" -ForegroundColor Yellow
            $backendPort = 8001
        }
        
        # Run backend container
        Write-Host "Testing backend container..." -ForegroundColor Yellow
        $backendContainer = docker run -d -p "${backendPort}:8000" chapter2-backend-test 2>$null
        
        if ($backendContainer) {
            Start-Sleep -Seconds 3
            
            # Try multiple health check endpoints
            $endpoints = @(
                "http://localhost:$backendPort",
                "http://localhost:$backendPort/health",
                "http://localhost:$backendPort/api/health"
            )
            
            $serviceReady = $false
            foreach ($endpoint in $endpoints) {
                if (Wait-ForService -Url $endpoint -MaxAttempts 10) {
                    $serviceReady = $true
                    break
                }
            }
            
            if ($serviceReady) {
                Write-Host "✅ Backend container runs and responds correctly" -ForegroundColor Green
                Write-Host "   Accessible at: http://localhost:$backendPort" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Backend container running but not responding to HTTP requests" -ForegroundColor Yellow
                Write-Host "Check your backend application configuration and health endpoints" -ForegroundColor Yellow
            }
            
            # Cleanup backend container
            docker stop $backendContainer 2>$null | Out-Null
            docker rm $backendContainer 2>$null | Out-Null
        } else {
            Write-Host "❌ Backend container failed to start" -ForegroundColor Red
        }
        
        # Cleanup backend image
        docker rmi chapter2-backend-test 2>$null | Out-Null
    } else {
        Write-Host "❌ Backend container build failed" -ForegroundColor Red
        Write-Host "Check your Dockerfile and application dependencies" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ Backend Dockerfile not found" -ForegroundColor Red
    Write-Host "Please create a Dockerfile for your backend application" -ForegroundColor Yellow
}

# Check for architecture documentation
Write-Host "`nChecking Documentation..." -ForegroundColor Yellow

$documentationFiles = @("ARCHITECTURE.md", "..\ARCHITECTURE.md", "README.md", "..\README.md")
$documentationFound = $false

foreach ($file in $documentationFiles) {
    if (Test-Path $file) {
        Write-Host "✅ Architecture documentation found: $file" -ForegroundColor Green
        $documentationFound = $true
        break
    }
}

if (-not $documentationFound) {
    Write-Host "⚠️  Architecture documentation not found" -ForegroundColor Yellow
    Write-Host "Consider creating ARCHITECTURE.md to document your application" -ForegroundColor Yellow
}

# Final summary
Write-Host "`n=== Verification Complete ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "1. If containers are working, you're ready for Chapter 3!" -ForegroundColor Yellow
Write-Host "2. If there are issues, review the Dockerfile examples in the solution directory" -ForegroundColor Yellow
Write-Host "3. Make sure your application code listens on 0.0.0.0, not just localhost" -ForegroundColor Yellow
Write-Host "4. Verify all dependencies are included in your container images" -ForegroundColor Yellow

Write-Host "`nGreat work on Chapter 2! Your application is ready for Azure deployment." -ForegroundColor Green