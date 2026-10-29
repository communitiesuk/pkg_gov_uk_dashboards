window.myNamespace = Object.assign({}, window.myNamespace, {
    mapColorScaleFunctions: {
        continuousColorScale: function (feature, context) {
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
    mapMarkerFunctions: {
    pointToLayer: function(feature, latlng) {
        const properties = feature.properties || {};
        const color = properties.color;

        // Preserve the original marker appearance and stacking when
        // proposed-unit information has not been supplied.
        if (
            properties.units === undefined ||
            properties.units === null
        ) {
            return L.circleMarker(latlng, {
                radius: 7,
                color: color,
                fillColor: color,
                fillOpacity: 1,
                weight: 1,
                pane: "marker-pane"
            });
        }

        const units = Number(properties.units ?? 0);

        const maturity = String(
            properties.maturity || ""
        ).trim();

        const majorSiteThreshold = Number(
            properties.major_site_threshold);

        const veryLargeSiteThreshold = Number(
            properties.very_large_site_threshold);

        const isOutline =
            maturity.toLowerCase() === "outline";

        const isPin =
            units > majorSiteThreshold;

        const pane = isPin
            ? (
                isOutline
                    ? "outline-pin-pane"
                    : "detailed-pin-pane"
            )
            : (
                isOutline
                    ? "outline-dot-pane"
                    : "detailed-dot-pane"
            );

        // Very large development: maturity-coloured pin
        // containing a white star.
        if (units > veryLargeSiteThreshold) {
            const pinIcon = L.divIcon({
                className: "major-site-pin",
                html: `
                    <div
                        style="
                            width: 24px;
                            height: 24px;
                            background-color: ${color};
                            border: 2px solid ${color};
                            border-radius: 50% 50% 50% 0;
                            transform: rotate(-45deg);
                            box-sizing: border-box;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        "
                    >
                        <span
                            style="
                                color: white;
                                font-size: 14px;
                                line-height: 1;
                                transform: rotate(45deg);
                            "
                        >
                            ★
                        </span>
                    </div>
                `,
                iconSize: [24, 24],
                iconAnchor: [12, 24],
                tooltipAnchor: [0, -24]
            });

            return L.marker(latlng, {
                icon: pinIcon,
                pane: pane
            });
        }

        // Large development: maturity-coloured pin
        // containing a dark centre.
        if (units > majorSiteThreshold) {
            const pinIcon = L.divIcon({
                className: "major-site-pin",
                html: `
                    <div
                        style="
                            width: 24px;
                            height: 24px;
                            background-color: ${color};
                            border: 2px solid ${color};
                            border-radius: 50% 50% 50% 0;
                            transform: rotate(-45deg);
                            box-sizing: border-box;
                            position: relative;
                        "
                    >
                        <div
                            style="
                                width: 7px;
                                height: 7px;
                                background-color: rgba(0, 0, 0, 0.35);
                                border-radius: 50%;
                                position: absolute;
                                top: 5.5px;
                                left: 5.5px;
                            "
                        ></div>
                    </div>
                `,
                iconSize: [24, 24],
                iconAnchor: [12, 24],
                tooltipAnchor: [0, -24]
            });

            return L.marker(latlng, {
                icon: pinIcon,
                pane: pane
            });
        }

        // Smaller development.
        return L.circleMarker(latlng, {
            radius: 4,
            color: color,
            fillColor: color,
            fillOpacity: 1,
            weight: 1,
            pane: pane
        });
    },

    onEachFeature: function(feature, layer) {
        const properties = feature.properties || {};
        const tooltip = document.createElement("div");

        Object.entries(properties.tooltip || {}).forEach(
            ([column, value]) => {
                const row = document.createElement("div");
                const label = document.createElement("strong");

                label.textContent = column + ": ";
                row.appendChild(label);
                row.appendChild(
                    document.createTextNode(String(value ?? ""))
                );

                tooltip.appendChild(row);
            }
        );

        layer.bindTooltip(tooltip, {
            pane: "tooltip-pane"
        });
    }
}
});