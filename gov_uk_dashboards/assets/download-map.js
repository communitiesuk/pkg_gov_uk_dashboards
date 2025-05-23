window.mynamespace = window.mynamespace || {};

window.mynamespace = {
  downloadMap: function(index) {
      if (typeof index !== "string") {
          console.warn("Invalid index passed to downloadMap:", index);
          return;
      }

      const buttonId = `${index}-map`;
      const mapDiv = document.getElementById(`${buttonId}-hidden-map-container`);

      if (!mapDiv) {
          alert("Map container not found");
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
  }
};
