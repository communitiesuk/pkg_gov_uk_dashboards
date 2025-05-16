const script = document.createElement("script");
script.src = "https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js";
script.onload = () => console.log("html2canvas loaded");
document.head.appendChild(script);