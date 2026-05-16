import re

def fix_gallery_loading_bug():
    with open('gallery.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # The issue is modifying innerHTML in a loop. Let's fix that.
    old_loop = """        galleryImages.forEach((imgData, index) => {
            const delay = (index % 4) * 100;
            const itemHtml = `
                <div class="break-inside-avoid group relative rounded-sm overflow-hidden shadow-md hover:shadow-2xl transition-all duration-500 cursor-pointer bg-silversand-light/40 min-h-[250px]" data-aos="zoom-in" data-aos-delay="${delay}">
                    
                    <!-- Pulsing Skeleton Background -->
                    <div class="absolute inset-0 animate-pulse bg-gray-300 z-0 skeleton-bg"></div>
                    
                    <!-- Image with onload handler for smooth reveal -->
                    <img src="${imgData.src}" alt="${imgData.title}" loading="lazy" 
                         class="relative z-10 w-full h-auto object-cover transform transition-all duration-700 group-hover:scale-105 opacity-0"
                         onload="
                            this.classList.remove('opacity-0'); 
                            this.classList.add('opacity-100'); 
                            if(this.previousElementSibling) this.previousElementSibling.classList.add('hidden'); 
                            if(this.nextElementSibling) this.nextElementSibling.classList.remove('opacity-0');
                         ">
                    
                    <!-- Permanent Overlay (Hidden until image loads) -->
                    <div class="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#1a1c14]/95 via-[#1a1c14]/60 to-transparent pt-24 pb-5 px-5 opacity-0 transition-opacity duration-700 z-20">
                        <h3 class="text-white font-bold text-lg md:text-xl leading-tight group-hover:text-army-light transition-colors duration-300 drop-shadow-md">${imgData.title}</h3>
                        <div class="w-8 h-[2px] bg-army mt-3 transform origin-left transition-all duration-500 group-hover:w-full opacity-80"></div>
                    </div>
                </div>
            `;
            galleryGrid.innerHTML += itemHtml;
        });"""

    # We need to find the actual code, since my old_loop string might not match perfectly.
    # Let's just use regex to replace `galleryGrid.innerHTML += itemHtml;`
    content = content.replace("galleryGrid.innerHTML += itemHtml;", "galleryGrid.insertAdjacentHTML('beforeend', itemHtml);")

    with open('gallery.html', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Gallery loading bug fixed by using insertAdjacentHTML.")

if __name__ == "__main__":
    fix_gallery_loading_bug()
