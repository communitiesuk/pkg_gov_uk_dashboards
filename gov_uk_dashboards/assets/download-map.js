window.mynamespace = window.mynamespace || {};

window.mynamespace.downloadMap = function(id) {
    const mapDiv = document.getElementById(`${id}-hidden-map-container`);
    if (!mapDiv || typeof html2canvas !== "function") {
        alert("Map container not found or html2canvas not loaded");
        return;
    }

    html2canvas(mapDiv, { useCORS: true, scale: 1 }).then(originalCanvas => {
        const cropHeight = originalCanvas.height - 300;
        const cropWidth = originalCanvas.width;

        const croppedCanvas = document.createElement("canvas");
        croppedCanvas.width = cropWidth;
        croppedCanvas.height = cropHeight;

        const ctx = croppedCanvas.getContext("2d");
        ctx.drawImage(originalCanvas, 0, 0, cropWidth, cropHeight, 0, 0, cropWidth, cropHeight);

        const link = document.createElement("a");
        link.download = `${id}.png`;
        link.href = croppedCanvas.toDataURL("image/png");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }).catch(error => {
        console.error("html2canvas error:", error);
        alert("Failed to capture the map.");
    });
};
