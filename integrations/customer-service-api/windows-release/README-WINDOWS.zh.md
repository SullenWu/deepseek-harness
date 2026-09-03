# Windows 客服服务发布包

这个压缩包已经包含 Windows x64 运行文件、Python 安装包和客服 HTTP 服务源码，服务器不需要 Node.js、pnpm 或外网。

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
