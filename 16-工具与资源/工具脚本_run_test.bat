@echo off
echo ============================================================
echo 🤖 知识库验证系统 - 功能完整性测试
echo ============================================================

REM 设置Python路径和脚本路径
set PYTHON_SCRIPT=%~dp0测试验证系统.py
set KB_PATH=C:/Users/jia'yue/Desktop/以观其妙书院知识库/观其妙书院

echo.
echo 📁 知识库路径: %KB_PATH%
echo 📄 测试脚本: %PYTHON_SCRIPT%
echo.

REM 检查Python是否安装
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    exit /b 1
)

REM 检查脚本文件是否存在
if not exist "%PYTHON_SCRIPT%" (
    echo ❌ 测试脚本不存在: %PYTHON_SCRIPT%
    exit /b 1
)

echo ✅ 环境检查通过
echo.

REM 运行测试脚本
echo 🧪 开始运行功能测试...
echo.

python "%PYTHON_SCRIPT%"

if %errorlevel% equ 0 (
    echo.
    echo 🎉 测试完成! 系统功能正常。
) else (
    echo.
    echo ⚠️  测试完成，但发现一些问题。
)

echo.
echo 📋 测试报告位置:
echo    知识库路径\08-工具与脚本\测试报告\
echo.

pause