param(
    [string]$ProjectPath = $PSScriptRoot | Split-Path -Parent,
    [string]$EnvName = "trquant",
    [switch]$UseConda,
    [string]$PythonExe = "python",
    [string]$NodeCmd = "npm"
)

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERROR] $msg" -ForegroundColor Red }

if (-not (Test-Path $ProjectPath)) {
    Write-Err "ProjectPath not found: $ProjectPath"
    exit 1
}

Push-Location $ProjectPath

function Ensure-Command($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        Write-Err "Required command not found: $name"
        exit 1
    }
}

function Run($cmd, $useConda = $false) {
    if ($useConda) {
        & conda run -n $EnvName pwsh -c $cmd
    } else {
        pwsh -c $cmd
    }
}

Write-Info "ProjectPath: $ProjectPath"
Write-Info "EnvName: $EnvName"
Write-Info "UseConda: $UseConda"

Ensure-Command $NodeCmd

if ($UseConda) {
    Ensure-Command "conda"
    $envExists = conda env list | Select-String "^\s*$EnvName\s"
    if (-not $envExists) {
        Write-Info "Creating conda env '$EnvName' with Python 3.11..."
        conda create -y -n $EnvName python=3.11
    } else {
        Write-Info "Using existing conda env '$EnvName'."
    }

    Write-Info "Upgrading pip/setuptools/wheel..."
    conda run -n $EnvName python -m pip install --upgrade pip setuptools wheel

    Write-Info "Installing ta-lib via conda-forge..."
    conda install -y -n $EnvName -c conda-forge ta-lib

    Write-Info "Installing project requirements (without deps already satisfied)..."
    conda run -n $EnvName python -m pip install --no-cache-dir -r requirements.txt --no-deps

    Write-Info "Installing extension requirements..."
    conda run -n $EnvName python -m pip install --no-cache-dir -r extension/requirements.txt --no-deps

    $PyBin = "conda run -n $EnvName python"
    $PipBin = "conda run -n $EnvName python -m pip"
} else {
    Write-Info "Ensuring Python exists..."
    Ensure-Command $PythonExe

    $venvPath = Join-Path $ProjectPath ".venv"
    $pyPath = Join-Path $venvPath "Scripts/python.exe"
    $pipPath = Join-Path $venvPath "Scripts/pip.exe"

    if (-not (Test-Path $pyPath)) {
        Write-Info "Creating venv at $venvPath ..."
        & $PythonExe -m venv $venvPath
    } else {
        Write-Info "Using existing venv at $venvPath."
    }

    Write-Info "Upgrading pip/setuptools/wheel..."
    & $pyPath -m pip install --upgrade pip setuptools wheel

    Write-Info "Installing project requirements..."
    & $pipPath install --no-cache-dir -r requirements.txt

    Write-Info "Installing extension requirements..."
    & $pipPath install --no-cache-dir -r extension/requirements.txt

    $PyBin = "`"$pyPath`""
    $PipBin = "`"$pipPath`""
}

Write-Info "Installing Node dependencies for extension..."
Push-Location (Join-Path $ProjectPath "extension")
& $NodeCmd install

Write-Info "Compiling VS Code extension..."
& $NodeCmd run compile

Write-Info "Packaging VS Code extension via vsce..."
if (-not (Get-Command "vsce" -ErrorAction SilentlyContinue)) {
    Write-Warn "vsce not found; installing locally via npx. To install globally: npm install -g @vscode/vsce"
    & npx vsce package
} else {
    & vsce package
}
$vsix = Get-ChildItem -Filter "trquant-cursor-extension-*.vsix" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($vsix) {
    Write-Info "VSIX generated at: $($vsix.FullName)"
} else {
    Write-Warn "VSIX not generated. Check build output above."
}
Pop-Location

Write-Info "Validating key Python packages..."
if ($UseConda) {
    conda run -n $EnvName python - <<'PYCODE'
import importlib
mods = ["numpy","pandas","flask","fastapi","uvicorn","talib"]
for m in mods:
    try:
        importlib.import_module(m)
        print(f"[OK] {m}")
    except Exception as e:
        print(f"[WARN] {m} not available: {e}")
PYCODE
} else {
    pwsh -c "$PyBin - <<'PYCODE'
import importlib
mods = ['numpy','pandas','flask','fastapi','uvicorn']
for m in mods:
    try:
        importlib.import_module(m)
        print(f'[OK] {m}')
    except Exception as e:
        print(f'[WARN] {m} not available: {e}')
PYCODE"
}

Write-Info "Done. If TA-Lib failed with pip, rerun with -UseConda or install a prebuilt wheel, then re-run this script without cleaning the env."

Pop-Location







