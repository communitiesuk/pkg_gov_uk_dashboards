document.addEventListener("DOMContentLoaded", () => {
    function waitForButton() {
      const btn = document.getElementById("btn-download");
      if (!btn) {
        console.error("Button with id 'btn-download' not found, retrying...");
        setTimeout(waitForButton, 100); // Retry after 100ms
        return;
      }
  
      btn.addEventListener("click", () => {
        const mapDiv = document.getElementById("map-container");
        if (!mapDiv) {
          alert("Map container not found");
          return;
        }
        if (typeof html2canvas !== "function") {
          alert("html2canvas is not loaded");
          return;
        }
  
        html2canvas(mapDiv,{ useCORS: true }).then(canvas => {
          const link = document.createElement("a");
          link.download = "map.png";
          link.href = canvas.toDataURL("image/png");
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
  