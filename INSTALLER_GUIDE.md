# دليل بناء التطبيق وإنشاء Installer
# Building and Installer Creation Guide

**المطور / Developer:** المهندس حمزة ضمرة - Eng. Hamza Damra

---

## 📦 طرق إنشاء Installer

يوجد طريقتان لإنشاء installer للتطبيق:

### الطريقة 1: Simple Installer (موصى بها - بدون برامج إضافية) ✅

**المميزات:**
- ✅ لا يحتاج برامج خارجية
- ✅ سريع وسهل
- ✅ ملف ZIP قابل للتوزيع
- ✅ سكريبت تثبيت تلقائي

**الخطوات:**

```powershell
# 1. بناء البرنامج وإنشاء الـ installer دفعة واحدة
.\build_all.ps1

# أو بناء كل خطوة على حدة:

# 1. بناء الملف التنفيذي
.\build_exe.ps1

# 2. إنشاء حزمة التثبيت
.\create_installer_simple.ps1
```

**النتيجة:**
- `BGRemover_Setup_v1.0.0.zip` - ملف ZIP للتوزيع
- `BGRemover_Installer\` - مجلد يحتوي على الملفات

**للمستخدم النهائي:**
1. فك ضغط الـ ZIP
2. تشغيل `install.ps1` بـ PowerShell
3. اتباع التعليمات

---

### الطريقة 2: MSI Installer (احترافي - يحتاج WiX Toolset)

**المميزات:**
- ✅ ملف MSI احترافي
- ✅ تثبيت من Windows Installer
- ✅ يظهر في Add/Remove Programs
- ✅ uninstaller رسمي

**المتطلبات:**
- تثبيت WiX Toolset v3.11
- تحميل من: https://wixtoolset.org/releases/

**الخطوات:**

```powershell
# 1. بناء الملف التنفيذي
.\build_exe.ps1

# 2. إنشاء MSI
.\create_msi.ps1

# أو دفعة واحدة مع MSI:
.\build_all.ps1 -CreateMSI
```

**النتيجة:**
- `BGRemover_Setup.msi` - ملف MSI للتوزيع

**للمستخدم النهائي:**
1. تشغيل `BGRemover_Setup.msi`
2. اتباع معالج التثبيت
3. يتم التثبيت تلقائياً

---

## 🔨 شرح مفصل للخطوات

### الخطوة 1: بناء الملف التنفيذي

```powershell
.\build_exe.ps1
```

**ماذا يفعل:**
1. ينشط البيئة الافتراضية
2. يثبت PyInstaller إذا لم يكن مثبتاً
3. ينظف builds السابقة
4. يبني الملف التنفيذي من `bgremover.spec`
5. ينسخ الملفات الإضافية (README, LICENSE)
6. ينشئ مجلد models

**النتيجة:**
- `dist\BGRemover\BGRemover.exe` - الملف التنفيذي
- `dist\BGRemover\` - جميع الملفات المطلوبة

**الوقت المتوقع:** 5-10 دقائق

---

### الخطوة 2أ: Simple Installer

```powershell
.\create_installer_simple.ps1
```

**ماذا يفعل:**
1. ينشئ مجلد `BGRemover_Installer`
2. ينسخ جميع ملفات التطبيق
3. ينشئ سكريبت تثبيت `install.ps1`
4. ينشئ سكريبت إلغاء التثبيت
5. ينشئ ملف README
6. يضغط كل شيء في ZIP

**النتيجة:**
- `BGRemover_Setup_v1.0.0.zip`
- `BGRemover_Installer\` (للاختبار)

---

### الخطوة 2ب: MSI Installer

```powershell
.\create_msi.ps1
```

**ماذا يفعل:**
1. يتحقق من وجود WiX Toolset
2. ينشئ ملف `license.rtf`
3. يُترجم `installer.wxs` إلى `installer.wixobj`
4. يربط الملفات لإنشاء MSI

**النتيجة:**
- `BGRemover_Setup.msi`

---

## 📋 الملفات المستخدمة في البناء

### ملفات التكوين:

1. **bgremover.spec**
   - تكوين PyInstaller
   - يحدد الملفات والمكتبات المطلوبة
   - يحدد الأيقونة والإعدادات

2. **version_info.txt**
   - معلومات الإصدار للملف التنفيذي
   - تظهر في Properties بعد البناء

3. **installer.wxs**
   - تكوين WiX لـ MSI
   - يحدد المجلدات والاختصارات
   - UI وخيارات التثبيت

### ملفات السكريبت:

1. **build_exe.ps1**
   - بناء الملف التنفيذي

2. **create_installer_simple.ps1**
   - إنشاء ZIP installer

3. **create_msi.ps1**
   - إنشاء MSI installer

4. **build_all.ps1**
   - سكريبت شامل (الكل في واحد)

---

## 🎯 الاستخدام السريع

### للتطوير والاختبار:

```powershell
# بناء سريع واختبار
.\build_exe.ps1
.\dist\BGRemover\BGRemover.exe
```

### للتوزيع (Simple):

```powershell
# إنشاء حزمة كاملة
.\build_all.ps1
```

### للتوزيع (MSI):

```powershell
# إنشاء MSI (بعد تثبيت WiX)
.\build_all.ps1 -CreateMSI
```

### تخطي البناء (استخدام executable موجود):

```powershell
.\build_all.ps1 -SkipBuild
```

---

## 🔧 استكشاف الأخطاء

### خطأ: "PyInstaller not found"
**الحل:**
```powershell
.\venv\Scripts\Activate.ps1
pip install pyinstaller
```

### خطأ: "WiX Toolset not found"
**الحل:**
- تحميل وتثبيت من: https://wixtoolset.org/releases/
- أو استخدام Simple Installer بدلاً من ذلك

### خطأ: "Executable not found"
**الحل:**
```powershell
# إعادة البناء
.\build_exe.ps1
```

### البرنامج لا يعمل بعد البناء
**الحل:**
```powershell
# تحقق من اللوج
.\dist\BGRemover\BGRemover.exe

# أو اختبر في بيئة نظيفة
```

---

## 📦 التوزيع

### Simple Installer:

**للمطور:**
1. شارك `BGRemover_Setup_v1.0.0.zip`

**للمستخدم:**
1. فك ضغط الـ ZIP
2. انقر بزر الماوس الأيمن على `install.ps1`
3. اختر "Run with PowerShell"
4. اتبع التعليمات

### MSI Installer:

**للمطور:**
1. شارك `BGRemover_Setup.msi`

**للمستخدم:**
1. افتح الملف (double-click)
2. اتبع معالج التثبيت
3. انتهى!

---

## 📊 حجم الملفات المتوقع

- **Executable (BGRemover.exe):** ~15-20 MB
- **Complete dist folder:** ~150-200 MB
- **ZIP Installer:** ~150 MB مضغوط
- **MSI Installer:** ~150-160 MB

*ملاحظة: الحجم يعتمد على المكتبات المضمنة*

---

## 🎨 تخصيص الـ Installer

### تغيير الأيقونة:
1. ضع `icon.ico` في `bgremover\app\ui\assets\`
2. أعد البناء

### تغيير معلومات المطور:
1. عدل `version_info.txt`
2. عدل `installer.wxs` (للـ MSI)
3. أعد البناء

### إضافة ملفات:
1. عدل `bgremover.spec` (قسم `datas`)
2. أعد البناء

---

## ✅ Checklist قبل التوزيع

- [ ] اختبر البرنامج على جهازك
- [ ] تحقق من جميع الوظائف
- [ ] اختبر الـ installer
- [ ] تحقق من الاختصارات
- [ ] اختبر على جهاز نظيف (بدون Python)
- [ ] تحقق من ملفات التوثيق
- [ ] تحقق من معلومات المطور
- [ ] جرب الـ uninstaller

---

## 📞 الدعم

للمشاكل أو الأسئلة:
- راجع هذا الملف
- تحقق من الأخطاء في الـ logs
- افتح Issue على GitHub

---

**المطور / Developer:**
المهندس حمزة ضمرة
Eng. Hamza Damra

**© 2025 All Rights Reserved**
