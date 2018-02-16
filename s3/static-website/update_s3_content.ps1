# stop execution of the script if any error occured
$ErrorActionPreference = "Stop"


$artifact_extract_folder = ""
$s3_bucket = ''
$aws_profile = ''
$cloudfront_distribution_id = ''


aws s3 sync "$artifact_extract_folder" s3://$s3_bucket/ --delete --only-show-errors --profile $aws_profile
# aws s3 cp "$artifact_extract_folder" s3://$s3_bucket/ --recursive --profile $aws_profile
# aws cloudfront create-invalidation --distribution-id $cloudfront_distribution_id --path '/*' --profile $aws_profile
