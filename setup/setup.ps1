$BaseDir = "C:\Program Files\avd-reset-portal"
$ManagedClientID = "YourManagedClientID"  # Replace with your actual Managed Client ID
$ResourceGroupName = "YourResourceGroupName"  # Replace with your actual Resource Group Name


# Function to create directories with error handling
function Create-Directory {
    param (
        [string]$Path
    )

    try {
        if (-Not (Test-Path -Path $Path)) {
            New-Item -Path $Path -ItemType Directory -Force
            Write-Host "Directory created: $Path"
        } else {
            Write-Host "Directory already exists: $Path"
        }
    } catch {
        Write-Host "Error creating directory $Path: $_"
    }
}

# Main script execution
try {
    # Create base directory
    Create-Directory -Path $BaseDir

    # Create sub-directories
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
