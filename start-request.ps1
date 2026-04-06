param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$RequestSummary,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

$scriptPath = Join-Path $PSScriptRoot "tools\multiagent\lead_entrypoint.py"
python $scriptPath $RequestSummary @ExtraArgs
