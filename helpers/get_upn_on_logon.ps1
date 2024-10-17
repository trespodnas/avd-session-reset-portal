# Capture user upn when user logs in and send to flask/API

# Toggle logging on or off
$EnableLogging = $true  # Set to $false to disable logging

$currentDir = Get-Location

$UPN = whoami /upn
$body = @{ upn = $UPN }

try {
    $response = Invoke-RestMethod -Uri http://localhost:5000/api/upn -Method Post -Body $body
    $status = "Success"
} catch {
    $status = "Failed: $_"
}

if ($EnableLogging) {
    $logFilePath = Join-Path -Path $currentDir -ChildPath "upn_log.txt"

    $logEntry = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') - UPN: $UPN, Status: $status"
    Add-Content -Path $logFilePath -Value $logEntry
}
