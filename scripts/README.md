# Thai Whisper ASR Fine-Tuning

This repository contains code for fine-tuning the **Pathumma Whisper TH Large v3** model.  
The base model is built on [nectec/Pathumma-whisper-th-large-v3](https://huggingface.co/nectec/Pathumma-whisper-th-large-v3). To finetune model, you can follow the steps below:
1. Navigate to the `scripts` directory: `cd scripts`.
2. Install the required packages: `pip install -r requirements.txt`.
3. Prepare your training data. You can refer to the sample data format in [`train_examples.json`](train_examples.json).
4. Configure the training settings in [`config/default.json`](config/default.json)
5. Start training the model: `python train.py`.
