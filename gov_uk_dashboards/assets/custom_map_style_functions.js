window.myNamespace = Object.assign({}, window.myNamespace, {  
    mapColorScaleFunctions: {  
        continuousColorScale: function(feature, context) {
            const {
                colorscale,
                colorProp,
                style,
                min,
                max
            } = context.hideout;
            const value = feature.properties[colorProp];
            const colors = Array.from(colorscale); // defensive copy
            if (value === null || value === undefined) {
                return {
                    ...style,
                    fillColor: "#b1b4b6"
                };
            }
            // Normalize value to 0-1
            const t = (value - min) / (max - min);

            // Helper: interpolate between two hex colors
            function interpolateColor(color1, color2, t) {
                const c1 = parseInt(color1.slice(1), 16);
                const c2 = parseInt(color2.slice(1), 16);
                const r = Math.round(((c2 >> 16) - (c1 >> 16)) * t + (c1 >> 16));
                const g = Math.round((((c2 >> 8) & 0xFF) - ((c1 >> 8) & 0xFF)) * t + ((c1 >> 8) & 0xFF));
                const b = Math.round(((c2 & 0xFF) - (c1 & 0xFF)) * t + (c1 & 0xFF));
                return `rgb(${r},${g},${b})`;
            }

            // Find segment and interpolate
            const n = colors.length - 1;
            const idx = Math.min(Math.floor(t * n), n - 1);
            const local_t = (t * n) - idx;
            const fillColor = interpolateColor(colors[idx], colors[idx + 1], local_t);

            return {
                ...style,
                fillColor: fillColor
            };
        },
        discreteColorScale: function(feature, context) {
            const {
                colorscale,  // e.g., ["#d7191c", "#fdae61", "#abdda4", "#2b83ba"]
                colorProp,   // e.g., "category"
                style,
                min          // e.g., 1
            } = context.hideout;
        
            const value = feature.properties[colorProp];
            const colors = Array.from(colorscale); // ensure no mutation
        
            if (value === null || value === undefined) {
                return {
                    ...style,
                    fillColor: "#b1b4b6"  // default gray
                };
            }
        
            // Convert value to zero-based index
            const idx = value - min;
        
            // Defensive check
            const fillColor = colors[idx] || "#b1b4b6";
        
            return {
                ...style,
                fillColor: fillColor
            };
        }
    },
    mapExportFunctions: {
        setupDownloadMapButton: function(buttonId, mapContainerId, cropPixels = 300) {
            function waitForDownloadButtons() {
                const buttons = document.querySelectorAll("button[id*='-map']");

                if (buttons.length === 0) {
                    console.warn("No map download buttons found yet, retrying...");
                    setTimeout(waitForDownloadButtons, 200); // Wait and retry
                    return;
                }

                buttons.forEach(btn => {
                    // Avoid duplicate event listeners
                    if (btn.dataset.listenerAttached === "true") return;

                    btn.dataset.listenerAttached = "true"; // mark as attached

                    btn.addEventListener("click", (event) => {
                    const clickedButton = event.currentTarget;
                    const id = clickedButton.id;

                    const mapDiv = document.getElementById(`${id}-hidden-map-container`);
                    if (!mapDiv) {
                        alert("Map container not found");
                        return;
                    }

                    if (typeof html2canvas !== "function") {
                        alert("html2canvas is not loaded");
                        return;
                    }

                    html2canvas(mapDiv, { useCORS: true, scale: 1 }).then(originalCanvas => {
                        const cropHeight = originalCanvas.height - 300;
                        const cropWidth = originalCanvas.width;

                        const croppedCanvas = document.createElement("canvas");
                        croppedCanvas.width = cropWidth;
                        croppedCanvas.height = cropHeight;

                        const ctx = croppedCanvas.getContext("2d");

                        ctx.drawImage(
                        originalCanvas,
                        0, 0,
                        cropWidth, cropHeight,
                        0, 0,
                        cropWidth, cropHeight
                        );

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
                    });
                });
                }

                waitForDownloadButtons();
            }
        }
    
});