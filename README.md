# 🗣️ Blender Lip Sync Addon

Official Documentation: [https://docs.cgpoly.io](https://docs.cgpoly.io/lip-sync-documentation)

A **Blender addon** for automatic lip-syncing based on audio input.  
Cross-platform (Windows, macOS, Linux), works **out of the box** with **~25 languages**.

⚡ **Just install it from Blender’s Add-ons panel and you’re ready to go!**
## Video Demo

https://github.com/user-attachments/assets/cb90ea7b-02fc-4ca1-b19f-631024cd79cd

https://github.com/user-attachments/assets/57ea3912-2d50-4090-ba49-3035ab673a05

Animated Platformer Character by [Quaternius](https://poly.pizza/m/kKtL4zvS3n)

Wall Art 06 by Jarlan Perez [CC-BY](https://creativecommons.org/licenses/by/3.0/) via [Poly Pizza](https://poly.pizza/m/1U5roiXQZAM)

---

## ✨ Features

- 🎤 Converts voice audio into animated mouth shapes
- Interpolates between Shape Key to give natural lips motion
- 🖼️ Projects a viseme **spritesheet** onto your character’s face (one spritesheet is shipped with the add-on, but you can use your own)
- 🧠 Uses offline speech recognition (Vosk + Phonemizer + eSpeak)
- 🖥️ Fully supported on Windows, macOS and Linux
- 🔜 Future upgrade: **Pose-based animation** for facial rigs

## 📦 Installation

1. Open Blender.
2. Go to **Edit > Preferences > Get Extensions**.
3. Look for **Lip Sync**
4. Install it – done!

When you select a Language Model for the first time, Model file is downloaded and cached for future uses  (~40Mo, depending on the language).

## 🛠️ How to Use (Spritesheet)

1. Import or create a 3D character.
2. Add your movie / sound clip in Video Sequencer
3. Go to the **Lip Sync** tab in the **N-panel**.
4. Select your Language among 30 available languages.
5. Click **Add Spritesheet on Selection** 
6. Click **Set Mouth Area** from **Edit Mode**
7. Click **Analyze Audio** and wait few seconds – your character now speaks!

## 🚧 Roadmap

- [x] Sprite-based viseme projection
- [x] Timeline keyframe baking
- [x] Shapekey-based viseme support
- [ ] Pose-based animation

## 🐞 Known Issues

- Characters require no rotation and applied Scale

## 🧩 Compatibility

- Blender **4.4+**
- Works on **Windows**, **macOS**, and **Linux**

## 🤝 Contribute

Found a bug or want to help improve the addon?  
Open an issue or submit a pull request – contributions are welcome!

## 📜 License

This project is licensed under the [GNU General Public License v3.0 or later](https://spdx.org/licenses/GPL-3.0-or-later.html).

---

Made with ❤️ by [Charley 3D](https://github.com/charley3d)
