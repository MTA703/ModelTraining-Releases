# Model Training

**Train YOLO models without touching a terminal.**

Windows desktop app that turns YOLO detection, segmentation and pose training
into a 3-click flow. Built for people who want results, not a Python tutorial.

[![Latest Release](https://img.shields.io/github/v/release/MTA703/ModelTraining-Releases?label=Download%20latest&style=for-the-badge)](https://github.com/MTA703/ModelTraining-Releases/releases/latest)

---

## Download

Grab the latest installer from the **[Releases page](https://github.com/MTA703/ModelTraining-Releases/releases/latest)**.

A 3-day free trial starts automatically on first launch — no credit card,
no signup. License keys are sold separately (see the website for pricing).

## What you get

- **Guided env setup** — we detect your NVIDIA GPU, install the right CUDA build, create a clean Python environment. You click Next twice.
- **Smart defaults** — 90/10 split, AMP, VRAM-aware batch sizing, patience tuned to dataset size. Override anything you want, but you won't need to.
- **Live training charts** — loss, mAP, GPU usage, ETA all streaming in real time.
- **Test Mode** — drag any image on the result screen and see the model's predictions with confidence scores.
- **All YOLO families** — v8 / v9 / v10 / v11 (detect / segment / pose where supported).
- **One-click export** — PT, ONNX, TorchScript + a PDF training report.

## System requirements

| | Requirement |
|---|---|
| OS | Windows 10 / 11 (64-bit) |
| GPU | NVIDIA, 4 GB VRAM minimum (8 GB recommended) |
| Disk | 20 GB free (~5 GB for the ML environment, the rest for datasets/models) |
| Internet | Required (license check every ~5 minutes; trial start needs online) |

**Not supported:** AMD / Intel GPUs (training needs CUDA), macOS / Linux,
virtual machines (VirtualBox, VMware, Hyper-V — the license server blocks
these).

## First launch — what to expect

The installer is ~180 MB. After install:

1. **Windows SmartScreen** may show "Windows protected your PC".
   Click *More info* → *Run anyway*. We're working on a code signing
   certificate to remove this warning.
2. The app opens. Pick where to store your training environment (~5 GB).
3. It downloads PyTorch + CUDA + ultralytics into that folder (~3.5 GB,
   one-time download).
4. Your 3-day free trial activates automatically.
5. Open the wizard, pick a dataset folder, hit Start.

## Support

- **Activation / billing / installation help:** [Discord support server](https://discord.gg/3DNdzFqFPf)
- **Community + showcase + ML chat:** [Discord community](https://discord.gg/pyTUVvt7bH)
- **Bug reports:** open a ticket in the support Discord, or [file an issue](https://github.com/MTA703/ModelTraining-Releases/issues)

## License

This repository hosts only the installer binaries. The Model Training
application itself is proprietary software. Use is governed by the
end-user license shown during install / on first launch.

Models you train with this app are entirely yours — train, sell, deploy
or embed them however you want.

---

Powered by **Taher's House**.
