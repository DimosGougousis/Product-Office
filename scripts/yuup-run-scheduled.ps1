#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Wrapper script invoked by Windows Task Scheduler for unattended YUUP runs.
  Handles budget enforcement, logging, and run trace initialization.

.DESCRIPTION
  Called by yuup-schedule.ps1 (which registers the scheduled task).
  Can also be run directly for testing with -WhatIf.

.PARAMETER Objective
  The YUUP objective to run.

.PARAMETER RunId
  Stable run identifier.

.PARAMETER RepoRoot
  Path to the Product Office repo root.

.PARAMETER MaxMinutes
  Budget cap in minutes.

.PARAMETER WhatIf
  Dry-run mode: initializes run trace but does NOT invoke YUUP.
#>

param(
    [string]$Objective,
    [string]$RunId,
    [string]$RepoRoot = "C:\Users\dimos\Product Office",
    [int]$MaxMinutes = 15,
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"

# Initialize run trace
$TraceFile = Join-Path $RepoRoot "governance" "runs" "$RunId.jsonl"

function Write-TraceLine {
    param([string]$Type, [hashtable]$Extra)
    $entry = @{
        type      = $Type
        run_id    = $RunId
        timestamp = (Get-Date -Format "o")
    }
    if ($Extra) { $Extra.GetEnumerator() | ForEach-Object { $entry[$_.Key] = $_.Value } }
    $json = $entry | ConvertTo-Json -Compress
    Add-Content -Path $TraceFile -Value $json
}

# Ensure trace directory
New-Item -ItemType Directory -Force -Path (Split-Path $TraceFile -Parent) | Out-Null

# Write run start marker
Write-TraceLine "dispatch" @{ task = "scheduled_run"; agent = "yuup"; objective = $Objective; objective_hash = (Get-Date -Format "o") }

Write-Host "===== YUUP Scheduled Run =====" -ForegroundColor Cyan
Write-Host "Run ID:    $RunId"
Write-Host "Objective: $Objective"
Write-Host "Budget:    ${MaxMinutes}min"
Write-Host "Trace:     $TraceFile"
Write-Host ""

if ($WhatIf) {
    Write-Host "== DRY-RUN MODE (WhatIf) ==" -ForegroundColor Yellow
    Write-Host "Would invoke: python .claude/skills/yuup-orchestration.md with objective"
    Write-Host "Budget cap: ${MaxMinutes}min (process would be killed if exceeded)"
    
    # Write a synthetic trace for the dry run
    Write-TraceLine "result" @{ task = "scheduled_run"; agent = "yuup"; verdict = "DRY_RUN"; score = 0; tokens = 0; latency_ms = 0 }
    Write-TraceLine "summary" @{
        run_id            = $RunId
        total_dispatches  = 0
        total_tokens      = 0
        wall_clock_ms     = 0
        final_verdict     = "DRY_RUN"
        timestamp         = (Get-Date -Format "o")
    }
    
    # Run the dashboard for this trace
    Write-Host ""
    Write-Host "Dry-run trace written. Running dashboard..."
    & python (Join-Path $RepoRoot "scripts" "yuup-dashboard.py") $RunId
    
    Write-Host ""
    Write-Host "Dry run complete. Check governance/runs/$RunId.jsonl for trace." -ForegroundColor Green
    exit 0
}

# --- Real run (not WhatIf) ---

Write-Host "Starting YUUP run with ${MaxMinutes}min timeout..."

# Build the command
$Cmd = "cd `"$RepoRoot`"; python `"$RepoRoot\scripts\yuup-workspace-init.py`" `"$RunId`""

# Invoke with timeout
$sw = [System.Diagnostics.Stopwatch]::StartNew()


$proc = Start-Process -FilePath "powershell.exe" `
    -ArgumentList "-NoProfile -Command `"$Cmd`"" `
    -PassThru `
    -WindowStyle Normal

$proc | Wait-Process -Timeout $MaxMinutes -ErrorAction SilentlyContinue
$sw.Stop()

if (-not $proc.HasExited) {
    # Budget breach — kill the process
    Write-Host "BUDGET BREACH: killing process after ${MaxMinutes}min" -ForegroundColor Red
    $proc.Kill()
    $proc.WaitForExit(5000) | Out-Null
    Write-TraceLine "budget_breach" @{ cap = "max_wall_clock"; current = ("${MaxMinutes}min") }
    Write-TraceLine "summary" @{
        total_dispatches = 0
        total_tokens     = 0
        wall_clock_ms    = $sw.ElapsedMilliseconds
        final_verdict    = "BREACHED"
        timestamp        = (Get-Date -Format "o")
    }
    exit 1
}

$exitCode = $proc.ExitCode
Write-TraceLine "summary" @{
    total_dispatches = 0
    total_tokens     = 0
    wall_clock_ms    = $sw.ElapsedMilliseconds
    final_verdict    = (if ($exitCode -eq 0) { "COMPLETE" } else { "ERROR" })
    timestamp        = (Get-Date -Format "o")
}

Write-Host ""
Write-Host "Run complete. Exit code: $exitCode" -ForegroundColor $(if ($exitCode -eq 0) { "Green" } else { "Red" })
Write-Host "Trace saved to: $TraceFile"
exit $exitCode
