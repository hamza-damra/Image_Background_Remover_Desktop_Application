# UI Assets

This directory contains UI assets for the application.

## Icons

Place application icons here:

- `icon.png` - Main application icon (256x256 recommended)
- `icon.ico` - Windows icon file
- `icon.icns` - macOS icon file

## Creating Icons

### From PNG to ICO (Windows)

```powershell
# Using ImageMagick
magick convert icon.png -define icon:auto-resize=256,128,64,48,32,16 icon.ico
```

### From PNG to ICNS (macOS)

```bash
# Create iconset directory
mkdir icon.iconset

# Create required sizes
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png

# Create icns file
iconutil -c icns icon.iconset
```

## Recommended Icon Design

- Use a simple, recognizable symbol
- High contrast for visibility
- Transparent background
- Test at different sizes (16x16 to 512x512)

Example icon ideas:
- Scissors cutting paper
- Magic wand with sparkles
- Image with transparency grid
- Eraser removing background

## Current Status

⚠️ **Placeholder**: Add your custom icon files here.

For now, the application uses the default system icon.

---

**Tip**: Design your icon in vector format (SVG) first, then export to required formats and sizes.
