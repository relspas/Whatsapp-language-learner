# WhatsApp Word Frequency Extractor

This Python script analyzes WhatsApp chat exports and computes word or expression frequencies. It can process a single text file or a folder of multiple exports.

## 📦 Setup Instructions

### 1. Export WhatsApp Chats
To use this tool:
- Open the WhatsApp chat you want to export on your phone.
- Tap the three-dot menu > **More** > **Export Chat**.
- Choose **Without Media**.
- Send the `.txt` file to your computer (e.g., via email or cloud service).

Repeat as needed for multiple chats.

### 2. Organize Files
- Create a folder (e.g., `whatsapp_chats/`).
- Place all exported `.txt` files into this folder.

### 3. Clone This Repository
```bash
git clone https://github.com/yourusername/whatsapp-wordfreq.git
cd whatsapp-wordfreq
```

### 4. Install Requirements
Make sure you have Python 3 installed. Then run:

```bash
pip install -r requirements.txt
```

## 🚀 Usage
Run the script with:
```
python extract_user_wordfreq.py <path_to_text_file>
```
Or to analyze a folder of multiple chats:

```bash
python extract_user_wordfreq.py -f <path_to_folder>
```

### Optional Arguments
`-w <num_words>`: Number of top individual words to display (default: 30)
`-e <num_expressions>`: Number of top multi-word expressions to display (default: 10)

### Examples
- Analyze a single exported chat file
```
python extract_user_wordfreq.py exported_chat.txt
```
- Analyze all chats in a folder, return top 50 words and top 20 expressions
```
python extract_user_wordfreq.py -f whatsapp_chats -w 50 -e 20
```
