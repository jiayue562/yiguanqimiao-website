# Hermes Agent Wrapper Script
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Prompt,
    
    [Parameter(Mandatory=$false)]
    [string]$Model = "",
    
    [Parameter(Mandatory=$false)]
    [switch]$Continue
)

$hermesExe = "C:\Users\jia'yue\.local\bin\hermes.exe"

if ($Continue) {
    # Resume last session
    & $hermesExe -c 2>&1
} elseif ($Model) {
    # Specify model
    & $hermesExe -z $Prompt -m $Model 2>&1
} else {
    # Default call
    & $hermesExe -z $Prompt 2>&1
}
