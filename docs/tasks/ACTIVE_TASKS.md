# real-photo-generator — 作業・検証タスク一覧（進捗台帳）

**更新日:** 2026-11-28 (JST)  
**対象リポジトリ:** `Pin-Gin/real-photo-generator`  
**現在位置:** **T-010：既存の成功ComfyUIワークフローの実体確認・凍結（準備段階）**  
**最初の画像QAゲート:** **T-020 / TEST 01 — SFW衣装画像参照による着用検証**（未実行）  
**関連:** [既存確定要件](../requirements/REQUIREMENTS_V1.md) / [2026-11-26引継ぎ](../handoff/2026-11-26_NATURAL_LANGUAGE_COMFYUI_HANDOFF.md) / [Dドライブ配置](../architecture/D_DRIVE_LAYOUT.md)

## 0. 進捗表示ルール

| 記号 | 定義 |
| --- | --- |
| DONE | 必要な証跡を確認済み。完了を主張できる範囲を限定する |
| ACTIVE | 現在検証・確認する作業。結果が出るまではPASSとしない |
| BLOCKED | 外部情報／実機／承認などが不足しており、完了できない |
| TODO | 待機中、未着手 |
| PASS / WARN / FAIL | 生成画像・実行設定・ユーザー判定に基づく**テスト単位の判定**。タスク進捗とは別 |

**運用:** 各実施後にこのファイルの状態・日付・根拠（コミット、ワークフローID、ログ概要、画像ファイルのローカル識別子、ユーザー判定）を更新する。新しい仮説を成功実績として記録しない。未検証ならBLOCKED/TODOのままにする。

## 1. 作業全体一覧

| ID | 領域 | タスク／完了条件 | 状態 | 依存 |
| --- | --- | --- | --- | --- |
| T-001 | Git基盤 | GitHubの書き込み権限復旧、既存引継ぎMarkdownの新規コミット、読み戻し内容一致を確認 | **DONE** | — |
| T-002 | Git読込 | mainの要件・引継ぎ・配置資料を再取得、既存の優先順位と要件差分を確認 | **DONE** | T-001 |
| T-003 | 追跡 | 本書をmainに保存し、タスク・テスト位置を一元化 | **DONE**（コミット済み） | T-002 |
| T-004 | 要件整合 | FIXED要件「動画の後にアプリ化」と後続の「自然言語Webアプリを早期に構築」の**差分を保持**。正式な順序改訂は別途承認 | **BLOCKED**（正式改訂未承認） | T-002 |
| T-010 | **現行位置** | ローカルにある成功ワークフローの**API JSON実体**を特定（モデル、ノード、Seed、Steps、CFG、画像入力、出力識別子） | **ACTIVE**（実機の確認待ち） | T-002 |
| T-011 | ベース保全 | T-010で指定・確認したJSONを原本として保存し、ハッシュ・版・モデル構成を記録。元JSONは上書きしない | **BLOCKED** | T-010 |
| T-012 | 実行前検査 | ComfyUI `/object_info`・`/models/*`・`/history`・`/queue`を確認。現時点のノード／ファイル／API稼働を確認 | **BLOCKED**（Windows実機） | T-010 |
| T-013 | 参照準備 | Master候補の承認状態、衣装画像実体・保管場所、画像ロール（identity / garment）を確認。Gitへの画像アップロード禁止 | **BLOCKED** | T-010 |
| T-014 | 成功ベースの再現 | 変更前ワークフローを同条件で再実行し、出力品質・人物維持を再評価。過去の「成功」と現在の再現PASSを分離 | **TODO** | T-011〜013 |
| **T-020** | **TEST 01** | **衣装参考画像を適用し、Masterの顔・髪・体格・ポーズを維持したまま自然な着用状態を生成** | **TODO / 未生成** | T-014 |
| T-021 | TEST 01 QA | トップス／カーディガン／スカートの正しい接続、重なり、装飾、しわ、布厚、身体との整合、残留服・貼り付けの有無を判定 | **TODO** | T-020 |
| T-022 | ネガティブA/B | 同一条件でnegativeだけ変えた比較。実効性、アニメ化、ノイズ、副作用、同一性の変化を別判定 | **TODO** | T-014 |
| T-030 | 衣装・背景制御 | 服装・背景について**文章指定**と**画像参照指定**の各ルートを検証 | **TODO** | T-020 |
| T-031 | 肌色・肌質 | Masterを維持し色／材質のみを制御。色むら、肌ノイズ、顔変形を確認 | **TODO** | T-014 |
| T-032 | レンダリング | セミリアルCG〜フォトリアル寄りの品質・素材感を検証。単なる拡大／シャープ化をPASSにしない | **TODO** | T-014 |
| T-033 | 光源・表情・視線 | 各制御を単独で比較し、他属性への漏れを確認 | **TODO** | T-014 |
| T-040 | ポーズ1 | **マネキン画像のみ**。体型を移さず姿勢だけ抽出・適用 | **TODO** | T-020 |
| T-041 | ポーズ2 | **文章のみ**。姿勢の指示追従性・安定性を確認 | **TODO** | T-020 |
| T-042 | ポーズ3 | **マネキン画像＋文章**。画像と文章の役割・競合を確認 | **TODO** | T-040〜041 |
| T-043 | マネキン規則 | 参照するのは関節配置・腕脚方向・体幹のひねり・重心。**マネキン体型・頭身・質感は転写しない**。Master骨格へリマッピング可能性を確認 | **TODO** | T-040 |
| T-044 | ポーズ＋衣装 | 手足の変化に衣装（袖・裾・しわ・接触）が追従するか | **TODO** | T-040〜043 |
| T-050 | アングル | 正面／斜め／側面／俯瞰を別制御にし、人物と衣装の立体構造を評価 | **TODO** | T-020 |
| T-051 | カメラ | カメラ高さ、距離、画角、焦点距離、アスペクト比、被写界深度を制御。アングルと分離する | **TODO** | T-050 |
| T-052 | 実寸対比 | **153cm・7.3頭身を指定ベース**として、既知寸法の柵・棚・浴槽等と人物の相対スケール、接地・遠近を検証。Master実寸比の実測は未確認 | **TODO** | T-050〜051 |
| T-053 | 空間整合 | 背景画像の接地・遮蔽・パース・ライティングと人物の整合性を検証 | **TODO** | T-030,T-052 |
| T-060 | JSON基盤 | 原文そのまま保存 → 意図解析Intent（未指定/推定を区別） → API Workflow JSON生成、差分プレビュー、schema/ノード互換性検査 | **TODO** | T-011 |
| T-061 | 画像ロール | 人物Master、衣装、背景、マネキン、構図、品質参照を入力枠と内部データで分離 | **TODO** | T-060 |
| T-062 | モデル別アダプター | Qwen Edit／SDXL等で利用可能ノードと接続方式を区別。論理制御と物理ノードを混同しない | **TODO** | T-060 |
| T-063 | Web UI・履歴 | テキスト/negative/画像入力、モデル・テンプレート選択、原文とJSON diff、出力ギャラリー・再現設定・QAの保存 | **TODO** | T-060〜062 |
| T-064 | ComfyUI実行 | `/upload/image` → `/prompt` → 完了確認 → `/history/{prompt_id}` → `/view`、失敗時も記録 | **TODO** | T-060〜063 |
| T-065 | 入力競合・複数コマ | 例：「3:4、2×2の4分割」「5種類の動作」を検出し、4コマと5候補の不一致を明示。勝手に1種類を捨てない | **TODO** | T-060 |
| T-066 | 複合統合QA | 複数人物、着衣、ポーズ、背景、アングル、ネガティブなどの同時制御。単体PASSの寄せ集めを統合PASS扱いしない | **TODO** | T-020〜065 |
| T-070 | 品質向上 | GPT画像生成を品質・人物同一性・指示追従・衣装自然性で比較。未達を未達と記録し、再現性を伴う改善だけ採用 | **TODO** | T-066 |
| T-080 | 将来動画 | Master＋動作文章、Image-to-Video、60FPS出力目標の個別検証。動画モデル・補間方法・生成品質は未選定 | **TODO** | 静止画品質ゲート |

### 段階の切り分け

1. **今:** T-010〜014（実機にある成功フローの特定・保全・再実行）
2. **最初の画質ゲート:** T-020/021（SFW衣装適用／着用確認）。ここを通過するまではポーズ変更へ進めない
3. **単体制御:** negative、衣装・背景、肌、レンダリング等
4. **ポーズ比較:** マネキンのみ／文章のみ／併用の3条件
5. **空間制御:** アングル、カメラ、実寸対比、背景整合
6. **アプリ化・複合:** 自然文からのJSON自動生成・UI・実行・統合QA
7. **長期:** GPT級品質目標、動画

**注意:** 2026-11-24のFIXED開発順と2026-11-26のWebアプリ先行構想の間に差分がある。ここに記載した工程は作業を追跡する台帳であり、**FIXED要件を書き換える承認ではない**。T-004で正式に扱う。

## 2. TEST 01 — SFW衣装適用（実行前仕様）

**使用するもの:** 
- 人物Master：ユーザー指定の架空成人女性。ローカルの実体・承認状態をT-013で確定する。
- 衣装参照：ユーザー添付の透明マネキン画像（白いレース装飾ニットトップス、ブラウンのリボン、白いオーバーサイズケーブルニットカーディガン、ブラウン系チェックプリーツミニスカート、ハート型バックル・チェーン）。
- **画像の参照役割:** Master＝人物の同一性／衣装写真＝衣類の構造・素材・配色・装飾。マネキンの身体・透明な質感・背景は取り込まない。
- ベースのモデル、API JSON、Seed、Steps、CFG、サイズ、サンプラーは**T-010/011の実体確認が終わるまで未確定**とする。画像参照用の複数入力がノードに対応するかもT-012で検証する。

**手順（各操作で成功原本を保全）**
1. T-014で成功したベースと同一の入力で再実行し、基準出力を取得する。
2. モデル固有の**衣装参照画像の接続手段**を調査し、コピーしたワークフローに衣装画像を接続する（プロンプトに「衣装画像を参照」と書くだけではない）。
3. 初回はベースの人物・ポーズ・カメラ・背景を可能な限り維持し、衣装だけを変更。
4. 生成した画像と前後JSONの差分を保存。人体・着衣・同一人物性・画質を分離評価。
5. ユーザーがPASS/WARN/FAILを確定。FAILなら**成功原本を復元**し、崩れた制御だけを調査。

**TEST 01 QA表**

| 評価項目 | PASSの判断対象 | FAIL例 |
| --- | --- | --- |
| 人物同一性 | 顔・髪色／髪型・体型・頭身 | 他人化／マネキン体型へ変形 |
| 着衣構造 | トップスとカーディガンの重なり、袖口、襟、裾 | 身体へ平面的に貼り付く／布が浮く |
| 素材と装飾 | ニット編み・レース、リボン、バックル、チェーン | 接続が不自然／装飾が消える |
| 身体・衣装整合 | 胸郭、肩、腰、脚と衣服の空間関係 | 腕が袖から抜ける／スカートが脚に癒着 |
| レンダリング | 顔・髪・肌・布・背景の立体表現が両立 | アニメ化、指・関節異常、色ノイズ |
| 参照ロール | 服装だけを参照する | 透明マネキン・参考背景まで人物へ転写 |

**記録テンプレート:** `試験ID / 日時 / API JSONファイル名・SHA256 / Masterローカル識別子 / 衣装画像識別子 / 使用モデル / Seed / Steps / CFG / ネガティブ / ComfyUI prompt_id / 出力画像識別子 / QA（各項目PASS/WARN/FAIL） / ユーザー総合判定 / 次の調整`。公開Gitへ機微な画像・私的プロンプトそのものはコミットしない。

## 3. 現時点での根拠・制約（2026-11-28）

- **確認済み:** `docs/requirements/REQUIREMENTS_V1.md`、`docs/handoff/2026-11-26_NATURAL_LANGUAGE_COMFYUI_HANDOFF.md`、`docs/START_HERE.md`、`docs/architecture/D_DRIVE_LAYOUT.md` のGit main上の原文を読み直した。
- **確認済み:** GitHub書込み403は引継ぎファイルの追加コミット `36d4e352ca5f4a23ae776dc237e5349407561d17` で解消。内容読み戻し一致。
- **確認済み:** Gitに `workflows/image/.gitkeep`、`src/image/.gitkeep`、`tests/quality/.gitkeep` が存在する。これらは**フォルダの骨格**であり、成功ワークフローのAPI JSON本体ではない。
- **未確認:** WindowsのComfyUI稼働状況、ユーザーPC内のWorkflow JSON、モデルファイル現状、Master実体、衣装画像の配置、Webアプリ試作品の存在と起動。Git検索にヒットがないことだけでファイル不存在を断定しない。
- **未実施:** TEST 01の新規生成、TEST 01 QA、ポーズ3系統、negative A/B、Web UIの動作試験。
- **禁止:** 旧環境の削除、`git clean`、画像・モデル重みの公開Git登録、FIXED設定の無断変更、成功原本への上書き、複数条件を無秩序に変える比較。

## 3A. 2026-11-28 失敗試行の記録：衣装テキスト変更（受理画像あり／FAIL）

**ローカル出力の識別名:** `Qwen_SFW_Clothes_TEST01_00001_`（ユーザーがチャットで画像提示、画像ファイル自体はGitに保存しない）。

- **試行内容:** Master候補を入力し、文章指定「白い半袖トップス＋紺色プリーツスカート」へ変更。**衣装参照画像は未入力**。したがって元来の **T-020 / TEST 01（衣装*画像*参照）とは異なる試行**であり、TEST 01を完了としない。
- **観察した出力:** 衣装指示は概ね反映。しかし顔・髪色と髪型・体型・ポーズ・フレーミングが原Masterから大きく逸脱。元Masterはほぼ全身で手を背面、結果は太腿付近で切れ腕は横に下りた。
- **判定:** **FAIL**（「衣装のみ変更」の検証として）。衣装の自然な着用自体に一定の描写はあるが、人物維持・構図維持が成立しないため全体不合格。ユーザーの「NG」を記録。
- **設計上の原因候補（コード比較に基づく）:** 前回提示されたコマンドは、成功履歴に示された16ノード構成を確認せず、新しい12ノード構成を使用した。画像編集用 `TextEncodeQwenImageEditPlus` に入力画像 `image1` と `vae` の明示的な接続がなく、元の `FluxKontextImageScale`、`FluxKontextMultiReferenceLatentMethod`、`CFGNorm` を省略していた。**このため失敗原因をモデル性能の限界と確定してはいけない**。 `CFG=1` では通常のnegative文字列の効果も検証できない。
- **作業位置:** **T-010を継続（ACTIVE）**。まず `GET /object_info/TextEncodeQwenImageEditPlus` と既存成功フローのAPI JSON/テンプレートを照合し、必要ノードが接続された「成功フローのコピー」でのみ衣装編集を再試験する。比較は顔・髪・体格・ポーズ・構図を固定する。
- **T-020 / TEST 01 の扱い:** **未実施**。マネキン着用の白ニット＋チェック柄スカートという衣装**画像**を参照して生成する本来の試験は、成功フロー固定と入力接続確認後に行う。
- **禁止:** 失敗出力をMasterとして採用しない。失敗した12ノードのJSONを「成功ベース」として上書き保存しない。

## 4. 次回の実機からの引継ぎ入力

T-010/012を進めるには、ユーザーPCの**成功ワークフロー API JSON**またはComfyUIの当該生成履歴のJSON実体、及び現在の`/object_info`の使用ノード定義が必要。チャットだけではlocalhost:8188の実行状態を取得できない。**モデルや画像の秘密実体は不要。** 実機のJSON中に機密パスや個人プロンプトがある場合は共有前に確認する。

再開するたびに本書の**現在位置（ACTIVE）**と**最初のQAゲート**を宣言してから作業する。修正は検証根拠を残す。


## 3B. 2026-11-28 衣装文章変更 fixA — ユーザーPASSの範囲と実画像判定

**出力識別名:** `Qwen_SFW_Clothes_TEST01_fixA_00001_`。会話へ添付済み。画像本体・Masterは公開Gitへ追加しない。

- **実行した内容:** `TextEncodeQwenImageEditPlus` の positive/negative に `vae` と `image1` を接続し、前回の12ノード構成の一部を修正。KSampler `denoise=0.65`、`steps=4`、`cfg=1.0`、`seed=2026112811`（ユーザーが実行した提示コード上の値。ComfyUI履歴との照合は未実施）。
- **ユーザー判定:** 「PASS」。
- **画像比較で確認できた改善:** 明るいブラウンのショートヘア、顔立ち、人物の体格、両腕を背面に回す姿勢、頭から足先までの全身構図がMaster候補に近づいた。**Master維持の検証としてPASSを受領**。
- **残課題:** 指示した白い半袖トップス＋紺色プリーツスカートには変更されず、元のキャミソールとショートパンツが残っている。無地グレーの背景は室内背景に変わった。**衣装制御の達成は未確認／画像上は未達、背景維持はWARN**。
- **前回との技術的差分:** `vae`/`image1` 参照接続と denoise、Seed、プロンプトを同時変更しているため、改善の**単一原因は特定できない**。成功した16ノード構成への完全復帰は未実施。
- **次の方針:** fixAを`Master維持の比較基準`として原本保全（実行JSONの読み戻し・SHA256が必要）。次にベースフローを固定したまま衣装だけ変更できるよう、1条件ずつ検証。服装画像参照の本来のTEST 01は別タスクとして引き続き未実施。


## 3C. 2026-11-28 衣装参照画像による追加テスト（T-020A）

**状態:** 実機生成待ち（ComfyUI localhost環境はChatGPTから直接操作できない）。**QA未判定**。これは元の白ニット衣装のTEST01とは別の衣装画像を用いた追加テスト。

- **参照衣装:** ユーザー提示の薄紫／ラベンダー色のリボン、フリル、シアー素材を含む衣装画像。公開Gitに画像を含めない。
- **検証基準:** fixA `Qwen_SFW_Clothes_TEST01_fixA_*.png` のユーザーPASSは「人物・ポーズ・フレーミング維持」に限定され、衣装変更は未達だった。**その時点の実行履歴（`/history`）からAPI JSONを回収・保全**して出発する。
- **コード:** ComfyUI REST API用の標準Python検証スクリプト。原本Workflowを複製し、衣装 `LoadImage` ノードを1個追加。2画像対応の`TextEncodeQwenImageEditPlus`のpositive・negative両方に `image2` を渡す。モデル/LoRA/Seed/Steps/CFG/denoiseとMasterは元のfixA値を変更しない。自然文は画像1＝人物Master、画像2＝衣装だけと明示する。
- **現時点の事前検証:** 構造の静的チェック、模擬ComfyUI HTTPサーバーで履歴読込・画像アップロード・JSON改変・キュー登録・完了画像ダウンロードまでのソフトウェア試験はPASS。**Windows PC上のモデル生成・出力画質は未検証**。
- **画像のSFW要件:** 素材の透け方によって衣装忠実度と身体の露出抑制が競合する場合がある。隠すための変更は結果QAで明示し、勝手に「衣装完全一致」と判定しない。
- **実機の次作業:** 検証キットをユーザーPCに置き、ComfyUI起動後に1行PowerShellから実行。実体がないfixA履歴は自動で捏造せずエラー終了。結果画像を受け取り、人物／体型／ポーズ／構図／着衣／背景／SFWを分離評価してPASS/WARN/FAIL確定。
- **検証キットSHA256:** `2c1a0b996f9e6940ab5295249907afbf009b8a1cfc52e907ab9279b69e8ed95b`（会話添付ZIP。画像やバイナリはGitに保存しない）。


## 3D. 2026-11-28 T-020A 実機出力QA（ユーザーNG）

- **実機出力:** `Qwen_SFW_GarmentRef_T020A_cc2d1733_00001_.png` をユーザーが提示し**NG**と判定。画像ファイル自体は公開Gitに保存しない。
- **人物性・ポーズ・構図:** fixAとほぼ一致して維持（本テストの部分的成果）。
- **服装参照:** ラベンダー色の首リボンと袖フリルのみ反映。元の淡色キャミソールとショートパンツが残存し、参照衣装全体の置換・構造的着用は未成立。**衣装適用FAIL**。
- **背景:** fixA由来の室内背景を維持（元の無地Master背景への復帰ではない）。
- **コード確認:** ZIP内の `test01_garment_reference.py` では参照衣装 `LoadImage` を増設し、`TextEncodeQwenImageEditPlus` のpositive/negativeの両方へ`image2`を接続。衣装交換を明示したテキストも含まれる。**画像入力が無接続とは言えない。**
- **原因は未確定:** `denoise=0.65`で元衣装を維持する傾向、画像1と画像2の参照優先順位、透明マネキンや透け衣装の解釈、局所編集ノード／マスク不使用等の可能性。これらを確定原因として記録しない。
- **次の検証 T-020B（計画）:** T-020Aの保存済みAPI JSONをコピーし、`KSampler.denoise` **0.65→0.80のみ**変更してA/B比較（SaveImageの出力prefix変更は識別用途）。同一Master、衣装画像、プロンプト、モデル、Seed、Steps、CFG、構図維持指示を固定。**生成前は未判定**。顔・髪・体型・ポーズ・衣装全体の差を確認。
- **次の分岐:** T-020Bでも衣装交換が成立しない／人物逸脱が起きるなら、全画面denoiseの繰り返しより**衣装領域をマスクした局所編集**を調査。利用可能ノードはComfyUI `/object_info`で確認してから実装。PASS条件を緩めない。


## 3E. 2026-11-28 T-020B実機QA：denoise 0.80 でも衣装置換FAIL

- **生成結果名:** `Qwen_SFW_GarmentRef_T020B_Denoise080_00001_.png`（ユーザーが画像提示。Gitに画像そのものは保存しない）。
- **ユーザー判定:** NG／FAIL。「元の服装が強くでている」。
- **A/B変更:** T-020Aと比較して `KSampler.denoise` のみ `0.65 -> 0.80`（出力識別prefixも変更）。モデル・衣装参照・人物Master・Seed/steps/CFG・文章は前回保存JSONを継承する設計。実際の送信JSONのハッシュとの照合は未実施。
- **観察:** ラベンダー色の首リボン・上腕フリル・腿周囲フリルなどの参照衣装の装飾はT-020Aより増加。しかし元の淡色キャミソールとショートパンツが中心構造として残り、参照衣装の全体構造への交換はできていない。人物の顔・髪・体型・両手背面ポーズ・全身フレーミングは概ね維持。
- **判定の分離:** 人物維持はPASS、衣装装飾の部分反映あり、元衣装除去と自然な全身衣装交換はFAIL。T-020B総合FAIL。
- **確定できること:** 0.65→0.80の変更では服装全体を置き換えられない。単にdenoiseを増やせば解決するという根拠はない。
- **原因は未確定:** 元衣装の画像情報が強く残ること、参照役割の競合、透け素材の解釈、局所編集の未実装等のいずれか、または複合が考えられる。技術的原因を推測で確定しない。
- **次段階:** **T-020C：衣装領域マスクを使用する局所編集の適用可否・ノード構成調査（ACTIVE）**。元の成功fixA JSONを必ず保全し、マスクは衣装領域に限定、人物の顔・髪・四肢・背景は原則保護する。ComfyUI `/object_info` から利用できるinpaint・maskノードを確認してから新規ワークフローを作る。実画像生成・PASS判定は未実施。
- **作業境界:** T-020A/Bの失敗ワークフローを成功基準に昇格しない。顔・体型維持と衣装変更を別QA。人物の新規属性や露出を勝手に補完しない。


## 3F. T-020C ノード存在確認（ユーザー実機 /object_info）

- **確認入力:** ユーザーが実機ComfyUI `GET /object_info` から抽出したノード名一覧（2026-11-28）。
- **存在確認済み:** `LoadImageMask`, `ImageToMask`, `GrowMask`, `FeatherMask`, `MaskPreview`, `SetLatentNoiseMask`, `VAEEncodeForInpaint`, `InpaintModelConditioning`, `ImageCompositeMasked`, `LatentCompositeMasked`, `SAM3_Detect`, `SAM3_TrackToMask`, `ConditioningSetMask` 等。
- **判断:** マスク作成・潜在マスク・インペイントに関連するノード群が登録されているので**T-020Cは技術的調査を継続可能**。登録名があるだけではQwen Image Edit 2511との互換性・マスクの実効性・SAM3の必要モデル存在は未確認。
- **次のチェック:** 上記の主要ノードについて `/object_info/<node>` の required/optional 入力および出力型を取得して、`fixA` の参照接続との適合性を確認。マスク対象は元衣装のある上半身・腰回りを中心にし、顔・髪・手・脚・背景を保護する方針。**ユーザーの画像にない領域をAIが勝手に作り込まない**。
- **段階:** T-020C／ノード一覧の存在確認=完了、ノード接続仕様確認=未実施、実機マスク生成・衣装置換=未実施。結果画像とユーザーQAなしにPASSとしない。


## 3G. T-020C 入出力仕様確認完了（次は局所編集A/B）

**状態:** ノード入出力インターフェースの存在・型確認＝DONE。**マスク実体と実機生成は未実施、T-020C QA未判定**。

2026-11-28、ユーザーComfyUIの `GET /object_info/<node>` 実行結果（直接提示）：
- `LoadImageMask`: required `image, channel`; output `MASK`。
- `SetLatentNoiseMask`: required `samples, mask`; output `LATENT`。
- `VAEEncodeForInpaint`: required `pixels, vae, mask, grow_mask_by`; output `LATENT`。
- `InpaintModelConditioning`: required `positive, negative, vae, pixels, mask, noise_mask`; outputs `CONDITIONING, CONDITIONING, LATENT`。
- `ImageCompositeMasked`: required `destination, source, x, y, resize_source`; optional `mask`; output `IMAGE`。
- `GrowMask`: required `mask, expand, tapered_corners`; output `MASK`。
- `FeatherMask`: required `mask, left, top, right, bottom`; output `MASK`。
- `MaskPreview`: required `mask`; output `MASK`。
- `SAM3_Detect`: required `model, image, threshold, refine_iterations, individual_masks`; optional `conditioning, bboxes, positive_coords, negative_coords`; outputs `MASK, BOUNDING_BOX`。
- `SAM3_TrackToMask`: required `track_data, object_indices`; output `MASK`。

**初期実験案（まだ未実行）:** `LoadImageMask`（白＝編集、黒＝保護のマスクを指定画像と同寸で用意） → `SetLatentNoiseMask`（従来の `VAEEncode` 潜在出力と接続） → 既存 `KSampler.latent_image` に接続。Qwenの `TextEncodeQwenImageEditPlus.image1` は元Master、`image2` は衣装参照のまま保持。実装は元JSONのコピーで行う。**Qwen編集モデルで有効に作用するかは画像生成で判定**。

**重要:** 手動マスクの輪郭が衣装だけでなく肌・髪・背景を広く覆うと、人物維持の比較が無効になる。まず元衣装のトップス／ショートパンツ領域に合わせてマスクを作り、実際のマスク画像を目視確認する。元の服を取り除く目的と、透け素材の再現およびSFW維持の関係は別評価。生成成功とPASS判定を混同しない。

次はマスクPNGの同寸・配色・位置確認、次にローカルで保存済みのT-020A API JSONの複製へマスクノード追加。その後、出力をT-020A/Bと比較。

## 3H. T-020C マスク不足エラーの対応（マスクキットを提供）

- **ユーザー実行時エラー:** `FILE_NOT_FOUND: D:\AI\real-photo-generator\assets\references\masks\garment_mask.png`。ComfyUIモデル・ノードが失敗したのではなく、マスクPNG未配置の事前検査で停止。
- **対応:** Master候補（752×1392）の衣装範囲から手動近似の白黒マスクを作成。`T020C_GarmentMask_Kit.zip`（マスク雛形・赤色範囲プレビュー・ローカルMasterからマスクを出力するPythonスクリプト・README）を会話で提供。ZIP内のファイル一覧を検査し、Pythonスクリプトのマスク・レビューPNG生成をテスト済み。
- **検証待ち:** ユーザーPCでZIP展開、マスク実体配置、`garment_mask_preview.png` の目視確認。マスクは元衣装と新衣装の想定配置の近似であり、上腕・太腿や一部背景が含まれる。**正確な衣服領域抽出ではない**。参照Masterが異なる場合は適用不可。マスク範囲確認前にT-020Cを走らせない。
- **Gitに画像やZIPを置かない。** T-020Cの生成・QAは未実施のまま。

## 3I. T-020C マスク生成スクリプト終了コード1の診断と回避

- **ユーザー結果:** `MASK_CREATION_FAILED: 1`。PowerShell側でラップした終了コードであり、**Python内部の正確な例外内容はまだ未確認**。生成が成功したとは扱わない。
- **キット実体を再確認:** ZIPには `install_and_preview.py` と、既に作成された `mask_template_752x1392.png`、`mask_preview_reference.png` が含まれる。スクリプトは既存ファイル・アスペクト比の違い・Pythonの画像ライブラリエラー等で停止し得る。どれが原因かはログ未取得。
- **次の回復手順:** ユーザーPCのMaster画像とマスクテンプレートがいずれも752×1392であることを検証し、**Pythonを使わずに**ZIPから展開済みのマスクPNGとプレビューを`assets/references/masks/`へ配置する1行PowerShellを案内。既存の片方だけがある場合は上書きせず停止する。生成前にプレビューで範囲確認を要求。
- **作業位置:** T-020Cマスク配置・事前目視確認。**ComfyUI Inpaint生成未実施、QA未判定**。手動マスクは上腕・腿・背景も一部含み、結果の人物維持リスクを警告する。


## 3J. T-020C マスク解像度不一致・修正版V2の検証

- **ユーザーエラー:** `IMAGE_DIMENSIONS_MISMATCH`。前回渡したPowerShellはテンプレート（752×1392）だけでなく、**ローカル人物Masterも752×1392であることを要求**しており、ユーザーのMasterと一致しない場合には必ず停止する。前回の「修正」は成立していなかった。
- **調査:** 添付されたマスク雛形の実寸は**752×1392**と確認。ローカルMasterの正確な幅・高さは未取得（GitからユーザーPCのファイルにはアクセスできない）。従って実際の構図一致は未確認。
- **対応キット:** `T020C_GarmentMask_Kit_V2.zip` は `install_and_preview_v2.py` と元マスク雛形、READMEを収録。Master画像の実寸を動的取得し、マスクをその幅×高さに最近傍スケールして、**実際のMasterとの赤色重ね合わせプレビュー**を作る。マスク/プレビューは既存なら上書き拒否。ComfyUIへの生成送信は行わない。
- **テストした内容:** ユーザーPCとは別環境で752×1392、768×1344、1024×1536、832×1216の各画像を模した入力を用いて、出力マスクとプレビューが入力画像と同寸になることを確認。**ユーザーPCの実寸・ポーズ・衣装位置については検証していない**。
- **注意:** 異なる縦横比を伸縮しても実際の人物・衣装領域との一致は保証されない。生成前にプレビューを表示して、赤い領域が正しいかユーザー確認を得る。**ズレている場合はT-020C生成へ進めない**。必要に応じて実際のMaster上でマスクの描き直しが必要。
- **現状:** T-020Cマスク準備の技術的対処は用意済み。実機配置・マスク位置承認・画像生成は未実施。

## 3K. T-020D ユーザー指摘に基づくQA訂正（衣装を着せる要件）

- **ユーザーの明示的要求（優先）:** 参照衣装を人物Masterに**実際に着せている状態**で生成する。元の衣服を半透明にする／新衣装を上から被せる／人体やマネキンの透明構造を重ねる表現は、衣装の色や装飾が一致しても**FAIL**。
- **T-020Dユーザー最終判定:** NG。首が不自然に長い・身体全体のプロポーションが不自然・元衣装を透かして別衣装を被せたように見える。旧評価「元の部屋着残留が大幅改善」「顔や髪が似ている」はこれらの**人体・着衣FAILを相殺しない**。
- **QAを分ける:** (1) 顔だけではないMasterの頭身・首長・肩幅・胸郭・胴体・骨盤・四肢接続、(2) 衣装が正しく身体を包むトポロジー、縫い目・開口部・布の厚み・張力・重力・レイヤー、(3) 参照衣装の意匠再現、(4) 透け素材の布表現と人体ガラス化／マネキン転写の区別、(5) 人物の全身・ポーズ・カメラ/背景。
- **重要な区別:** 参照衣装の透明・シアー素材自体はNGとしない。NGは身体や元衣服が透明マネキン的な構造になり、着用関係が破綻したこと。モデルが透明マネキンを転写したかは**原因未確定**、画像からの観察と因果仮説を分ける。
- **前回提案の取り消し:** 「人物Masterの顔・髪だけ切り抜いて対処する」案を**採用しない**。全身骨格・体格が破綻する問題を解消する検証ではなく、人物維持条件をむしろ失う可能性がある。
- **次の作業状態:** T-020D総合FAIL。T-020Eは**衣装の実際の着用と全身人体構造を維持する生成方式の再設計・検証**。原因が未確定のままネガティブを強める、クロップだけで解決したと扱う、透明衣装を不透明へ勝手に変更することは禁止。生成済み画像や提示されたコードに基づく問題の切り分けから開始。

## 3L. T-020E 正式QAゲート・次の技術棚卸し

- **ユーザーの再確認:** T-020E以降は「①Masterの身体全体を保持」「②参照衣装を実際に着せる」を両方必須とし、人体の不自然さ／旧衣装の透過・新衣装の重ね描きは**無条件FAIL**。衣装が参照に似ていても総合PASS扱いしない。
- **固定QA仕様:** [GARMENT_WEARING_GATE.md](../quality/GARMENT_WEARING_GATE.md) を追加。人物の首・肩・胸郭・胴・骨盤・手足、衣服の構造・接触・縫い目・重量感・透け素材と透明身体の区別、入力ロールを明文化。
- **今回の確認:** T-020Dで `EmptyLatentImage` を使っただけでは実着用・身体維持を満たせないことが実画像で確認済み。前回の「顔と髪だけ切り抜く」提案は撤回。元MasterへのInpaintを再開しない。
- **現在位置:** T-020E / **E-01 モデル・ノード棚卸し（ACTIVE、ユーザーPCの結果待ち）**。LoRA、ControlNet、diffusion_models、対応ノードの認識を確認してから、実装可能性と条件に基づきE-02のワークフロー候補を選ぶ。
- **注意:** 仮に衣装専用のVirtual Try-Onワークフローが存在しても、元画像を編集するタイプは今回の「1から生成」条件に適合するとは扱わない。ローカル導入とライセンス・VRAM・モデル互換性も未確認。

## 3M. T-020E / E-01モデル・ノード棚卸し結果（実機）

- **入力:** 2026-11-28ユーザー実機でComfyUI `/models` と `/object_info` を照会した結果。
- `loras`: 合計2件。条件に一致するのは `Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors` だけ。衣装専用LoRAは名称から確認できない（該当しない1件の名称は未取得）。
- `controlnet`: 合計1件、`SDXL\controlnet-openpose-sdxl-1.0\diffusion_pytorch_model.safetensors`。**SDXL OpenPose用**でありQwen Editへ直接流用できると判断しない。
- `diffusion_models`: 合計7件、条件に一致したモデル `qwen_image_2.1_int8_convrot.safetensors`、`qwen_image_edit_2511_int8_convrot.safetensors`。残り5件の詳細未取得。
- `checkpoints`: 合計4件だがフィルタ条件に該当せず名称未開示。**SDXLが含まれるかはユーザーの今回の一覧だけでは未確定**（過去会話でRealVisXL/Juggernaut認識履歴あり、現在の実機にあるかは一覧の再取得が必要）。
- **ノード:** `ControlNetLoader`, `ControlNetApplyAdvanced`, `OpenposePreprocessor`, `DensePosePreprocessor`, `DepthAnythingPreprocessor`, `BriaVirtualTryOn`, `KlingTryOnNode` 等を認識。
- **重要な制約:** `BriaVirtualTryOn` は外部API利用のComfyUIパートナーノードと公開資料に記載。ノードが存在してもローカル無料推論・対応モデルがあることを意味しない。Klingもローカルモデルとしてカウントしない。現状、ローカル衣装専用try-onパイプラインの導入は確認できていない。
- **次の段階:** **E-02＝候補構成の適合検査（ACTIVE）**。まずcheckpoint実名と`ControlNetLoader`、`ControlNetApplyAdvanced`、`OpenposePreprocessor`、`CheckpointLoaderSimple` の入出力仕様を取得。SDXLによる新規生成＋骨格制御を「身体形状テスト」の候補として評価する。**OpenPoseだけではMasterの体型や衣装の物理的着用が保証できない**。衣装画像参照は別の独立した技術ゲート。
- **不変のQA:** [GARMENT_WEARING_GATE.md](../quality/GARMENT_WEARING_GATE.md) に従い、(G1) 首・肩・胸郭・全身身体比率の維持、(G2) 布が実際に着用された物理関係の成立を**同時必須**とする。過去のT-020D失敗画像を成功基準に昇格させない。

## 3N. T-020E E-02：SDXLモデル・ノード接続の実機確認

**状態：E-02 一部完了（モデル・ノード名確認）、参照分離方式の適合確認は継続中。生成・G1/G2 QAは未実施。**

ユーザーの実機結果（2026-11-28）：

- `checkpoints`（4件）：`Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors`、`RealVisXL_V5.0_fp16.safetensors`、`sd_xl_base_1.0.safetensors`、`waiIllustriousSDXL_v170.safetensors`。
- `loras`（2件）：`Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors`、`local-rag\rendering\matte_dimensional_anime_v1.safetensors`。衣装専用LoRAの導入は名前上は未確認。
- `diffusion_models`（7件）：`flux-2-klein-base-4b-fp8.safetensors`、`flux3-image-klein-base-int8-convrot.safetensors`、`flux3-image-klein-int8-convrot.safetensors`、`omnigen2_fp16.safetensors`、`qwen_image_2.1_int8_convrot.safetensors`、`qwen_image_edit_2511_int8_convrot.safetensors`、`z_image_turbo_bf16.safetensors`。
- `CheckpointLoaderSimple`: required `ckpt_name`; outputs MODEL, CLIP, VAE。
- `ControlNetLoader`: required `control_net_name`; output CONTROL_NET。
- `ControlNetApplyAdvanced`: required `positive,negative,control_net,image,strength,start_percent,end_percent`; outputs CONDITIONING×2。
- `OpenposePreprocessor`: required `image`; outputs IMAGE,POSE_KEYPOINT。
- `EmptyLatentImage`: required `width,height,batch_size`; output LATENT。
- `CLIPTextEncode`: required `text,clip`; output CONDITIONING。
- 先に確認した `controlnet` はSDXL OpenPose用1件。

**結論と制限:** RealVisXL、Juggernaut、SDXLベース＋SDXL OpenPose ControlNetによる**新規生成と2D姿勢誘導**の接続候補は揃っている。ただしOpenPoseはMasterの首・胸郭・体積・全身寸法の固定を保証しない。衣装参照画像から**衣服の着用構造だけを抽出して実際に着せる**ためのローカルモデル／参照アダプターもまだ確認できていない。これを満たしたと誤記しない。

**次の読取専用の調査:** `/object_info` で `IPAdapter`, `InstantID`, `PuLID`, `PhotoMaker`, `Reference`, `VirtualTryOn`, `garment`, `cloth` 関連ノードの実在・種類と、`/models/clip_vision`, `/models/ipadapter` を確認する。外部APIノードはローカル推論候補から除外。検証に使うノードとモデルを確定してから実画像の局所QAを開始し、G1・G2の両方を必須とする。

## 3O. T-020E / E-02：参照アダプター系ノード確認（実機）

**実機調査結果（ユーザー提示、2026-11-28）:** `REFERENCE_NODES COUNT=76`。主に `IPAdapter`, `IPAdapterAdvanced`, `IPAdapterUnifiedLoader`, `IPAdapterUnifiedLoaderCommunity`, `IPAdapterUnifiedLoaderFaceID`, `IPAdapterModelLoader`, `IPAdapterRegionalConditioning`, `IPAdapterPreciseComposition`, `IPAdapterPreciseStyleTransfer`, `IPAdapterFaceID`, `IPAdapterInsightFaceLoader`, `PhotoMakerLoader`, `PhotoMakerEncode` の名称を確認。外部API系 `BriaVirtualTryOn`, `KlingTryOnNode` などはローカル実行モデル導入の証拠ではない。

**判定:** アダプターノードの導入は**確認済み**。必要なIP-Adapterモデル、CLIP Visionモデル、FaceID/PhotoMaker重みの存在とSDXLモデル適合性、衣装画像からの着用構造生成能力は**未確認**。直近のユーザー提供出力には `MODEL: clip_vision` 等のファイル名・件数が含まれていないため、存在を推測して埋めない。

**次:** 読み取り専用で `GET /models/ipadapter`, `GET /models/clip_vision`、必要なら `/models/photomaker` と `/object_info/IPAdapterUnifiedLoader`, `/object_info/IPAdapterAdvanced`, `/object_info/IPAdapterRegionalConditioning`, `/object_info/CLIPVisionLoader` の入出力を確認。その結果を根拠に候補構成を絞る。重みのダウンロード・ノード追加・生成試験はまだ行わない。

**変更不可の品質ゲート:** [GARMENT_WEARING_GATE.md](../quality/GARMENT_WEARING_GATE.md) の G1（首・体幹・四肢を含むMaster全身維持）と G2（服が物理的に着用された状態）を両方満たす必要がある。衣装参照に似た模様の重ね描き、元衣装の透過、マネキン構造の転写はFAIL。

## 3P. T-020E / E-02：SDXL IP-Adapterモデル重みの適合確認

**ユーザー実機照会結果（2026-11-28）**
- `/models/ipadapter`：1件 `ip-adapter-plus_sdxl_vit-h.safetensors`
- `/models/clip_vision`：1件 `CLIP-ViT-H-14-laion2B-s32B-b79K.safetensors`
- `/models/photomaker`：`COUNT=1`だがモデル名が空行のため重み実在確認不能。PhotoMakerは試験候補にしない。
- `IPAdapterUnifiedLoader`: required `model,preset`; optional `ipadapter`; output `MODEL,IPADAPTER`
- `IPAdapterAdvanced`: required `model,ipadapter,image,weight,weight_type,combine_embeds,start_at,end_at,embeds_scaling`; optional `image_negative,attn_mask,clip_vision`; output `MODEL`
- `IPAdapterRegionalConditioning`: required `image,image_weight,prompt_weight,weight_type,start_at,end_at`; optional `mask,positive,negative`; outputs `IPADAPTER_PARAMS,CONDITIONING,CONDITIONING`
- `IPAdapterModelLoader`: required `ipadapter_file`; output `IPADAPTER`。
- `CLIPVisionLoader`: required `clip_name`; output `CLIP_VISION`。
- `PhotoMakerLoader`: required `photomaker_model_name`; output `PHOTOMAKER`。

**評価:** 導入済みIP-Adapter Plus SDXL ViT-HとCLIP ViT-Hのファイル名は公式cubiq/ComfyUI_IPAdapter_plusの対応表と一致。**SDXL画像参照パイプラインの導入条件が揃った**。ロード成功・モデル互換の実行結果・人物維持・服の実際の着用は**まだ未確認**。

**重要:** IP-Adapter Plusは一般的な画像条件付けであり、衣装専用の3D/布着用制御ではない。特に透明マネキンに衣装が着いている参照画像を直接条件化すると、マネキン材質・身体形状が混入する懸念があり、T-020D総合FAILの観察を踏まえ**未検証のまま完成ワークフローに採用しない**。通常のVirtual Try-OnではMasterを編集する方式もあるため新規潜在生成条件との適合に注意。

**E-03への引継ぎ：** まず、**空の潜在画像＋RealVisXL＋SDXL OpenPose（Masterから姿勢のみ抽出）＋衣装の文章説明**で、G1に関係する身体解剖の自然さとG2の「布を着用している」状態がそもそも成立するか、最小限の診断テストを実施。その出力は**Master同一性と衣装画像の正確な再現を検証していない**ため総合PASSにできない。診断結果が自然なら、Master全身参照と衣装画像参照の独立制御およびマネキン転写抑止を追加試験する。1回に変更する要素を限定する。検証ではマスクや元画像VAEEncodeの局所編集を使わない。

## 3Q. T-020E E-03A 総合FAIL・設計上の逸脱（ユーザー指摘）

**ユーザー評価：NG（2026-11-28）。** 出力 `T020E_E03A_SDXL_OpenPose_TextWear_00001_.png` では、人物Masterとは別人（顔・髪・肌色・体格が異なる）、衣装参照とも異なる不透明なラベンダー色ブラウス＋スカートを生成。ユーザーは「作業時短・意図に合う出力」の目標に反し、作業の方針転換と出力の大幅な逸脱を問題視。結果をPASSとして扱わない。

**重要：画像生成の偶発的失敗ではなく、提案したワークフローの設計上の欠落。**
- 実際のノード接続：Master `LoadImage` → `OpenposePreprocessor` → `ControlNetApplyAdvanced`（姿勢情報に限定）。Masterの同一性・髪・顔・体格に必要な画像参照制御はKSamplerに接続されていない。
- 衣装画像はLoadImageされず、英語の衣装テキストだけをCLIPTextEncodeに渡した。よって**Master/衣装の両参照を適用した試験ではない**。
- モデルもQwen Image Edit→RealVisXLへ変更し、Master参照・衣装参照の有無・画像プロンプトなど複数変数を同時変更。先行テストからの一要因比較になっていない。
- 前提の「構成要素を外して段階診断すれば問題を切り分けられる」は、ユーザーのG1全身Master維持・G2衣装着用・衣装参照適用がすべて実行上の必須要件という優先順位を見落としていた。OpenPoseは主に2D骨格誘導で顔/衣装を保全しない。今回の完全な別人出力は構成から予見可能で、不必要な実機生成を行わせた責任はワークフローを提示した側にある。

**QA再判定**
- マスター人物同一性：**FAIL／そもそも画像参照実装なし**
- 指定衣装の画像参照・意匠再現：**FAIL／そもそも入力なし**
- 全身Master比率維持：**FAIL／比率を固定する経路なし**
- 実際の着用構造：今回の**別衣装について**自然な描写が一部見られても、指定衣装の着用成功とは扱えず**FAIL**
- E-03Aは**要件適合の候補試験として無効**。SDXL＋ControlNetがノード的に動くことだけは観察された。

**次の方針（まだ生成しない）**
1. ユーザー確定要件をワークフローの必須条件として先に構造検査（新規潜在、全身Master人物参照、衣装画像参照、それらを区別する制御、既知の失敗パターン抑止）。
2. **IPAdapter Plus SDXL ViT-H＋CLIP Visionは重み存在を確認済み**だが、1つのグローバルアダプターで人物Masterと衣装画像を混ぜることは衣装着用保証としない。身体構造維持と衣装着用の実証が必要。
3. 先行で相対的に人物性が維持されたQwen fixA／T-020Dから得た観察を捨てず、構成を変更するなら変更要因と保全事項を記録する。局所編集への無断復帰は行わない。
4. ユーザーが要求した失敗原因の説明・責任明確化を優先し、根拠未確認の新しい1行生成コマンドを押し付けない。根拠が不足すれば機能・モデル能力の未確定を明記。
5. [GARMENT_WEARING_GATE.md](../quality/GARMENT_WEARING_GATE.md) のG1＋G2（両方必須）は変更しない。要件を試験の便宜に合わせて下げない。

## 3R. 作業時間の浪費と生成前静的ゲートの実装

- **ユーザーからの指摘（2026-11-28）:** 複数日にわたる失敗で、再生成・コマンド実行・エラー処理・画像QA・要件再説明に多大な時間を使っている。**実拘束時間の開始・終了ログがないため正確な時間数は不明**。根拠なく推定値を作らない。
- **現時点の成果を訂正:** ユーザーは既にローカルモデルの高品質画像出力を確認済み。現課題は**Masterの全身同一性＋指定衣装を実際に着用する複合制御**であり、モデル全般が低品質だと混同しない。
- **具体的な実装改善:** `scripts/validate_t020e_workflow.py` を作成。Master/衣装それぞれの参照経路、MasterのOpenPose条件、EmptyLatentImageからの新規生成を静的検査する。欠落時は終了コード2でREJECT。直近E-03Aの構造的欠陥（Masterはポーズのみ、衣装画像参照なし）を検出する。
- **回帰テスト:** `tests/unit/test_validate_t020e_workflow.py` に8ケース追加（E-03A欠落、衣装なし、ポーズなし、画像編集潜在、不一致ファイル、無効アダプター、無効ControlNet、構造整合ケース）。コンテナ環境で同等の8ケースがPASS。Git上のテストについてはユーザー実機実行未確認。
- **品質ゲートと制限:** 詳細は [GARMENT_WEARING_GATE.md](../quality/GARMENT_WEARING_GATE.md)。構造検査PASSは**完成画像QA PASSではない**。人体の首・全身寸法維持と正しい着衣状態は視覚検証が必要。既存PowerShell直送をツールが自動的に遮断するわけではないので、今後提示する生成手順の前段階で検査を組み込み、構造FAILなら生成実行を要求しない。
- **次の状態:** **新しい生成コマンドは未発行**。繰り返し失敗を止めた状態で、既存高品質生成の成果を保全し、全身Masterと衣装制御の構造・モデル対応を検討する。費用増加を前提としない。
