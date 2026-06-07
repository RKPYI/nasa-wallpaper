# 🌌 nasa-wallpaper

A lightweight Windows 11 script that hits NASA's APIs to pull the daily astronomy picture and forces Windows to update my desktop background automatically. 

Built for Hack Club Stardance 2026 🚀

---

## 🛠️ The Plan
* **Phase 1: Local Control (Done)** - Make Python forcefully change the Windows 11 wallpaper using a local file.
* **Phase 2: NASA API** - Grab a NASA developer key and pull the Astronomy Picture of the Day (APOD) JSON payload.
* **Phase 3: The Link** - Download the image from the API and pipe it straight into the Phase 1 script.
* **Phase 4: Automation** - Set up Windows Task Scheduler so it runs silently in the background every morning when I boot my PC.

---

## 💻 Phase 1 Notes
Windows 11 turns the screen pitch black if you pass a relative path to the background settings. I fixed this by using `os.path.abspath` to force a full qualified path on runtime.

The core hook uses `ctypes` to talk to `user32.dll` via `SystemParametersInfoW`. Passing the flags `SPIF_UPDATEINIFILE` and `SPIF_SENDWININICHANGE` forces Windows to broadcast the change immediately and makes it stick even after a reboot.