$train_data = $args[0]
$valid_data = $args[1]

if ([string]::IsNullOrEmpty($valid_data)) {
    openai -k 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 api fine_tunes.create  -t $train_data -m ada:ft-personal:new-prime-2023-06-07-01-27-19  
} else {
    openai -k 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 api fine_tunes.create  -t $train_data -v $valid_data -m ada:ft-personal:new-prime-2023-06-07-01-27-19  
}
