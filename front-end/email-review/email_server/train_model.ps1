$train_data = $args[0]
$valid_data = $args[1]

if ([string]::IsNullOrEmpty($valid_data)) {
    openai -k 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 api fine_tunes.create  -t $train_data -m ada:ft-personal:new-prime-2023-06-07-01-27-19  
} else {
    openai -k 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 api fine_tunes.create  -t $train_data -v $valid_data -m ada:ft-personal:new-prime-2023-06-07-01-27-19  
}
