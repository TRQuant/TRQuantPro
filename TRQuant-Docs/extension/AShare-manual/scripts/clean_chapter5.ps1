$files = Get-ChildItem '../src/pages/005_Chapter5/5.*_CN.md'
foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)"
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Remove top nav
    $content = $content -replace '(?s)<div class="page-nav">.*?</div>\s*\n?', ''
    
    # Add currentBook if missing
    if ($content -notmatch 'currentBook:') {
        $content = $content -replace '(layout: ../../layouts/Layout\.astro)\n---', '$1`ncurrentBook: theory`n---'
    }
    
    # Remove bottom nav and styles
    $content = $content -replace '(?s)\n?---\s*\n?<div class="bottom-nav">.*?</div>\s*<style>.*?</style>\s*$', ''
    
    Set-Content $file.FullName $content -NoNewline -Encoding UTF8
    Write-Host "✅ Updated: $($file.Name)"
}
Write-Host "🎉 第五章处理完成!" 
foreach ($file in $files) {
    Write-Host "Processing: $($file.Name)"
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Remove top nav
    $content = $content -replace '(?s)<div class="page-nav">.*?</div>\s*\n?', ''
    
    # Add currentBook if missing
    if ($content -notmatch 'currentBook:') {
        $content = $content -replace '(layout: ../../layouts/Layout\.astro)\n---', '$1`ncurrentBook: theory`n---'
    }
    
    # Remove bottom nav and styles
    $content = $content -replace '(?s)\n?---\s*\n?<div class="bottom-nav">.*?</div>\s*<style>.*?</style>\s*$', ''
    
    Set-Content $file.FullName $content -NoNewline -Encoding UTF8
    Write-Host "✅ Updated: $($file.Name)"
}
Write-Host "🎉 第五章处理完成!" 
 
 
 