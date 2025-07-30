@echo off
echo 启动PMP智能做题平台前端服务...
cd frontend

REM 检查node_modules是否存在
if not exist "node_modules" (
    echo 安装前端依赖...
    npm install
    if errorlevel 1 (
        echo 依赖安装失败，尝试清理缓存后重新安装...
        npm cache clean --force
        npm install
    )
)

REM 检查TypeScript配置
if not exist "tsconfig.json" (
    echo 创建TypeScript配置文件...
    echo {> tsconfig.json
    echo   "compilerOptions": {>> tsconfig.json
    echo     "target": "es5",>> tsconfig.json
    echo     "lib": [>> tsconfig.json
    echo       "dom",>> tsconfig.json
    echo       "dom.iterable",>> tsconfig.json
    echo       "es6">> tsconfig.json
    echo     ],>> tsconfig.json
    echo     "allowJs": true,>> tsconfig.json
    echo     "skipLibCheck": true,>> tsconfig.json
    echo     "esModuleInterop": true,>> tsconfig.json
    echo     "allowSyntheticDefaultImports": true,>> tsconfig.json
    echo     "strict": true,>> tsconfig.json
    echo     "forceConsistentCasingInFileNames": true,>> tsconfig.json
    echo     "noFallthroughCasesInSwitch": true,>> tsconfig.json
    echo     "module": "esnext",>> tsconfig.json
    echo     "moduleResolution": "node",>> tsconfig.json
    echo     "resolveJsonModule": true,>> tsconfig.json
    echo     "isolatedModules": true,>> tsconfig.json
    echo     "noEmit": true,>> tsconfig.json
    echo     "jsx": "react-jsx">> tsconfig.json
    echo   },>> tsconfig.json
    echo   "include": [>> tsconfig.json
    echo     "src">> tsconfig.json
    echo   ]>> tsconfig.json
    echo }>> tsconfig.json
)

REM 启动开发服务器
echo 启动React开发服务器...
npm start

pause 