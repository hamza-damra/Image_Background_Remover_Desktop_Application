; Inno Setup Script for BGRemover
; This creates a professional Windows installer

#define MyAppName "BGRemover"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Eng. Hamza Damra"
#define MyAppURL "https://github.com/hamzadamra"
#define MyAppExeName "BGRemover.exe"
#define MyAppDescription "Background Removal Tool - AI Powered"

[Setup]
; App Information
AppId={{12345678-1234-5678-1234-567812345678}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppComments={#MyAppDescription}
AppCopyright=Copyright (C) 2025 {#MyAppPublisher}

; Installation Directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output Configuration
OutputDir=.
OutputBaseFilename=BGRemover_Setup_v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes

; Modern UI
WizardStyle=modern
SetupIconFile=

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Directories
SourceDir=.
OutputManifestFile=setup_manifest.txt

; Architecture
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main executable
Source: "dist\BGRemover\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; All other files from dist\BGRemover
Source: "dist\BGRemover\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Documentation
Source: "README_AR.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "CREDITS.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
