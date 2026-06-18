; ================================================================
; 유튜브 다운로더 - Windows 설치 프로그램 스크립트
; Inno Setup 6.x 용
; ================================================================

#define MyAppName "유튜브 다운로더"
#define MyAppNameEng "YoutubeDownloader"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "myproject"
#define MyAppExeName "YoutubeDownloader.exe"
#define MyAppSourceDir "dist\YoutubeDownloader"

[Setup]
; 앱 기본 정보
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://github.com
AppSupportURL=https://github.com
AppUpdatesURL=https://github.com

; 설치 경로 (기본값: C:\Program Files\YoutubeDownloader)
DefaultDirName={autopf}\{#MyAppNameEng}
DefaultGroupName={#MyAppName}

; 설치 프로그램 출력 파일 이름 및 위치
OutputDir=Output
OutputBaseFilename=유튜브다운로더_Setup_v{#MyAppVersion}

; 압축 설정 (lzma2 = 최고 압축률)
Compression=lzma2
SolidCompression=yes

; 설치 프로그램 외관
WizardStyle=modern
WizardResizable=no

; 권한 설정 (관리자 권한 필요)
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 아키텍처
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; 최소 Windows 버전 (Windows 7 이상)
MinVersion=6.1

[Languages]
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"

[Tasks]
; 설치 옵션 체크박스
Name: "desktopicon"; Description: "바탕 화면에 바로 가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: unchecked
Name: "startmenuicon"; Description: "시작 메뉴에 바로 가기 만들기"; GroupDescription: "추가 아이콘:"; Flags: checkedonce

[Files]
; 메인 실행 파일
Source: "{#MyAppSourceDir}\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; _internal 폴더 전체 (PyInstaller 의존성)
Source: "{#MyAppSourceDir}\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 시작 메뉴 바로 가기
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenuicon
Name: "{group}\{#MyAppName} 제거"; Filename: "{uninstallexe}"; Tasks: startmenuicon

; 바탕 화면 바로 가기
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; 설치 완료 후 실행 옵션
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; 제거 시 설치 폴더까지 삭제
Type: filesandordirs; Name: "{app}"
