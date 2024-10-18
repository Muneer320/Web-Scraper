async function getSrcs(srcs) {
    let imgs = document.getElementsByTagName("img");
    for (var i = 0; i < imgs.length; i++) {
        srcs.push(imgs[i].src);
    }

    let scrollHeight = document.documentElement.scrollHeight;
    let currentPosition = 0;
    
    while (currentPosition < scrollHeight) {
        window.scrollTo(0, currentPosition);
        await new Promise(resolve => setTimeout(resolve, 1500));
    
        const images = document.querySelectorAll('div.vbI img');
        images.forEach(img => {
            const src = img.getAttribute('data-src') || img.getAttribute('src');
            if (src && !srcs.includes(src)) {
                srcs.push(src);
            }
        });
    
        currentPosition += window.innerHeight;
        scrollHeight = document.documentElement.scrollHeight;
    }

    return [...new Set(srcs)];
}
