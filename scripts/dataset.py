import json
import librosa
from torch.utils.data import Dataset
from transformers import (
    WhisperFeatureExtractor,
    WhisperTokenizer,
)

class CustomDataset(Dataset):
    def __init__(self, 
        ann_path: str, 
        target_sr: int = 16_000,
        feature_extractor: WhisperFeatureExtractor = None,
        tokenizer: WhisperTokenizer = None
    ):
        super(CustomDataset, self).__init__()
        self.data = self.load_json(ann_path)
        self.target_sr = target_sr
        self.tokenizer = tokenizer
        self.feature_extractor = feature_extractor

    def load_json(self, path):
        with open(path, "r") as f:
            data = json.load(f)
        return data
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        audio_path = self.data[idx]["path"]
        sentence = self.data[idx]["sentence"]

        array, sr = librosa.load(path=audio_path, sr=self.target_sr)
        input_features = self.feature_extractor(
            array, sampling_rate=sr
        ).input_features[0]

        labels = self.tokenizer(sentence, truncation=True, max_length=448).input_ids

        return dict(
            input_features=input_features,
            labels=labels
        )
