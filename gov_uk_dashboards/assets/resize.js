function sendSize() {
    const size = {
        width: window.innerWidth,
        height: window.innerHeight
    };

    if (window.dash_clientside) {
        window.dash_clientside.set_props("screen-size", {
            data: size
        });
    }
}

window.addEventListener("load", sendSize);
window.addEventListener("resize", sendSize);