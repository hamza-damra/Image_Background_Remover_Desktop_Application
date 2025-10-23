# 📖 User Guide - دليل المستخدم

## Background Remover - إزالة الخلفيات

Professional desktop application for removing image backgrounds using AI.

تطبيق سطح مكتب احترافي لإزالة خلفيات الصور باستخدام الذكاء الاصطناعي.

---

## 🚀 Getting Started - البدء السريع

### Installation - التثبيت

1. **Download** the application
2. **Extract** to your preferred location
3. **Run** `BackgroundRemover.exe` (Windows) or the app file for your OS
4. On **first run**, the AI model will download automatically (~176MB)

### First Time Setup

The application will:
- Download the AI model (one-time, ~3-5 minutes)
- Create configuration folder in your user directory
- Set default preferences

---

## 🎯 Basic Workflow - سير العمل الأساسي

### 1. Add Images - إضافة الصور

**Three ways to add images:**

**Method 1: Drag & Drop** ✨ Recommended
- Drag image files or folders directly into the queue panel
- Supports: PNG, JPG, JPEG, BMP, WebP

**Method 2: Open Button**
- Click **"Open"** in toolbar
- Select one or more image files
- Click **"Open"**

**Method 3: Menu**
- Go to **File → Open Images** or **File → Open Folder**
- Browse and select

### 2. Configure Settings - ضبط الإعدادات

**Output Tab:**
- **Format**: Choose PNG, WebP, or JPG
- **Quality**: Adjust slider (1-100)
- **Background**: Select type:
  - ✅ **Transparent**: For web, design work
  - 🎨 **Color**: Choose solid color
  - 🖼️ **Image**: Replace with another image

**Canvas Size:**
- Leave at 0 for **auto** (keeps original size)
- Set custom dimensions (e.g., 1600×1600)
- Enable **"Center Object"** to center in canvas
- Add **margin** for spacing

**Quality Tab:**
- **Alpha Matting**: Better edges (slower)
- **Remove Small Objects**: Clean up noise
- **Smooth Edges**: Softer edge transition

### 3. Use Presets (Optional) - استخدام القوالب

Quick settings for common use cases:

- **Transparent - Web**: Standard PNG with transparency
- **Marketplace 1600×1600**: Perfect for e-commerce
- **White Background**: Products on white
- **Social Media Square**: 1080×1080 for Instagram/Facebook
- **Product Photography**: High-quality product shots
- **Catalog / Print**: Large format with gray background

**To apply:**
1. Go to **Presets** tab
2. Select preset from dropdown
3. Click **"Apply"**

### 4. Choose Output Directory - اختيار مجلد الحفظ

- Click **output directory** button in toolbar
- Browse to desired save location
- Your choice is remembered

### 5. Start Processing - بدء المعالجة

- Click **"Start Processing"** button
- Monitor progress in queue panel:
  - ⏳ Yellow = Processing
  - ✓ Green = Completed
  - ✗ Red = Failed
- You can **pause** or **cancel** anytime

### 6. View Results - عرض النتائج

- Completed images are saved to output directory
- Filename format: `originalname_nobg.png`
- Click any item in queue to preview

---

## ⚙️ Advanced Features - الميزات المتقدمة

### Custom Presets - القوالب المخصصة

**Save your own presets:**

1. Configure all settings as desired
2. Go to **Presets** tab
3. Click **"Save Current as Preset"**
4. Give it a name
5. Use anytime by selecting from list

**Export/Import:**
- Share presets with colleagues
- Backup your configurations

### Batch Processing Tips - نصائح المعالجة الدفعية

**For best performance:**

- Process 20-50 images at a time
- Close other memory-intensive apps
- Use presets to avoid reconfiguring
- Enable alpha matting only when needed

**Handling Large Batches (100+ images):**

1. Split into smaller batches
2. Use CLI for automated processing
3. Disable alpha matting for speed
4. Process overnight if needed

### Background Options Explained

**1. Transparent Background**
- Best for: Web, design, overlays
- Format: PNG (required for transparency)
- Use when: You need to place object on different backgrounds

**2. Solid Color Background**
- Best for: Product photos, catalogs
- Common colors:
  - White (#FFFFFF): Clean, professional
  - Gray (#CCCCCC): Subtle, modern
  - Black (#000000): Dramatic, luxury
- Click color picker to choose custom

**3. Image Background**
- Best for: Creative compositions, themed shots
- Automatically resizes background to fit
- Use high-quality backgrounds for best results

### Quality Settings Explained

**Alpha Matting** 🔬
- What: Advanced edge refinement
- When: Photos with hair, fur, or complex edges
- Trade-off: 2-3x slower processing
- Recommended: High-value images only

**Foreground/Background Thresholds**
- Lower values = more aggressive
- Adjust if edges are too soft/hard
- Default (240/10) works for most images

**Remove Small Objects** 🧹
- What: Eliminates tiny artifacts
- When: Images with noise or specks
- Minimum size: Pixels to keep (default: 100)

**Smooth Edges** ✨
- What: Softens jagged edges
- Kernel size: Strength of smoothing (1-15)
- Higher = smoother but may lose detail

**Feather Edges** 🪶
- What: Gradual transparency at edges
- Amount: Pixels to feather (0-50)
- Creates soft transition for natural look

### Canvas and Positioning

**Auto vs Custom Size:**

- **Auto (0x0)**: Keeps original dimensions
- **Custom**: Resizes to exact canvas
  - Object is scaled to fit
  - Maintains aspect ratio
  - Uses maximum available space

**Center Object:**
- ✅ Enabled: Object centered in canvas
- ❌ Disabled: Object at top-left

**Margin:**
- Space from canvas edges
- Useful for borders, frames
- Example: 50px margin on 1600×1600 = object fits in 1500×1500

---

## 🌐 Language & Interface - اللغة والواجهة

### Switching Languages

- Click language button (EN/ع) in toolbar
- Restart application to apply
- Settings and presets are preserved

### RTL Support (Arabic)

When Arabic is selected:
- Entire interface mirrors (right-to-left)
- All text aligns correctly
- Icons and controls adjust automatically

### Theme

- **Dark** (default): Easy on eyes, modern
- **Light**: Traditional, high contrast
- **Auto**: Follows system preference (future)

---

## 🖱️ Keyboard Shortcuts - اختصارات لوحة المفاتيح

| Action | Shortcut | الاختصار |
|--------|----------|-----------|
| Open Images | `Ctrl + O` | فتح صور |
| Start Processing | `Ctrl + Enter` | بدء المعالجة |
| Cancel | `Esc` | إلغاء |
| Settings | `Ctrl + ,` | الإعدادات |
| Quit | `Ctrl + Q` | خروج |
| Zoom In | `Ctrl + +` | تكبير |
| Zoom Out | `Ctrl + -` | تصغير |
| Fit to Window | `Ctrl + 0` | ملء النافذة |

---

## 🔧 Troubleshooting - حل المشاكل

### Common Issues

**1. Application won't start**
- Ensure Windows 10+ / macOS 10.15+ / Recent Linux
- Check antivirus isn't blocking
- Run as administrator (Windows)

**2. Model download fails**
- Check internet connection
- Verify firewall settings
- Try manual download (see BUILD.md)

**3. Processing is very slow**
- Disable alpha matting
- Reduce batch size
- Close other apps
- Check CPU usage in Task Manager

**4. Out of memory error**
- Process fewer images at once
- Reduce canvas size
- Close other applications
- Restart application

**5. Poor quality results**
- Enable alpha matting
- Increase smoothing
- Try different image
- Use higher resolution input

**6. Images have artifacts**
- Enable "Remove Small Objects"
- Increase minimum object size
- Apply edge smoothing

**7. Arabic text not displaying**
- Restart after language change
- Check translation files exist
- Update to latest version

### Getting Help

1. Check this guide
2. Review BUILD.md for technical issues
3. Search [GitHub Issues](https://github.com/yourusername/bgremover/issues)
4. Create new issue with:
   - Operating system
   - Steps to reproduce
   - Screenshots
   - Error messages

---

## 💡 Tips & Best Practices - نصائح وأفضل الممارسات

### For Best Results

**1. Input Images:**
- Use high resolution (1000px+ recommended)
- Ensure good lighting
- Clear subject-background contrast
- Avoid very busy backgrounds

**2. Settings:**
- Start with a preset
- Enable alpha matting for important images
- Use transparent PNG for flexibility
- Test with one image before batch

**3. Workflow:**
- Organize images in folders by type
- Use consistent naming
- Keep original files
- Create preset for each use case

**4. Performance:**
- Process similar images together
- Use CLI for recurring tasks
- Schedule large batches during breaks
- Keep application updated

### Use Case Examples

**E-commerce Products:**
```
Preset: Marketplace 1600×1600
Format: PNG
Background: Transparent or White
Canvas: 1600×1600 centered
Margin: 50-100px
```

**Social Media:**
```
Preset: Social Media Square
Format: PNG or WebP
Background: Transparent (overlay later)
Canvas: 1080×1080 centered
Feather: 2-5px for soft edges
```

**Print Catalog:**
```
Preset: Catalog / Print
Format: PNG (high quality)
Background: Light gray or white
Canvas: 2400×3000
Quality: 100%
Alpha Matting: Enabled
```

**Web Thumbnails:**
```
Format: WebP (smaller size)
Canvas: 400×400
Quality: 80-85
Background: Transparent
Fast processing (no alpha matting)
```

---

## 📋 Specifications - المواصفات

### Supported Formats

**Input:** PNG, JPG, JPEG, BMP, WebP
**Output:** PNG, WebP, JPG

### File Size Limits

- **Recommended**: Up to 4000×4000 pixels
- **Maximum**: 8000×8000 pixels (may be slow)
- **Batch**: 100+ images (split for better UX)

### System Requirements

**Minimum:**
- CPU: Dual-core 2GHz
- RAM: 4GB
- Storage: 500MB
- Display: 1280×720

**Recommended:**
- CPU: Quad-core 2.5GHz+
- RAM: 8GB+
- Storage: 1GB
- Display: 1920×1080

---

## 🔄 Updates - التحديثات

### Checking for Updates

- Visit: [GitHub Releases](https://github.com/yourusername/bgremover/releases)
- Download latest version
- Extract and replace files
- Settings are preserved automatically

### Update Process

1. Backup your custom presets (export them)
2. Download new version
3. Extract to same location (overwrite)
4. Run application
5. Import presets if needed

---

## 📝 License & Credits - الترخيص والشكر

**License:** MIT - Free for personal and commercial use

**Credits:**
- [rembg](https://github.com/danielgatis/rembg) - Background removal library
- [U²-Net](https://github.com/xuebinqin/U-2-Net) - AI model
- [PySide6](https://www.qt.io/qt-for-python) - UI framework

**Made with ❤️ for creators, designers, and developers worldwide**

**صُنع بحب ❤️ للمبدعين والمصممين والمطورين حول العالم**

---

## 📧 Contact & Support - التواصل والدعم

- **Issues**: GitHub Issues page
- **Documentation**: README.md, BUILD.md
- **Community**: Discussions tab (coming soon)

---

**Last Updated:** October 23, 2025
**Version:** 1.0.0
