$chapters = @(6, 7, 8, 9, 10)
$totalFiles = 0
$updatedFiles = 0

foreach ($chapter in $chapters) {
    $chapterStr = $chapter.ToString().PadLeft(3, '0')
    $pattern = "../src/pages/${chapterStr}_Chapter${chapter}/*.*_CN.md"
    $files = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    
    if ($files.Count -gt 0) {
        Write-Host "Processing Chapter $chapter ($($files.Count) files)..."
        
        foreach ($file in $files) {
            $totalFiles++
            Write-Host "  Processing: $($file.Name)"
            
            try {
                $content = Get-Content $file.FullName -Raw -Encoding UTF8
                $originalContent = $content
                
                # Remove top nav
                $content = $content -replace '(?s)<div class="page-nav">.*?</div>\s*\n?', ''
                
                # Add currentBook if missing
                if ($content -notmatch 'currentBook:') {
                    $content = $content -replace '(layout: ../../layouts/Layout\.astro)\n---', '$1`ncurrentBook: theory`n---'
                }
                
                # Remove bottom nav and styles
                $content = $content -replace '(?s)\n?---\s*\n?<div class="bottom-nav">.*?</div>\s*<style>.*?</style>\s*$', ''
                
                if ($content -ne $originalContent) {
                    Set-Content $file.FullName $content -NoNewline -Encoding UTF8
                    Write-Host "  Updated: $($file.Name)"
                    $updatedFiles++
                } else {
                    Write-Host "  No changes needed: $($file.Name)"
                }
            }
            catch {
                Write-Host "  Failed: $($file.Name) - $($_.Exception.Message)"
            }
        }
    } else {
        Write-Host "Chapter $chapter: No subsection files found"
    }
}

Write-Host ""
Write-Host "Processing Summary:"
Write-Host "   Total files: $totalFiles"
Write-Host "   Updated files: $updatedFiles"
Write-Host "Chapters 6-10 processing complete!" 
$totalFiles = 0
$updatedFiles = 0

foreach ($chapter in $chapters) {
    $chapterStr = $chapter.ToString().PadLeft(3, '0')
    $pattern = "../src/pages/${chapterStr}_Chapter${chapter}/*.*_CN.md"
    $files = Get-ChildItem $pattern -ErrorAction SilentlyContinue
    
    if ($files.Count -gt 0) {
        Write-Host "Processing Chapter $chapter ($($files.Count) files)..."
        
        foreach ($file in $files) {
            $totalFiles++
            Write-Host "  Processing: $($file.Name)"
            
            try {
                $content = Get-Content $file.FullName -Raw -Encoding UTF8
                $originalContent = $content
                
                # Remove top nav
                $content = $content -replace '(?s)<div class="page-nav">.*?</div>\s*\n?', ''
                
                # Add currentBook if missing
                if ($content -notmatch 'currentBook:') {
                    $content = $content -replace '(layout: ../../layouts/Layout\.astro)\n---', '$1`ncurrentBook: theory`n---'
                }
                
                # Remove bottom nav and styles
                $content = $content -replace '(?s)\n?---\s*\n?<div class="bottom-nav">.*?</div>\s*<style>.*?</style>\s*$', ''
                
                if ($content -ne $originalContent) {
                    Set-Content $file.FullName $content -NoNewline -Encoding UTF8
                    Write-Host "  Updated: $($file.Name)"
                    $updatedFiles++
                } else {
                    Write-Host "  No changes needed: $($file.Name)"
                }
            }
            catch {
                Write-Host "  Failed: $($file.Name) - $($_.Exception.Message)"
            }
        }
    } else {
        Write-Host "Chapter $chapter: No subsection files found"
    }
}

Write-Host ""
Write-Host "Processing Summary:"
Write-Host "   Total files: $totalFiles"
Write-Host "   Updated files: $updatedFiles"
Write-Host "Chapters 6-10 processing complete!" 
 
 
 