@echo off

REM --------------------------------------------------------------------------
REM 要設定
REM Android SDK をインストールしたディレクトリ

SET ANDROID_SDK_DIR=%USERPROFILE%\AppData\Local\Android\android-sdk

REM --------------------------------------------------------------------------

REM python から参照するためのカレントディレクトリ
SET CURRENT_DIR=%CD%

SET ROOT_DIR=%~dp0..
SET BIN_DIR=%ROOT_DIR%\bin
SET JAR_DIR=%ROOT_DIR%\jar

SET ANDROID_MONKEY_JAR="%ANDROID_SDK_DIR%\tools\lib\MonkeyRunnerExt.jar"

REM JAR ファイルをコピーする
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
