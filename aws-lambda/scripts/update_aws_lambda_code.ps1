$source = "C:\Work\src"
$destination = "C:\Work\deploy\artifact.zip"

# deploy artifact is made by zipping the source folder
If(Test-path $destination) {Remove-item $destination}
Add-Type -assembly "system.io.compression.filesystem"
[io.compression.zipfile]::CreateFromDirectory($Source, $destination) 

# source code is pushed to aws function
aws lambda update-function-code --function-name my_lambda --zip-file fileb://C:/Work/deploy/artifact.zip
