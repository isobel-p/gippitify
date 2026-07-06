const textarea = document.getElementById('input');
const counter = document.getElementById('counter');

textarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';
    counter.textContent = textarea.value.length + " characters"
});