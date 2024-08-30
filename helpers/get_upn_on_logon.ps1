# Capture user upn when user logs in and send to flask/API
$UPN = whoami /upn
Invoke-RestMethod -Uri http://localhost:5000/api/upn -Method Post -Body @{ upn = $UPN }