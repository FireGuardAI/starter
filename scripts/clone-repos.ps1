$ErrorActionPreference = 'Stop'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$repositories = @(
    @{ Name = 'fireguard-vector-store'; Url = 'https://github.com/FireGuardAI/fireguard-vector-store.git' }
    @{ Name = 'fireguard-agent-retrieval'; Url = 'https://github.com/FireGuardAI/fireguard-agent-retrieval.git' }
    @{ Name = 'fireguard-agent-compliance'; Url = 'https://github.com/FireGuardAI/fireguard-agent-compliance.git' }
    @{ Name = 'fireguard-agent-report'; Url = 'https://github.com/FireGuardAI/fireguard-agent-report.git' }
    @{ Name = 'fireguard-agent-intake'; Url = 'https://github.com/FireGuardAI/fireguard-agent-intake.git' }
    @{ Name = 'fireguard-api'; Url = 'https://github.com/FireGuardAI/fireguard-api.git' }
    @{ Name = 'fireguard-frontend'; Url = 'https://github.com/FireGuardAI/fireguard-frontend.git' }
)

foreach ($repository in $repositories) {
    $path = Join-Path $root $repository.Name
    if (Test-Path (Join-Path $path '.git')) {
        Write-Host "$($repository.Name) already exists"
    } else {
        git clone $repository.Url $path
        if ($LASTEXITCODE -ne 0) { throw "Clone failed: $($repository.Name)" }
    }
}
