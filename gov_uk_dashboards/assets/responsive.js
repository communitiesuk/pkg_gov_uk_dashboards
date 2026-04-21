function sendSize() {
    const size = {
        width: window.innerWidth,
        height: window.innerHeight
    };

    const store = document.getElementById("screen-size");
    if (store) {
        store.dispatchEvent(new CustomEvent("screen-resize", { detail: size }));
    }
}

// initial load
window.addEventListener("load", sendSize);

// on resize
window.addEventListener("resize", sendSize);