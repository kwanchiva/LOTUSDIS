import os
import glob
import json
import string
import librosa
import torch
import numpy as np
import pandas as pd
from typing import List
from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration
)
from pythainlp.tokenize import word_tokenize
from jiwer import process_words, wer_default
from tqdm import tqdm
import argparse

# --------------------- Utilities ---------------------
# Load json
def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data

# Read audio function
def read_audio_to_array(
    audio_path: str,
    target_sr: int,
) -> np.ndarray:
    
    array, sr = librosa.load(path=audio_path, sr=target_sr)
    
    return array
    
# Batch transcribe function
def batch_transcribe(
    model,
    processor,
    audio_path_list: str,
    batch_size: int,
    sampling_rate: int,
    torch_dtype: torch.dtype,
    device: str
) -> List[str]:
    
    model.eval()
    transcriptions = []

    for i in tqdm(range(0, len(audio_path_list), batch_size)):
        audio_batch = audio_path_list[i : i + batch_size]
        
        array_list = [
            read_audio_to_array(audio_path, sampling_rate)
                for audio_path in audio_batch
        ]

        input_features = processor(
            array_list, 
            sampling_rate=sampling_rate, 
            return_tensors="pt"
        ).input_features
        input_features = input_features.to(torch_dtype)

        with torch.no_grad():
            output_ids = model.generate(input_features.to(device))
            output_texts = processor.batch_decode(output_ids, skip_special_tokens=True)

        transcriptions.extend(output_texts)
        
    return transcriptions
    
# Clean text funciton
def clean_text(txt: str) -> str:
    # Clean text credit by thonburian whisper (https://github.com/biodatlab/thonburian-whisper)

    # Remove zero-width and non-breaking space.
    txt = txt.replace("\u200b", " ")
    txt = txt.replace("\xa0", " ")

    # Normalize characters and correct common typing errors    
    txt = txt.replace("เเ", "แ")  
    txt = txt.replace("ํา", "ำ")
    txt = txt.replace("่ำ", "่ำ")
    txt = txt.replace("ำ้", "้ำ")
    txt = txt.replace("ํ่า", "่ำ")

    # Replace special underscore and dash
    txt = txt.replace("▁", "_")
    txt = txt.replace("—", "-")
    txt = txt.replace("–", "-")
    txt = txt.replace("−", "-")

    # Replace special characters
    txt = txt.replace("’", "'")
    txt = txt.replace("‘", "'")
    txt = txt.replace("”", '"')
    txt = txt.replace("“", '"')

    # Remove punctuation
    chars_to_remove = list(string.punctuation)
    for char in chars_to_remove:
        txt = txt.replace(char, "")
        
    txt = txt.strip()
    return txt

def compute_error_rate(preds, labels):
    
    # Word segmentation using newmm
    cut_preds = [" ".join(word_tokenize(clean_text(p).lower().replace(" ", ""), engine="newmm")) for p in preds]
    cut_labels = [" ".join(word_tokenize(clean_text(l).lower().replace(" ", ""), engine="newmm")) for l in labels]
    print(cut_preds)
    # Compute error rate (wer, ier, der)
    outputs = process_words(cut_labels, cut_preds, wer_default, wer_default)
    wer = 100 * outputs.wer
    ier = (100 * outputs.insertions / sum([len(ref) for ref in outputs.references]))
    der = (100 * outputs.deletions / sum([len(ref) for ref in outputs.references]))

    return dict(
        wer=wer,
        ier=ier,
        der=der
    )

# --------------------- Main ---------------------
def main():
    parser = argparse.ArgumentParser(description="Command-line Whisper Transcription and Evaluation")
    parser.add_argument("--model_path", type=str, required=True, help="Path to Whisper model")
    parser.add_argument("--test_json", type=str, required=True, help="Path to test JSON file")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for inference")
    parser.add_argument("--lang", type=str, default="th", help="Language code for inference")
    parser.add_argument("--task", type=str, default="transcribe", help="Task code for inference")
    parser.add_argument("--sampling_rate", type=int, default=16000, help="Audio sampling rate")
    
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.bfloat16 if device == "cuda" else torch.float32
    print(f"Device: {device}, Dtype: {torch_dtype}")

    processor = WhisperProcessor.from_pretrained(args.model_path, language=args.lang, task=args.task)
    model = WhisperForConditionalGeneration.from_pretrained(args.model_path, torch_dtype=torch_dtype)
    model.generation_config.forced_decoder_ids = processor.get_decoder_prompt_ids(language=args.lang, task=args.task)
    model = model.to(device)

    print(f'n_params: {sum(p.numel() for p in model.parameters())}')
    print(f'memory: {model.get_memory_footprint() / 1024**2:.2f} MiB')

    data = load_json(args.test_json)
    audio_path_list = [d["path"] for d in data]
    sentences = [d["sentence"] for d in data]

    transcriptions = batch_transcribe(
        model=model,
        processor=processor,
        audio_path_list=audio_path_list,
        batch_size=args.batch_size,
        sampling_rate=args.sampling_rate,
        torch_dtype=torch_dtype,
        device=device
    )

    results = compute_error_rate(transcriptions, sentences)
    print("Evaluation Results:", results)
    
if __name__ == "__main__":
    main()
