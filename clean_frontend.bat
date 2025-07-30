@echo off
echo 清理前端环境...
cd frontend

REM 删除node_modules
if exist "node_modules" (
    echo 删除node_modules...
    rmdir /s /q node_modules
)

REM 删除package-lock.json
if exist "package-lock.json" (
    echo 删除package-lock.json...
    del package-lock.json
)

REM 删除构建文件
if exist "build" (
    echo 删除构建文件...
    rmdir /s /q build
)

REM 清理npm缓存
echo 清理npm缓存...
npm cache clean --force

echo 清理完成！现在可以重新运行 start_frontend.bat
pause 