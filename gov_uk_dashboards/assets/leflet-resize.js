function getMap() {
    const el = document.querySelector(".leaflet-container");
    return el ? el._leaflet_map : null;
}

function resizeAndFit() {
    const map = getMap();
    if (!map) return;

    // Fix broken tiles/layout after resize
    map.invalidateSize();

    // IMPORTANT: re-fit to current layers
    const bounds = map.getBounds();

    if (bounds.isValid()) {
        map.fitBounds(bounds);
    }
}

window.addEventListener("resize", resizeAndFit);
window.addEventListener("load", resizeAndFit);