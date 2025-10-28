# Chapter 1 Solution: Azure Environment Setup

This directory contains the complete solution and setup verification scripts for Chapter 1: "Get Started with Confidence by Setting Up Your Azure Environment."

## What You Should Have Accomplished

By completing Chapter 1, you should have:

✅ **Azure Account Created**: Free Azure subscription with $200 credits  
✅ **Azure Portal Access**: Comfortable navigating the main interface  
✅ **Resource Group Created**: Organized foundation for your Azure resources  
✅ **Development Tools Installed**: Azure CLI, Azure Developer CLI, VS Code with Azure extensions  
✅ **Billing Alerts Configured**: Protection against unexpected costs  
✅ **Git and GitHub Setup**: Version control ready for future CI/CD work

## Verification Checklist

### Azure Account and Portal Access
- [ ] Can sign in to portal.azure.com successfully
- [ ] Can see your subscription in the Azure Portal
- [ ] Billing alerts are configured and working
- [ ] Resource group is created and visible

### Development Tools Installation
- [ ] Azure CLI installed and working (`az --version`)
- [ ] Azure CLI authenticated with your account (`az login`)
- [ ] Azure Developer CLI installed (`azd version`)
- [ ] VS Code installed with Azure extensions
- [ ] Git configured with your name and email

### Resource Organization
- [ ] Resource group created with descriptive name
- [ ] Resource group has appropriate tags applied
- [ ] Resource group is in your preferred region
- [ ] Can view resource group in both Portal and CLI

## Environment Verification Scripts

### PowerShell Verification Script (Windows)
```powershell
# Azure Environment Verification Script
Write-Host "=== Azure Environment Verification ===" -ForegroundColor Green

# Check Azure CLI
Write-Host "`nChecking Azure CLI..." -ForegroundColor Yellow
try {
    $azVersion = az --version 2>$null
    if ($azVersion) {
        Write-Host "✅ Azure CLI is installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Azure CLI not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Azure CLI not found" -ForegroundColor Red
}

# Check Azure CLI Authentication
Write-Host "`nChecking Azure CLI Authentication..." -ForegroundColor Yellow
try {
    $account = az account show 2>$null | ConvertFrom-Json
    if ($account) {
        Write-Host "✅ Azure CLI is authenticated" -ForegroundColor Green
        Write-Host "   Subscription: $($account.name)" -ForegroundColor Cyan
    } else {
        Write-Host "❌ Azure CLI not authenticated. Run 'az login'" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Azure CLI not authenticated. Run 'az login'" -ForegroundColor Red
}

# Check Azure Developer CLI
Write-Host "`nChecking Azure Developer CLI..." -ForegroundColor Yellow
try {
    $azdVersion = azd version 2>$null
    if ($azdVersion) {
        Write-Host "✅ Azure Developer CLI is installed" -ForegroundColor Green
    } else {
        Write-Host "❌ Azure Developer CLI not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Azure Developer CLI not found" -ForegroundColor Red
}

# Check VS Code
Write-Host "`nChecking VS Code..." -ForegroundColor Yellow
try {
    $codeVersion = code --version 2>$null
    if ($codeVersion) {
        Write-Host "✅ VS Code is installed" -ForegroundColor Green
    } else {
        Write-Host "❌ VS Code not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ VS Code not found" -ForegroundColor Red
}

# Check Git
Write-Host "`nChecking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
        
        # Check Git configuration
        $gitName = git config --global user.name 2>$null
        $gitEmail = git config --global user.email 2>$null
        
        if ($gitName -and $gitEmail) {
            Write-Host "✅ Git is configured" -ForegroundColor Green
            Write-Host "   Name: $gitName" -ForegroundColor Cyan
            Write-Host "   Email: $gitEmail" -ForegroundColor Cyan
        } else {
            Write-Host "⚠️  Git not fully configured. Set name and email." -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Git not found" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Git not found" -ForegroundColor Red
}

# Check Resource Groups
Write-Host "`nChecking Resource Groups..." -ForegroundColor Yellow
try {
    $resourceGroups = az group list 2>$null | ConvertFrom-Json
    if ($resourceGroups.Count -gt 0) {
        Write-Host "✅ Resource groups found:" -ForegroundColor Green
        foreach ($rg in $resourceGroups) {
            Write-Host "   - $($rg.name) (Location: $($rg.location))" -ForegroundColor Cyan
        }
    } else {
        Write-Host "⚠️  No resource groups found" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Cannot check resource groups" -ForegroundColor Red
}

Write-Host "`n=== Verification Complete ===" -ForegroundColor Green
```

### Bash Verification Script (macOS/Linux)
```bash
#!/bin/bash

# Azure Environment Verification Script
echo "=== Azure Environment Verification ==="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Azure CLI
echo -e "\n${YELLOW}Checking Azure CLI...${NC}"
if command -v az &> /dev/null; then
    echo -e "${GREEN}✅ Azure CLI is installed${NC}"
    az --version | head -1
else
    echo -e "${RED}❌ Azure CLI not found${NC}"
fi

# Check Azure CLI Authentication
echo -e "\n${YELLOW}Checking Azure CLI Authentication...${NC}"
if az account show &> /dev/null; then
    echo -e "${GREEN}✅ Azure CLI is authenticated${NC}"
    SUBSCRIPTION=$(az account show --query name -o tsv)
    echo -e "${CYAN}   Subscription: $SUBSCRIPTION${NC}"
else
    echo -e "${RED}❌ Azure CLI not authenticated. Run 'az login'${NC}"
fi

# Check Azure Developer CLI
echo -e "\n${YELLOW}Checking Azure Developer CLI...${NC}"
if command -v azd &> /dev/null; then
    echo -e "${GREEN}✅ Azure Developer CLI is installed${NC}"
else
    echo -e "${RED}❌ Azure Developer CLI not found${NC}"
fi

# Check VS Code
echo -e "\n${YELLOW}Checking VS Code...${NC}"
if command -v code &> /dev/null; then
    echo -e "${GREEN}✅ VS Code is installed${NC}"
else
    echo -e "${RED}❌ VS Code not found${NC}"
fi

# Check Git
echo -e "\n${YELLOW}Checking Git...${NC}"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}✅ Git is installed: $GIT_VERSION${NC}"
    
    # Check Git configuration
    GIT_NAME=$(git config --global user.name 2>/dev/null)
    GIT_EMAIL=$(git config --global user.email 2>/dev/null)
    
    if [ -n "$GIT_NAME" ] && [ -n "$GIT_EMAIL" ]; then
        echo -e "${GREEN}✅ Git is configured${NC}"
        echo -e "${CYAN}   Name: $GIT_NAME${NC}"
        echo -e "${CYAN}   Email: $GIT_EMAIL${NC}"
    else
        echo -e "${YELLOW}⚠️  Git not fully configured. Set name and email.${NC}"
    fi
else
    echo -e "${RED}❌ Git not found${NC}"
fi

# Check Resource Groups
echo -e "\n${YELLOW}Checking Resource Groups...${NC}"
if az group list &> /dev/null; then
    RG_COUNT=$(az group list --query "length(@)")
    if [ "$RG_COUNT" -gt 0 ]; then
        echo -e "${GREEN}✅ Resource groups found:${NC}"
        az group list --query "[].{Name:name, Location:location}" -o table
    else
        echo -e "${YELLOW}⚠️  No resource groups found${NC}"
    fi
else
    echo -e "${RED}❌ Cannot check resource groups${NC}"
fi

echo -e "\n${GREEN}=== Verification Complete ===${NC}"
```

## Common Setup Issues and Solutions

### Azure CLI Authentication Issues
**Problem**: `az login` opens browser but authentication fails
**Solution**: 
1. Clear browser cache and try again
2. Try incognito/private browsing mode
3. Use `az login --use-device-code` for alternative authentication

### VS Code Azure Extensions Not Working
**Problem**: Azure extensions don't show subscription or resources
**Solution**:
1. Restart VS Code after installing extensions
2. Sign out and sign back in to Azure Account extension
3. Check that Azure CLI is authenticated first

### Resource Group Not Visible in CLI
**Problem**: Resource group created in Portal but not visible in CLI
**Solution**:
1. Verify correct subscription selected: `az account show`
2. Refresh CLI cache: `az account clear` then `az login`
3. Check subscription access in Azure Portal

### Git Configuration Missing
**Problem**: Git not configured with user information
**Solution**:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Next Steps

With your environment verified and working, you're ready for Chapter 2: "Prepare for Success by Understanding Your Local Application."

### Recommended Follow-up Actions:
1. **Explore Azure Services**: Spend time browsing different Azure services in the Portal
2. **Practice CLI Commands**: Try various `az` commands to get comfortable with the interface
3. **Set Up Project Repository**: Create a GitHub repository for your learning project
4. **Install Docker**: Prepare for Chapter 2 by installing Docker Desktop

### Additional Resources:
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Developer CLI Documentation](https://docs.microsoft.com/en-us/azure/developer/azure-developer-cli/)
- [VS Code Azure Extensions Guide](https://code.visualstudio.com/docs/azure/extensions)
- [Azure Free Tier Services](https://azure.microsoft.com/en-us/free/)

## Support

If you encounter issues with your environment setup:
1. Run the verification script above to identify specific problems
2. Check the common issues section for solutions
3. Refer to the official Azure documentation for detailed troubleshooting
4. Consider reaching out to Azure community forums for additional help

Remember: A properly configured development environment is crucial for success in cloud development. Take time to ensure everything is working correctly before proceeding to the next chapter.