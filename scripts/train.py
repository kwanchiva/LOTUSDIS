import os
import torch
import yaml
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
    WhisperProcessor,
    WhisperForConditionalGeneration,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)
from dataset import CustomDataset
from data_collator import DataCollatorSpeechSeq2SeqWithPadding

def load_config(config_path="config/default.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()

    os.environ["WANDB_MODE"] = "offline"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.bfloat16 if device == "cuda" else torch.float32
    print(f"Device: {device}, Dtype: {torch_dtype}")

    model_name = config["model_name"]
    lang, task = config["language"], config["task"]

    model = WhisperForConditionalGeneration.from_pretrained(model_name, torch_dtype=torch_dtype)
    model.generation_config.language = lang
    model.generation_config.task = task
    model.generation_config.forced_decoder_ids = None

    feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name)
    tokenizer = WhisperTokenizer.from_pretrained(model_name)
    tokenizer.set_prefix_tokens(language=lang, task=task)

    processor = WhisperProcessor.from_pretrained(model_name, language=lang, task=task)

    train_dataset = CustomDataset(
        ann_path=config["train_annotation"],
        target_sr=config["audio"]["target_sr"],
        feature_extractor=feature_extractor,
        tokenizer=tokenizer,
    )

    dev_dataset = CustomDataset(
        ann_path=config["dev_annotation"],
        target_sr=config["audio"]["target_sr"],
        feature_extractor=feature_extractor,
        tokenizer=tokenizer,
    )

    data_collator = DataCollatorSpeechSeq2SeqWithPadding(
        processor=processor,
        decoder_start_token_id=model.config.decoder_start_token_id,
    )

    args = Seq2SeqTrainingArguments(**config["training"])

    trainer = Seq2SeqTrainer(
        args=args,
        model=model,
        train_dataset=train_dataset,
        eval_dataset=dev_dataset,
        data_collator=data_collator,
        tokenizer=processor.feature_extractor,
    )

    trainer.train()

    model.save_pretrained(args.output_dir)
    processor.save_pretrained(args.output_dir)
    print(f"Model and processor saved to {args.output_dir}")

if __name__ == "__main__":
    main()
