# 🗣️ Blender Lip Sync Addon

A **Blender addon** for automatic lip-syncing based on audio input.  
Cross-platform (Windows, macOS, Linux), works **out of the box** with **30 languages**.

⚡ **Just install it from Blender’s Add-ons panel and you’re ready to go!**
## Video Demo
### Lip Sync on a short animation
https://github.com/user-attachments/assets/57ea3912-2d50-4090-ba49-3035ab673a05
### Animation Making Of:
https://github.com/user-attachments/assets/cb5fa9a6-6deb-4997-a5af-41c00d0cefee

Animated Platformer Character by [Quaternius](https://poly.pizza/m/kKtL4zvS3n)

Wall Art 06 by Jarlan Perez [CC-BY](https://creativecommons.org/licenses/by/3.0/) via [Poly Pizza](https://poly.pizza/m/1U5roiXQZAM)

---

## ✨ Features

- 🎤 Converts voice audio into animated mouth shapes
- 🖼️ Projects a viseme **spritesheet** onto your character’s face (one spritesheet is shipped with the add-on, but you can use your own)
- 🧠 Uses offline speech recognition (Vosk + Phonemizer + eSpeak)
- 🖥️ Fully supported on Windows, macOS and Linux
- 🔜 Future upgrade: **shapekey-based animation** for facial rigs

## 📦 Installation

1. Open Blender.
2. Go to **Edit > Preferences > Add-ons > Install**.
3. Select the `.zip` file of the addon.
4. Enable it in the list – done!

When you select a Language Model for the first time, Model file is downloaded and cached for future uses  (~40Mo, depending on the language).

## 🛠️ How to Use

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
- [ ] Shapekey-based viseme support

## 🐞 Known Issues

- Your Movie / Sound clip needs to be placed at the \#1 frame of Video Sequencer
- Ukrainian Language cannot be cached (it works but it is downloaded each time you select it)

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
