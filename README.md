# Plisio Callback Simulator README

## 🇨🇳 中文说明

### 📌 项目简介

Plisio 官方目前没有提供 Webhook / Callback 测试功能，导致开发者无法在本地或测试环境中验证支付回调流程。本项目旨在通过脚本 **完整模拟 Plisio 回调**（含 new / pending / completed 三种状态），并生成与真实环境一致的 verify_hash，用于：

* 调试支付回调接口
* 验证后端回调逻辑
* 测试 HMAC-SHA1 签名验证
* 模拟真实 Plisio 行为

脚本可在 **非 PHP 环境** 使用，特别适用于 Python / Node.js / C# / Java 后端。

⚠ **注意：测试时需关闭（或暂时绕过）后端自主签名校验，否则验证必然失败，因为模拟环境不是真实来自 Plisio 的请求。**

---

## 🛠 使用说明

### 1. 填写 Secret Key

在脚本顶部设置你的 Plisio Secret Key：

```
SECRET_KEY = "your_secret_key_here"
```

### 2. 选择你需要模拟的回调状态

脚本提供三种基于真实日志结构的占位符模板：

* **NEW 状态**（订单刚创建、未付款）
* **PENDING 状态**（区块链已广播，但确认数未满足）
* **COMPLETED 状态**（支付完成）

你可以按照测试需求，将其中一个 payload 粘贴到脚本的 payload 区域，并补充必要字段。

### 3. 运行脚本生成签名

```
python plisio.py
```

运行后脚本将输出：

* 用于签名的 JSON 字符串（自动排序、移除 verify_hash）
* 计算后的 verify_hash
* 可直接用来模拟 Plisio POST 请求的 payload

### 4. 将模拟回调发送到你的测试接口

可以使用 curl/Postman：

```
curl -X POST your_callback_url \
-H "Content-Type: application/json" \
-d '{ ... 脚本生成的 JSON ... }'
```

### 5. 确认你的后端能正确处理三次变更流程

真实 Plisio 会经历：

1. **new** → 订单创建
2. **pending** → 用户已付款，等待链上确认
3. **completed** → 支付完成

你的后端应确保能正确处理三种状态。

---

## 📄 三种回调模板（占位符版）

脚本已包含以下模板，你只需要按需补充：

* NEW 状态
* PENDING 状态
* COMPLETED 状态

模板完全来自日志中的真实字段结构，可 100% 兼容你的生产环境。

---

## ⚠ 重要注意事项

### 1. 本脚本生成的 verify_hash 与 Plisio 算法完全一致

只要 Secret Key 正确，你就能得到与 Plisio 回调相同的签名。

### 2. 测试必须临时关闭二次校验

因为模拟请求不是 Plisio 服务器发送的，你必须：

* 关闭后端 IP 白名单验证
* 暂停 header 校验（如果有）
* 暂停 request origin 校验

否则回调会被拦截。

### 3. 请勿用于生产环境

本脚本仅用于开发测试。

---

## 🇺🇸 English Version

### 📌 Overview

Plisio currently does **not** provide a webhook testing function. This makes it difficult for developers to test their callback logic locally or in any development environment.

This project provides a script that **fully simulates Plisio callback behavior**, including new / pending / completed states, generating real HMAC-SHA1 signatures identical to Plisio’s format.

Useful for:

* Testing your callback API
* Validating backend payment logic
* Simulating blockchain confirmation flow
* Reproducing real Plisio behavior in non‑PHP environments

⚠ **Important: During testing, disable your backend’s internal signature validation. Simulated requests are not from Plisio servers.**

---

## 🛠 How to Use

### 1. Set Your Secret Key

```
SECRET_KEY = "your_secret_key_here"
```

### 2. Choose a callback state to simulate

The script includes placeholder templates based on your real production logs:

* **NEW** – invoice created, no payment yet
* **PENDING** – transaction broadcast, waiting for confirmations
* **COMPLETED** – payment fully confirmed

Fill the payload with your test data.

### 3. Run the script

```
python plisio.py
```

You will receive:

* The JSON string used for signature generation
* The calculated verify_hash
* A ready-to-send mock callback payload

### 4. Send the mock callback

```
curl -X POST your_callback_url \
-H "Content-Type: application/json" \
-d '{ ... JSON from script ... }'
```

### 5. Verify your backend logic

Plisio callback flow:

1. **new** → invoice created
2. **pending** → payment broadcast to blockchain
3. **completed** → payment confirmed

Ensure your backend properly handles all three states.

---

## ⚠ Important Notes

### 1. verify_hash is fully compatible with Plisio

The script follows the exact same logic: sorted JSON, HMAC-SHA1, secret key.

### 2. Disable backend security checks during testing

Mock callbacks are not sent from Plisio servers. Disable temporarily:

* IP whitelist
* Header verification
* Origin/domain checks

### 3. Not for production use

This tool is for development/testing only.

---

## ✔ Done
