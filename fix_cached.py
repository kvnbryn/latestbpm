import re

def add_cached_image_fix():
    with open('gallery.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the end of the loop
    # And add a script to check for already loaded images
    fix_script = """
        });

        // Trigger reveal for images that are already cached or loaded instantly
        setTimeout(() => {
            document.querySelectorAll('#galleryGrid img').forEach(img => {
                if (img.complete && img.classList.contains('opacity-0')) {
                    img.classList.remove('opacity-0');
                    img.classList.add('opacity-100');
                    if(img.previousElementSibling) img.previousElementSibling.classList.add('hidden');
                    if(img.nextElementSibling) img.nextElementSibling.classList.remove('opacity-0');
                }
            });
        }, 100);
"""
    
    content = content.replace("        });\n\n        // Modal Logic", fix_script + "\n        // Modal Logic")

    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Cached image fix added.")

if __name__ == "__main__":
    add_cached_image_fix()