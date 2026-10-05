# oh-my-pi — TUI: классификация UI-элементов и назначение модулей

Изучено: `/home/prog7/home/dev/contrib/clones/oh-my-pi/` (omp, форк Pi от
Stencil Labs; агент-кодер на TypeScript/Bun). Объект — пакет
`packages/tui` (`@oh-my-pi/pi-tui`, ~400 TS-файлов). Дата: 2026-10-04.

## 1. Что это

Двухслойный терминальный UI-фреймворк:

1. **ANSI-слой** — дифференциальный рендеринг: каждый компонент реализует
   `render(width): readonly string[]` (строки = физические строки терминала);
   `TUI` считает diff-кадры, использует synchronized output (CSI 2026),
   троттлит рендер от 30 fps до ~5 fps под нагрузкой, ставит аппаратный
   курсор по маркеру `CURSOR_MARKER` в тексте.
2. **Native-слой (TSP, Tern Surface Protocol)** — компонент дополнительно
   может вернуть `describe()` → семантическое дерево `NativeNode`
   (`card`/`row`/`list`/`kbd`/`picker`/…), которое уходит по APC-каналу в
   нативный бэкенд терминала. ANSI-карточка и TSP-вью обязаны показывать
   одно и то же.

Контракты: `Component` (`render`/`handleInput`/`invalidate`/`dispose`),
`Focusable` (фокус + курсор), `MouseRoutable` (`routeMouse`), компоненты
лэйаута владеют геометрией детей и транслируют координаты мыши.

Главный потребитель — `packages/coding-agent` (основной экран чата собирает
`Composer` из `prompt/`). Внутренние доки репо: `docs/tui.md`,
`docs/tui-core-renderer.md`, `docs/tui-runtime-internals.md`, `docs/theme.md`,
`docs/keybindings.md`.

## 2. Карта каталогов `packages/tui/src`

| Каталог | Роль | Файлов |
|---|---|---|
| `components/` (+`layout/`, `composer/`) | базовые примитивы, лэйаут, стили композера | ~42 |
| `prompt/` | композер ввода: редактор, автодополнения, чипы, очередь | ~35 |
| `chrome/` | «хром» чата: рамки сообщений, диффы, тосты, QR, подсказки | ~29 |
| `chat/` | компоненты сообщений транскрипта | ~35 |
| `tools/` | рендереры вывода инструментов агента | ~60 |
| `overlays/` | диалоги/пикеры/панели поверх экрана | ~62 |
| `status-line/` | статус-лайн: сегменты, пресеты, футер | ~14 |
| `render/` | переиспользуемые рендер-компоненты (карточки, списки, код) | ~14 |
| `apps/` | полноэкранные приложения | ~14 |
| `setup/` (+`scenes/`) | онбординг-визард и сплэш | ~13 |
| `native/` | TSP-слой: бэкенд, кодирование, reconcile | ~15 |
| `theme/` | темы, цвета, символы, shimmer | ~19 |
| корень | ядро: рендер-цикл, терминал, ввод, протоколы | ~35 |

## 3. Ядро фреймворка (корень src)

- **`tui.ts`** — класс `TUI`: рендер-цикл, стек оверлеев (`OverlayHandle`),
  фокус-менеджмент, позиционирование курсора, коалесценция SGR,
  DECCARA-оптимизация фонов, бюджет inline-изображений, alternatescreen,
  адаптивный троттлинг, CPR-зонд при ресайзе, native-бэкенд.
- **`terminal.ts`** — `Terminal`/`ProcessTerminal`: raw-режим, SIGWINCH,
  emergency-restore, backpressure-вытеснение stdout, off-thread pump,
  probes (OSC 11, Mode 2031, DECRQM, Glyph, TSP). `active-terminal.ts` —
  singleton активного терминала для out-of-band escape (title, OSC 52).
- **`terminal-capabilities.ts`** — детект терминала/возможностей (kitty,
  ghostty, wezterm, iterm2, vscode…): графические протоколы, hyperlinks
  OSC 8, styled underlines, notifications (OSC 99/9), ширины Hangul.
- **`stdin-buffer.ts`** — сборка полных escape-последовательностей из
  кусков, bracketed paste с watchdog'ами и лимитами, torn-payload discard.
- **Ввод**: `keys.ts` (Kitty CSI-u, modifyOtherKeys, key-release),
  `keybindings.ts` + `app-keybindings.ts` (28+ действий, конфиг
  keybindings.yml, миграции) + `keybinding-matchers.ts`; `vim.ts`
  (modal editing: insert/normal/visual, операторы, jujutsu undo),
  `kill-ring.ts` (emacs kill-ring, yank-pop); `bracketed-paste.ts`;
  `mouse.ts` (SGR mouse, роутинг); `windows-input-mode.ts`,
  `windows-altgr.ts` (ConPTY/AltGr-восстановление).
- **Поиск/дополнение**: `fuzzy.ts` (scoring), `autocomplete.ts`
  (пути: `@` repo-wide, `./`, `~/`).
- **Графика/типографика**: `glyph-protocol.ts` (APC-протокол нативных
  глифов, бандл outline-шрифтов), `kitty-graphics.ts` (unicode
  placeholder-плейсмент картинок), `latex-block.ts` (2D-layout display-
  формул: дроби, матрицы, радикалы), `latex-to-unicode.ts` (inline math).
- **Служебные**: `tmux.ts` (passthrough), `desktop-notify.ts` (D-Bus
  notify-send), `space-hold.ts` (push-to-talk), `loop-watchdog.ts`
  (детект блокировок event loop), `ttyid.ts`, `debug-server.ts`
  (TCP-инспектор TUI: tree/paint/inject), `thinking.ts` (уровни),
  `symbols.ts` (пресеты символов), `hotkeys-markdown.ts`,
  `key-hint-format.ts`, `lang-from-path.ts`, `terminal-multiplexer.ts`.

## 4. Классификация UI-элементов

### 4.1 Текст и статика

| Элемент | Файл (`components/`) | Назначение |
|---|---|---|
| `Text` | text.ts | текстовый блок |
| `TruncatedText` | truncated-text.ts | текст с обрезкой по ширине |
| `Markdown` | markdown.ts | полный MD-рендер (код, таблицы, ссылки, LaTeX); ~2000 строк, кэш рендера |
| `Box` | box.ts | контейнер с рамкой/отступами |
| `Section` | section.ts | контейнер с заголовком |
| `Spacer` | spacer.ts | вертикальный/горизонтальный зазор |
| `Disclosure` | disclosure.ts | аккордеон: summary + lazy detail |
| `WidthAwareText` | render/width-aware-text.ts | текст, форматируемый только при известной ширине |

### 4.2 Лэйаут (`components/layout/`)

- `Stack` — вертикальный стек (alignment, gap, hit-test).
- `Row` — горизонтальный ряд.
- `SplitPane` — две панели с resizable-разделителем.
- `geometry.ts` — rect/insets/аллокация ширины, конверсия контента,
  mouse-guards; `scroll-view.ts` + `scroll-viewport.ts` — ScrollView
  (follow-tail, якоря, scrollbar-thumb) и чистые функции вьюпорта.

### 4.3 Ввод и формы

| Элемент | Файл | Назначение |
|---|---|---|
| `Input` | input.ts | однострочное поле с курсором |
| `Editor` | editor.ts | многострочный редактор: подсветка, декорации, paste, нативное описание; поверх — vim-режим |
| `Form`, `TextFormField`, `SelectFormField` | form.ts | формы с валидацией, submit/cancel, фокус-рутингом |
| `WizardStep` | wizard-step.ts | шаг визарда (строка/выбор/подтверждение/async/custom) |

### 4.4 Выбор и данные

| Элемент | Файл | Назначение |
|---|---|---|
| `SelectList` | select-list.ts | список выбора (primary/secondary текст, mouse, темы) |
| `SettingsList` | settings-list.ts | список настроек: секции, editing state, источники значений |
| `MenuSelection<T>` | menu-selection.ts | дженерик-меню поверх SelectList (адаптер+окно+activation) |
| `TabBar` | tab-bar.ts | панель вкладок |
| `TreeView` | tree-view.ts | дерево (префиксы-иконки, flatten, анцестры) |
| `Table` | table.ts | таблица (колонки/выравнивание/гибкая ширина) |
| `KeyValueList` | key-value-list.ts | пары «ключ: значение» |
| `MetricRow` | metric.ts | строка метрик (число+unit, overflow) |
| `ProgressBar` | progress-bar.ts | полоса прогресса (несколько стилей) |

### 4.5 Индикаторы и медиа

- `Loader`, `CancellableLoader` — спиннеры (тик 80 мс, варианты строк).
- `Image` — inline-картинки: Kitty/Sixel/iTerm2, бюджет, кэш, fallback.
- `chrome/qrcode.ts` — полноценный QR-генератор (byte mode, EC L/M/Q/H,
  half-block рендер); `collab-qrcode.ts` — QR deep-link коллаб-сессии.
- `chrome/countdown-timer.ts` — таймер обратного отсчёта;
  `chrome/live-board.ts` — перерисовываемая доска для non-TUI CLI-режима;
  `theme/shimmer.ts` — анимированный shimmer (sweep и KITT-сканер).

### 4.6 Композер — главный экран ввода (`components/composer/`, `prompt/`)

**8 встроенных стилей рамки** (`ComposerStyle` + registry, расширяемо
`registerComposerStyle`): `box` (скруглённая рамка, статус в границе),
`band` (powerline-полоса, купол), `claude` (линии + статус-чип, `❯`),
`pi` (линии сверху/снизу), `borderless` (голый `❯`), `rule` (одна линия),
`field` (заполненное поле с акцент-капами `▐▌`), `rail` (левая рейка `▎`).

Ядро ввода: `prompt/composer.ts` (Composer — владеет терминалом, welcome,
редактор, статус, runtime-дети) и `prompt/custom-editor.ts` (CustomEditor:
клавиши interrupt/model/thinking, чипы, magic-keyword shimmer, spell-check,
`->` очередь, `!`/`$$` shell-режим).

Обвязка: `welcome.ts` (лого+tip с интро-анимацией), `attachment-chips.ts`
(превью картинок/видео/пейстов), `queued-messages.ts` (нумерованная
очередь над редактором), `composer-hints.ts` (обучаемые подсказки в
пустом поле), `editor-top-gap.ts`, `composer-cache.ts` (SQLite-кэш для
спекулятивного первого кадра).

**Автодополнения** (`prompt/*-autocomplete.ts`): `/`-команды,
`^` — упоминания моделей, `#N` — GitHub PR/issue, `:name` — эмодзи
(+раскрытие `:-)`), `scheme://` — внутренние URL (skill://, memory://…),
ghost-text слов (`word-completion.ts`, бэкенды ngram/smollm/apple).
`magic-keywords.ts` — слова с градиентным shimmer (14 fps);
`prose-gate.ts` — отличает прозу от кода/путей для spelling/подсказок;
`macos-spelling.ts` — нативная проверка орфографии.

### 4.7 Хром чата (`chrome/`)

- Каркас транскрипта: `chat-block.ts` (жизненный цикл блока),
  `transcript-container.ts` (порядок, live-ёмкость, retirement строк).
- Сообщения: `message-frame.ts` (framed extension/hook-сообщения),
  `message-notice.ts` (toned notice-card), `message-divider.ts`.
- Вывод: `diff.ts` (ANSI + intra-line word-diff + native), `error-block.ts`
  (bounded ошибки), `streaming-panel.ts` (shell стриминговых оверлеев),
  `tool-activity.ts` (переключатель видимости tool-активности),
  `visual-truncate.ts`.
- Мелочь: `status-notice.ts` (toast 2.4 с), `overlay-box.ts` (PanelRows/
  OverlayPanel — хром диалогов), `dynamic-border.ts`, `keybinding-hints.ts`,
  `context-thresholds.ts` (уровни заполнения контекста),
  `segment-track.ts` (powerline-трек ролей/уровней), `format.ts`,
  `local-date.ts`, `form-theme.ts`, `selector-helpers.ts`.

### 4.8 Сообщения транскрипта (`chat/`)

- `user-message.ts` — пузырь пользователя: MD, чипы скиллов/моделей/файлов,
  реакции, live-steer маркер, native hover-тулбар (время/Copy/Rewind).
- `assistant-message.ts` — ответ: MD + thinking (сворачивание Ctrl+T,
  пульсирующий индикатор «Thinking…» с tok/s) + изображения + inline-ошибки
  (8 строк, expand Ctrl+O); стриминг с stable-row публикацией.
- Исполнение: `bash-execution.ts` (PTY-фрейм ` $ cmd`, tail 20 строк,
  стриминг, sixel), `eval-execution.ts` (`>>>` Python/JS),
  `tool-execution.ts` (универсальный фрейм tool call/result, кастомные
  рендереры, спиннеры), `read-tool-group.ts` (группировка read'ов,
  превью по `p1`/`p2`…).
- Служебные маркеры: `cache-invalidation-marker.ts` (cache miss),
  `served-model-marker.ts` (ответ не той моделью), `compaction-summary-*`
  (точки сжатия контекста), `stripped-tool-calls-placeholder.ts`,
  `late-diagnostics-message.ts` (LSP после правки), `ttsr-notification.ts`,
  `todo-reminder.ts`, `recap-notice.ts`, `advisor-message.ts`
  (заметки советника: blocker/concern/nit).
- Навигация по истории: `transcript-browser.ts` (fullscreen viewport
  со скроллом/follow/outline) + `transcript-outline.ts` (движок
  selectable-outline: dotted-рамка вокруг выбранного turn'а, rail `…○◉○…`).
- Прочее: `skill-message.ts` (`/skill:` callout/inline), `collab-prompt-*`,
  `background-tan-message.ts`, `hook-message.ts`, `custom-message.ts`,
  `transcript-actions.ts` (шина retry/rewind/copy),
  `display-preferences.ts` (глобальные тогглы).

### 4.9 Рендереры инструментов (`tools/`)

Контракт `ToolRenderer` (`renderCall`/`renderResult` + `describeCall`/
`describeResult` для TSP), реестр `toolRenderers` в `index.ts`; флаги
`mergeCallAndResult`, `inline`, `animatedPendingPreview`. Инфраструктура:
`result-card.ts` (кэш-карточки), `streaming-output.ts` (OutputSink,
хвостовые окна, лимиты 3000 строк/50 КБ), `json-tree.ts` (свернуто глубина 2),
`grouped-file-output.ts` (группировка по файлам + hyperlinks),
`native-view.ts` (TSP-строители), `output-meta.ts`, `line-ranges.ts`,
`terminal-output.ts`, `eval-format/` (подсветка Python/JS).

Специализированные: `bash`, `edit` (диффы с подсветкой), `write`, `read`,
`grep`, `find` (semantic, score-gauge), `glob`, `fetch`, `web-search`
(ответ+источники), `task` (дерево подагентов до 8 уровней), `todo`
(фазы римскими, зачёркивание), `goal` (бюджеты), `wait`, `memory`
(retain/recall/reflect), `think`, `ask` (опросы radio/checkbox),
`mcp`, `lsp`, `debug`, `github` (PR/issue/runs), `eval`,
`ast-grep`/`ast-edit`, `vibe` (TV-wall сессий), `bash-interactive`
(PTY-оверлей), `cfg-render`/`cfg-url` (`cfg://`), `proc-render`
(`proc://`), `xdev`/`xd-url` (`xd://`), `resolve`, `autoresearch`,
`conflict-detect`, `daemon`, `irc`, `subprocess`.

### 4.10 Статус-лайн (`status-line/`)

Двухуровневая система: `StatusLineComponent` (компонент) + 28 сегментов
(`pi`, `model`, `mode`, `git`, `pr`, `cost`, `context_pct`, `vim`,
`collab`, `stream`, токены, время, subagents…), каждый с ANSI-`render` и
native-`describe`. **7 пресетов** (default/minimal/compact/full/nerd/
ascii/custom), **6 сепараторов** (powerline/slash/pipe/block/ascii/none),
**5 лэйаутов** под форму композера (box/band/plain-full/plain-left/
plain-right), gauge контекста (off/percentage/annotated/embedded).
Живые данные: git-ветка (reftable, async), статус (TTL 10 с), PR через
`gh`, usage (фон, кэш 5 мин), разбивка контекста по категориям
(`context-usage.ts`). `footer.ts` — отдельный футер (pwd+branch/stats).
`startup.ts` — статус-лайн до появления сессии.

### 4.11 Оверлеи (`overlays/`) — сгруппированы по функции

- **Сессии и навигация**: `session-selector`, `tree-selector` (дерево
  сессий, фильтры), `rewind-selector` (откат/бранч), `history-search`
  (fuzzy по промптам), `session-info-overlay`, `move-overlay` (`/move`),
  `pause-screen`, `show-images-selector`.
- **Модели и аккаунты**: `model-browser` (каталог по ролям),
  `model-hub` (назначение моделей ролям), `model-picker`/`model-selector`,
  `login-dialog` (OAuth device-flow), `logout-account-selector`,
  `oauth-selector`, `session-account-selector`, `reset-usage-selector`.
- **Конфигурация**: `settings-selector`+`settings-defs` (полный экран
  настроек: вкладки, тогглы, enum'ы), `plugin-selector`,
  `plugin-settings`, `mcp-add-wizard`, `hook-editor`/`hook-input`/
  `hook-selector`, `queue-mode-selector`, `thinking-selector`,
  `theme-selector`, `advisor-config` (визард WATCHDOG.yml), `agents-hub`.
- **Агенты**: `agent-hub` (+`-projection`/`-renderer`/`-types`,
  `agents-hub`) — реестр агентов: дерево, метрики, live-инспекция,
  inline-чат; `agent-transcript-viewer` (транскрипт агента + send/steer),
  `agent-activity` (лента событий), `running-subagent-badge`,
  `session-observer-registry`.
- **Планы**: `plan-review-overlay` (выделение/удаление секций,
  аннотации), `plan-save-overlay`, `plan-toc` (парсер заголовков).
- **Usage/статистика**: `usage-dashboard` (heatmap, карточки провайдеров,
  лимиты), `usage-display`, `usage-row`, `stats-notice`,
  `codex-reset-fireworks` (фейерверк при сбросе квоты).
- **Спец-панели**: `ask-dialog` (мульти-вопросы от расширений, таймер),
  `btw-panel`+`btw-history*` («between the worlds» ответы с follow-up),
  `cleanse-panel`, `jobs-panel` (фоновые задачи), `omfg-panel`,
  `report-panel`, `annotation-overlay` (code review с аннотациями),
  `error-banner` (перманентный баннер над редактором), `copy-selector` +
  `copy-targets` (копирование turn'ов/блоков с drill-down),
  `composer-shape-preview`, `snapcompact-shape-preview`, `hub-frame`.

### 4.12 Полноэкранные приложения (`apps/`)

- `session-picker` — селектор сессий с поиском/пинами; `standalone-picker`
  — каркас one-shot TUI (select/prompt) для встраивания;
  `setup-model-picker`.
- `ps-top` + `ps-data` — процесс-монитор демонов omp (btop-подобный,
  refresh 2 с, kill/restart).
- `git/` — полноэкранный git-клиент: `git-tui` (split-pane diff+sidebar,
  stage/unstage hunks, AI-стейджинг, генерация commit-сообщения),
  `diff-pane` (режимы file/split/inline/hunk, выбор строк),
  `sidebar` (дерево файлов + commit-форма), `help`, `state`,
  `avatar`, `colors`.
- `live-visualizer` — голосовой режим: аудио-спектр, фазы
  (connecting/listening/working/speaking), транскрипт, mute пробелом.
- `autoresearch-dashboard`+`autoresearch-data`, `cleanse-board`/
  `cleanse-picker`, `if-bench-board` — панели бенчмаркинга/экспериментов.
- `debug/` — log-viewer, protocol-probe, raw SSE, terminal-info.

### 4.13 Онбординг (`setup/`)

`wizard.ts` (сцены: providers → model → glyph → composer → theme,
version-gating) → `wizard-overlay.ts` (fullscreen, фазы
splash→transition→scene→outro, cross-dissolve) → сцены `scenes/`:
`splash` (анимация воды/звёзд), `sign-in` (OAuth), `model`, `glyph`
(выбор ascii/unicode/nerd), `composer` (выбор формы поля),
`theme` (живой превью через mock статус-лайна), `outro`.
`startup-splash.ts` — стартовая анимация; `lazy.ts` — ленивый вызов
одной сцены; `setup-version.ts` — гейт версии.

### 4.14 Native-слой TSP (`native/`)

`backend.ts` (surfaces, credit-based flow control, blobs, события),
`encode.ts` (APC-фреймы, чанки, base64), `node.ts` (тип `NativeNode`),
`describe.ts` (строители: `card`, `row`, `col`, `kbd`, `picker`,
`overlay`, `shimmer`, `spinner`…), `spans.ts` (ANSI→spans, обратный
маппинг к токенам темы), `icons.ts`, `memo.ts` (мемоизация describe),
`reconcile.ts` (diff деревьев узлов → move/append-операции), `settle.ts`
(фиксация готовых блоков), `overlay.ts`/`picker.ts` (хром диалогов),
`apply.ts` (тестовый applier), `blobs.ts` (sha256-картинки), `tone.ts`
(цвета→тоны), `state.ts` (глобальный флаг native-режима — отключает
таймерные анимации).

### 4.15 Темы и символы (`theme/`)

`Theme`-класс (`fg/bg/bold/dim/symbol`), 45+ именованных цветов,
JSON-темы (`light.json`, `dark.json`, пользовательские
`~/.omp/themes/*.json`), валидация по schema; **3 пресета символов**
(ascii/unicode/nerd, ~130 ключей: глифы статусов, навигации, деревьев,
спиннеров, иконки языков); сессионные акцентные цвета (djb2 → OKLCH
hue, WCAG-контраст); shimmer-палитры; `tui-adapters.ts` — мост к
tree-sitter подсветке, темам markdown/editor/select; `mermaid-cache.ts`;
`glyph-bundle.json` — бандл иконок для Glyph Protocol.

## 5. Сводная классификация «по типу элемента»

- **Контейнеры**: Stack, Row, SplitPane, Box, Section, ScrollView,
  OverlayPanel, PanelRows, hub-frame, TranscriptContainer.
- **Поля ввода**: Input, Editor (+vim), TextFormField, HookEditor,
  CustomEditor,WizardStep(custom), MoveOverlay-input.
- **Списки/выбор**: SelectList, SettingsList, MenuSelection, TreeView,
  TabBar, Table, WizardStep(select), ~25 picker-оверлеев.
- **Диалоги/окна**: ask-dialog, login, plan-review/save, error-banner,
  pause-screen, session-info, ~30 overlay-панелей.
- **Индикаторы**: Loader/CancellableLoader, ProgressBar, shimmer,
  countdown, context-thresholds gauge, MetricRow, спиннеры в карточках.
- **Медиа**: Image (3 протокола), QR, коллаб-QR, video-превью,
  sixel-passthrough, kitty placeholders.
- **Навигация по контенту**: transcript-browser/outline, copy-selector,
  rewind-selector, history-search, tree-selector.
- **Данные времени выполнения**: status-line (28 сегментов), footer,
  usage-dashboard, jobs-panel, ps-top, agent-hub.

## 6. Наблюдения

1. **Двухрежимный вывод — главная фишка**: каждый виджет живёт двойной
   жизнью (ANSI-строки ↔ TSP-семантика); это позволяет одному и тому же UI
   работать и в «глупом» терминале, и в нативном бэкенде с настоящими
   виджетами.
2. **Композер — настраиваемый визуальный примитив**: 8 стилей рамки +
   registry для расширений + отдельная сцена онбординга с живым превью.
3. **Прогрессивное сворачивание везде**: transcript (Ctrl+O), thinking
   (Ctrl+T), группировка read'ов, лимиты вывода (3000 строк) с
   tail/head/middle-обрезкой и выдачей в артефакты.
4. **Расширяемость как first-class**: extension-сообщения, кастомные
   рендереры инструментов, кастомные composer-стили, кастомные темы,
   keybindings-профили.
5. Для изучения/заимствования наиболее интересны: `tui.ts` (рендер-цикл),
   `native/reconcile.ts` (diff-подход к TUI), `status-line/` (декларативные
   сегменты), `components/composer/` (стили-обвязки), `prompt/` (ux
   автодополнений).
