$unformated_data = ".\train_gpt_data.json"
# Check if the file exists
if (Test-Path $unformated_data) {
    # Run the command
    openai tools fine_tunes.prepare_data -f $unformated_data
    Write-Host "Command executed successfully."
} else {
    Write-Host "File not found: $unformated_data"
}
$formated_data = $unformated_data -replace "\.json$", "_prepared_train.jsonl"
$valid_data = $unformated_data -replace "\.json$", "_prepared_valid.jsonl"

# Run the fine_tuning and store the output
$output = openai -k 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 api fine_tunes.create  -t .\$formated_data -v .\$valid_data -m ada --suffix "CollinGTK2" | ForEach-Object { $_ }
Write-Output $output > training_output.txt
Write-Output $output
# Initialize variable
$FineTuneId = $null

# Iterate over each line of output
foreach ($line in $output) {
    # Check if line contains "Created fine-tune"
    if ($line -match "Created fine-tune:") {
        # Use regex to find fine-tune ID and assign it to variable
        $FineTuneId = [regex]::match($line, '(ft-\w+)').Groups[1].Value
        break
    }
}

# Output the fine-tune ID

Write-Output $FineTuneId
openai api fine_tunes.results -i $FineTuneId > result.csv
