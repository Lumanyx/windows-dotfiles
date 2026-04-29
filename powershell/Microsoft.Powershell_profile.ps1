$Env:KOMOREBI_CONFIG_HOME = 'C:\Users\me\.config\komorebi'

# Allows running Docker commands within Powershell
Function Start-WslDocker {
    wsl docker $args
}

Function Start-WslDockerCompose {
    wsl docker-compose $args
}

Set-Alias -Name docker -Value Start-WslDocker
Set-Alias -Name docker-compose -Value Start-WslDockerCompose

# Cat :3 (works best with "JetBrainsMono Nerd Font Mono")
Write-Host -ForegroundColor darkgray  ""
Write-Host -ForegroundColor darkgray  "    ／l、"
Write-Host -ForegroundColor darkgray  "  （°､ ｡７"
Write-Host -ForegroundColor darkgray  "   l   ~ヽ"
Write-Host -ForegroundColor darkgray  "   じしf_,)ノ"
Write-Host -ForegroundColor darkgray  ""

