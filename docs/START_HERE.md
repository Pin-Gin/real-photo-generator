# real-photo-generator — START HERE

- **Git:** `Pin-Gin/real-photo-generator`
- **ローカルroot:** `D:\AI\real-photo-generator`
- **Git clone先:** `D:\AI\real-photo-generator\repo`

## 読む順序

1. [`requirements/REQUIREMENTS_V1.md`](requirements/REQUIREMENTS_V1.md) — ユーザー確定の目標と開発順序
2. [`architecture/D_DRIVE_LAYOUT.md`](architecture/D_DRIVE_LAYOUT.md) — Git構成とDドライブの配置
3. [`../scripts/setup_d_drive.ps1`](../scripts/setup_d_drive.ps1) — Dドライブの空フォルダ配置

**ターゲット画風:** 添付画像品質のセミリアルCG〜フォトリアル寄り。純粋な実写だけ、アニメだけに限定しない。

**順序:** テキストのみの静止画モデル選定・複数生成・品質確認 → Master＋テキストで人物維持 → Image-to-Video／動画60FPS目標 → 最後にWeb／デスクトップの選定。

**現状:** ディレクトリ骨格だけ。モデル・ワークフロー・アプリ・GPU実生成は未導入／未検証。
