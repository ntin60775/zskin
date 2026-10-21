# План 3. Карточки инструментов

Шаг 3 — каркас и доменные карточки. Зависит от шага 1; дифф берёт
правила из 2.21, подсветка — из 2.8.

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 3.1. Карточка субагента (пара 51)
`AgentToolCallBlock`, `ConversationAgentToolCallRow`.
**Что.** Как карточка 3.2: фазовая рамка, заголовок-intent, дерево
инструментов с `└─` и приглушёнными именами.
**Как.** Наследует стили 3.2; дерево — классы agent-tree (гипотеза).

### 3.2. Каркас карточки (пара 64)
`ToolCallBlock`, `ToolLayout`, `ToolCallBody`.
**Что.** Рамка 1px, радиус 6px; running — brand, success — `#3c3836`,
error — `#fb4934`, warning — `#fabd2f`; фон: running — прозрачный, success —
`#1d2021`, error — `#3c2021`; заголовок внутри рамки, подписи секций — над
секцией; статус-иконка и время (`283ms`) — `#7c6f64`.
**Как.** `[data-tool-name]` (подтверждён в DOM 3.16.2),
`[data-tool-status]` — бордер/фон по статусу (в перепись текущего вида
не попал — проверить на живом тул-колле); `ToolLayout` — заголовок;
врезание титула в линию — опция `position: relative` + лейбл с фоном
базы, включать после проверки (P2).

### 3.3. Прогресс вызова (пара 65)
`ToolCallProgressIndicator`, `Spinner`, `Loader`.
**Что.** Спиннер brand на ходу, после успеха — точка `#b8bb26`, ошибка —
`#fb4934`; glow (drop-shadow) убрать — в omp его нет.
**Как.** `.animate-spin` уже перекрашен; убрать `filter: drop-shadow`;
статусные варианты — `[data-tool-status]`.

### 3.4. Чтение файла (пара 66)
`ReadToolCallBlock`, `ReadFileChip`.
**Что.** Чип файла: фон `#32302f`, рамка `#3c3836`, имя `#ebdbb2`, диапазон
строк `#7c6f64`; иконка файла — `#83a598`.
**Как.** Классы `ReadFileChip` (гипотеза), `[data-code-file]`, токены
surface/border.

### 3.5. Правка файла (пара 67)
`EditToolCallBlock`, `EditInlineDiffContent`.
**Что.** Шапка правки — `#ebdbb2`, статистика `+N`/`−N` — success/destructive,
дифф — правила 2.21.
**Как.** `--color-diff-*` (1.1), `[data-diff-*]`; счётчики —
`[data-additions-count]`, `[data-deletions-count]` (есть в бандле).

### 3.6. Поиск (пара 68)
`SearchToolCallBlock`, `ToolSearchToolCallBlock`, `ExploreToolCallBlock`.
**Что.** Группы по файлам: путь `#bdae93`, совпадения `#ebdbb2`, счётчик —
brand, лимит — `#928374`.
**Как.** Классы search-блоков; `--color-foreground-*`; подсветка совпадений —
`--color-find-highlight` (есть).

### 3.7. Shell (пара 69)
`ExecuteToolCallBlock`, `ExecuteCommand`, `ExecuteOutput`.
**Что.** Команда — mono `#ebdbb2` на `#1d2021`, вывод — `#928374`, хвост с
фейдом; статус — exit code: 0 success, ≠0 destructive.
**Как.** `ExecuteOutput` + `--color-terminal-fg`/`--color-foreground-subtlest`;
высоту превью не менять (поведение).

### 3.8. Eval (пара 70)
`NodeReplToolCallBlock`, `NodeReplImageGrid`.
**Что.** Код-ячейка как в omp: заголовок-intent, гуттер номеров `#7c6f64`,
`Output` — `#928374`, дерево `└─` приглушённое; подсветка — 2.8.
**Как.** Классы `NodeRepl*`, `[data-code]`; гуттер — селектор номеров строк;
синтаксис — общий маппинг 2.8.

### 3.9. Задача субагента (пара 71)
`AgentToolCallBlock`, `TaskOutputToolCallBlock`.
**Что.** Дерево: ветки `└─`/`├─` цветом `#7c6f64`, имена — `#928374`,
статусы — status; вложенность на 2 символа.
**Как.** Классы agent-tree (гипотеза); токены muted/dim.

### 3.10. Ожидание и результат (пара 72)
`TaskStopToolCallBlock`, `SubmitResultToolCallBlock`.
**Что.** Строка ожидания — `#928374`, результат — `#8ec07c` с иконкой
success; ошибка — destructive.
**Как.** `[data-tool-status]`, токены status.

### 3.11. MCP (пара 73)
`McpToolCallBlock`.
**Что.** Заголовок `server/tool`: сервер — `#bdae93`, инструмент —
`#ebdbb2`; вывод — `#928374`; иконка MCP — `#fe8019`.
**Как.** Классы MCP-блока; `--color-trajectory-tool-call` (есть) для иконки.

### 3.12. Веб-поиск и fetch (пара 74)
`WebFetchToolCallBlock`, `Sources`.
**Что.** Заголовок с URL — `#bdae93`, ссылки aqua, вывод `#928374`,
источники — 2.17.
**Как.** Классы web-блока + `data-source-*`; `a` — 2.5/2.7.

### 3.13. Автоматизация (пара 75)
`CronCreateToolCallBlock`, `OffPeakCreateTaskCard`.
**Что.** Поля schedule/next-run: label `#928374`, value `#ebdbb2`; бейдж
статуса — капсула 1.10; фон card.
**Как.** Классы карточек + `[data-slot="badge"]`; токены card/surface.
