# План 2. Транскрипт и markdown

Шаг 2 — основной визуальный эффект. Зависит от шага 1 (токены и
недостающие группы). Дифф и подсветка кода — здесь же.

Статус 2026-10-21 (вечер): **выполнен целиком**, 23 задачи, коммиты
`9fbd953..7d6b1c3` (от `e033274`). Приёмка: тема инжектирована, smoke снят
скриншотами в `theme-zai-dark` и `theme-zai-light`; смысловой текст в обеих
схемах ≥ 4,5:1 — там, где стоковый серый не дотягивал (reasoning, подписи,
стек), введена пара `--zskin-text-muted`: #a89984 / #665c54.

Разведка 3.16.2 подтвердила и поправила предположения плана:

- `data-streamdown` есть, но не на 20 блоках: приложение заменило компоненты
  Streamdown, поэтому атрибут несут только заголовки `heading-1..6`, списки,
  пункты, ссылки, таблица и цитата; абзацы и инлайн-код — простые `p`/`code`
  без атрибутов.
- `data-markdown-table-layout-root` — не обёртка таблицы, а скролл-контейнер
  таймлайна (`data-testid="v4-timeline"`). Таблица —
  `table[data-streamdown="table"]` внутри `div[data-markdown-table-frame]`.
- `data-row-kind` — только у маркеров таймлайна (`timelineMarker`), не у хода;
  ходы и строки адресуются `data-turn-id` / `data-row-id`.
- `.message-response` — displayName React-компонента, не DOM-класс.
- `data-plan-status` — это todo-список панели статуса (2.22); план (2.14) —
  строки `data-plan-directory-tool-call-id` и вкладка «plan-detail».
- Блок кода и дифф рендерит pierre/diffs: кастомный элемент
  `<diffs-container>` с открытым shadow root. Селекторы внутрь не проходят;
  работают только custom properties (`--diffs-*`).

Оставшиеся гипотезы: фактический вид тинтов диффа внутри тени (2.21),
поведение окна виртуализации с ненулевого индекса (2.3), привязка решек
вопросника по `role="listbox"/"group"` (2.15), отсутствие StackTrace
в сборке (2.20).

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 2.1. Таблица (пара 12)
`MarkdownTable`, `ArtifactTable`, `SettingsResourceList`.
**Что.** Квадратный грид `┌─┬┐…` 1px цветом текста `#d5c4a1`, шапка bold,
разделители после каждой строки, без зебры; если грид окажется тяжёлым на
экране — рамки `#7c6f64` (компромисс, отметить в коммите).
**Как.** `[data-markdown-table-layout-root] table` и `th/td` —
`border-collapse: separate; border: 1px solid …`; `th { font-weight: 700 }`.
Для `ArtifactTable`/`SettingsResourceList` — только токены `--color-border`.

### 2.2. Лента сообщений (пара 38)
`ConversationTimeline`, `Conversation`.
**Что.** База `#282828` без полос и градиентов; между ходами — воздух.
**Как.** `--color-background` (есть); проверить, что фейды/маски ленты не
рисуют второй фон.

### 2.3. Блок хода (пара 39)
`ConversationTurnGroup`, `ConversationTurnRow`.
**Что.** Ход не карточка: одна пустая строка между ходами, без рамок.
**Как.** `[data-row-kind]` (подтверждён в DOM 3.16.2) — отступы; убрать
бордеры/фоны, если есть.

### 2.4. Сообщение пользователя (пара 40)
`ConversationUserInputBubble`, `ConversationUserInputBody`.
**Что.** Плашка темнее базы (`#1d2021`), отступ 1 клетка (≈ 8px при 17px),
текст `#ebdbb2`, радиус умеренный.
**Как.** `--color-background-win-alt` (есть); селектор пузыря подтверждён
в DOM 3.16.2: `[data-v4-user-input-bubble]` (рядом
`data-v4-user-input-collapsible-content`).

### 2.5. Ответ ассистента (пара 41)
`ConversationRowView`, `MessageResponse`.
**Что.** Проза на базе, `#ebdbb2`, mono; ссылки `#8ec07c` с underline; без
пузыря и фона.
**Как.** Контейнер ответа — класс `message-response`; ссылки — `a` внутри
контейнера (переопределяет глобальный brand).

### 2.6. Reasoning (пара 42)
`Reasoning`, `ReasoningTrigger`, `ReasoningContent`.
**Что.** Свёрнутый триггер — `#928374`, без рамок; раскрытое содержимое —
`#928374` с отступом как у цитаты; рамок и фонов нет.
**Как.** `[data-reasoning-content]`, `[data-reasoning-label]`; токен
`--color-foreground-subtlest` (есть).

### 2.7. Markdown (пара 43)
`MessageResponse`, `markdown-*`.
**Что.** H1 — 2em, bold, underline, `#fabd2f`; H2 — 1em bold `#fabd2f`;
H3–H4 — 1em bold `#fabd2f` (решётки `###` — TUI-артефакт, по умолчанию не
переносить). Инлайн-код `#d3869b` **без подложки**; ссылки aqua; списки —
маркер `#fe8019`, отступ 2 символа; цитата — `#928374` без курсива, планка
`#504945`; hr — 1px `#504945`.
**Как.** Markdown-контент рендерит Streamdown: блоки несут
`data-streamdown="…"` — при разведке снять значения атрибута для
абзаца, кода, цитаты, списка и вести селекторы от них; плюс `h1..h4`,
`li::marker`, `a`; `--color-markdown-inline-code` (есть). Снять
фон/бордер у `code` — сейчас приложение красит плашкой.

### 2.8. Блок кода (пара 44)
`CodeBlock`, `CodeBlockHeader`, `CodeBlockLanguageSelector`.
**Что.** Тело — `#ebdbb2`, рамка/шапка — линии `#504945`, фон без плашки
(или `#1d2021` для контраста с базой — решить на живом клиенте); подсветка
по ролям omp: keyword `#fb4934`, function `#fabd2f`, variable `#83a598`,
string `#b8bb26`, number `#d3869b`, type `#8ec07c`, operator `#fe8019`,
punctuation `#d5c4a1`, comment `#928374`.
**Как.** Движок в бандле — highlight.js (`hljs-*`) и Shiki (`--shiki-*`):
сопоставить `.hljs-keyword/.hljs-title.function_/.hljs-variable/.hljs-string/
.hljs-number/.hljs-type/.hljs-operator/.hljs-comment`; если токены идут
инлайн-стилями Shiki — переопределять через `--shiki-token-*` или
`span[style]` с `!important` (крайний случай, зафиксировать в комментарии).
Шапку/кнопки — `[data-code]` + `data-slot="button"`.

### 2.9. Действия сообщения (пара 46)
`MessageActions`, `ConversationAssistantTextActions`.
**Что.** Hover-тулбар: иконки `#928374`, hover — `#ebdbb2`, фона нет.
**Как.** Контейнер тулбара — класс/`data-slot="button"` с size=icon; цвет
иконок наследовать, hover — `color`.

### 2.10. Откат и checkpoint (пара 48)
`Checkpoint`, `CheckpointTrigger`, `ConversationFileRewindDialog`.
**Что.** Строка checkpoint — пунктир `#3c3836` и подпись `#928374`; диалог
отката — палитра 1.7.
**Как.** Классы `Checkpoint*` (гипотеза) + токены границ; диалог — 1.7.

### 2.11. Копирование фрагментов (пара 49)
`SelectionActionMenu`, `MarkdownSelectionTooltip`.
**Что.** Меню на `#1d2021`, пункты `#ebdbb2`, hover `#32302f`, выбранный
`#3c3836`.
**Как.** `[data-slot="dropdown-menu-item"]`, `--color-menu-hover` (1.1).

### 2.12. Фоновая работа (пара 50)
`ConversationBackgroundWorks`, `JobsSheet`, `JobWidget*`.
**Что.** Карточки задач: `#282828`, рамка `#3c3836`, статус-точка
success/warning/error, полоса прогресса — `--color-progress-surface`.
**Как.** Классы job-виджетов + `--color-progress-surface*` (1.1).

### 2.13. Транскрипт субагента (пара 52)
`SubagentSessionSidePane`, `SubagentDrilldown`.
**Что.** Панель на хроме `#1d2021`, заголовки `#bdae93`, вложенный
транскрипт — на базе `#282828`.
**Как.** Токены panel/background; классы side pane.

### 2.14. План (пара 54)
`Plan`, `PlanReviewOverlay`, `PlanDetailSidePane`.
**Что.** Карточка плана: заголовок bold `#ebdbb2`, номера шагов brand,
статусы success/warning, фон `#282828`, рамка `#3c3836`.
**Как.** `[data-plan-status]` (подтверждён в DOM 3.16.2), классы `Plan*`;
токены card/border.

### 2.15. Вопрос пользователю (пара 55)
`AskQuestionToolCallBlock`, `V4UserInputDialog`, `ElicitationDialog`.
**Что.** Карточка вопроса на тёплом тинте `interaction-ask-surface`,
заголовок `#fabd2f`, варианты — рамка `#504945`, выбранный — brand.
**Как.** `--color-interaction-ask-surface` (1.1),
`[data-elicitation-dialog-*]`, `[data-slot="button"]`.

### 2.16. Подтверждение (пара 56)
`Confirmation`, `PermissionDialog`, `ConfirmDialogHost`.
**Что.** Тинт `interaction-confirmation-surface`, кнопка подтверждения brand
с тёмным текстом, отмена — рамка; **видимость и поведение не менять**.
**Как.** `--color-interaction-confirmation-surface` (1.1),
`[data-confirm-intent]`, `[data-permission-rule-*]`.

### 2.17. Источники (пара 57)
`Sources`, `Source`, `InlineCitation*`.
**Что.** Чипы источников: фон `#32302f`, текст `#bdae93`, hover `#ebdbb2`,
номер — brand; рамка `#3c3836`.
**Как.** `data-source-*` (есть в бандле), `[data-slot="badge"]`.

### 2.18. Артефакт (пара 58)
`Artifact`, `ArtifactHeader`, `ArtifactContent`.
**Что.** Карточка `#282828`, рамка `#3c3836`, заголовок `#ebdbb2`,
иконка типа — `#8ec07c`, действия — subtle.
**Как.** `[data-artifact-kind]`, `[data-artifact-body]`; токены card/border.

### 2.19. Терминальный вывод (пара 59)
`Terminal`, `TerminalContent`, `TerminalStatus`.
**Что.** Экран `#282828`/`#ebdbb2`, шапка на `#1d2021`, статус — success/
error, mono; палитра ANSI уже из omp-темы.
**Как.** `--color-terminal-*` (есть); шапку — `TerminalHeader` +
`data-slot="button"`; `.terminal-xterm-shell` — только цвета.

### 2.20. Ошибка и стек (пара 60)
`StackTrace`, `formatErrorBlock`.
**Что.** Блок ошибки `#3c2021` с рамкой `#fb4934`, тело `#ebdbb2`, стек —
mono 0.9em, `#928374`.
**Как.** `--color-destructive-surface/-foreground` (1.1), классы
`StackTrace*`.

### 2.21. Дифф (пара 61)
`DiffViewer`, `EditInlineDiffContent`, `LightweightDiffPreview`.
**Что.** Добавлено — `#b8bb26` (фон — тинт), удалено — `#fb4934`, контекст —
`#928374`, номера строк — `#7c6f64`; конфликт — `#fabd2f`.
**Как.** `--color-diff-added*`, `--color-diff-removed*` (1.1) + `[data-diff-*]`,
`[data-diffs-header]`, `[data-selected-line]`, `[data-merge-conflict*]`.
Тема pierre может игнорировать токены — проверить, какие переменные читает
`diffs-container`, и переопределить их напрямую.

### 2.22. Todo (пара 62)
`TodoToolCallBlock`, `TodoPanel`.
**Что.** Сделано — `#b8bb26` + зачёркивание, в работе — brand, ждёт —
`#928374`; чекбокс — success в отмеченном.
**Как.** `[data-slot="checkbox"]`, классы `Todo*`; токены status.

### 2.23. Цель (пара 63)
`GoalToolCallBlock`.
**Что.** Цель и бюджет: заголовок `#ebdbb2`, подписи `#928374`, прогресс —
`--color-progress-surface`, статус — status-цвета.
**Как.** `[data-goal-status]`, `[data-goal-iteration]`, токены progress (1.1).
