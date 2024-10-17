# Avd-session-reset-portal


### About:
* A simple self-serve portal that allows avd users to disconnect/logoff their stuck sessions <br>
* Runs as a remote app in avd <br>
* Currently only scoped to be used in azure gov cloud <br>

### Requirements:
* Host pool w/one windows 11 multi-session vm (2x8)
* Python 3.12.5 & git loaded on environment (win11)
* A local GPO (gpedit.msc) must be set on host machines that kicks off the get_upn_on_logon.ps1 upon user logon.
  this can be found under: LocalGroupPolicyEditor >> "User Configuration" >> "Windows Settings" >> "Scripts (Logon/Logoff)".
  From this location you can add a "PowerShell Scripts" and point it to the installation directory where the get_upn_on_logon.ps1
  script resides; by default, the installation script puts it in: C:\Program Files\avd-reset-portal\helpers\get_upn_on_logon.ps1
  This setting could also be set via registry settings.
* Managed identity with the following role assignment:
    * Desktop Virtualization Contributor
* Assignment of managed identity to host pool/vm(s) (user assigned)

### Setup:
* Download the setup script from [here](https://raw.githubusercontent.com/trespodnas/avd-session-reset-portal/refs/heads/main/setup/setup.ps1): 
  * Open up the script & change the following variables (lines 6-8):
  * $MANAGED_IDENTITY_CLIENT_ID = ""
  * $AZURE_SUBSCRIPTION_ID = ""
  * $AZURE_RESOURCE_GROUP_NAME = ""
* Add setup script to your build process or manually run on host(s) w/elevated privileges.


### TODO:
* further refinements for setup script
* error handling
* logging
* include commercial support


###### Application front page:
![AVD-session-reset-portal-main-page](setup/images/AVD-reset-portal-main-page.png)

###### Application success page:
![AVD-session-reset-portal-success-page](setup/images/AVD-session-reset-portal-success-page.png)


