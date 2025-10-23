# Background Remover - Models Directory

This directory contains the AI models used for background removal.

## Models

### U²-Net (u2net.onnx)

- **Size**: ~176 MB
- **Format**: ONNX
- **Purpose**: Salient object detection and background removal
- **License**: Apache 2.0
- **Source**: https://github.com/danielgatis/rembg

## First Run

On the first run of the application, the U²-Net model will be automatically downloaded from GitHub releases. The download includes:

1. Model file (~176 MB)
2. SHA256 checksum verification
3. Local storage in this directory

## Manual Download

If you need to manually download the model:

```powershell
# Download from GitHub releases
$url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
Invoke-WebRequest -Uri $url -OutFile "models/u2net.onnx"
```

## Verification

The application automatically verifies the model checksum on first use. Expected SHA256:

```
60024c5c889badc19c04ad937298a77da6dc8df30476a58540a7e99dff9b74dc
```

To manually verify:

```powershell
# PowerShell
Get-FileHash -Algorithm SHA256 models/u2net.onnx
```

## Cache Location

By default, models are stored in:
- **Development**: `<project_root>/models/`
- **Production**: `<app_dir>/models/`

## Troubleshooting

### Model Download Fails

1. Check internet connection
2. Verify firewall settings
3. Try manual download (see above)

### Checksum Mismatch

1. Delete the existing model file
2. Restart the application to re-download
3. If problem persists, check for corrupted download

### Model Not Found

Ensure the `models/` directory exists and contains `u2net.onnx` or allow the application to download it on first run.

---

**Note**: The model file is not included in the repository due to its size. It will be downloaded automatically on first use.
