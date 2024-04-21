$headers = @{
    "X-Shopify-Access-Token" = "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"
}

$url = "https://e565dd-2.myshopify.com/admin/api/2023-04/smart_collections.json"

function Get-ShopifyData {
    param(
        [string]$Url
    )

    $allCollections = @()

    do {
        try {
            $response = Invoke-WebRequest -Uri $Url -Method Get -Headers $headers
            $data = $response.Content | ConvertFrom-Json
            $allCollections += $data.smart_collections | ForEach-Object {
                [PSCustomObject]@{
                    ID = $_.id
                    Handle = $_.handle
                }
            }
            
            # Extract next page URL from Link header
            $linkHeader = $response.Headers.Link
            if ($linkHeader -and $linkHeader -match '<(https://[^>]+)>;\s*rel="next"') {
                $Url = $matches[1]
            }
            else {
                $Url = $null
            }
        }
        catch {
            Write-Host "Error: $($_.Exception.Message)"
            $Url = $null
        }
    } while ($Url)

    return $allCollections
}

# Fetch all data
$collections = Get-ShopifyData -Url $url

# Output data to CSV file
$outputFile = "Shopify_Collections.csv"
$collections | Export-Csv -Path $outputFile -NoTypeInformation

Write-Host "Data exported to $outputFile successfully."
