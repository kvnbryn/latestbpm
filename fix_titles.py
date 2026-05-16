import re
import os

titles = {
    1: "Anniversary BPM 16th",
    2: "Bina Temu Angkatan 2024",
    3: "Forum Komunikasi Ormawa BPM dan BEM",
    4: "Pelantikan 6 Maret 2025",
    5: "Rapat Kerja",
    6: "Rapat bulanan Kamis 10 Apr 2025",
    7: "Rapat bulanan Kamis 13 maret 2025"
}

def clean_title(filename):
    # Get base name without extension
    base = os.path.splitext(filename)[0]
    # Remove _IMG-... or _IMG_...
    base = re.sub(r'_(IMG|img)[\-_].*$', '', base)
    # Remove -WA...
    base = re.sub(r'-WA\d+', '', base)
    return base

# Fix index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

for i in range(1, 7):
    title = titles[i]
    
    # Replace alt text
    index_content = re.sub(
        f'(<img src="converted/kegiatan{i}\.webp" alt=")Foto Kegiatan [^"]+(")',
        f'\\1{title}\\2',
        index_content
    )
    
    # Replace h3 text
    # It might already have the right text or wrong text
    pattern = f'(<img src="converted/kegiatan{i}\\.webp".*?<h3 class="text-lg font-bold leading-tight truncate">).*?(</h3>)'
    index_content = re.sub(pattern, f'\\g<1>{title}\\2', index_content, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)


# Fix gallery.html
with open('gallery.html', 'r', encoding='utf-8') as f:
    gallery_content = f.read()

# Locate the galleryImages array
array_pattern = re.compile(r'const galleryImages = \[(.*?)\];', re.DOTALL)
match = array_pattern.search(gallery_content)
if match:
    array_content = match.group(1)
    
    # Let's rebuild the array content based on the files in converted folder
    # Or just replace the hardcoded ones and clean others
    lines = array_content.split('\n')
    new_lines = []
    for line in lines:
        if not line.strip():
             new_lines.append(line)
             continue
        
        # Extract src
        src_match = re.search(r"src:\s*'([^']+)'", line)
        if src_match:
            src = src_match.group(1)
            filename = os.path.basename(src)
            
            if filename.startswith('kegiatan') and filename.endswith('.webp'):
                idx_match = re.search(r'kegiatan(\d)\.webp', filename)
                if idx_match:
                    idx = int(idx_match.group(1))
                    if idx in titles:
                        # Replace title
                        new_line = re.sub(r"title:\s*'[^']+'", f"title: '{titles[idx]}'", line)
                        new_lines.append(new_line)
                        continue
            
            # Clean other titles
            title_match = re.search(r"title:\s*'([^']+)'", line)
            if title_match:
                old_title = title_match.group(1)
                new_title = clean_title(filename)
                new_line = re.sub(r"title:\s*'[^']+'", f"title: '{new_title}'", line)
                new_lines.append(new_line)
                continue
        
        new_lines.append(line)
        
    # Check if kegiatan4, 5, 6, 7 exist, if not add them
    # Wait, gallery.html might not have 4, 5, 6, 7. Let's list all files in converted folder and completely rebuild the array to be safe and accurate!
    
    import glob
    webp_files = glob.glob('converted/*.webp')
    
    final_images = []
    for f in webp_files:
        basename = os.path.basename(f)
        # Skip the logo and profile pics if any. Wait, the gallery should only have activities.
        # It's better to just use what was in the list, plus the missing kegiatans.
        pass

    # Actually, the user just wants to fix the titles.
    new_array_content = '\n'.join(new_lines)
    
    # If kegiatan 4, 5, 6, 7 are missing from the array, we can append them
    existing_kegiatans = re.findall(r"kegiatan(\d)\.webp", new_array_content)
    for i in range(1, 8):
        if str(i) not in existing_kegiatans:
            # Check if file exists
            if os.path.exists(f'converted/kegiatan{i}.webp'):
                new_array_content += f"\n            {{ src: 'converted/kegiatan{i}.webp', title: '{titles[i]}' }},"
    
    # remove trailing comma if any
    new_array_content = new_array_content.rstrip(',')
    
    gallery_content = gallery_content[:match.start(1)] + new_array_content + gallery_content[match.end(1):]

with open('gallery.html', 'w', encoding='utf-8') as f:
    f.write(gallery_content)

print("Titles updated.")
