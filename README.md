<<<<<<< HEAD
# Volcengine Image Generator Skill

这是一个用于调用火山引擎（Volcengine）Seedream 系列大模型生成图片的 Agent Skill（智能体技能）。它将火山引擎 Ark API 封装成了标准的命令行调用接口，方便各类智能体（Agent）或自动化脚本集成使用。

## 功能特性

* **多模型支持**：支持调用火山引擎 Seedream 5.0 lite、4.5、4.0、3.0 等系列图像生成模型。
* **丰富的参数控制**：支持自定义图片尺寸、参考图、生图种子、组图生成、联网搜索工具调用等。
* **标准化输出**：返回标准的 JSON 格式数据，包含生图结果链接、Token 消耗等信息。


## 目录结构

```text
volcengine-image-generator/
├── SKILL.md            # 智能体（Agent）阅读的技能描述文件
├── scripts/
│   └── generate.py     # 技能执行的核心 Python 脚本
└── README.md           # 项目说明文档
```

## 依赖与安装

1. **安装 Python 依赖**：
   本技能依赖于火山引擎官方 Python SDK 以及环境变量加载工具：
   ```bash
   pip install 'volcengine-python-sdk[ark]' python-dotenv
   ```

2. **配置环境变量**：
   在项目根目录创建一个 `.env` 文件，或者直接在系统环境变量中配置您的火山引擎 API Key：
   ```env
   ARK_API_KEY=your_api_key_here
   ```

## 使用方法

此技能通过命令行调用 `scripts/generate.py`，并将包含请求参数的 JSON 字符串作为唯一参数传入。

### 命令行示例

```bash
python scripts/generate.py '{"model": "doubao-seedream-5-0-260128", "prompt": "一只可爱的卡通小狗，在赛博朋克城市奔跑，4k分辨率", "size": "2048x2048"}'
```

### 参数说明

| 参数名 | 类型 | 是否必填 | 描述说明 |
|-----------|------|----------|-------------|
| `model` | string | **是** | 模型接入点 ID 或模型名称（如 `doubao-seedream-5-0-260128` 或 `ep-xxx`）。 |
| `prompt` | string | **是** | 用于生成图像的提示词。 |
| `image` | string/array | 否 | 参考图片 URL 或 Base64 编码（图生图）。 |
| `size` | string | 否 | 图像尺寸（如 `2048x2048`）。 |
| `seed` | integer | 否 | 随机数种子（如 `-1`）。 |
| `tools` | array | 否 | 启用的工具列表，如联网搜索 `[{"type": "web_search"}]`。 |
| `response_format` | string | 否 | 返回格式：`url`（下载链接，默认）或 `b64_json`（Base64编码）。 |

*更多参数详情及模型限制，请参考 [SKILL.md](./SKILL.md) 中的详细定义。*

## ⚠️ 重要注意事项

### 1. 关于生成的图片链接

当 API 调用成功且 `response_format` 为 `url`（默认值）时，API 将返回包含签名的图片下载链接。**处理此链接时请严格遵守以下规则**：

- **原样返回，禁止多余处理**：返回的图片 URL（例如包含大量鉴权参数的长链接或 `lf-ark-images-sign.volces.com` 格式的短链接）是完整的防盗链签名网址。**绝对不要**对生成的 URL 进行任何截断、拼接、URL 解码/编码或多余的字符串处理，否则会导致签名失效、图片无法访问。
- **直接使用链接下载或展示**：该链接是一个标准的 HTTP/HTTPS 图片资源，用户可以直接点击在浏览器中打开，程序也可以直接使用该链接通过代码（如 `requests.get`、`urllib` 等工具）下载图片。
- **格式化输出注意**：由于签名 URL 极长且包含大量特殊字符（如 `&`, `%`），如果在 Markdown 或其他文档中渲染展示，建议直接以纯文本或代码块形式提供，避免 Markdown 解析器将其截断或错误转义。

### 2. 调用等待与 Token 消耗

- **耐心等待，避免重复调用**：由于调用远程大模型 API 生成图片需要一定的计算时间（通常为几秒到几十秒不等，具体取决于模型负载和网络情况），在脚本执行期间请保持耐心。**在等待时间较长时，请勿轻易强行中断并重新运行脚本**，否则会造成重复生成，导致不必要的 API Token 消耗和费用浪费。

## 错误处理

如果调用失败，脚本会向标准错误流（`stderr`）输出带有 `"error"` 键的 JSON 错误信息，并以非零状态码退出，方便调用方捕获处理。
=======
# volcengine-image-generator
>>>>>>> f043f21003e281675453a3681e20e3bfe3a90f9a
