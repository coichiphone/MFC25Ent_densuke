# MFC25Ent_densuke

松丘FC 出欠管理アプリ（`index.html` 単体で動作）。

## Firebase（Firestore）連携

複数端末でデータを共有するため、Firestore にリアルタイム同期します。
`index.html` 末尾の `FIREBASE_CONFIG` が空のあいだは、従来どおり端末内（localStorage）だけで動作します。

### セットアップ
1. [Firebaseコンソール](https://console.firebase.google.com/) でプロジェクトを作成
2. 「Firestore Database」を作成（本番モード・リージョンは `asia-northeast1` 推奨）
3. 「ルール」に `firestore.rules` の内容を貼り付けて公開
4. 「プロジェクトの設定 > マイアプリ」で Web アプリを追加し、表示された設定値を `index.html` の `FIREBASE_CONFIG` に貼り付け
5. **管理者の端末（現在のデータが入っている端末）で最初に開く** → クラウドが空なら、そのデータが初期データとして登録されます
6. 以降、他の端末はクラウドのデータを読み込みます

### データ構造
| パス | 内容 |
|---|---|
| `team/meta` | アプリ名・入力期限日数・Googleカレンダー設定 |
| `team/logo` | ロゴ画像（base64） |
| `team/users` / `team/members` / `team/events` | ログイン情報 / 選手・コーチ / 予定 |
| `att/{eventId}` | 予定ごとの出欠。フィールド名が member id（本人の分だけ書くので同時入力でも上書きしません） |

### 注意（セキュリティ）
- 現状は Firebase Auth を使わない構成のため、ルールは全開放です。PIN も `team/users` に平文で入ります。
  チーム外には URL を共有しないでください。厳密に守る場合は Firebase Auth + ルールの導入が必要です。
- 初回同期が終わるまでは書き込みません（古い端末のデータでクラウドを上書きしないため）。
