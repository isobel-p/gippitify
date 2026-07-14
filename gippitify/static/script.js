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

document.getElementById("copy")?.addEventListener("click", async function() {
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

document.getElementById("paste")?.addEventListener("click", async function() {
    const text = await navigator.clipboard.readText();
    if (text) {
        const textarea = document.getElementById('input');
        textarea.value = text;
        textarea.dispatchEvent(new Event('input'));
        
        const icon = document.getElementById("paste-icon");
        icon.src = "/static/tick.png";
        setTimeout(() => {
            icon.src = "/static/paste.png";
        }, 1500);
    }
});

document.getElementById("prompt")?.addEventListener("click", async function() {
    x = Math.floor(Math.random()*4); // random number from 0-3 (hopefully)
    const prompts = ["How much wood would a woodchuck chuck if a woodchuck could chuck wood?", "Bye, I hope everyone has a great summer!", "Let's create an engaging and interactive PowerPoint together.", "Hey, I found this cool website called Gippitify! You guys should check it out!"];
    
    document.getElementById('input').value = prompts[x]; 
    document.getElementById('input').dispatchEvent(new Event('input'));
})

const splash_text = [
    "Works on my machine.", 
    "Also try Gippitify!", 
    "Now with 50% more exclamation marks!!!",
    "Stay determined!",
    "macondo!!",
    "Welcome to the Amazing Digital Gippitify!"]
document.getElementById('splash').textContent = splash_text[Math.floor(Math.random() * splash_text.length)];