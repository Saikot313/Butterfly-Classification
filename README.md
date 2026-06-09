# 🦋 Butterfly Classification Project
### CNN-based Butterfly Species Identifier | Flask API + Modern Web UI

---

## 📁 Folder Structure

```
BUTTERFLY CLASSIFICATION/
│
├── 📁 classifier_UI/                  # Frontend Web Application
│   ├── 📄 index.html                  # Main UI page
│   ├── 📄 script.js                   # Frontend logic & API calls
│   └── 📄 style.css                   # Styling & animations
│
├── 📁 DataSets/                       # Dataset folder
│   ├── 📁 test/                       # Test images
│   ├── 📁 train/                      # Training images
│   ├── 📄 Testing_set.csv             # Test labels & filenames
│   └── 📄 Training_set.csv            # Train labels & filenames
│
├── 📁 models/                         # Saved model files (auto-generated)
│   ├── 📁 models/
│   ├── 🧠 butterfly_cnn.h5            # Trained CNN model weights
│   ├── 📄 class_names.json            # 75 butterfly class labels
│   └── 📄 model_summary.txt           # CNN architecture summary
│
├── 📁 static/                         # Static assets
│   ├── 📁 uploads/                    # User uploaded images (auto-generated)
│   ├── 🖼️ class_distribution.png      # Class distribution chart
│   ├── 🖼️ sample_butterflies.png      # Sample species grid
│   ├── 🖼️ test_prediction.png         # Sample prediction output
│   └── 🖼️ training_history.png        # Training accuracy/loss graph
│
├── 📓 butterfly_cnn_training.ipynb    # Jupyter Notebook for CNN training
├── 🐍 app.py                          # Flask API backend
├── 📄 README.md                       # Project documentation
└── 📄 LICENSE                         # License file
```

---

## 🚀 Step-by-Step Setup (VS Code)

### Step 1 — Install Python packages
Open a terminal in VS Code and run:
```bash
pip install -r requirements.txt
```

### Step 2 — Open Jupyter Notebook for training
```bash
jupyter notebook butterfly_cnn_training.ipynb
```
Then run all cells **top to bottom** (Cell 1 → Cell 13).

> ⏱️ Training takes 20–60 minutes depending on your CPU/GPU.
> After training, `models/butterfly_cnn.h5` and `models/class_names.json` are auto-saved.

### Step 3 — Start the Flask server
```bash
python app.py
```
Open your browser: **http://127.0.0.1:5000**

### Step 4 — Use the Web App
- Drag & drop any butterfly image onto the upload zone
- Click **"Identify Butterfly"**
- See the top-5 predicted species with confidence scores!

---

## 🦋 Model Details

| Property        | Value                     |
|----------------|---------------------------|
| Architecture   | Custom CNN (4 Conv Blocks) |
| Input Size     | 128 × 128 × 3             |
| Classes        | 75 butterfly species       |
| Training Data  | ~6,499 images             |
| Augmentation   | Rotation, Flip, Zoom, etc.|
| Optimizer      | Adam (lr=0.001)           |
| Loss           | Categorical Crossentropy  |

---

## 🌐 API Endpoints

| Method | Endpoint         | Description                |
|--------|-----------------|----------------------------|
| GET    | `/`             | Web App UI                 |
| GET    | `/api/status`   | Model status & species list|
| POST   | `/api/predict`  | Predict butterfly species  |
| GET    | `/api/species`  | Get all 75 species names   |

### Example API call (curl):
```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -F "image=@your_butterfly.jpg"
```

### Example Response:
```json
{
  "success": true,
  "top_prediction": {
    "species": "MONARCH",
    "confidence": 94.73,
    "rank": 1
  },
  "predictions": [...],
  "inference_time_ms": 45.2
}
```

---

## 🔧 Tips for Better Accuracy

1. **Use Transfer Learning** — Uncomment Cell 8 in the notebook (MobileNetV2) for significantly better accuracy.
2. **More epochs** — Increase `EPOCHS = 50` if you have time.
3. **Larger images** — Change `IMG_SIZE = (224, 224)` (needs more RAM).
4. **GPU acceleration** — Install `tensorflow-gpu` if you have an NVIDIA GPU.

---

## 📦 75 Butterfly Species

The model recognizes:
ADONIS, AFRICAN GIANT SWALLOWTAIL, AMERICAN SNOOT, AN 88, APPOLLO, ATALA,
BANDED ORANGE HELICONIAN, BANDED PEACOCK, BECKERS WHITE, BLACK HAIRSTREAK,
BLUE MORPHO, BLUE SPOTTED CROW, BROWN SIPROETA, CABBAGE WHITE, CAIRNS BIRDWING,
CHECQUERED SKIPPER, CHESTNUT, CLEOPATRA, CLODIUS PARNASSIAN, CLOUDED SULPHUR,
COMMON BANDED AWL, COMMON WOOD-NYMPH, COPPER TAIL, CRECENT, CRIMSON PATCH,
DANAID EGGFLY, EASTERN COMA, EASTERN DAPPLE WHITE, EASTERN PINE ELFIN,
ELBOWED PIERROT, GOLD BANDED, GREAT EGGFLY, GREAT JAY, GREEN CELLED CATTLEHEART,
GREY HAIRSTREAK, INDRA SWALLOW, IPHICLUS SISTER, JULIA, LARGE MARBLE, MALACHITE,
MANGROVE SKIPPER, MESTRA, METALMARK, MILBERTS TORTOISESHELL, MONARCH,
MOURNING CLOAK, ORANGE OAKLEAF, ORANGE TIP, ORCHARD SWALLOW, PAINTED LADY,
PAPER KITE, PEACOCK, PINE WHITE, PIPEVINE SWALLOW, POPINJAY, PURPLE HAIRSTREAK,
PURPLISH COPPER, QUESTION MARK, RED ADMIRAL, RED CRACKER, RED POSTMAN,
RED SPOTTED PURPLE, SCARCE SWALLOW, SILVER SPOT SKIPPER, SLEEPY ORANGE,
SOOTYWING, SOUTHERN DOGFACE, STRAITED QUEEN, TROPICAL LEAFWING,
TWO BARRED FLASHER, ULYSES, VICEROY, WOOD SATYR, YELLOW SWALLOW TAIL,
ZEBRA LONG WING

---
---
Built with Md. Sakender Saikot
Powered by TensorFlow · Flask · CNN Deep Learning

