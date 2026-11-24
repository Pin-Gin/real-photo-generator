# Dドライブ配置計画 — 初期ディレクトリ構成

**Status:** 初期ディレクトリ作成の対象。アプリ／モデルのインストール、Git以外の実ファイルの移行は未実施。
**Git:** `https://github.com/Pin-Gin/real-photo-generator`
**ルート:** `D:\AI\real-photo-generator`

## 1. Dドライブ全体（Git管理領域と非管理領域を分ける）

```text
D:\AI\real-photo-generator\
├─ repo\                         # 新Gitリポジトリ（clone先）
├─ runtime\
│  ├─ comfyui\                   # 将来のComfyUI実行環境
│  ├─ python\                    # 将来のPython実行環境
│  └─ video-tools\               # 将来の動画処理ツール
├─ assets\
│  ├─ models\                    # モデルの使用領域（採用モデル未選定）
│  └─ references\
│     ├─ incoming\               # 入力された参照画像
│     ├─ masters\                # ユーザー承認Master
│     └─ poses\                  # ポーズ参照
├─ outputs\
│  ├─ quality-tests\             # 静止画の品質試験
│  ├─ approved\                  # 承認済み静止画
│  ├─ videos\
│  │  ├─ quality-tests\          # 動画品質試験
│  │  └─ approved\               # 承認済み動画
│  └─ video-frames\              # 中間フレーム（必要時）
├─ backups\
│  ├─ downloaded-apps\           # DLしたアプリ／アーカイブの保全
│  ├─ downloaded-models\         # DL済みモデルの保全コピー
│  └─ manifests\                 # モデル／ファイル棚卸し表
├─ state\                        # ローカル状態／設定
├─ logs\
└─ temp\
```

当初案の `repo/`、`runtime/`、`assets/`、`outputs/`、`backups/`、`state/`、`logs/`、`temp/` の区分を維持し、**動画要件に必要な専用領域だけ**追加した。アプリ／モデルの実運用構造は検証後に決める。

## 2. `repo/` のGit管理用骨格

```text
repo\
├─ README.md
├─ .gitignore
├─ docs\
│  ├─ START_HERE.md
│  ├─ requirements\REQUIREMENTS_V1.md
│  └─ architecture\D_DRIVE_LAYOUT.md
├─ src\
│  ├─ common\
│  ├─ image\
│  └─ video\
├─ workflows\
│  ├─ image\
│  └─ video\
├─ config\
├─ tests\
│  ├─ unit\
│  ├─ integration\
│  └─ quality\
└─ scripts\setup_d_drive.ps1
```

空ディレクトリはGitに保存されないため、初期骨格は各ディレクトリの `.gitkeep` で管理する。`src` などは**空のプレースホルダー**であり、特定フレームワークの採用を意味しない。

## 3. 構築順序

1. GitHubの新リポジトリにこの骨格と要件書を反映する。
2. `D:\AI\real-photo-generator\repo` に新リポジトリをcloneする。
3. `repo\scripts\setup_d_drive.ps1` を実行し、`repo/` 以外の空ディレクトリを作る。
4. 既存モデル／アプリの棚卸しとバックアップは別途実施。まだ旧環境を削除しない。

**注意:** 旧 `C:\Dev\local-image-generator` に未追跡コードが多数ある。新環境の初期化処理で `git clean`、旧フォルダ削除、既存データの上書き、モデル移動は実施しない。新Gitにモデルや個人参照画像を直接保存しない。
