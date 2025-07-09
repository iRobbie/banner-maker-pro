# 📄 **BannerMaker**

BannerMaker is a Python script to generate banners by combining multiple images into a neat grid.  
It optionally adds:
-  a customizable **info band** with color of your choice.
-  a **watermark** with adjustable transparency.

It automatically prepares the workspace and installs any missing dependencies.

---

## 🚀 Features

✅ Combine images into a 2000×2000 banner  
✅ Add info band (optional)  
✅ Add watermark (optional)  
✅ Adjustable watermark transparency  
✅ Supports HEX, RGB, CMYK color formats  
✅ Automatically installs dependencies  
✅ Works interactively — no coding required

---

## 🖥️ Requirements

- Windows (recommended — uses Desktop API)
- Python **3.8+**

You can check if Python is already installed by running:

```bash
python --version
```

You should see something like:

```text
Python 3.11.4
```

If not, [download and install Python here](https://www.python.org/downloads/) and make sure to check **Add Python to PATH** during installation.

---

## 🔷 Installation

1️⃣ Clone or download this repository.  
2️⃣ Place the `final.py` script somewhere convenient.  
3️⃣ Open a terminal or command prompt in the same folder as the script.  
4️⃣ Run the script — it will install all required Python libraries if needed.

```bash
python final.py
```

On first run, it will also create a workspace folder (`BannerMaker`) and ask you to create or choose a folder with your input images.

---

## 🧑‍💻 How to use

✅ Just follow the interactive prompts.  
You will be asked:
- Do you want an info band?  
  - If yes: enter color (HEX / RGB / CMYK)  
- Do you want a watermark?  
  - If yes: enter transparency (0–100)  
- Enter a name for your output folder

The script will process all `.png` images from your specified folder(s) and generate a banner like this:

📁 `BannerMaker/Banners/<YourOutputName>_<Timestamp>/final_output.png`

---

## 📦 Dependencies

The script uses these Python packages:
- [`Pillow`](https://pillow.readthedocs.io/) — image processing
- [`requests`](https://docs.python-requests.org/) — download font

They are installed automatically.  
If you ever need to install them manually, you can run:

```bash
pip install pillow requests
```

---

## 🔧 Supported color formats

When entering a color for the info band, you can use:
- HEX: `#FF0000` or `FF0000`
- RGB: `rgb(255, 0, 0)` or `255,0,0`
- CMYK: `cmyk(0, 100, 100, 0)` or `0,100,100,0`

Examples:
```text
#FF0000
rgb(255,0,0)
cmyk(0,100,100,0)
```

---

## 📂 Output Example

```
BannerMaker/
├── Banners/
│   └── MyBanner_08.07.2025 23-45-12/
│       └── final_output.png
```

---

## 💡 Tips

- Run the script as Administrator if you encounter permission errors.
- Always check your input folder contains valid image files before running.
- You can edit `folder_list.txt` in the `BannerMaker` folder to specify multiple input folders.

---

## 📃 License

MIT License. Free to use and modify.
