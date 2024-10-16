$BaseDir = "C:\Program Files\avd-reset-portal"
$tempDir = "C:\Windows\Temp\"
$tempGitRepo = "C:\Windows\Temp\avd-reset-portal\"
$gitRepoUrl = "https://github.com/trespodnas/avd-session-reset-portal.git"
$logFile = Join-Path -Path $PSScriptRoot -ChildPath "avd-reset-portal-install.log"
$MANAGED_IDENTITY_CLIENT_ID = ""
$AZURE_SUBSCRIPTION_ID = ""
$AZURE_RESOURCE_GROUP_NAME = ""

<#
AVD Reset portal install script.
Set the global variables above: lines 6-8, prior to running the script.

This script depends on python and git already being installed on the target windows 11 virtual machine via
some other build process.
#>

Start-Transcript -Path $logFile -Append


<#
Create needed directories for install
#>

function Create-Directory {
    param (
        [string]$Path
    )

    try {
        if (-Not (Test-Path -Path $Path)) {
            New-Item -Path ${Path} -ItemType Directory -Force
            Write-Host "Directory created: ${Path}"
        } else {
            Write-Host "Directory already exists: ${Path}"
        }
    } catch {
        Write-Host "Error creating directory ${Path}: $_"
    }
}
try {
    Create-Directory -Path $BaseDir

    $settingsDir = "$BaseDir\avd-remote-app-settings"
    Create-Directory -Path $settingsDir

    $iconDir = "$settingsDir\icon"
    Create-Directory -Path $iconDir

    $scriptsDir = "$settingsDir\scripts"
    Create-Directory -Path $scriptsDir

    Write-Host "All directories created successfully."
} catch {
    Write-Host "An error occurred in the script: $_"
}


<#
Create persistent environment variables for avd-reset-portal application
#>


function Set-EnvVar {
    param (
        [string]$Name,
        [string]$Value
    )

    try {
        cmd.exe /c "setx $Name $Value /M" | Out-Null
        Write-Host "Successfully set $Name to $Value."
    } catch {
        Write-Host "Failed to set $Name. Error: $_"
    }
}

Set-EnvVar "MANAGED_IDENTITY_CLIENT_ID" $MANAGED_IDENTITY_CLIENT_ID
Set-EnvVar "AZURE_SUBSCRIPTION_ID" $AZURE_SUBSCRIPTION_ID
Set-EnvVar "AZURE_RESOURCE_GROUP_NAME" $AZURE_RESOURCE_GROUP_NAME


<#
Download sourcecode from github repository
#>


if (-Not (Test-Path -Path $tempDir)) {
    New-Item -ItemType Directory -Path $tempDir
}
Set-Location -Path $tempDir
try {
    git clone $gitRepoUrl
    Write-Host "Successfully cloned the repository."
} catch {
    Write-Host "Failed to clone the repository. Error: $_"
}


<#
Move files/directories from downloaded repository into the install directories
#>


$sourceDir = "C:\windows\Temp\avd-session-reset-portal"
$destDir = "C:\Program Files\avd-reset-portal"

$itemsToMove = @(
    "helpers",
    "static",
    "templates",
    "app.py",
    "license.txt",
    "requirements.txt"
)

$additionalFilesToMove = @{
    "C:\windows\Temp\avd-session-reset-portal\setup\images\reset-portal-remote-app-icon.png" = "C:\Program Files\avd-reset-portal\avd-remote-app-settings\icon\"
    "C:\windows\Temp\avd-session-reset-portal\setup\scripts\start-application.cmd" = "C:\Program Files\avd-reset-portal\helpers\"
    "C:\windows\Temp\avd-session-reset-portal\setup\scripts\remote-app-start-kiosk.cmd" = "C:\Program Files\avd-reset-portal\avd-remote-app-settings\scripts\"
}

function Move-ItemWithErrorHandling {
    param (
        [string]$sourcePath,
        [string]$destPath
    )
    try {
        if (Test-Path $sourcePath) {
            Move-Item -Path $sourcePath -Destination $destPath -ErrorAction Stop
            Write-Host "Successfully moved: $sourcePath to $destPath"
        } else {
            Write-Host "Source not found: $sourcePath"
        }
    } catch {
        Write-Host "Error moving ${sourcePath} to ${destPath}: $_"
    }
}

foreach ($item in $itemsToMove) {
    $sourcePath = Join-Path -Path $sourceDir -ChildPath $item
    $destPath = Join-Path -Path $destDir -ChildPath $item
    Move-ItemWithErrorHandling -sourcePath $sourcePath -destPath $destPath
}

foreach ($sourcePath in $additionalFilesToMove.Keys) {
    $destPath = $additionalFilesToMove[$sourcePath]
    Move-ItemWithErrorHandling -sourcePath $sourcePath -destPath $destPath
}

Write-Host "File move operation completed."


<#
Download nssm to the temp. directory.
This program will be used to install our .cmd script as a windows
service.
#>


$url = "https://nssm.cc/release/nssm-2.24.zip"
$destinationPath = "C:\Windows\Temp\nssm-2.24.zip"
$extractPath = "C:\Windows\Temp\nssm-2.24"

try {
    if (-not (Test-Path -Path (Split-Path -Path $destinationPath -Parent))) {
        New-Item -ItemType Directory -Path (Split-Path -Path $destinationPath -Parent) -ErrorAction Stop
    }

    Write-Host "Downloading ZIP file from $url to $destinationPath..."
    Invoke-WebRequest -Uri $url -OutFile $destinationPath -ErrorAction Stop

    if (-not (Test-Path -Path $destinationPath)) {
        throw "The ZIP file was not downloaded successfully."
    }

    if (-not (Test-Path -Path $extractPath)) {
        New-Item -ItemType Directory -Path $extractPath -ErrorAction Stop
    }

    Write-Host "Extracting ZIP file to $extractPath..."
    Expand-Archive -Path $destinationPath -DestinationPath $extractPath -Force -ErrorAction Stop

    Write-Host "Download and extraction completed successfully."

} catch {
    Write-Host "An error occurred: $_"
}


<#
Use nssm to install the .cmd file as a windows service
#>


$extractPath = "C:\Windows\Temp\nssm-2.24\nssm-2.24\win64"
$command = "nssm"
$serviceName = "avd-reset-portal"
$applicationPath = "C:\Program Files\avd-reset-portal\helpers\start-application.cmd"

try {
    Write-Host "Changing to directory: $extractPath"
    Set-Location -Path $extractPath -ErrorAction Stop

    $nssmPath = Join-Path -Path $extractPath -ChildPath "nssm.exe"
    if (-not (Test-Path -Path $nssmPath)) {
        throw "NSSM executable not found at $nssmPath."
    }

    Write-Host "Running command: $command install $serviceName '$applicationPath'"
    & $nssmPath install $serviceName $applicationPath

    Write-Host "Service '$serviceName' installed successfully."

} catch {
    Write-Host "An error occurred: $_"
}


<#
Create the python venv for the application and install
required packages using the requirements.txt file.
#>


try {
    Set-Location -Path $BaseDir -ErrorAction Stop
    Write-Host "Changed to directory: $BaseDir"
} catch {
    Write-Host "Error: Failed to change directory to $BaseDir"
    Write-Host $_.Exception.Message
    exit 1
}

try {
    Start-Process python -ArgumentList "-m venv .venv" -Wait -ErrorAction Stop
    Write-Host "Virtual environment created successfully."
} catch {
    Write-Host "Error: Failed to create virtual environment."
    Write-Host $_.Exception.Message
    exit 1
}

$activateScript = Join-Path -Path $BaseDir -ChildPath "\.venv\Scripts\Activate.ps1"
try {
    & $activateScript -ErrorAction Stop
    Write-Host "Virtual environment activated."
} catch {
    Write-Host "Error: Failed to activate virtual environment."
    Write-Host $_.Exception.Message
    exit 1
}

try {
    Start-Process pip -ArgumentList "install -r requirements.txt" -Wait -ErrorAction Stop
    Write-Host "Requirements installed successfully."
} catch {
    Write-Host "Error: Failed to install requirements."
    Write-Host $_.Exception.Message
    exit 1
}

Write-Host "Script completed successfully."


<#
Create login script for users.
This script collects the users UPN upon login and sends a POST
request to the application endpoint.
#>

$appName = "UPN Collector"
$appPath = "$BaseDir\helpers\get_upn_on_logon.ps1"
# Define the registry path for the current user
$regPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
# Add the application to the registry
Set-ItemProperty -Path $regPath -Name $appName -Value $appPath
Write-Output "Application $appName added to Windows logon."


<#
Stop logging
#>

Stop-Transcript

<#
Restart machine after setup is completed.
#>

try {
Restart-Computer -Force
} catch {
 Write-Host $_.Exception.Message
}