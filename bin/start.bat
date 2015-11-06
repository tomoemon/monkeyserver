@echo off

REM --------------------------------------------------------------------------
REM �v�ݒ�
REM Android SDK ���C���X�g�[�������f�B���N�g��

SET ANDROID_SDK_DIR=%USERPROFILE%\AppData\Local\Android\android-sdk

REM --------------------------------------------------------------------------

REM python ����Q�Ƃ��邽�߂̃J�����g�f�B���N�g��
SET CURRENT_DIR=%CD%

SET ROOT_DIR=%~dp0..
SET BIN_DIR=%ROOT_DIR%\bin
SET JAR_DIR=%ROOT_DIR%\jar

SET ANDROID_MONKEY_JAR="%ANDROID_SDK_DIR%\tools\lib\MonkeyRunnerExt.jar"

REM JAR �t�@�C�����R�s�[����
IF NOT EXIST "%ANDROID_MONKEY_JAR%" (
  COPY /B /Y "%JAR_DIR%\MonkeyRunnerExt.jar" "%ANDROID_MONKEY_JAR%"
) ELSE (
  for %%i in (%ANDROID_MONKEY_JAR%) do @set UPDATE_EXIST=%%~ti
  for %%i in ("%JAR_DIR%\MonkeyRunnerExt.jar") do @set UPDATE_NEW=%%~ti

  IF "%UPDATE_NEW%" GTR "%UPDATE_EXIST%" (
    COPY /B /Y "%JAR_DIR%\MonkeyRunnerExt.jar" "%ANDROID_MONKEY_JAR%"
  )
)

"%ANDROID_SDK_DIR%\tools\monkeyrunner.bat" "%BIN_DIR%\start.py" %*
