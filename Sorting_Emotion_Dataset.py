import os
import shutil
import random
from tqdm import tqdm

# ---------- SETTINGS ----------
DATASET_DIRS = [
    r"C:\Users\aswin.ASWIN-L480\Downloads\Compressed\Speech_Emotion_Recognition\Sorted_emotions",
    r"C:\Users\aswin.ASWIN-L480\Downloads\Compressed\Speech_Emotion_Recognition\SAVEE_Sorted",
    r"C:\Users\aswin.ASWIN-L480\Downloads\Compressed\Speech_Emotion_Recognition\TESS_Sorted"
]

FINAL_DIR = r"C:\Users\aswin.ASWIN-L480\Downloads\Compressed\Speech_Emotion_Recognition\Final_Emotion_Dataset"

# Emotion folders expected in each dataset
EMOTIONS = ["happy", "sad", "neutral"]

# Limit per emotion to balance dataset (set None for no limit)
MAX_SAMPLES_PER_EMOTION = 400
# --------------------------------


def prepare_folders():
    """Clear and create destination folders."""
    if os.path.exists(FINAL_DIR):
        shutil.rmtree(FINAL_DIR)
    for emotion in EMOTIONS:
        os.makedirs(os.path.join(FINAL_DIR, emotion), exist_ok=True)


def gather_files():
    """Collect and merge files from all datasets."""
    for emotion in EMOTIONS:
        all_files = []

        # Collect from each dataset folder
        for dataset in DATASET_DIRS:
            src_dir = os.path.join(dataset, emotion)
            if os.path.exists(src_dir):
                files = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith(".wav")]
                all_files.extend(files)

        # Shuffle and balance
        random.shuffle(all_files)
        if MAX_SAMPLES_PER_EMOTION:
            all_files = all_files[:MAX_SAMPLES_PER_EMOTION]

        print(f"\n🎭 Emotion: {emotion} → {len(all_files)} files")

        # Copy to final folder
        for file in tqdm(all_files, desc=f"Copying {emotion}", leave=False):
            dest_path = os.path.join(FINAL_DIR, emotion, os.path.basename(file))
            shutil.copy(file, dest_path)

    print("\n✅ All datasets merged successfully!")
    print(f"Final merged dataset saved at: {FINAL_DIR}")


if __name__ == "__main__":
    prepare_folders()
    gather_files()
