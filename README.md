# cp-heuristics-adapter

AtCoder Heuristics Contest (AHC) の各種操作を自動化することを目標にしたツール。

## 対応言語

- [x] C++
- [x] Python
- [ ] ...

## インストール

```bash
cd /path/to/install
git clone git@github.com:suisen-cp/cp-heuristics-adapter.git
cd /path/to/install/cp-heuristics-adapter
pip install .
```

## アンインストール

```bash
pip uninstall cp-heuristics-adapter
```

## Usage

このツールを利用した AHC プロジェクトの構造のイメージ:

```text
.
├── .cp-heuristics-adapter  # 設定ファイル
│   ├── cpp_config.toml    # C++ の設定ファイル
│   └── py_config.toml     # Python の設定ファイル
├── your_solver.cpp         # C++ のソルバー
├── your_solver.py          # Python のソルバー
├── in                      # 入力ファイル
│   ├── 0000.txt
│   ├── 0001.txt
│   └── 0002.txt
├── out                     # 出力ファイル
│   ├── 0000.txt
│   ├── 0001.txt
│   └── 0002.txt
└── scores                  # スコアファイル
    ├── scores_20240617-000049.summary.txt
    ├── scores_20240617-000049.txt
    ├── scores_20240617-000223.summary.txt
    └── scores_20240617-000223.txt
```

### `cp-heuristics-adapter init`

プロジェクトを初期化する。

- `-p`, `--path`: プロジェクトディレクトリのパス
- `--overwrite`: 既存のファイルを上書きする

```text
usage: cp-heuristics-adapter init [-h] [-p PATH] [--overwrite]

Initialize a new project

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to project directory
  --overwrite           Overwrite existing files
```

### `cp-heuristics-adapter clean`

プロジェクトをクリーンアップする。

- `-p`, `--path`: プロジェクトディレクトリのパス

```text
usage: cp-heuristics-adapter clean [-h] [-p PATH]

Clean the project

options:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Path to project directory
```

### `cp-heuristics-adapter run`

プログラムを実行する。

- `source`: ソースファイルのパス
  - 通常のコードに加えて、**コマンドライン引数の 1 番目 (0-indexed) にスコアの出力先が与えられるので、そこにスコアを 1 行で出力する処理を追加する必要がある**。
  - [C++ の例](templates/example_solver.cpp)
  - [Python の例](templates/example_solver.py)
- `number`: 実行するケースの数
- `-b`, `--build-mode`: ビルドモード (デフォルトは `debug`)
  - `debug`: デバッグビルド
  - `release`: リリースビルド
  - 例えば C++ の場合、`debug` モードでは `-fsanitize=address` を有効にし、`release` モードでは `-O2` を有効にするという使い分けを想定
  - 各ビルドモードの設定は `.cp-heuristics-adapter` ディレクトリ内の設定ファイルに記述
- `-t`, `--time-limit`: 実行時間制限 (デフォルトは 2.0 秒)
- `-s`, `--score-type`: スコアの種類 (デフォルトは `plain`)
  - `plain`: 通常のスコア
  - `log`: スコアの対数
  - 相対スコアの場合は `log` を使うとよい (と思われる)

```text
usage: cp-heuristics-adapter run [-h] [-b {debug,release}] [-t TIME_LIMIT] [-s {plain,log}] source number

Run the program

positional arguments:
  source                Path to source file.
  number                Number of cases to run.

options:
  -h, --help            show this help message and exit
  -b {debug,release}, --build-mode {debug,release}
                        Build mode. Default is 'debug'.
  -t TIME_LIMIT, --time-limit TIME_LIMIT
                        Time limit for execution. Default is 2.0 seconds.
  -s {plain,log}, --score-type {plain,log}
                        Type of score. If a standings is calculated by the relative score, it is recommended to use 'log' type.
                        Default is 'plain'.
```
