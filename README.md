# 🎨 Background Remover - إزالة الخلفيات

تطبيق سطح مكتب احترافي لإزالة خلفيات الصور محليًا باستخدام الذكاء الاصطناعي، مع دعم كامل للعربية (RTL) والإنجليزية.

## ✨ الميزات

- 🖼️ **معالجة دفعات (Batch)** - معالجة 50+ صورة دفعة واحدة
- 🎯 **سحب وإفلات** - واجهة سهلة الاستخدام
- 🌐 **ثنائي اللغة** - عربي/إنجليزي مع دعم RTL كامل
- 🎨 **خيارات متعددة للخلفية** - شفافة، لون ثابت، أو صورة أخرى
- 📐 **قوالب جاهزة (Presets)** - للمتاجر الإلكترونية والمنصات
- 👁️ **معاينة مباشرة** - قبل/بعد مع شريط مقارنة
- 🌙 **وضع داكن/فاتح** - واجهة عصرية
- ⚡ **معالجة محلية بالكامل** - لا حاجة للإنترنت
- 🔄 **سجل المهام** - إعادة التصدير بنفس الإعدادات

## 🚀 التثبيت والتشغيل

### المتطلبات

- Python 3.8 أو أحدث
- 4GB RAM كحد أدنى (8GB موصى به)
- مساحة تخزين: ~500MB للنموذج والمكتبات

### خطوات التثبيت

1. **استنساخ المشروع:**
```powershell
cd "c:\Users\Hamza Damra\Documents\image manu"
```

2. **إنشاء بيئة افتراضية:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **تثبيت المكتبات:**
```powershell
pip install -r requirements.txt
```

4. **تشغيل التطبيق:**
```powershell
python -m bgremover.app.main
```

## 📦 البناء والتوزيع

### Windows (.exe)

```powershell
pyinstaller build/pyinstaller.spec
```

الملف التنفيذي سيكون في: `dist/BackgroundRemover/BackgroundRemover.exe`

### إنشاء MSI (اختياري)

```powershell
# يتطلب WiX Toolset
python build/create_msi.py
```

### macOS (.dmg)

```bash
pyinstaller build/pyinstaller_mac.spec
hdiutil create -volname "Background Remover" -srcfolder dist/BackgroundRemover.app -ov -format UDZO dist/BackgroundRemover.dmg
```

### Linux (.AppImage)

```bash
pyinstaller build/pyinstaller_linux.spec
# استخدم appimagetool لإنشاء AppImage
```

## 🎯 الاستخدام

### واجهة رسومية

1. افتح التطبيق
2. اسحب الصور أو اضغط "فتح صور"
3. اختر الإعدادات المطلوبة:
   - نوع الخلفية (شفافة/لون/صورة)
   - الحجم والهوامش
   - جودة المعالجة
4. اضغط "ابدأ المعالجة"
5. احفظ النتائج

### سطر الأوامر (CLI)

```powershell
python -m bgremover.cli --input "path/to/images" --output "path/to/output" --preset marketplace
```

**خيارات CLI:**
- `--input`: مجلد الصور المدخلة
- `--output`: مجلد الإخراج
- `--preset`: قالب جاهز (transparent, marketplace, white-bg)
- `--bg-color`: لون الخلفية (hex: #FFFFFF)
- `--size`: حجم الإخراج (width x height)
- `--lang`: اللغة (ar/en)

## 🎨 القوالب الجاهزة (Presets)

### Marketplace (1600×1600)
مثالي للمتاجر الإلكترونية والمنصات

### Transparent Web
PNG شفاف للويب

### Product White BG
خلفية بيضاء للمنتجات

### Custom Presets
يمكنك حفظ إعداداتك الخاصة

## 🧪 الاختبارات

```powershell
# تشغيل جميع الاختبارات
pytest

# اختبارات محددة
pytest tests/test_pipeline.py -v

# مع تقرير التغطية
pytest --cov=bgremover tests/
```

## 🔧 استكشاف الأخطاء

### التطبيق لا يبدأ
- تأكد من تثبيت جميع المكتبات: `pip install -r requirements.txt`
- تحقق من إصدار Python: `python --version` (يجب أن يكون 3.8+)

### النموذج لا يُحمّل
- سيتم تنزيل النموذج تلقائيًا عند أول تشغيل
- تحقق من الاتصال بالإنترنت للتنزيل الأول
- موقع النموذج: `models/u2net.onnx`

### بطء في المعالجة
- استخدم CPU متعدد النوى
- قلل عدد الصور في الدفعة
- أغلق التطبيقات الأخرى

### مشاكل في العربية/RTL
- تأكد من وجود ملفات الترجمة في `app/ui/i18n/`
- أعد تشغيل التطبيق بعد تغيير اللغة

## 📁 هيكل المشروع

```
bgremover/
├── app/                    # الكود الرئيسي
│   ├── main.py            # نقطة الدخول
│   ├── ui/                # واجهة المستخدم
│   ├── core/              # المنطق الأساسي
│   └── widgets/           # عناصر الواجهة
├── models/                # نماذج ML
├── samples/               # صور تجريبية
├── tests/                 # الاختبارات
├── build/                 # ملفات البناء
└── requirements.txt       # المكتبات المطلوبة
```

## 🤝 المساهمة

المساهمات مرحب بها! يرجى:

1. Fork المشروع
2. إنشاء فرع للميزة (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت MIT License - انظر ملف LICENSE للتفاصيل.

## 🙏 شكر وتقدير

- [rembg](https://github.com/danielgatis/rembg) - مكتبة إزالة الخلفيات
- [U²-Net](https://github.com/xuebinqin/U-2-Net) - نموذج الذكاء الاصطناعي
- [PySide6](https://www.qt.io/qt-for-python) - إطار عمل الواجهة

## 📞 الدعم

لأي استفسارات أو مشاكل، يرجى فتح Issue على GitHub.

---

صنع بـ ❤️ للمطورين والمصممين العرب
