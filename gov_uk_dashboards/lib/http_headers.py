"""http_headers"""


import os
import dash


def setup_application_http_response_headers(dash_app: dash.Dash):
    """Add HTTP headers to the response"""
    server = dash_app.server

    @server.after_request
    def add_headers(response):
        content_security_policy = (
            "default-src 'self' 'unsafe-eval' 'unsafe-inline' data:"
        )
        frame_ancestors = os.environ.get("ALLOWED_FRAME_ANCESTORS")
        if frame_ancestors:
            content_security_policy += "; frame-ancestors " + frame_ancestors
        response.headers.add("Content-Security-Policy", content_security_policy)

        response.headers.add("X-Content-Type-Options", "nosniff")
        response.headers.add("Referrer-Policy", "no-referrer")
        response.headers.add("X-Frame-Options", "DENY")

        # The below header will disable all browser features for the dashboard website
        response.headers.add(
            "Permission-Policy",
            "accelerometer=(), ambient-light-sensor=(), autoplay=(), battery=(), camera=(), "
            "cross-origin-isolated=(), display-capture=(), document-domain=(), encrypted-media=()"
            ", execution-while-not-rendered=(), execution-while-out-of-viewport=(), fullscreen=(),"
            " geolocation=(), gyroscope=(), keyboard-map=(), magnetometer=(), microphone=(), "
            "midi=(), navigation-override=(), payment=(), picture-in-picture=(), "
            "publickey-credentials-get=(), screen-wake-lock=(), sync-xhr=(), usb=(), web-share=()"
            ", xr-spatial-tracking=()",
        )
        return response
