---
name: "volcengine-seedream-image-generator"
description: "调用火山引擎 Seedream 5.0 lite 等模型 API 生成图片。当用户要求使用火山引擎 Ark API 或着想使用大模型生成图片时调用此技能。"
---

# 火山引擎 Seedream 图片生成器 (Volcengine Seedream Image Generator)

此技能使智能体（Agent）能够使用火山引擎方舟平台（特别是 Seedream 5.0 lite、4.5、4.0 和 3.0 模型）生成图片。它将所有 API 参数封装成了一个通用的工具接口。

## 前置条件
- 必须在 `.env` 文件或环境变量中设置 `ARK_API_KEY`。
- 必须安装 `volcenginesdkarkruntime` Python 依赖包（`pip install 'volcengine-python-sdk[ark]'`）。

## 使用方法

要使用此技能，请运行提供的 Python 脚本 `scripts/generate.py`，并传入包含 API 参数的 JSON 字符串作为 Payload。

```bash
python .trae/skills/volcengine-seedream-image-generator/scripts/generate.py '<json_payload>'
```

### JSON Payload 参数说明

JSON payload 与火山引擎 Ark API 的请求体完全对应。以下是支持的参数：

| 参数名 | 类型 | 是否必填 | 描述说明 |
|-----------|------|----------|-------------|
| `model` | string | **是** | 模型 ID 或推理接入点 ID（例如：`ep-202xxxxxxxx` 或 `doubao-seedream-5-0-260128`）。此参数必须由调用者动态提供。 |
| `prompt` | string | **是** | 用于生成图像的文本提示词。 |
| `image` | string/array | 否 | 输入的参考图片 URL 或 Base64 编码，用于图生图或多图融合（`doubao-seedream-3.0-t2i` 不支持此参数）。 |
| `size` | string | 否 | 生成图像的尺寸或分辨率（例如：`2K`、`2048x2048`）。请注意不同模型的具体限制。 |
| `seed` | integer | 否 | 随机数种子 `[-1, 2147483647]`。默认值为 `-1`（仅 `doubao-seedream-3.0-t2i` 支持）。 |
| `sequential_image_generation` | string | 否 | 控制组图生成功能：`auto`（自动）或 `disabled`（关闭）。默认值为 `disabled`。 |
| `sequential_image_generation_options` | object | 否 | 组图功能的配置选项，例如：`{"max_images": 15}`。 |
| `tools` | array | 否 | 配置模型要调用的工具，例如：`[{"type": "web_search"}]` 开启联网搜索（仅 5.0-lite 支持）。 |
| `stream` | boolean | 否 | 是否开启流式输出模式。默认值为 `false`。 |
| `guidance_scale` | float | 否 | 文本权重，控制生成结果与提示词的一致性 `[1, 10]`。（仅 3.0-t2i 支持，默认值 `2.5`）。 |
| `output_format` | string | 否 | 生成图像的文件格式：`png` 或 `jpeg`。默认值为 `jpeg`（仅 5.0-lite 支持）。 |
| `response_format` | string | 否 | 返回格式：`url`（下载链接）或 `b64_json`（Base64编码）。默认值为 `url`。 |
| `watermark` | boolean | 否 | 是否在生成的图片中添加“AI生成”水印。默认值为 `true`。 |
| `optimize_prompt_options` | object | 否 | 提示词优化配置，例如：`{"mode": "standard"}` 或 `{"mode": "fast"}`。 |

## 调用示例

### 1. 简单的文生图请求

```json
{
  "model": "doubao-seedream-5-0-260128",
  "prompt": "一只可爱的卡通小狗，在赛博朋克城市奔跑，4k分辨率",
  "size": "2048x2048",
  "response_format": "url"
}
```

```bash
python .trae/skills/volcengine-seedream-image-generator/scripts/generate.py '{"model": "doubao-seedream-5-0-260128", "prompt": "一只小狗", "size": "2048x2048"}'
```

### 2. 开启联网搜索并生成组图

```json
{
  "model": "ep-xxxxxx",
  "prompt": "生成一组今天北京天气的插画",
  "sequential_image_generation": "auto",
  "sequential_image_generation_options": {"max_images": 4},
  "tools": [{"type": "web_search"}]
}
```


## 错误处理

如果发生错误，脚本会将包含 `error` 键的 JSON 格式错误信息直接输出到控制台的标准错误（stderr）中，Agent 可以捕获并处理这些信息。

## 注意事项（重要）

### 1. 返回参数与链接处理

当 API 调用成功并返回图片链接（`url`）时，**智能体（Agent）必须严格遵守以下规则**：

- **原样返回，禁止多余处理**：返回的图片 URL（无论是 `ark-acg-cn-beijing.tos...` 还是 `lf-ark-images-sign...`）是完整的防盗链签名网址。**绝对不要**对生成的 URL 进行任何截断、拼接、URL 解码/编码或多余的字符串处理，否则会导致签名失效、图片无法访问。
- **直接使用链接下载或展示**：该链接是一个标准的 HTTP/HTTPS 图片资源，用户可以直接点击在浏览器中打开，Agent 也可以直接使用该链接通过代码（如 `requests.get`、`urllib` 等工具）下载图片。
- **格式化输出注意**：由于签名 URL 极长且包含大量特殊字符（如 `&`, `%`），在 Markdown 中渲染时，建议直接以纯文本或代码块形式提供给用户，避免 Markdown 解析器截断或错误转义参数。

### 2. 调用等待与 Token 消耗

- **耐心等待，避免重复调用**：由于调用远程大模型 API 生成图片需要一定的计算时间（通常为几秒到几十秒不等，具体取决于模型负载和网络情况），在脚本执行期间请保持耐心。**在等待时间较长时，请勿轻易强行中断并重新运行脚本**，否则会造成重复生成，导致不必要的 API Token 消耗和资源浪费。
