from __future__ import annotations

import argparse
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from scipy.io.wavfile import write


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a synthetic Mandarin dialogue wav for pipeline testing.")
    parser.add_argument("--input", default="samples/dialogue_tts_test.txt", help="Dialogue text file.")
    parser.add_argument("--output", default="samples/dialogue_tts_test.wav", help="Output wav path.")
    parser.add_argument("--model", default=None, help="TTS model id or local path.")
    parser.add_argument("--voice-preset", default="v2/zh_speaker_1", help="Bark voice preset.")
    args = parser.parse_args()

    load_dotenv()
    os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS", "1")

    import torch
    from transformers import AutoProcessor, BarkModel, SpeechT5ForTextToSpeech, SpeechT5HifiGan, SpeechT5Tokenizer

    model_id = args.model or os.getenv("TTS_MODEL_ID", "suno/bark-small")
    text = _dialogue_to_spoken_text(Path(args.input).read_text(encoding="utf-8"))
    device = "cuda" if torch.cuda.is_available() else "cpu"

    if "speecht5" in model_id.lower():
        tokenizer = SpeechT5Tokenizer.from_pretrained(model_id)
        model = SpeechT5ForTextToSpeech.from_pretrained(model_id).to(device)
        vocoder_id = os.getenv("TTS_VOCODER_ID", "microsoft/speecht5_hifigan")
        vocoder = SpeechT5HifiGan.from_pretrained(vocoder_id).to(device)
        inputs = tokenizer(text=text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        generator = torch.Generator(device=device).manual_seed(7)
        speaker_embeddings = torch.randn((1, 512), generator=generator, dtype=torch.float32, device=device)
        speaker_embeddings = torch.nn.functional.normalize(speaker_embeddings, dim=1)
        with torch.inference_mode():
            waveform = model.generate_speech(input_ids, speaker_embeddings, vocoder=vocoder)
        sample_rate = 16000
        waveform = waveform.detach().cpu().numpy().squeeze()
    else:
        processor = AutoProcessor.from_pretrained(model_id)
        model = BarkModel.from_pretrained(model_id).to(device)
        inputs = processor(text, voice_preset=args.voice_preset, return_tensors="pt")
        inputs = {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}
        with torch.inference_mode():
            audio = model.generate(**inputs)
        sample_rate = model.generation_config.sample_rate
        waveform = audio.detach().cpu().numpy().squeeze()
    waveform = _to_int16(waveform)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    write(output_path, sample_rate, waveform)
    print(f"Wrote {output_path} ({sample_rate} Hz, {len(waveform) / sample_rate:.1f}s)")
    return 0


def _dialogue_to_spoken_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    spoken: list[str] = []
    for line in lines:
        if line.startswith("醫師：") or line.startswith("醫生："):
            spoken.append("醫師說，" + line.split("：", 1)[1])
        elif line.startswith("患者："):
            spoken.append("患者說，" + line.split("：", 1)[1])
        else:
            spoken.append(line)
    return " ".join(spoken)


def _to_int16(waveform: np.ndarray) -> np.ndarray:
    waveform = np.asarray(waveform, dtype=np.float32)
    peak = float(np.max(np.abs(waveform))) if waveform.size else 0.0
    if peak > 0:
        waveform = waveform / peak * 0.95
    return np.clip(waveform * 32767, -32768, 32767).astype(np.int16)


if __name__ == "__main__":
    raise SystemExit(main())
