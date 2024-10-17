$Uri = "http://localhost:5000/api/upn"
$Timeout = 30
$RetryInterval = 2
$StartTime = Get-Date

while ($true) {
    # Re-fetch the UPN on each retry
    $UPN = whoami /upn

    try {
        $response = Invoke-RestMethod -Uri $Uri -Method Post -Body @{ upn = $UPN }
        if ($response.StatusCode -eq 200) {
            Write-Output "Successfully posted UPN."
            break
        }
    } catch {
        Write-Output "Error: $($_.Exception.Message)"
    }

    # Check if timeout is reached
    if ((Get-Date) -gt $StartTime.AddSeconds($Timeout)) {
        Write-Output "Timeout reached. Exiting."
        break
    }

    Start-Sleep -Seconds $RetryInterval
}
