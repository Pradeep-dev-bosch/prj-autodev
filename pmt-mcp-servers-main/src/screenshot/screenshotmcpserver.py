#!/usr/bin/env python3

import os
from mcp.server.fastmcp import FastMCP
from PIL import ImageGrab
import tempfile
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("screenshot")


@mcp.tool()
async def take_screenshot(save_path: str | None = None) -> str:
    """Take a screenshot of the entire screen.

    Args:
        save_path: Optional path to save the screenshot. If not provided, will save to a temp directory.
    """
    # Take the screenshot
    screenshot = ImageGrab.grab()

    # Generate filename with timestamp if no path provided
    if not save_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_dir = tempfile.gettempdir()
        save_path = os.path.join(temp_dir, f"screenshot_{timestamp}.png")

    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    # Save the screenshot
    screenshot.save(save_path)

    return f"Screenshot saved to: {save_path}"


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()  # Uses STDIO transport by default
