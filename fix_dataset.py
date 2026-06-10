import os

folders = [
    "dataset/train/violence",
    "dataset/train/non_violence"
]

for folder in folders:
    print("\nChecking folder:", folder)

    files = os.listdir(folder)
    removed = 0

    for file in files:
        path = os.path.join(folder, file)

        # check if file exists
        if not os.path.isfile(path):
            print("Removing broken entry:", file)
            try:
                os.remove(path)
            except:
                pass
            removed += 1

    print("Total files checked:", len(files))
    print("Broken files removed:", removed)

print("\nDataset check completed")