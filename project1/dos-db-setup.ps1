$config = Get-Content -Raw -Path config.json | ConvertFrom-Json
$jsonPath = $config."pathToTweets"
$dbName = $config."dbName"
$dbCollection = $config."dbCollection"
# $jsonFileName = [io.path]::GetFileNameWithoutExtension($jsonPath)
mongoimport --db $dbName --collection $dbCollection --file $jsonPath --jsonArray
mongo db-setup.js
