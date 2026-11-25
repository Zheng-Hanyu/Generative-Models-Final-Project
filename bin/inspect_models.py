#!/usr/bin/env python3
"""Collect non-invasive model configuration and checkpoint inventory evidence."""

from collections import Counter
import hashlib
import json
from pathlib import Path

from safetensors import safe_open

ROOT = Path("/home/genai/spec_decoding_study")
TARGET = Path("/home/model/Qwen3.8-27B-FP8")
DRAFT = Path("/home/genai/models/Qwen3.8-27B-DSpark-vLLM")


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tensor_inventory(path):
    with safe_open(str(path), framework="pt", device="cpu") as handle:
        keys = list(handle.keys())
    return {
        "file": str(path),
        "size_bytes": path.stat().st_size,
        "tensor_count": len(keys),
        "first_tensor_keys": keys[:20],
        "sha256": sha256(path) if path.stat().st_size < 5 * 1024**3 else None,
    }


def target_inventory():
    config = json.loads((TARGET / "config.json").read_text())
    text_config = config.get("text_config", config)
    index_path = TARGET / "model.safetensors.index.json"
    index = json.loads(index_path.read_text())
    weight_map = index.get("weight_map", {})
    shards = sorted(set(weight_map.values()))
    mtp_keys = sorted(key for key in weight_map if "mtp" in key.lower())
    layer_types = text_config.get("layer_types", [])
    return {
        "path": str(TARGET),
        "architectures": config.get("architectures"),
        "model_type": config.get("model_type"),
        "text_model_type": text_config.get("model_type"),
        "num_hidden_layers": text_config.get("num_hidden_layers"),
        "mtp_num_hidden_layers": text_config.get("mtp_num_hidden_layers"),
        "mtp_use_dedicated_embeddings": text_config.get("mtp_use_dedicated_embeddings"),
        "layer_type_counts": dict(Counter(layer_types)),
        "quantization_config": config.get("quantization_config"),
        "index_tensor_count": len(weight_map),
        "index_shard_count": len(shards),
        "missing_index_shards": [name for name in shards if not (TARGET / name).is_file()],
        "index_mtp_tensor_count": len(mtp_keys),
        "index_mtp_key_examples": mtp_keys[:20],
        "required_tokenizer_files": {
            name: (TARGET / name).is_file()
            for name in ["tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt"]
        },
        "config_sha256": sha256(TARGET / "config.json"),
        "index_sha256": sha256(index_path),
        "mtp_checkpoint": tensor_inventory(TARGET / "mtp.safetensors"),
    }


def draft_inventory():
    config = json.loads((DRAFT / "config.json").read_text())
    return {
        "path": str(DRAFT),
        "architectures": config.get("architectures"),
        "model_type": config.get("model_type"),
        "dtype": config.get("dtype"),
        "num_hidden_layers": config.get("num_hidden_layers"),
        "num_target_layers": config.get("num_target_layers"),
        "block_size": config.get("block_size"),
        "training_block_size": config.get("training_block_size"),
        "confidence_head_enabled": config.get("enable_confidence_head"),
        "config_sha256": sha256(DRAFT / "config.json"),
        "checkpoint": tensor_inventory(DRAFT / "model.safetensors"),
    }


inventory = {"target": target_inventory(), "draft": draft_inventory()}
output = ROOT / "config" / "model_inventory.json"
output.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n")
print(json.dumps(inventory, indent=2, ensure_ascii=False))
print(f"Saved inventory to {output}")
