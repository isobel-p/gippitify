const textarea = document.getElementById('input');
const counter = document.getElementById('counter');

textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
    if (this.value.length === 0) {
        counter.textContent = ""
    } else {
        counter.textContent = textarea.value.length + " characters"
    }
    
});

document.getElementById("copy")?.addEventListener("click", function() {
    const outputDiv = document.querySelector(".output");
    if (!outputDiv) return;
    
    const clone = outputDiv.cloneNode(true);
    const button = clone.querySelector("#copy");
    if (button) button.remove();
    const text = clone.textContent.trim();
    
    if (text) {
        navigator.clipboard.writeText(text).then(() => {
            const icon = document.getElementById("copy-icon");
            if (icon) {
                icon.src = "/static/tick.png";
            }
            setTimeout(() => {
                if (icon) {
                    icon.src = "/static/copy.png";
                }
            }, 2000);
        });
    }
});