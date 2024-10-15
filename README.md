# Avd-session-reset-portal


### About:
* A simple self-serve portal that allows avd users to disconnect/logoff their stuck sessions <br>
* Runs as a remote app in avd <br>
* Currently only scoped to be used in azure gov cloud <br>

### Requirements:
* Host pool w/one windows 10/11 multi-session vm (2x8)
* Managed identity with the following role assignment:
    * Desktop Virtualization Contributor
* Assignment of managed identity to host pool/vm(s) (user assigned)

### Setup


### TODO:
* further refinements for setup script
* error handling
* logging
* include commercial support


###### Application front page:
![AVD-session-reset-portal-main-page](setup/images/AVD-reset-portal-main-page.png)

###### Application success page:
![AVD-session-reset-portal-success-page](setup/images/AVD-session-reset-portal-success-page.png)


