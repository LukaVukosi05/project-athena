# Starts an isolated local auth database. Never overwrites the normal .env/database.
$ErrorActionPreference = 'Stop'
$AthenaRoot = Split-Path -Parent $PSScriptRoot
$AthenaBackend = Join-Path $AthenaRoot 'backend'
$env:ATHENA_BILLING_TEST_MODE = 'true'
$AthenaSecretFile = Join-Path $AthenaBackend '.env.auth-test-secret'
if (!(Test-Path $AthenaSecretFile)) {
    $AthenaSecret = & python -c "import secrets; print(secrets.token_urlsafe(48))"
    if ($LASTEXITCODE -ne 0) { throw 'Could not generate the local test secret.' }
    [System.IO.File]::WriteAllText($AthenaSecretFile, $AthenaSecret.Trim())
}
$env:ATHENA_JWT_SECRET = [System.IO.File]::ReadAllText($AthenaSecretFile).Trim()
$env:ATHENA_DATABASE_URL = 'sqlite:///' + ((Join-Path $AthenaBackend 'athena-auth-test.db') -replace '\\', '/')
$env:ATHENA_ENVIRONMENT = 'development'
$env:ATHENA_COOKIE_SECURE = 'false'
$env:ATHENA_PUBLIC_BASE_URL = 'http://127.0.0.1:8000'
Push-Location $AthenaBackend
try {
    & python (Join-Path $PSScriptRoot 'migrate_database.py')
    if ($LASTEXITCODE -ne 0) { throw 'Database migration failed. Server was not started.' }
    Write-Host 'Open http://127.0.0.1:8000/login.html. Use this exact host in every tab.'
    Write-Host 'Database: backend/athena-auth-test.db. Ctrl+C stops the server.'
    & python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --no-access-log
} finally { Pop-Location }
