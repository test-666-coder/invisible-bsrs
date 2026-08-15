from __future__ import annotations

import argparse
import os

from .config import load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download configured Hugging Face models into the local cache.")
    parser.add_argument("--model", action="append", help="Extra Hugging Face model id to download.")
    args = parser.parse_args(argv)

    config = load_config()
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")
    model_ids = [config.asr_model_id, config.ner_model_id, config.emotion_model_id]
    model_ids.extend(args.model or [])

    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise SystemExit("請先安裝 requirements.txt，才能下載 Hugging Face 模型。") from exc

    for model_id in model_ids:
        print(f"Downloading {model_id} ...")
        snapshot_download(repo_id=model_id, cache_dir=config.hf_cache_dir)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
