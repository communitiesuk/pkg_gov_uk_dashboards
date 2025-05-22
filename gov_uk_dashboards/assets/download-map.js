document.addEventListener("DOMContentLoaded", () => {
    function waitForButton() {
      const btn = document.getElementById("btn-download");
      if (!btn) {
        console.error("Button with id 'btn-download' not found, retrying...");
        setTimeout(waitForButton, 100); // Retry after 100ms
        return;
      }
  
      btn.addEventListener("click", () => {
        const mapDiv = document.getElementById("hidden-map-container");
        if (!mapDiv) {
          alert("Map container not found");
          return;
        }
        if (typeof html2canvas !== "function") {
          alert("html2canvas is not loaded");
          return;
        }
  
        html2canvas(mapDiv,{ useCORS: true, scale: 1 }).then(originalCanvas => {
          const cropHeight = originalCanvas.height - 300;
          const cropWidth = originalCanvas.width;

          const croppedCanvas = document.createElement("canvas");
          croppedCanvas.width = cropWidth;
          croppedCanvas.height = cropHeight;

          const ctx = croppedCanvas.getContext("2d");

          // Draw only the top portion (no scaling)
          ctx.drawImage(
            originalCanvas,
            0, 0,                     // source x, y
            originalCanvas.width, cropHeight,    // source width, height (cut off bottom)
            0, 0,                     // destination x, y
            originalCanvas.width, cropHeight     // destination size = source size (no scaling)
          );
          const link = document.createElement("a");
          link.download = "map.png";
          link.href = croppedCanvas.toDataURL("image/png");
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }).catch(error => {
          console.error("html2canvas error:", error);
          alert("Failed to capture the map.");
        });
      });
    }
  
    waitForButton();
  });
  