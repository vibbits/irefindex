# Default env file path
$DEFAULT_ENV_FILE = ".\terraform\irefindex.auto.tfvars"

# Function to display usage
function Show-Usage {
    Write-Host "Usage: $ScriptName [env_file]"
}

# Function to check if a file exists
function Test-FileExists {
    param (
        [string]$file
    )
    Test-Path $file -PathType Leaf
}

# Function to read and parse the env file
function Read-EnvFile {
    param (
        [string]$env_file
    )

    Get-Content $env_file | ForEach-Object {
        $key, $value = $_ -split '='
        $key = $key.Trim()
        $value = $value.Trim() -replace '^"|"$'
        switch ($key) {
            "ssh_port" { $ssh_port = $value }
            "floating_ip" { $floating_ip = $value }
        }
    }
}

# Function to remove SSH host key entry
function Remove-SSHHostKey {
    param (
        [string]$host
    )
    ssh-keygen -R $host
    Write-Host "SSH host key entry removed for $host"
}

# Default env file path
$env_file = $args[0] -or $DEFAULT_ENV_FILE

# Check if the provided or default env file exists
if (-not (Test-FileExists $env_file)) {
    Write-Host "Error: Env file not found: $env_file"
    Show-Usage
    exit 1
}

# Read and parse the env file
Read-EnvFile $env_file

# Check if required variables are set
if (-not $ssh_port -or -not $floating_ip) {
    Write-Host "Error: Missing required information in the env file."
    Show-Usage
    exit 1
}

# Remove the SSH host key entry
$host = "[${floating_ip}]:${ssh_port}"
Remove-SSHHostKey $host
