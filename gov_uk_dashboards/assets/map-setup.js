window.addEventListener("load", () => {
    // Wait a little to ensure the map is rendered
    setTimeout(() => {
        const maps = document.getElementsByClassName("leaflet-container");
        if (maps.length > 0 && maps[0]._leaflet_map) {
            window.leafletMap = maps[0]._leaflet_map;
        }
    }, 1000);
});