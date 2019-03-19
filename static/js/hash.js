String.prototype.hashCode = function () {
    let hash = 0;
    if (this.length === 0) return hash;
    for (let i = 0; i < this.length; i++) {
        const char = this.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};

function update_hash(element, text) {
    element.find('.hash').val(text.trim().hashCode());
}

function update_hash_and_id(element, hash, id) {
    element.find('.id').val(id);
    element.find('.hash').val(hash);
}

function reset_hash_and_id(element) {
    element.find('.id').val("");
    element.find('.hash').val("");
}