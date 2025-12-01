import json
import hmac
import hashlib

SECRET_KEY = "your_secret_key_here"

payload = {
    "amount": "<string>",
    "comment": "<string>",
    "currency": "<string>",
    "invoice_commission": "<string>",
    "invoice_sum": "<string>",
    "invoice_total_sum": "<string>",
    "ipn_type": "invoice",
    "merchant": "<string>",
    "merchant_id": "<string>",
    "order_name": "<string>",
    "order_number": "<string>",
    "pending_amount": "<string>",
    "psys_cid": "<string>",
    "qr_code": "<string>",
    "source_amount": "<string>",
    "source_currency": "<string>",
    "source_rate": "<string>",
    "status": "new",
    "tx_urls": "null",
    "txn_id": "<string>",
    "wallet_hash": "<string>",
    "verify_hash": "<verify_hash_from_plisio>"
}

def generate_verify_hash(secret, data: dict) -> str:
    data = data.copy()
    data.pop("verify_hash", None)

    ordered_items = sorted(data.items(), key=lambda x: x[0])
    ordered_dict = {k: v for k, v in ordered_items}

    json_str = json.dumps(
        ordered_dict,
        ensure_ascii=False,
        separators=(',', ':')
    )

    signature = hmac.new(
        secret.encode("utf-8"),
        json_str.encode("utf-8"),
        hashlib.sha1
    ).hexdigest()

    return signature, json_str

verify_hash, json_str = generate_verify_hash(SECRET_KEY, payload)

print("用于签名的 JSON 串：")
print(json_str)
print("\n计算得到的 verify_hash:", verify_hash)
print("日志中的 verify_hash:", payload.get("verify_hash"))
