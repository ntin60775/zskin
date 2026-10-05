# Полное соединение классификаций UI: ZCode (рендерер) × oh-my-pi (TUI)

Соединение карт UI двух агентов — [ui-elements.md](ui-elements.md)
(десктоп-рендерер ZCode, Electron/React) и
[oh-my-pi-tui-classification.md](oh-my-pi-tui-classification.md)
(терминальный фреймворк oh-my-pi, `packages/tui`). Приоритеты заимствования
согласованы с [oh-my-pi-borrow-ideas.md](oh-my-pi-borrow-ideas.md).

Тип связи (как в FULL OUTER JOIN):
- **INNER** — аналог есть у обоих (совпадение или частичное пересечение);
- **ZCode-only** — зона есть только в рендерере ZCode;
- **omp-only** — есть только у oh-my-pi.

Приоритет заимствования:
- **Высокий** — брать в первую очередь, применимо в темах zskin сейчас;
- **Средний** — брать: референс для собственных проектов / второй этап zskin;
- **Низкий** — по мере нужды, в основном UX-идеи;
- **—** — заимствовать нечего (нет аналога, уже реализовано или граница проекта).

| Зона / элемент | ZCode (рендерер) | oh-my-pi (TUI) | Тип | Приоритет |
|---|---|---|---|---|
| Темы и дизайн-токены | 578 токенов `--color-*` в 5 скоупах; темы = классы на `<html>` (`theme-zai-dark`…) | `theme/`: Theme-класс, 45+ именованных цветов, JSON-темы, 3 пресета символов, loader | INNER | **Высокий** (A6 — палитровая дисциплина, маппинг токен→токен) |
| Акцентные цвета сессий | нет (один `--color-brand`) | `theme/session-color.ts`: хэш→OKLCH hue, WCAG-контраст, дистанция от акцента | omp-only | **Высокий** (A2 — генератор тем zskin) |
| Композер (поле ввода) | `prompt-input*`, `prompt-editor`, `data-slot="textarea"`; один вид | 8 стилей обвязки (`box/band/claude/pi/borderless/rule/field/rail`) + registry, CustomEditor, welcome, чипы вложений, очередь | INNER | **Высокий** (A1 — серии CSS-тем по силуэтам omp) |
| Автодополнения ввода | упоминания (`mentions/`, `.prompt-mention`), чипы | оркестратор автодополнений (`/`, `^`, `#N`, `:`, `scheme://`, ghost-text), prose-gate, magic-keywords | INNER (частично) | Средний (B6 — свои проекты; для zskin — только стиль подсветки) |
| Метры квот / контекста | `chat-input-toolbar`: `--color-usage*`, `--color-context-breakdown*` | `chrome/context-thresholds.ts` (тиры normal/warning/purple/error), usage-dashboard, сегменты cost/context_pct | INNER | **Высокий** (A3 — тировая шкала в темы) |
| Анимации / индикаторы | `shimmer`, `chat-loading`, `data-zcode-stream-animate` | `Loader`/`CancellableLoader`, `theme/shimmer.ts` (KITT-сканер, скорость в ячейках/с) | INNER | Средний (A4 — keyframes-перенос) |
| Сообщения чата | `ai-elements/`: message, reasoning, markdown-*, image, sources | `chat/`: user/assistant-message, thinking-display (сворачивание, tok/s), реакции | INNER | Средний (A7 — «свернуто по умолчанию» как стиль) |
| Карточки инструментов | `ToolCallBlocks`, `tool.tsx`, `code-block.tsx` | `tools/` (~40 рендереров), `render/tool-card`, `output-pane`, `streaming-output` (лимиты, tail) | INNER | Средний (A5 — quiet mode: приглушение без скрытия) |
| Исполнение shell/eval | bash-вывод внутри ToolCallBlocks | `bash-execution`/`eval-execution` (PTY-фрейм, tail 20, стриминг) | INNER | Низкий |
| Диффы и git | `GitPane`, `git-graph`, `diff-viewer`, `--color-git*` | `chrome/diff.ts` (intra-line word-diff) + `apps/git/DiffPane` (4 режима, выбор строк, AI-стейджинг) | INNER | Средний (стиль диффов в темы; AI-стейджинг — не тема) |
| Подтверждения операций | `confirmation.tsx`, `ConfirmDialog`, `ElicitationDialog`, `AlertDialogHost` | `confirmation.tsx`, `ask-dialog`, `hook-input` (таймеры, multi-question) | INNER | **—** (только стиль; поведение/видимость не трогаем — принцип 2) |
| Навигация по истории | `checkpoint.tsx` | `transcript-browser` + `transcript-outline` (dotted-outline, rail), rewind/copy-селекторы | INNER (частично) | Низкий (UX-идеи, не перенос) |
| Списки сессий/задач, деревья | `workspace-grouped-tasks`, файл-дерево сайдбара | `session-selector`, `tree-selector`, `session-picker`, `TreeView`, `agent-tree` | INNER (частично) | Низкий |
| Командная палитра / поиск | `CommandCenterDialog`, `quickpick/` | slash-команды, model-picker, `history-search` (fuzzy по промптам) | INNER (частично) | Низкий |
| Базовые виджеты | shadcn/ui: button, input, dialog, select, tabs, table, toast… | `components/`: SelectList, SettingsList, Form, Table, TabBar, TreeView, Disclosure, KeyValueList | INNER (концепт) | Низкий (для zskin стили уже есть; референс API) |
| Настройки | `settings/` (вкладки, автоматизации) | `settings-selector` + `SettingsList` (секции, editing state) | INNER | Низкий |
| Вход / онбординг | `login/`, `onboarding/` | `setup/` (визард с version-gating, живое превью тем), `login-dialog`, `oauth-selector` | INNER | Средний (B11 — живое превью в своих проектах) |
| Фидбек / отчёты | `feedback/` (FeedbackCenter, скриншот-пикер) | `report-panel` | INNER | Низкий |
| Граф / диаграммы | `.wf-*`, `workflow-graph`, mermaid-блоки | `ai-elements/` node/edge/canvas, `mermaid-block` | INNER (частично) | Низкий |
| Терминал | `terminal/` (xterm), 22 токена `--color-terminal-*` | `terminalTheme.ts` читает CSS-переменные в рантайме, PTY-вывод | INNER | **—** (у ZCode тот же механизм; брать нечего) |
| Тосты / баннеры | `toast` (shadcn), `ChatErrorBanner` | `status-notice` (toast, TTL 2.4 с), `error-banner` (перманентный, над редактором) | INNER | Низкий |
| Медиа и вьюверы | `image.tsx`, галерея, pptx/pdf-вьюверы | `Image` (Kitty/Sixel/iTerm2, бюджет), kitty-placeholder-плейсмент | INNER (частично) | Низкий |
| Хром окна / титлбар | `DesktopWindowFrame`, `DesktopTopOverlay`, `WindowControls` | нет (TUI без оконного хрома) | ZCode-only | — |
| Сайдбар как зона | `WorkspaceSidebar`, collapsed-rail (`data-rail-position`) | нет постоянного сайдбара (фуллскрин-чат + оверлеи) | ZCode-only | — |
| Встроенный браузер / CUA | `browser-use/`, `EmbeddedWebsiteHeader`, `cua-permission/` | нет | ZCode-only | — |
| Типографика страницы | `--ui-font-size`, скроллбары, `::selection` | нет (шрифт/метрики терминала) | ZCode-only | — |
| Ядро рендеринга и ввода | — (роль играют DOM/Electron) | `tui.ts` (diff-кадры, фокус, курсор-маркер), `terminal.ts`, `stdin-buffer`, mouse/keys/keybindings | omp-only | Средний (B2, B8 — референс рендер-цикла) |
| Статус-лайн как полоса | нет (ближайшее — композер-тулбар/хедер) | 28 сегментов, 7 пресетов, 6 сепараторов, 5 лэйаутов, footer | omp-only | Средний (B4 — декларативная схема для своих проектов) |
| Утилитарные приложения | отдельные окна: resource-manager, CUA-панель | `ps-top`, `debug/*` (log-viewer, debug-сервер TUI) | omp-only | Низкий (B10 — debug-сервер, Средний) |
| LaTeX-рендер | нет | `latex-block.ts` (2D-layout), `latex-to-unicode.ts` | omp-only | Низкий |
| Экспериментальные дашборды | нет | `autoresearch-dashboard`, `cleanse-*`, `if-bench-board` | omp-only | Низкий |

## Исключено из таблицы (раздел C borrow-файла — осознанные отказы)

Native-слой TSP и Glyph-протокол (`native/`, `glyph-protocol.ts`), голосовой
слой (`live-visualizer`, push-to-talk, STT), collab-QR/QR-рендерер,
vim/kill-ring полной комплектации, перенос оверлеев/приложений omp «как есть».

## Сводка по приоритетам

- **Высоких** четыре: темы/токены (дисциплина палитры), акценты сессий,
  композер-силуэты, тиры метров.
- **Средних** восемь: автодополнения, анимации, сообщения, tool-карточки,
  диффы, онбординг-превью, ядро рендеринга, статус-лайн (с оговорками в
  ячейках).
- Отдельная строка с приоритетом «—» у подтверждений операций — не «нечего
  брать», а граница проекта: стиль допустим, поведение и видимость — нет.
- Остальное — Низкий или «—»: либо у ZCode уже реализовано, либо это
  UX-идеи без прямой проекции в CSS, либо референс на далёкую перспективу.
