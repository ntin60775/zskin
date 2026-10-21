# Сопоставление компонентов ZCode UI и oh-my-pi TUI

Финальная таблица соединяет [zcode-ui-components.md](zcode-ui-components.md) и
[oh-my-pi-tui-components.md](oh-my-pi-tui-components.md). ZCode-сторона сверена
с установленным клиентом **3.16.2**: публичный исходник заканчивается на
3.15.1, но в 3.16.2 сохранились все 6 981 ключ словаря сообщений и добавились
8 новых, а набор data-атрибутов вырос на 73. Роли компонентов от этого не
изменились.

В таблицу попали только пары, у которых совпадает пользовательская роль.
Односторонние зоны — оконный хром, сайдбар как постоянная колонка, встроенный
браузер, PDF/PPTX-вьюверы, удалённые подключения, шаринг разговоров, награды —
в таблицу не включены.

## Как читать полноту

- **Полное** — совпадает роль и набор данных; различаются форма и среда.
- **Частичное** — совпадает роль, но модель данных или взаимодействие шире
  либо уже.
- **Концептуальное** — совпадает назначение, прямой проекции компонента нет;
  пара полезна как ориентир, не как перенос.

## 1. Основа интерфейса

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 1 | Темы и цветовые роли | CSS-токены `--color-*`, классы `theme-zai-dark/light` | `Theme`, JSON-темы, `theme/schema.ts` | Полное | Оба задают именованные роли для фона, текста, границ, статусов и diff. ZCode — CSS-переменные, omp — JSON и ANSI-коды. |
| 2 | Символы и глифы | Lucide-иконки, файловые иконки | `SYMBOL_PRESETS`, `SymbolMap`, Glyph Protocol | Частичное | ZCode рисует SVG-иконки, omp — текстовые глифы с тремя пресетами. Роль «иконка» общая, носитель разный. |
| 3 | Shimmer и живая подсветка | `Shimmer`, `ChatLoading` | `theme/shimmer.ts`, `MagicKeywordSpec` | Полное | Анимированная подсветка активного текста и ключевых слов. |
| 4 | Спиннер и загрузка | `Spinner`, `Loader`, `ChatLoading` | `Loader`, `CancellableLoader` | Полное | Индикатор ожидания; у omp есть отменяемый вариант. |
| 5 | Прогресс | `Progress` | `ProgressBar` | Полное | Полоса выполнения с несколькими стилями у omp. |
| 6 | Метрика | `FlipMetricValue`, `SmoothMetricValue` | `MetricRow`, `MetricSpec` | Частичное | Оба показывают число и единицу; ZCode анимирует смену значения, omp форматирует строку. |
| 7 | Уведомление | `Toast`, `AnchoredToastStack` | `StatusNotice` | Полное | Короткое всплывающее сообщение с TTL. |
| 8 | Ошибка | `ChatErrorBanner`, `Alert`, `ErrorBoundary` | `ErrorBlock`, `ErrorBannerComponent` | Полное | Баннер ошибки; omp добавляет перманентный баннер над редактором. |
| 9 | Скролл | `ScrollArea`, `ScrollFadeViewport` | `ScrollView`, `ScrollViewport` | Полное | Прокрутка с якорями; у omp есть follow-tail и thumb. |
| 10 | Разделители панелей | `Resizable` | `SplitPane` | Полное | Две панели с перетаскиваемым разделителем. |
| 11 | Вкладки | `Tabs`, `SettingsSegmentedTabs`, `SidePaneTabTrigger` | `TabBar` | Полное | Горизонтальный набор вкладок. |
| 12 | Таблица | `MarkdownTable`, `ArtifactTable`, `SettingsResourceList` | `Table` | Полное | Колонки, выравнивание, гибкая ширина. |
| 13 | Список выбора и меню | `Select`, `DropdownMenu`, `Command` | `SelectList`, `MenuSelection` | Полное | Список опций с клавиатурой и мышью. |
| 14 | Дерево | `FileTree`, `WorkspaceFileTree` | `TreeView` | Полное | Иерархия с раскрытием и префиксами. |
| 15 | Диалог и оверлей | `Dialog`, `Popover`, `AlertDialog` | `OverlayPanel`, `HubFrame` | Полное | Слой поверх основного экрана с рамкой и фокусом. |
| 16 | Поля формы | `Input`, `Textarea`, `Select`, `Switch`, `Checkbox`, `RadioGroup` | `Input`, `Form`, `TextFormField`, `SelectFormField` | Полное | Однострочные и многострочные поля, выбор, валидация. |
| 17 | Визард | `OnboardingDialog`, `OnboardingWizardHeader/Footer/Sidebar` | `WizardStep`, `SetupWizardComponent` | Полное | Пошаговый сценарий с навигацией и валидацией. |
| 18 | Подсказка клавиши | `ControlShortcutBadge`, `Kbd`, `ShortcutBindingRow` | `keybinding-hints.ts`, `KeyName`, `HotkeysSheetComponent` | Полное | Отображение горячей клавиши и лист подсказок. |

## 2. Композер

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 19 | Композер целиком | `ConversationComposer` | `Composer` | Полное | Владеет вводом, вложениями, очередью, отправкой и статусом. |
| 20 | Силуэт композера | `ChatPromptEditor`, оболочка `ConversationComposer` (3.16.2: раскладка с ведущими и хвостовыми действиями) | 8 стилей `box/band/claude/pi/borderless/rule/field/rail` | Концептуальное | ZCode имеет один силуэт, omp — реестр сменных. Прямого API стилей у ZCode нет, но CSS может собрать похожие формы. |
| 21 | Текстовый редактор | `LexicalChatInput`, `ChatPromptEditor` | `Editor`, `CustomEditor` | Полное | Многострочный ввод с подсветкой, вставкой и декорациями. |
| 22 | Отправка и стоп | `PromptInputSubmit`, состояние `ConversationComposer` | `CustomEditor` (send/stop) | Полное | Одна кнопка меняет смысл в зависимости от состояния хода. |
| 23 | Выбор модели | `ComposerModelMenu`, `V4ComposerModelControls` | `ModelPickerComponent`, `ModelBrowser` | Полное | Каталог моделей с группировкой и выбором. |
| 24 | Выбор провайдера и аккаунта | `ComposerProviderMenu` | `ModelHubComponent`, `OAuthSelectorComponent`, `SessionAccountSelectorComponent` | Частичное | ZCode разделяет провайдера и модель; omp распределяет модели по ролям и аккаунтам. |
| 25 | Глубина мышления | `ThoughtLevelCycleControl`, `ComposerEffortHeading` | `ThinkingSelectorComponent`, сегмент `thinking` | Полное | Выбор уровня reasoning. |
| 26 | Режим работы | `ChatModeSwitchControl` | `QueueModeSelectorComponent`, сегмент `mode` | Частичное | ZCode переключает режим чата, omp — очередь и режим отображения; общей модели режимов нет. |
| 27 | Расход контекста | `ChatContextUsage`, `ContextQuotaResetOpportunityReminderContent` | `context-usage.ts` (`ContextUsageView`), сегмент `context_pct` | Полное | Процент заполнения, разбивка и предупреждения. |
| 28 | Расход и стоимость | `ChatCodingPlanMcpUsageMeter`, `CodingPlanUsageRemainingPanel` | `UsageDashboardComponent`, сегменты `cost`/`usage` | Полное | Квоты, лимиты и стоимость; ZCode привязан к тарифу, omp — к провайдерам. |
| 29 | Чипы вложений | `Attachments`, `Attachment`, `AttachmentRemove`, контекстные чипы `v4/composer/` | `AttachmentChipsBand` | Полное | Полоса вложений с превью и удалением. |
| 30 | Просмотр вложения | `ImagePreviewDialog`, `ImageThumbnailGallery`, `ChatMediaAttachmentPreviewDialog` | `Image`, `ShowImagesSelectorComponent` | Полное | Увеличение и перебор изображений. |
| 31 | Очередь сообщений | `ConversationQueuePanel`, `Queue` | `QueuedMessagesBand`, `QueueModeSelectorComponent` | Полное | Нумерованная очередь с редактированием и отправкой. |
| 32 | Упоминания и автодополнение | `MentionPanel`, `LexicalChatInput`, `mentions/` | `CombinedAutocompleteProvider`, `prompt/*-autocomplete.ts` | Полное | `@`-файлы, `#`-сессии, `$`-скиллы, схемы и модели. |
| 33 | Slash-команды | `SlashCommandPlugin`, `slashCommandPanelSections` | `SlashCommand`, `autocomplete.ts` | Полное | Каталог команд с фильтрацией. |
| 34 | История промптов | история в `ConversationComposer` | `HistorySearchComponent` | Частичное | ZCode подставляет историю в поле, omp открывает отдельный fuzzy-поиск. |
| 35 | Подсказки в пустом поле | `ConversationDraftSuggestedPromptsContainer`, `ConversationDraftEmptyState` | `ComposerHint`, `WelcomeComponent` | Частичное | ZCode предлагает готовые промпты, omp — обучающие подсказки и tip. |
| 36 | Приветствие | `WelcomeScreen`, `LoginPanel` | `WelcomeComponent` | Полное | Лого, подсказка и вход в первый запрос. |
| 37 | Голосовой ввод | `SpeechInput`, `MicSelector`, `VoiceSelector`, `Transcription` | `LiveVisualizer`, dictation в `CustomEditor` | Частичное | ZCode встраивает запись в композер, omp показывает полноэкранный визуализатор. |

## 3. Транскрипт

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 38 | Лента сообщений | `ConversationTimeline` | `TranscriptContainer` | Полное | Контейнер истории с прокруткой и жизненным циклом блоков. |
| 39 | Блок хода | `ConversationTurnGroup`, `ConversationTurnRow` | `ChatBlock` | Полное | Группирует ввод, работу и ответ в один ход. |
| 40 | Сообщение пользователя | `ConversationUserInputBubble`, `ConversationUserInputBody` | `UserMessageComponent` | Полное | Пузырь с markdown, вложениями и действиями. |
| 41 | Ответ ассистента | `ConversationRowView` (ветка assistant text) | `AssistantMessageComponent` | Полное | Markdown, изображения, ошибки, стриминг. |
| 42 | Reasoning | `Reasoning`, `ReasoningTrigger`, `ReasoningContent` | thinking-блок `AssistantMessageComponent` + `thinking-display.ts` | Полное | Сворачиваемые рассуждения с индикатором. |
| 43 | Markdown | `MessageResponse`, `markdown-*`, `MarkdownBlockquote/List/Table/Image` | `Markdown` | Полное | Полный MD-рендер с кодом, таблицами и ссылками. |
| 44 | Блок кода | `CodeBlock`, `CodeBlockCopyButton`, `CodeBlockLanguageSelector` | `render/code-cell.ts`, markdown-fence | Полное | Код с языком, копированием и переносом. |
| 45 | Mermaid | `MermaidBlock`, `CodeBlockMermaidPreviewButton` | `theme/mermaid-cache.ts`, `FigureMarkdown` | Частичное | ZCode рендерит mermaid как блок, omp кэширует и вставляет фигуру. |
| 46 | Действия сообщения | `MessageActions`, `ConversationAssistantTextActions` | `transcript-actions.ts`, hover-тулбар `UserMessageComponent` | Полное | Копировать, повторить, откатить, оценить. |
| 47 | Навигация по истории | `ConversationTurnNavigator` | `TranscriptBrowser`, `transcript-outline.ts` | Полное | Оглавление ходов и прыжки по истории. |
| 48 | Откат и checkpoint | `Checkpoint`, `ConversationFileRewindDialog` | `RewindSelectorComponent` | Полное | Точка возврата и выбор ветки. |
| 49 | Копирование фрагментов | действия копирования в `ConversationRowView`, `SelectionActionMenu` | `CopySelectorComponent`, `copy-targets.ts` | Полное | Выбор блока или хода для копирования. |
| 50 | Фоновая работа | `ConversationBackgroundWorks`, `ConversationStatusPanel` | `JobsSheet`, `JobWidget*` | Полное | Список фоновых задач с отменой и статусом. |
| 51 | Карточка субагента | `AgentToolCallBlock`, `ConversationAgentToolCallRow` | `tools/task.ts`, `agent-tree.ts` | Полное | Дерево подагентов и прогресс. |
| 52 | Транскрипт субагента | `SubagentSessionSidePane`, `SubagentDrilldown` | `AgentTranscriptViewer` | Полное | Просмотр чужого транскрипта и переход по цепочке. |
| 53 | Реестр агентов | `SubagentsSection`, `SubagentDirectorySidePane` | `AgentHubOverlayComponent`, `AgentsHubComponent` | Полное | Список агентов, метрики и live-инспекция. |
| 54 | План | `Plan`, `PlanDetailSidePane`, `PlanGuidanceToolCallBlock` | `PlanReviewOverlay`, `PlanSaveOverlay`, `plan-toc.ts` | Полное | Просмотр, правка и сохранение плана. |
| 55 | Вопрос пользователю | `AskQuestionToolCallBlock`, `V4UserInputDialog`, `ElicitationDialog` | `AskDialogComponent` | Полное | Мультивопрос с вариантами и таймером. |
| 56 | Подтверждение | `Confirmation`, `PermissionDialog`, `ConfirmDialogHost` | `ApprovalDialogComponent` | Полное | Разрешение опасного действия с явным согласием. |
| 57 | Источники | `Sources`, `InlineCitation*` | `web-search.ts` (ответ и источники) | Полное | Список цитат и переход к источнику. |
| 58 | Артефакт | `Artifact`, `WorkflowArtifactBody`, `ArtifactPresetBody` | `CachedOutputBlock`, `FramedBlockComponent` | Частичное | Оба показывают вложенный результат; ZCode богаче пресетами. |
| 59 | Терминальный вывод | `Terminal`, `TerminalContent`, `TerminalStatus` | `BashExecutionComponent`, `terminal-output.ts` | Полное | Вывод команды с копированием и статусом. |
| 60 | Ошибка и стек | `ChatErrorBanner`, `StackTrace` | `formatErrorBlock`, `ErrorBannerComponent` | Частичное | ZCode показывает стек как отдельный блок, omp ограничивает ошибку 8 строками. |
| 61 | Дифф | `DiffViewer` (3.16.2: `diffs-container`/pierre), `EditInlineDiffContent`, `LightweightDiffPreview` | `chrome/diff.ts` | Полное | Построчный и intra-line diff; ZCode добавляет выбор строк, аннотации и разрешение конфликтов. |
| 62 | Todo | `TodoToolCallBlock`, `TodoPanel` | `tools/todo.ts` | Полное | Фазы, статусы и зачёркивание. |
| 63 | Цель | `GoalToolCallBlock` | `tools/goal.ts` | Полное | Цель, бюджет и статус. |

## 4. Карточки инструментов

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 64 | Каркас карточки | `ToolCallBlock`, `ToolLayout`, `ToolCallBody` | `ToolExecutionComponent`, `ToolCard` | Полное | Заголовок, тело, футер, фазы. |
| 65 | Прогресс вызова | `ToolCallProgressIndicator` | `Loader`, спиннер `ToolExecutionComponent` | Полное | Индикатор выполнения инструмента. |
| 66 | Чтение файла | `ReadToolCallBlock`, `ReadFileChip` | `tools/read.ts`, `ReadToolGroupComponent` | Полное | Файл, диапазон строк, группировка чтений. |
| 67 | Правка файла | `EditToolCallBlock`, `EditInlineDiffContent` | `tools/edit.ts` | Полное | Патч, дифф, результат по файлам. |
| 68 | Поиск | `SearchToolCallBlock`, `ToolSearchToolCallBlock`, `ExploreToolCallBlock` | `tools/grep.ts`, `find.ts`, `glob.ts`, `ast-grep.ts` | Полное | Совпадения, группы по файлам, лимиты. |
| 69 | Shell | `ExecuteToolCallBlock`, `ExecuteCommand`, `ExecuteOutput` | `BashExecutionComponent` | Полное | Команда, PTY, хвост вывода, стриминг. |
| 70 | Eval | `NodeReplToolCallBlock`, `NodeReplImageGrid` | `EvalExecutionComponent` | Полное | `>>>` Python/JS и результат. |
| 71 | Задача субагента | `AgentToolCallBlock`, `TaskOutputToolCallBlock` | `tools/task.ts` | Полное | Дерево, прогресс, структурированный результат. |
| 72 | Ожидание и результат | `TaskStopToolCallBlock`, `SubmitResultToolCallBlock` | `tools/wait.ts`, `yield.ts` | Частичное | ZCode разделяет stop и submit, omp объединяет ожидание и yield. |
| 73 | MCP | `McpToolCallBlock` | `tools/mcp.ts` | Полное | Текст, изображения, ресурсы и прогресс. |
| 74 | Веб-поиск и fetch | `WebFetchToolCallBlock`, `Sources` | `tools/web-search.ts`, `fetch.ts` | Полное | Ответ, цитаты, источники. |
| 75 | Автоматизация | `CronCreateToolCallBlock`, `OffPeakCreateTaskCard` | `tools/daemon.ts`, `tools/subprocess.ts` | Частичное | ZCode создаёт расписание, omp управляет демонами и процессами. |

## 5. Навигация и списки

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 76 | Список сессий и задач | `ProjectSidebar`, `TaskGroupedView`, `TaskList` | `SessionSelectorComponent`, `TreeSelectorComponent`, `SessionPickerHost` | Полное | Список сессий с поиском, группами и пинами. |
| 77 | Поиск и палитра | `CommandCenterDialog`, `QuickPickCommandDialog`, `TaskFindDialog` | `HistorySearchComponent`, `CombinedAutocompleteProvider` | Частичное | ZCode даёт одну палитру, omp — отдельные поиски по истории и командам. |
| 78 | Файловое дерево | `WorkspaceFileTree`, `FileManagerPane`, `FileTree` | `TreeView`, `file-list.ts`, `MoveOverlay` | Полное | Дерево и список файлов с навигацией. |
| 79 | Git | `GitPane`, `GitGraphPane`, `GitBranchSwitcher`, `DiffViewer` | `GitTuiHost`, `DiffPane`, `Sidebar` | Полное | Статус, ветки, диффы, stage и commit. |
| 80 | Терминал | `Terminal`, `TerminalSession`, `AnimatedTerminalPanel` | `BashInteractiveOverlayComponent`, `terminal-output.ts` | Частичное | ZCode держит постоянную панель, omp открывает PTY-оверлей. |
| 81 | Настройки | `SettingsPage` | `SettingsSelectorComponent`, `settings-defs.ts` | Полное | Полноэкранные настройки с вкладками и поиском. |
| 82 | Строки настроек | `SettingsRow`, `SettingsRangeControl`, `SettingsGroupCard` | `SettingsList`, `TextFormField`, `SelectFormField` | Полное | Строка, переключатель, ползунок, выбор. |
| 83 | Выбор темы | `ThemeSelect`, `ThemePreviewCard` | `ThemeSelectorComponent` | Полное | Список тем с превью. |
| 84 | Плагины | `PluginStorePage`, `InstalledPluginDetailPanel` | `PluginSelectorComponent`, `PluginSettingsComponent` | Полное | Каталог, установка, настройки. |
| 85 | Hooks | `HooksSection`, `HookForm`, `HooksList` | `HookSelectorComponent`, `HookEditorComponent`, `HookInputComponent` | Полное | Список, редактирование и ввод hook. |
| 86 | MCP | `McpSettingsSection`, `McpServerList`, `McpServerForm` | `MCPAddWizard`, `extensions/mcp-runtime` | Полное | Подключение, статус и ошибки серверов. |
| 87 | Субагенты | `SubagentsSection`, `SubagentReasoningField` | `AgentHubOverlayComponent`, `AgentsHubComponent` | Полное | Реестр, роли, уровни reasoning. |
| 88 | Горячие клавиши | `ShortcutSettingsSection`, `ShortcutBindingRow`, `ShortcutSearchBar` | `keybindings.ts`, `HotkeysSheetComponent`, `keybinding-hints.ts` | Полное | Просмотр и переназначение клавиш. |
| 89 | Статистика использования | `UsageStatsSection`, `UsageHeatmap`, `CodingPlanUsagePanel` | `UsageDashboardComponent` | Полное | Heatmap, карточки провайдеров, лимиты. |
| 90 | Фидбек | `FeedbackCenter`, `FeatureRequestDialog`, `TicketDetailView` | `ReportPanel` | Частичное | ZCode ведёт тикеты, omp отправляет отчёт. |
| 91 | Отладочные экраны | `DeveloperToolsPane` | `DebugLogViewerComponent`, `ProtocolProbeComponent`, `RawSseViewerComponent` | Полное | Логи, протокол, сырой поток. |
| 92 | Онбординг | `OnboardingDialog`, `OccupationOnboarding` | `SetupWizardComponent`, `setup/scenes` | Полное | Пошаговый вход с выбором провайдера, модели и темы. |
| 93 | Вход | `WelcomeScreen`, `LoginPanel`, `LoginApiKeyForm` | `LoginDialogComponent`, `OAuthSelectorComponent` | Полное | API-ключ и OAuth-поток. |

## 6. Визуализации и приложения

| № | Роль | ZCode UI | oh-my-pi TUI | Полнота | Что совпадает и чем отличается |
|---:|---|---|---|---|---|
| 94 | Графики | `Chart`, `UsageHeatmap`, `AppUsageDailyModelTrendChart`, `CodingPlanUsageBarChart` | `charts/chart-plan.ts`, `renderChartSvg`, `TableChartFigure` | Полное | Линии, столбцы, heatmap и таблица как график. |
| 95 | Монитор ресурсов | `ResourceManagerApp`, `UsageMeter`, `StorageSection` | `PsTopComponent`, `ps-data.ts` | Частичное | ZCode считает файлы и сеть, omp — процессы и демоны. |
| 96 | Голосовой визуализатор | `SpeechInput`, `AudioPlayer`, `Transcription` | `LiveVisualizer` | Частичное | ZCode показывает запись внутри поля, omp — полноэкранный спектр и фазы. |
| 97 | Копирование и экспорт | `ConversationShare*`, действия копирования | `CopySelectorComponent`, `copy-targets.ts` | Частичное | ZCode публикует разговор, omp копирует выбранные блоки. |

## 7. Что не сопоставилось

За таблицей остались зоны, у которых нет второй стороны: оконный хром и
титлбар, постоянный сайдбар проектов, встроенный браузер и CUA, удалённые
SSH/WSL-подключения, шаринг разговоров, PDF/PPTX/DOCX-вьюверы, награды и
маркетинговые поверхности, боты и мессенджеры, ресурсный менеджер целиком,
workflow-граф и его панели, а также TUI-специфичные вещи — TSP, Glyph
Protocol, мультиплексоры, QR, LaTeX и полноэкранные приложения вроде
`ps-top` и git-TUI.

Эти зоны перечислены в двух каталогах и остаются материалом для отдельных
сопоставлений, если появится третий UI или понадобится перенос конкретной
идеи.

## 8. Сводка

В таблице 97 пар: 78 полных, 18 частичных, 1 концептуальная. Полные пары
образуют ядро, которое переносится между средами почти один в один:
композер, транскрипт, карточки инструментов, списки, настройки, темы и
статус. Частичные пары полезны как ориентир по данным, но требуют
собственной модели взаимодействия. Концептуальные пары — только источник
формы, не функциональности.