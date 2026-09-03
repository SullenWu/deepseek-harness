# Windows 客服服务发布包

这个压缩包已经包含 Windows x64 运行文件、Python 安装包和客服 HTTP 服务源码，服务器不需要 Node.js、pnpm 或外网。

## 在 Windows 上生成发布包

发布包必须在 Windows x64 电脑上构建，因为运行时包含 Windows 原生模块，不能在 macOS 上直接生成受支持的 Windows 发布包。

构建电脑需要提前准备：

- Node.js 24 x64
- Python 3.10 x64，并安装 Windows Python Launcher（`py`）
- pnpm 11.7.0
- Windows 开发者模式

在 `deepseek-harness` 项目根目录打开 PowerShell，执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-customer-service-windows-release.ps1
```

构建完成后，发布包位于：

```text
dist-customer-service-windows\deepseek-harness-customer-service-<版本号>-win-x64-exe-visible.zip
```

脚本会自动完成以下工作：

- 安装项目锁定的依赖并构建两个 Windows EXE
- 构建 Python SDK wheel 和 Windows 运行时 wheel
- 下载 Python 3.10 至 3.14 x64 的离线依赖
- 生成不会触发 Windows PowerShell 5.1 中文编码解析问题的安装和启动脚本
- 打包客服 API 集成文件、部署说明、构建信息和 SHA-256 校验文件
- 排除服务器本地的 `customer-service.model.json`，避免模型密钥进入发布包

如果依赖已经按照当前 `pnpm-lock.yaml` 完整安装，可以使用 `-SkipInstall`。只有确认 `dist-exe` 中已有当前源码构建出的两个 Windows EXE 时，才可以使用 `-SkipRuntimeBuild`。

## 首次部署

1. 安装 64 位 Python 3.10、3.11、3.12、3.13 或 3.14，并勾选安装 Python Launcher。
2. 将整个压缩包解压到固定目录，例如 `C:\webroot\kefu\_ai`。不要只复制两个 EXE。
3. 在该目录打开 PowerShell，运行：

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\install.ps1
   ```

4. 编辑 `integrations\customer-service-api\customer-service.model.json`，填写模型地址、模型名和 API Key。
5. 将产品技能完整放入 `skills`，需要只读访问的资料放入 `workspace`。
6. 启动服务：

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\start.ps1
   ```

默认监听 `127.0.0.1:8765`，存活检查地址是 `http://127.0.0.1:8765/health/live`。

## 更新

推荐使用新压缩包覆盖程序文件后，再运行一次 `install.ps1`。保留服务器自己的以下内容：

- `integrations\customer-service-api\customer-service.model.json`
- `skills`
- `workspace`
- `data\dsh-home`

只有在确认 Python SDK、HTTP 集成代码和配置协议都没有变化时，才可以只替换 `runtime` 目录里的两个 EXE。

## 文件校验

`BUILD-INFO.txt` 记录构建版本和提交；`SHA256SUMS.txt` 记录包内文件的 SHA-256，可用于确认传输后文件没有损坏。

## 会话留存清理

Harness 会话不会自动过期。先保持服务运行并执行预览，确认只匹配超过 90 天的 `customer-service-*` 会话：

```powershell
.\.venv\Scripts\python.exe integrations\customer-service-api\cleanup_sessions.py --dsh-home data\dsh-home --older-than-days 90
```

确认预览结果后停止客服服务，再执行实际清理；`--confirm-service-stopped` 是必填的安全确认：

```powershell
.\.venv\Scripts\python.exe integrations\customer-service-api\cleanup_sessions.py --dsh-home data\dsh-home --older-than-days 90 --apply --confirm-service-stopped
```

不得直接递归删除整个 `data\dsh-home`，否则所有仍需续接的客服会话都会丢失。
