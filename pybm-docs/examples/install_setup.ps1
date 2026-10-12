# PyBM Development Environment Setup Script for Windows
# This script must be run with Administrator privileges for some operations

param(
    [switch]$SkipPython = $false,
    [switch]$SkipVSCodeExtension = $false
)

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
    return $currentUser.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to download file
function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath
    )
    Write-Host "Downloading from $Url..." -ForegroundColor Cyan
    try {
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($Url, $OutputPath)
        Write-Host "Download completed: $OutputPath" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "Error downloading file: $_" -ForegroundColor Red
        return $false
    }
}

# Get current username
$username = $env:USERNAME
Write-Host "Setting up PyBM development environment for user: $username" -ForegroundColor Yellow

# ============================================
# 1. Download and Install Python
# ============================================
if (-not $SkipPython) {
    Write-Host "`n=== Step 1: Python Installation ===" -ForegroundColor Yellow
    
    # Check if Python is already installed
    $pythonInstalled = $false
    try {
        $pythonVersion = & python --version 2>&1
        if ($pythonVersion -match "Python") {
            Write-Host "Python is already installed: $pythonVersion" -ForegroundColor Green
            $response = Read-Host "Do you want to reinstall Python? (y/N)"
            if ($response -ne 'y' -and $response -ne 'Y') {
                $pythonInstalled = $true
            }
        }
    }
    catch {
        Write-Host "Python not found. Will proceed with installation." -ForegroundColor Cyan
    }
    
    if (-not $pythonInstalled) {
        # Download Python installer (using Python 3.11 as a stable version)
        $pythonVersion = "3.11.9"
        $pythonUrl = "https://www.python.org/ftp/python/$pythonVersion/python-$pythonVersion-amd64.exe"
        $pythonInstaller = "$env:TEMP\python-installer.exe"
        
        if (Download-File -Url $pythonUrl -OutputPath $pythonInstaller) {
            Write-Host "Installing Python $pythonVersion..." -ForegroundColor Cyan
            Write-Host "This will add Python to PATH automatically." -ForegroundColor Cyan
            
            # Install Python with options to add to PATH
            $installArgs = "/quiet InstallAllUsers=0 PrependPath=1 Include_test=0"
            Start-Process -FilePath $pythonInstaller -ArgumentList $installArgs -Wait -NoNewWindow
            
            # Clean up installer
            Remove-Item $pythonInstaller -Force
            
            Write-Host "Python installation completed!" -ForegroundColor Green
            Write-Host "You may need to restart your terminal for PATH changes to take effect." -ForegroundColor Yellow
        }
        else {
            Write-Host "Failed to download Python installer. Please install Python manually from https://www.python.org" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "`n=== Step 1: Python Installation (SKIPPED) ===" -ForegroundColor Yellow
}

# ============================================
# 2. Install VS Code Python Extension
# ============================================
if (-not $SkipVSCodeExtension) {
    Write-Host "`n=== Step 2: VS Code Python Extension ===" -ForegroundColor Yellow
    
    # Check if VS Code is installed
    $codeCommand = Get-Command code -ErrorAction SilentlyContinue
    if ($codeCommand) {
        Write-Host "Installing Python extension for VS Code..." -ForegroundColor Cyan
        & code --install-extension ms-python.python --force
        Write-Host "Python extension installation completed!" -ForegroundColor Green
    }
    else {
        Write-Host "VS Code 'code' command not found in PATH." -ForegroundColor Red
        Write-Host "Please ensure VS Code is installed and added to PATH, or install the Python extension manually." -ForegroundColor Yellow
    }
}
else {
    Write-Host "`n=== Step 2: VS Code Python Extension (SKIPPED) ===" -ForegroundColor Yellow
}

# ============================================
# 3. Setup pip registry configuration
# ============================================
Write-Host "`n=== Step 3: pip Registry Configuration ===" -ForegroundColor Yellow

$pipConfigDir = "C:\Users\$username\pip"
$pipConfigFile = "$pipConfigDir\pip.ini"

# Create directory if it doesn't exist
if (-not (Test-Path $pipConfigDir)) {
    Write-Host "Creating pip configuration directory: $pipConfigDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $pipConfigDir -Force | Out-Null
}

# Create pip.ini file
Write-Host "Creating pip.ini configuration file..." -ForegroundColor Cyan
$pipConfig = @"
[global]
index-url = https://pip:5jXpNnQe0l450buVYKt9uvEO5Vz5Hdnmm47f3unAmHTo9GlBnpF5a40qEIOL@pypi.app.barge-master.com/simple/
"@

Set-Content -Path $pipConfigFile -Value $pipConfig -Force
Write-Host "pip.ini created at: $pipConfigFile" -ForegroundColor Green

# ============================================
# 4. Create venvs folder
# ============================================
Write-Host "`n=== Step 4: Virtual Environment Folder ===" -ForegroundColor Yellow

$venvsDir = "C:\Users\$username\Documents\venvs"

if (-not (Test-Path $venvsDir)) {
    Write-Host "Creating virtual environments directory: $venvsDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $venvsDir -Force | Out-Null
    Write-Host "Directory created successfully!" -ForegroundColor Green
}
else {
    Write-Host "Virtual environments directory already exists: $venvsDir" -ForegroundColor Green
}

# ============================================
# 5. Update VS Code settings.json
# ============================================
Write-Host "`n=== Step 5: VS Code Settings Configuration ===" -ForegroundColor Yellow

$vscodeSettingsPath = "$env:APPDATA\Code\User\settings.json"

if (Test-Path $vscodeSettingsPath) {
    Write-Host "Found VS Code settings file: $vscodeSettingsPath" -ForegroundColor Cyan
    
    try {
        # Read current settings
        $settingsContent = Get-Content $vscodeSettingsPath -Raw
        $settings = $settingsContent | ConvertFrom-Json
        
        # Update or add venvPath setting
        $venvPathValue = "C:\\Users\\$username\\Documents\\venvs"
        
        if ($settings.PSObject.Properties.Name -contains "python.venvPath") {
            $currentValue = $settings.'python.venvPath'
            Write-Host "Current python.venvPath: $currentValue" -ForegroundColor Cyan
            
            if ($currentValue -ne $venvPathValue) {
                $response = Read-Host "Do you want to update python.venvPath to $venvPathValue? (Y/n)"
                if ($response -ne 'n' -and $response -ne 'N') {
                    $settings.'python.venvPath' = $venvPathValue
                    $settings | ConvertTo-Json -Depth 100 | Set-Content $vscodeSettingsPath -Force
                    Write-Host "Updated python.venvPath in settings.json" -ForegroundColor Green
                }
                else {
                    Write-Host "Keeping existing python.venvPath setting." -ForegroundColor Yellow
                }
            }
            else {
                Write-Host "python.venvPath is already set correctly." -ForegroundColor Green
            }
        }
        else {
            # Add the setting
            $settings | Add-Member -MemberType NoteProperty -Name "python.venvPath" -Value $venvPathValue
            $settings | ConvertTo-Json -Depth 100 | Set-Content $vscodeSettingsPath -Force
            Write-Host "Added python.venvPath to settings.json" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "Error updating settings.json: $_" -ForegroundColor Red
        Write-Host "Please manually add the following to your VS Code settings:" -ForegroundColor Yellow
        Write-Host "  `"python.venvPath`": `"C:\\Users\\$username\\Documents\\venvs`"" -ForegroundColor Cyan
    }
}
else {
    Write-Host "VS Code settings file not found. Creating new settings.json..." -ForegroundColor Yellow
    
    $settingsDir = Split-Path $vscodeSettingsPath -Parent
    if (-not (Test-Path $settingsDir)) {
        New-Item -ItemType Directory -Path $settingsDir -Force | Out-Null
    }
    
    $newSettings = @{
        "python.venvPath" = "C:\\Users\\$username\\Documents\\venvs"
    }
    
    $newSettings | ConvertTo-Json -Depth 100 | Set-Content $vscodeSettingsPath -Force
    Write-Host "Created settings.json with python.venvPath configuration" -ForegroundColor Green
}

# ============================================
# Summary
# ============================================
Write-Host "`n=== Setup Complete ===" -ForegroundColor Green
Write-Host "`nConfiguration Summary:" -ForegroundColor Yellow
Write-Host "  - Python: Installed (if not skipped)" -ForegroundColor Cyan
Write-Host "  - VS Code Python Extension: Installed (if not skipped)" -ForegroundColor Cyan
Write-Host "  - pip config: $pipConfigFile" -ForegroundColor Cyan
Write-Host "  - venvs folder: $venvsDir" -ForegroundColor Cyan
Write-Host "  - VS Code settings: Updated" -ForegroundColor Cyan

Write-Host "`nNext Steps:" -ForegroundColor Yellow
Write-Host "  1. Restart your terminal/PowerShell to ensure PATH changes take effect" -ForegroundColor White
Write-Host "  2. Restart VS Code to load the new settings" -ForegroundColor White
Write-Host "  3. Create a virtual environment: python -m venv $venvsDir\PyBM" -ForegroundColor White
Write-Host "  4. Activate the environment: $venvsDir\PyBM\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  5. Install PyBM: pip install pybm" -ForegroundColor White

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
