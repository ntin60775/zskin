# oh-my-pi TUI — полный разбор на компоненты

Каталог разбирает терминальный UI oh-my-pi (`omp`, форк Pi от Stencil Labs) на
компоненты: от рендер-цикла и раскладки до отдельной пилюли статус-лайна.
Источник — клон `/home/prog7/home/dev/contrib/clones/oh-my-pi`, пакет
`packages/tui/src` (424 файла `.ts`, 345 файлов с экспортируемыми символами).

## 1. Границы разбора

- Разобран **весь пакет `packages/tui`**: 14 каталогов и корень, 424 файла.
- Главный потребитель — `packages/coding-agent`: он собирает экран из
  `Composer`, транскрипта и оверлеев. Сам `packages/coding-agent` в каталог
  не входит, но его точки сборки названы там, где без них непонятна роль
  компонента.
- Компонент TUI живёт двойной жизнью: ANSI-строки через
  `render(width): readonly string[]` и семантическое дерево `describe()`
  для TSP. Если у компонента есть только ANSI-рендер, это отмечено.
- Числа файлов — по срезу клона на 2026-10-21. Классификация элементов
  дополняет [oh-my-pi-tui-classification.md](oh-my-pi-tui-classification.md),
  но не заменяет её: там карта назначения, здесь — компонентный состав.

## 2. Слои

| Слой | Что содержит | Где живёт |
|---|---|---|
| L4. Приложения | полноэкранные TUI: сессии, git, процессы, отладка, визуализатор | `apps/` |
| L3. Оверлеи и визарды | диалоги, пикеры, панели, настройки, онбординг | `overlays/`, `setup/` |
| L2. Композиции экрана | композер, транскрипт, хром, статус-лайн, карточки инструментов | `prompt/`, `chat/`, `chrome/`, `status-line/`, `tools/` |
| L1. Компоненты | текст, markdown, списки, формы, раскладка, медиа | `components/`, `render/` |
| L0. Рантайм | рендер-цикл, терминал, ввод, клавиши, мышь, темы | корень `src/`, `theme/`, `native/` |

Дерево главного экрана:

```text
TUI
└── Composer
    ├── WelcomeComponent
    ├── TranscriptContainer
    │   └── ChatBlock
    │       ├── UserMessageComponent
    │       ├── AssistantMessageComponent
    │       │   ├── Markdown
    │       │   └── thinking-блок
    │       ├── ToolExecutionComponent
    │       │   └── ToolCard / ToolRenderer
    │       ├── BashExecutionComponent / EvalExecutionComponent
    │       └── служебные маркеры и карточки
    ├── StatusLineComponent
    │   └── 28 сегментов + сепараторы
    ├── CustomEditor
    │   ├── Editor
    │   ├── AttachmentChipsBand
    │   └── QueuedMessagesBand
    ├── ComposerHints
    └── OverlayPanel (по требованию)
        ├── SelectList / SettingsList / TreeView
        └── специализированные оверлеи
```

## 3. Ядро рантайма

| Компонент / модуль | Файл | Роль |
|---|---|---|
| `TUI` | `tui.ts` | Рендер-цикл, стек оверлеев, фокус, курсор, синхронизированный вывод, троттлинг, native-бэкенд. |
| `Component`, `Container`, `Focusable`, `OverlayHandle`, `OverlayOptions`, `TerminalFramePlan`, `TerminalFrameProvider` | `tui.ts` | Контракты: рендер, ввод, фокус, оверлей, кадр истории/вьюпорта. |
| `Terminal`, `ProcessTerminal` | `terminal.ts` | Raw-режим, SIGWINCH, emergency restore, backpressure, пробы OSC/DECRQM/TSP. |
| `TerminalAppearance`, `CursorShape`, `CURSOR_SHAPE_CODES` | `terminal.ts` | Внешний вид терминала и курсора. |
| `TerminalCapabilities`, `RuntimeTerminal`, `TERMINAL` | `terminal-capabilities.ts` | Детект терминала и возможностей: kitty, ghostty, wezterm, iterm2, vscode. |
| `StdinBuffer`, `BracketedPasteHandler` | `stdin-buffer.ts`, `bracketed-paste.ts` | Сборка escape-последовательностей и bracketed paste. |
| `Key`, `KeyId`, `ModifierName` | `keys.ts` | Разбор клавиш, Kitty CSI-u, modifyOtherKeys. |
| `Keybindings`, `KeybindingsManager`, `AppKeybinding` | `keybindings.ts`, `app-keybindings.ts` | 28+ действий, конфиг, миграции, конфликты. |
| `VimBuffer`, `VimState`, `VimMode`, `VimOperator` | `vim.ts` | Modal editing: insert/normal/visual, операторы, undo. |
| `KillRing` | `kill-ring.ts` | Emacs kill-ring и yank-pop. |
| `SgrMouseHandler`, `MouseRoutable` | `mouse.ts` | SGR-мышь и маршрутизация координат. |
| `Win32InputModeDecoder`, `Win32PasteMarkerNormalizer` | `windows-input-mode.ts` | Windows ConPTY-ввод и вставка. |
| `AltGrHost`, `RIGHT_ALT_LATCH_MS` | `windows-altgr.ts` | Восстановление AltGr. |
| `FuzzyCorpus`, `FuzzyQuery`, `FuzzyText` | `fuzzy.ts` | Нечёткий поиск и скоринг. |
| `AutocompleteProvider`, `CombinedAutocompleteProvider`, `SlashCommand` | `autocomplete.ts` | Дополнение путей, `@`, slash-команд. |
| `GlyphBundle`, `GlyphProtocolReply` | `glyph-protocol.ts` | APC-протокол нативных глифов. |
| `KittyGraphicsFeatures`, `KITTY_PLACEHOLDER` | `kitty-graphics.ts` | Kitty-графика и placeholder-плейсмент. |
| `MATH_FONT_COMMANDS` | `latex-to-unicode.ts` | Inline-математика в Unicode. |
| `DesktopNotifier` | `desktop-notify.ts` | D-Bus/notify-send уведомления. |
| `SpaceHoldHandler`, `SpaceHoldGesture` | `space-hold.ts` | Push-to-talk. |
| `LoopWatchdog`, `LoopWatchdogOptions` | `loop-watchdog.ts` | Детект блокировки event loop. |
| `TuiDebugServer`, `TuiDebugTree`, `TuiDebugOverlayNode` | `debug-server.ts` | TCP-инспектор TUI: tree/paint/inject. |
| `TerminalMultiplexer`, `TERMINAL_MULTIPLEXER_ENV_KEYS` | `terminal-multiplexer.ts` | Определение tmux/screen/zellij и passthrough. |
| `activeTerminal` | `active-terminal.ts` | Singleton активного терминала для out-of-band escape: заголовок, OSC 52. |
| `KeybindingMatchers` | `keybinding-matchers.ts` | Сопоставление клавиш с действиями и модификаторами. |
| `HotkeysSheetComponent`, `KeyName` | `hotkeys-markdown.ts`, `key-hint-format.ts` | Лист горячих клавиш и форматирование подсказок. |
| `langFromPath` | `lang-from-path.ts` | Язык по расширению и пути файла. |
| `LatexBlock` | `latex-block.ts` | 2D-layout display-формул: дроби, матрицы, радикалы. |
| `Sixel` | `sixel.ts` | Кодирование и вывод sixel-изображений. |
| `TmuxPassthrough` | `tmux.ts` | Passthrough escape-последовательностей через tmux. |
| `TtyId` | `ttyid.ts` | Идентификация TTY. |
| `index.ts` | `index.ts` | Публичный барель пакета. |
| `ThinkingLevelMetadata`, `CLI_THINKING_LEVELS` | `thinking.ts` | Уровни мышления. |
| `BoxSymbols`, `SymbolTheme` | `symbols.ts` | Пресеты символов. |
| `visibleWidth`, `truncateToWidth`, `sliceByColumn`, `wrapTextWithAnsi` | `utils.ts` | ANSI-aware ширина, обрезка, перенос. |
| `DeccaraPlan`, `BgFillAnalysis` | `deccara.ts` | Оптимизация фонов DECCARA. |
| `EditorComponent` | `editor-component.ts` | Контракт редактора для композера. |

## 4. Компоненты и раскладка

### 4.1 Текст, контейнеры, данные

| Компонент | Файл | Роль |
|---|---|---|
| `Text` | `components/text.ts` | Текстовый блок. |
| `TruncatedText` | `components/truncated-text.ts` | Текст с обрезкой по ширине. |
| `WidthAwareText` | `render/width-aware-text.ts` | Текст, форматируемый только при известной ширине. |
| `Markdown` | `components/markdown.ts` | Полный MD-рендер: код, таблицы, ссылки, LaTeX; кэш. |
| `Box`, `BoxBorder` | `components/box.ts` | Контейнер с рамкой и отступами. |
| `Section`, `SectionOptions` | `components/section.ts` | Контейнер с заголовком. |
| `Spacer` | `components/spacer.ts` | Вертикальный и горизонтальный зазор. |
| `Disclosure`, `DisclosureSlot` | `components/disclosure.ts` | Аккордеон: summary и ленивое тело. |
| `KeyValueList`, `KeyValueRow` | `components/key-value-list.ts` | Пары «ключ: значение». |
| `MetricRow`, `MetricSpec`, `MetricOverflow` | `components/metric.ts` | Строка метрик. |
| `ProgressBar`, `ProgressBarStyle` | `components/progress-bar.ts` | Полоса прогресса. |
| `Sparkline`, `SPARK_LEVELS` | `components/sparkline.ts` | Мини-график. |
| `Table`, `TableColumn`, `TableCell` | `components/table.ts` | Таблица с выравниванием и гибкой шириной. |
| `TabBar`, `Tab` | `components/tab-bar.ts` | Панель вкладок. |
| `TreeView`, `TreeRow`, `TreePrefix` | `components/tree-view.ts` | Дерево с префиксами и flatten. |
| `SelectList`, `SelectItem` | `components/select-list.ts` | Список выбора. |
| `MenuSelection`, `MenuWindow`, `MenuActivation` | `components/menu-selection.ts` | Меню поверх `SelectList`. |
| `SettingsList`, `SettingItem`, `PrefsSectionRef` | `components/settings-list.ts` | Список настроек с секциями и editing state. |
| `Form`, `FormField`, `TextFormField`, `SelectFormField` | `components/form.ts` | Формы с валидацией и фокусом. |
| `WizardStep`, `WizardStepKind` | `components/wizard-step.ts` | Шаг визарда. |
| `Input` | `components/input.ts` | Однострочное поле. |
| `Editor` | `components/editor.ts` | Многострочный редактор: подсветка, декорации, paste, native layout. |
| `Loader`, `CancellableLoader` | `components/loader.ts`, `cancellable-loader.ts` | Спиннеры и отменяемая загрузка. |
| `Image`, `ImageBudget` | `components/image.ts` | Inline-картинки: Kitty, Sixel, iTerm2. |
| `ScrollView`, `ScrollAnchor` | `components/scroll-view.ts` | Скролл с follow-tail, якорями и thumb. |
| `ScrollViewport`, `ScrollbarThumbRange`, `ViewportRange` | `components/scroll-viewport.ts` | Чистые функции вьюпорта. |

### 4.2 Лэйаут

| Компонент | Файл | Роль |
|---|---|---|
| `Stack`, `StackChild` | `components/layout/stack.ts` | Вертикальный стек, gap, hit-test. |
| `Row`, `RowChild` | `components/layout/row.ts` | Горизонтальный ряд. |
| `SplitPane`, `SplitPaneGeometry` | `components/layout/split-pane.ts` | Две панели с resizable-разделителем. |
| `LayoutRect`, `LayoutInsets`, `LayoutContent`, `LayoutRenderer` | `components/layout/geometry.ts` | Геометрия, отступы, аллокация ширины, mouse-guards. |

### 4.3 Переиспользуемые рендер-блоки

| Компонент | Файл | Роль |
|---|---|---|
| `renderOutputBlock`, `CachedOutputBlock`, `FramedBlockComponent` | `render/output-block.ts` | Рамка, кэш и отрисовка вывода. |
| `OutputPane`, `OutputPaneEdge` | `render/output-pane.ts` | Панель вывода с обрезкой. |
| `ToolCard`, `ToolCardBuildContext`, `ToolCardSnapshot` | `render/tool-card.ts` | Универсальная карточка инструмента. |
| `WidthAwareText` | `render/width-aware-text.ts` | Текст с отложенным форматированием. |
| `RenderCache`, `Hasher` | `render/utils.ts` | Кэш рендера. |
| `RenderedStringCache`, `ToolUIStatus`, `ToolUITitleOptions` | `render/render-utils.ts` | Кэш строк, статусы и заголовки инструментов. |
| `FileListOptions`, `TreeListOptions`, `CodeCellOptions` | `render/file-list.ts`, `tree-list.ts`, `code-cell.ts` | Списки файлов, деревья, кодовые ячейки. |
| `StatusLineOptions` | `render/status-line.ts` | Опции отрисовки статус-строки. |

## 5. Композер

### 5.1 Ядро

| Компонент | Файл | Роль |
|---|---|---|
| `Composer` | `prompt/composer.ts` | Владеет терминалом, welcome, редактором, статусом и runtime-детьми. |
| `CustomEditor` | `prompt/custom-editor.ts` | Редактор композера: клавиши interrupt/model/thinking, чипы, shimmer, spell-check, очередь, shell-режим. |
| `WelcomeComponent` | `prompt/welcome.ts` | Лого, tip и intro-анимация. |
| `ComposerCache`, `ComposerStartupCache` | `prompt/composer-cache.ts` | Кэш первого кадра. |
| `EditorTopGap` | `prompt/editor-top-gap.ts` | Верхний зазор редактора. |
| `ComposerHint`, `ComposerHintContext` | `prompt/composer-hints.ts` | Обучающие подсказки в пустом поле. |
| `AttachmentChipsBand` | `prompt/attachment-chips.ts` | Полоса чипов вложений. |
| `QueuedMessagesBand`, `QueuedMessageGroup` | `prompt/queued-messages.ts` | Очередь над редактором. |
| `ComposerChipDescriptor`, `ComposerNativeState`, `TextAttachment` | `prompt/custom-editor.ts` | Чипы и native-состояние. |
| `ChipKind`, `PlaceholderRenderers`, `COMPOSER_TOKEN_REGEX` | `prompt/composer-attachments.ts` | Токены и плейсхолдеры вложений. |
| `ComposerStyle`, `ComposerBox`, `ComposerChromeContext`, `ComposerRowContext` | `components/composer/types.ts` | Контракт стиля рамки композера. |
| `registerComposerStyle`, `isBuiltinComposerStyle` | `components/composer/registry.ts` | Реестр стилей. |

### 5.2 Восемь стилей обвязки

| Стиль | Файл | Силуэт |
|---|---|---|
| `box` | `components/composer/box.ts` | Скруглённая рамка, статус в границе. |
| `band` | `components/composer/band.ts` | Powerline-полоса, купол. |
| `claude` | `components/composer/claude.ts` | Линии и статус-чип, `❯`. |
| `pi` | `components/composer/pi.ts` | Линии сверху и снизу. |
| `borderless` | `components/composer/borderless.ts` | Голый `❯`. |
| `rule` | `components/composer/rule.ts` | Одна линия. |
| `field` | `components/composer/field.ts` | Заполненное поле с акцент-капами `▐▌`. |
| `rail` | `components/composer/rail.ts` | Левая рейка `▎`. |

### 5.3 Автодополнения и текст

| Компонент / модуль | Файл | Роль |
|---|---|---|
| `SlashCommand` | `autocomplete.ts` | Slash-команды. |
| `PromptActionAutocompleteProvider` | `prompt/prompt-action-autocomplete.ts` | Действия в промпте. |
| `InternalUrlCallerContext`, `InternalUrlCompletionHost` | `prompt/internal-url-autocomplete.ts` | `skill://`, `memory://` и другие схемы. |
| `GithubRefContext` | `prompt/github-ref-autocomplete.ts` | `#N` — PR/issue. |
| `ModelMentionCandidateSource`, `ModelMention` | `prompt/model-mention-autocomplete.ts`, `model-mention-syntax.ts` | `^` — упоминания моделей. |
| `EmojiAutocomplete` | `prompt/emoji-autocomplete.ts` | `:name` и раскрытие `:-)`. |
| `WordCompletionEngine`, `WordPredictionBackend` | `prompt/word-completion.ts` | Ghost-text слов. |
| `KeywordHighlighter`, `GradientHighlightSpec` | `prompt/gradient-highlight.ts` | Градиентная подсветка. |
| `MagicKeywordSpec` | `prompt/magic-keywords.ts` | Слова с shimmer. |
| `ProseSource`, `SpellingDecorationContext` | `prompt/prose-gate.ts` | Отличие прозы от кода и путей. |
| `MacOSSpellingProvider`, `SpellingBackend` | `prompt/macos-spelling.ts` | Нативная проверка орфографии. |
| `TypingWord`, `TypingWordTracker` | `prompt/typing-word.ts` | Отслеживание слова под курсором. |
| `SkillToken`, `SKILL_TOKEN_RE` | `prompt/skill-tokens.ts` | Токены скиллов. |
| `ImageAttachmentSource`, `SourceTaggedImage`, `VideoPreviewImage` | `prompt/image-source.ts`, `video.ts` | Источники изображений и видео. |
| `ToolsMarkdownBindings` | `prompt/tools-markdown.ts` | Привязка markdown к инструментам. |
| `QUEUE_LIST_MARKER_RE` | `prompt/queue-input.ts` | Маркер очереди во вводе. |
| `AssistantMessageHost`, `AssistantMessageSession` | `prompt/interactive-context-helpers.ts` | Контекст интерактивных сообщений. |

## 6. Транскрипт

### 6.1 Сборка и контейнер

| Компонент | Файл | Роль |
|---|---|---|
| `ChatTranscriptBuilder` | `chat/chat-transcript-builder.ts` | Собирает блоки транскрипта из сообщений. |
| `TranscriptContainer`, `TranscriptBlock`, `TranscriptStableRow` | `chrome/transcript-container.ts` | Жизненный цикл блоков: active, settled, committed; append-only. |
| `ChatBlock`, `ChatBlockHost` | `chrome/chat-block.ts` | Блок транскрипта и его хост. |
| `TranscriptEntryLike`, `SessionMessageEntryLike` | `chat/transcript-entry.ts` | Входные типы записей. |
| `ChatTranscriptDisplayPreferences` | `chat/display-preferences.ts` | Глобальные тогглы отображения. |
| `TranscriptAction` | `chat/transcript-actions.ts` | Шина retry/rewind/copy. |
| `TranscriptBrowser` | `chat/transcript-browser.ts` | Полноэкранный просмотр истории; `TranscriptBrowserBody` и `TranscriptBrowserFrame` задают его раскладку. |
| `OutlineRowCache`, `composeOutlineColumn`, `positionRail`, `OutlineTarget` | `chat/transcript-outline.ts` | Оглавление, колонка и рельс выделенного хода. |

### 6.2 Сообщения

| Компонент | Файл | Роль |
|---|---|---|
| `UserMessageComponent`, `CollapsedSyntheticMessageComponent` | `chat/user-message.ts` | Пузырь пользователя: MD, чипы, реакции, hover-тулбар. |
| `AssistantMessageComponent` | `chat/assistant-message.ts` | Ответ: MD, thinking, изображения, inline-ошибки, стриминг. |
| thinking-блок `AssistantMessageComponent` + `thinking-display.ts` | `chat/assistant-message.ts`, `chat/thinking-display.ts` | Сворачивание thinking, tok/s, индикатор; `thinking-display.ts` держит форматирование и фолдинг. |
| `BashExecutionComponent` | `chat/bash-execution.ts` | PTY-фрейм ` $ cmd`, tail, стриминг, sixel. |
| `EvalExecutionComponent` | `chat/eval-execution.ts` | `>>>` Python/JS. |
| `ToolExecutionComponent`, `ToolExecutionHandle`, `ToolResultFrame` | `chat/tool-execution.ts` | Универсальный фрейм tool call/result. |
| `ReadToolGroupComponent` | `chat/read-tool-group.ts` | Группировка read'ов. |
| `SkillMessageComponent` | `chat/skill-message.ts` | `/skill:` callout. |
| `HookMessageComponent` | `chat/hook-message.ts` | Сообщение hook. |
| `CustomMessageComponent` | `chat/custom-message.ts` | Кастомное сообщение расширения. |
| `AdvisorMessageCard` | `chat/advisor-message.ts` | Заметки советника. |
| `RecapNotice` | `chat/recap-notice.ts` | Итоговая сводка. |
| `TodoReminderComponent` | `chat/todo-reminder.ts` | Напоминание о todo. |
| `LateDiagnosticsMessageComponent` | `chat/late-diagnostics-message.ts` | LSP-диагностика после правки. |
| `CacheInvalidationMarkerComponent` | `chat/cache-invalidation-marker.ts` | Cache miss. |
| `ServedModelMarkerComponent` | `chat/served-model-marker.ts` | Ответ не той моделью. |
| `CompactionSummaryMessageComponent`, `BranchSummaryMessageComponent`, `HandoffSummaryMessageComponent` | `chat/compaction-summary-message.ts` | Точки сжатия и передачи. |
| `StrippedToolCallsPlaceholder` | `chat/stripped-tool-calls-placeholder.ts` | Заглушка вырезанных вызовов. |
| `TtsrNotificationComponent` | `chat/ttsr-notification.ts` | Уведомление TTSR. |
| `CollabPromptMessageComponent` | `chat/collab-prompt-message.ts` | Коллаб-промпт. |
| `BackgroundTanDispatchDetails`, `BackgroundTan...` | `chat/messages.ts`, `background-tan-message.ts` | Фоновые сообщения. |
| `FigureMarkdown`, `FenceFigure` | `chat/figure-markdown.ts`, `fence-figure.ts` | Markdown с figure. |
| `SvgFigure`, `FigureSegment` | `chat/svg-figure.ts`, `svg-source.ts` | SVG-фигуры. |
| `TableChartFigure`, `TableChartPlanner` | `chat/table-chart.ts` | Таблица как график. |
| `ReactionSplit`, `ReactionTarget` | `chat/reaction.ts` | Реакции. |
| `SkillTitleInput` | `chat/skill-title-input.ts` | Заголовок скилла. |
| `AssistantErrorPresentation` | `chat/transcript-render-helpers.ts` | Ошибка ответа. |
| `ImageInputTooLargeError`, `InvalidImageDataError` | `chat/image-loading.ts` | Ошибки изображений. |

## 7. Хром чата

| Компонент | Файл | Роль |
|---|---|---|
| `TranscriptContainer` | `chrome/transcript-container.ts` | Контейнер и жизненный цикл блоков. |
| `TranscriptStatusBlock`, `TranscriptStatusRow`, `TranscriptStatusPart` | `chrome/transcript-status.ts` | Статусные строки транскрипта. |
| `ChatBlock` | `chrome/chat-block.ts` | Блок транскрипта. |
| `FramedMessage`, `FramedMessageComponent`, `FramedRenderer` | `chrome/message-frame.ts` | Рамка extension/hook-сообщений. |
| `MessageNoticeComponent`, `MessageNoticePresentation` | `chrome/message-notice.ts` | Toned notice-card. |
| `MessageDividerComponent` | `chrome/message-divider.ts` | Разделитель сообщений. |
| `ToolActivityComponent`, `ToolActivityContainer` | `chrome/tool-activity.ts` | Переключатель видимости tool-активности. |
| `StreamingPanelContent`, `StreamingPanelPresentation` | `chrome/streaming-panel.ts` | Shell стриминговых оверлеев. |
| `OverlayPanel`, `PanelRows`, `PanelDivider` | `chrome/overlay-box.ts` | Хром диалогов. |
| `StatusNotice`, `StatusNoticeOptions` | `chrome/status-notice.ts` | Toast на 2,4 с. |
| `ErrorBlock` | `chrome/error-block.ts` | Ограниченный вывод ошибок. |
| `DynamicBorder` | `chrome/dynamic-border.ts` | Подвижная граница. |
| `Diff` (`RenderDiffOptions`) | `chrome/diff.ts` | ANSI-диффы, intra-line word-diff. |
| подсказки клавиш: `keyHint`, `appKeyHint`, `rawKeyHint` | `chrome/keybinding-hints.ts` | Форматирование подсказок для действий и сырых клавиш. |
| `SegmentTrack`, `TrackSegment` | `chrome/segment-track.ts` | Powerline-трек ролей и уровней. |
| `ContextUsageLevel` | `chrome/context-thresholds.ts` | Тиры заполнения контекста. |
| `QrCode`, `QrEcLevel` | `chrome/qrcode.ts` | QR-генератор. |
| `CollabQrCodeComponent` | `chrome/collab-qrcode.ts` | QR коллаб-сессии. |
| `CountdownTimer` | `chrome/countdown-timer.ts` | Таймер обратного отсчёта. |
| `LiveBoard`, `LiveBoardOutput` | `chrome/live-board.ts` | Перерисовываемая доска для CLI. |
| `VisualTruncateResult` | `chrome/visual-truncate.ts` | Визуальная обрезка. |
| `SelectorHelpers`, `SelectListMouseRouting` | `chrome/selector-helpers.ts`, `select-list-mouse-routing.ts` | Общие помощники селекторов. |
| `Format`, `LocalDate`, `FormTheme` | `chrome/format.ts`, `local-date.ts`, `form-theme.ts` | Форматирование и тема форм. |

## 8. Рендереры инструментов

### 8.1 Контракт и инфраструктура

| Компонент | Файл | Роль |
|---|---|---|
| `ToolRenderer` | `tools/renderer.ts` | Контракт `renderCall`/`renderResult` + `describe*`. |
| `toolRenderers`, `DefaultToolRenderInput` | `tools/index.ts`, `default-renderer.ts` | Реестр и рендерер по умолчанию. |
| `ToolCard`, `ToolCardSnapshot`, `ToolCardSection` | `render/tool-card.ts` | Карточка вызова и результата. |
| `CardToolResult` | `tools/result-card.ts` | Кэш-карточки. |
| `OutputSink`, `TailBuffer`, `TruncationResult` | `tools/streaming-output.ts` | Стриминг, хвостовые окна, лимиты 3000 строк/50 КБ. |
| `JsonTree` | `tools/json-tree.ts` | JSON-дерево со свёрткой. |
| `GroupedFilesOutput`, `FileMatchSection` | `tools/grouped-file-output.ts` | Группировка по файлам. |
| `NativeToolView`, `NativeToolHead` | `tools/native-view.ts` | TSP-строители. |
| `OutputMeta`, `DiagnosticMeta`, `LimitsMeta` | `tools/output-meta.ts` | Метаданные вывода. |
| `LineRange`, `BareLineMode` | `tools/line-ranges.ts` | Диапазоны строк. |
| `TerminalOutput` | `tools/terminal-output.ts` | Терминальный вывод. |
| `HlFilePrefix`, `HL_LINE_BODY_SEP` | `tools/hashline-format.ts` | Формат hashline. |
| `ToolError` | `tools/tool-errors.ts` | Ошибки инструментов. |

### 8.2 Специализированные рендереры

| Домен | Компоненты и модули |
|---|---|
| Файлы | `read`, `edit`, `write`, `grep`, `find`, `glob`, `ast-grep`, `ast-edit` |
| Исполнение | `bash`, `bash-interactive`, `eval`, `subprocess`, `terminal-output` |
| Агенты | `task`, `agent-tree`, `ask`, `wait`, `yield`, `task-yield-assembly`, `task-repair-args` |
| Планирование | `todo`, `goal`, `think` |
| Сеть и данные | `fetch`, `web-search`, `web-search-types`, `github`, `gh-format`, `mcp`, `lsp` |
| Память и контекст | `memory`, `resolve`, `cfg-render`, `cfg-url`, `proc-render`, `xd-url`, `xdev` |
| Спец-инструменты | `debug`, `daemon`, `irc`, `vibe`, `autoresearch`, `conflict-detect`, `report-tool-issue` |
| Виджеты | `job-widget` (JobTile, JobWidgetGridBlock, JobWidgetMeterBlock, JobWidgetSparkBlock), `json-tree`, `grouped-file-output` |

### 8.3 Полный состав `tools/`

| Файл | Роль |
|---|---|
| `renderer.ts` | Контракт `ToolRenderer`: вызов, результат, native-описание. |
| `index.ts` | Реестр рендереров по имени инструмента. |
| `default-renderer.ts` | Фолбэк для неизвестного инструмента. |
| `result-card.ts` | Кэшированная карточка результата. |
| `streaming-output.ts` | Стриминг, хвостовые окна, лимиты и артефакты. |
| `json-tree.ts` | JSON-дерево со свёрткой. |
| `grouped-file-output.ts` | Группировка совпадений по файлам. |
| `native-view.ts` | Строители TSP-представления. |
| `output-meta.ts` | Метаданные вывода: диагностика, лимиты, источник. |
| `line-ranges.ts` | Диапазоны строк и режим «голых» строк. |
| `terminal-output.ts` | Стилизация и чтение терминальных строк. |
| `hashline-format.ts` | Формат hashline для правок. |
| `match-line-format.ts` | Формат строк совпадений. |
| `list-limit.ts` | Ограничение длины списков. |
| `tool-errors.ts` | Типы ошибок инструментов. |
| `read.ts` | Чтение файла с диапазонами и усечением. |
| `edit.ts` | Патч, режимы правки, diff по файлам. |
| `write.ts` | Создание и перезапись файла. |
| `grep.ts` | Поиск по содержимому. |
| `find.ts` | Семантический поиск с coverage и score. |
| `glob.ts` | Поиск по маске. |
| `ast-grep.ts` | Структурный поиск по AST. |
| `ast-edit.ts` | Структурная правка по AST. |
| `bash.ts` | Shell-команда, preview и wall-time. |
| `bash-interactive.ts` | PTY-оверлей интерактивной команды. |
| `eval.ts` | Python/JS-ячейки и таблицы. |
| `subprocess.ts` | Рендерер подпроцесса. |
| `task.ts` | Дерево субагентов, findings, review. |
| `agent-tree.ts` | Строки дерева агентов и статистика. |
| `ask.ts` | Вопросы и ответы инструмента. |
| `wait.ts` | Ожидание агента или задания. |
| `yield.ts` | Промежуточная выдача результата. |
| `task-yield-assembly.ts` | Сборка секций yield. |
| `task-repair-args.ts` | Починка аргументов задачи. |
| `todo.ts` | Фазы, статусы и зачёркивание todo. |
| `goal.ts` | Цель и бюджет. |
| `think.ts` | Блок размышления. |
| `fetch.ts` | Загрузка URL. |
| `web-search.ts` | Ответ поиска и источники. |
| `web-search-types.ts` | Типы поиска и провайдеров. |
| `github.ts` | PR, issue, runs, jobs. |
| `gh-format.ts` | Форматирование GitHub-данных. |
| `mcp.ts` | MCP-контент: текст, изображения, ресурсы. |
| `lsp.ts` | Диагностика LSP по файлу. |
| `memory.ts` | Retain/recall/reflect. |
| `resolve.ts` | Разрешение конфликта или выбора. |
| `cfg-render.ts` | Чтение и запись `cfg://`. |
| `cfg-url.ts` | Схема `cfg://`. |
| `proc-render.ts` | Чтение и запись `proc://`. |
| `xd-url.ts` | Схема `xd://`. |
| `xdev.ts` | Внешний dev-рендерер. |
| `debug.ts` | Отладочный снимок инструмента. |
| `daemon.ts` | Демоны: статус, рестарт, политика. |
| `irc.ts` | Сообщения IRC и квитанции. |
| `vibe.ts` | TV-wall сессий. |
| `autoresearch.ts` | Эксперименты и метрики. |
| `conflict-detect.ts` | Блоки конфликтов. |
| `report-tool-issue.ts` | Отчёт о проблеме инструмента. |
| `job-widget.ts` | Плитки, метры и спарклайны фоновых задач. |
| `url-scheme-host.ts` | Хост внутренних URL-схем. |

## 9. Статус-лайн

| Компонент | Файл | Роль |
|---|---|---|
| `StatusLineComponent` | `status-line/component.ts` | Главный компонент строки, ANSI + native. |
| `SEGMENTS`, `ALL_SEGMENT_IDS` | `status-line/segments.ts` | 28 сегментов: `pi`, `model`, `mode`, `git`, `pr`, `cost`, `context_pct`, `vim`, `collab`, `stream`, токены, время, subagents. |
| `STATUS_LINE_PRESETS` | `status-line/presets.ts` | 7 пресетов: default, minimal, compact, full, nerd, ascii, custom. |
| `STATUS_LINE_SEPARATOR_VALUES`, `SeparatorDef` | `status-line/schema.ts`, `types.ts` | 6 сепараторов. |
| модель расхода контекста: `ContextUsageView`, `ContextBreakdown`, `ContextSavingsEstimate` | `status-line/context-usage.ts` | Расход контекста и разбивка по категориям. |
| `FooterComponent` | `status-line/footer.ts` | Футер: pwd, ветка, статистика. |
| `StatusLineStartupData` | `status-line/startup.ts` | Строка до появления сессии. |
| `BillingSummaryOptions` | `status-line/metrics.ts` | Метрики биллинга. |
| `LoopConditionConfig`, `LoopLimitRuntime` | `status-line/loop.ts` | Лимиты циклов. |
| `PrCacheContext` | `status-line/git-utils.ts` | Кэш PR. |
| `EffectiveStatusLineSettings`, `StatusLineSettings`, `SegmentView` | `status-line/types.ts` | Типы настроек и сегментов. |
| `StatusLineHost`, `FooterHost` | `status-line/host.ts` | Хосты данных статус-строки. |

## 10. Оверлеи

### 10.1 Сессии и навигация

`SessionSelectorComponent`, `TreeSelectorComponent`, `RewindSelectorComponent`,
`HistorySearchComponent`, `SessionInfoOverlay`, `MoveOverlay`, `PauseScreenComponent`,
`ShowImagesSelectorComponent`, `SessionObserverRegistry`, `RunningSubagentRegistrySource`.

### 10.2 Модели и аккаунты

`ModelBrowser`, `ModelHubComponent`, `ModelPickerComponent`, `model-selector.ts`,
`LoginDialogComponent`, `LogoutAccountSelectorComponent`, `OAuthSelectorComponent`,
`SessionAccountSelectorComponent`, `ResetUsageSelectorComponent`.

### 10.3 Конфигурация

`SettingsSelectorComponent`, `settings-defs`, `PluginSelectorComponent`,
`PluginSettingsComponent`, `MCPAddWizard`, `HookEditorComponent`, `HookInputComponent`,
`HookSelectorComponent`, `QueueModeSelectorComponent`, `ThinkingSelectorComponent`,
`ThemeSelectorComponent`, `AdvisorConfigOverlayComponent`, `AgentsHubComponent`,
`ExtensionDashboard`, `ExtensionList`, `InspectorPanel`.

### 10.4 Агенты

`AgentHubOverlayComponent`, `AgentHubProjection`, `AgentHubRenderer`, `AgentsHubComponent`,
`AgentTranscriptViewer`, `AgentActivitySource`, `RunningSubagentRegistrySource`,
`HubFrame`, `SidebarEntry`, `StripChip`.

### 10.5 Планы

`PlanReviewOverlay`, `PlanSaveOverlay`, `plan-toc.ts` (`PlanSection`, `parsePlanSections`).

### 10.6 Usage и статистика

`UsageDashboardComponent`, `usage-display.ts`, `usage-row.ts`, `StatsNotice`,
`CodexResetFireworksController`, `TurnUsageTally`.

### 10.7 Спец-панели

`AskDialogComponent`, `BtwPanelComponent`, `BtwHistoryPanel`, `CleansePanelComponent`,
`JobsSheet`, `JobsPanelDetail`, `OmfgPanelComponent`, `ReportPanel`,
`AnnotationOverlay`, `ErrorBannerComponent`, `CopySelectorComponent`,
`ComposerShapePreview`, `SnapcompactShapePreview`, `BorderedLoader`,
`ApprovalDialogComponent`, `ExtensionDashboard`.

### 10.8 Полный состав `overlays/`

| Файл | Роль |
|---|---|
| `approval-dialog.ts` | Подтверждение опасного действия с arm-задержкой. |
| `ask-dialog.ts` | Мультивопрос расширения с вариантами и таймером. |
| `bordered-loader.ts` | Загрузчик в рамке для долгих операций. |
| `error-banner.ts` | Постоянный баннер ошибки над редактором. |
| `hub-frame.ts` | Каркас хаба: сайдбар, чипы, полосы. |
| `pause-screen.ts` | Экран паузы. |
| `report-panel.ts` | Панель отчёта. |
| `stats-notice.ts` | Уведомление статистики. |
| `codex-reset-fireworks.ts` | Фейерверк при сбросе квоты. |
| `composer-shape-preview.ts` | Живое превью формы композера. |
| `composer-shape-registry.ts` | Реестр форм композера. |
| `snapcompact-shape-preview.ts` | Превью формы Snapcompact. |
| `queue-mode-selector.ts` | Выбор режима очереди. |
| `thinking-selector.ts` | Выбор глубины мышления. |
| `theme-selector.ts` | Выбор темы. |
| `settings-selector.ts` | Полноэкранные настройки. |
| `settings-defs.ts` | Определения вкладок, тогглов и enum'ов настроек. |
| `plugin-selector.ts` | Выбор плагина. |
| `plugin-settings.ts` | Настройки установленного плагина и маркетплейс. |
| `mcp-add-wizard.ts` | Визард добавления MCP-сервера. |
| `hook-editor.ts` | Редактор hook. |
| `hook-input.ts` | Ввод hook. |
| `hook-selector.ts` | Выбор hook и слайдеры. |
| `model-browser.ts` | Каталог моделей по ролям. |
| `model-hub.ts` | Назначение моделей ролям. |
| `model-picker.ts` | Выбор модели. |
| `model-selector.ts` | Разбор строки модели и thinking-суффикса. |
| `login-dialog.ts` | Вход по OAuth device-flow. |
| `logout-account-selector.ts` | Выбор аккаунта для выхода. |
| `oauth-selector.ts` | Выбор OAuth-провайдера. |
| `session-account-selector.ts` | Аккаунт текущей сессии. |
| `reset-usage-selector.ts` | Сброс usage-аккаунта. |
| `session-selector.ts` | Выбор сессии с поиском. |
| `tree-selector.ts` | Дерево сессий и фильтры. |
| `rewind-selector.ts` | Откат и выбор ветки. |
| `history-search.ts` | Fuzzy-поиск по промптам. |
| `session-info-overlay.ts` | Информация о сессии. |
| `move-overlay.ts` | Перемещение файла или каталога. |
| `show-images-selector.ts` | Выбор изображений для показа. |
| `session-observer-registry.ts` | Реестр наблюдателей за сессиями. |
| `running-subagent-badge.ts` | Бейдж работающего субагента. |
| `agent-hub.ts` | Хаб агентов: дерево, метрики, live-инспекция. |
| `agent-hub-projection.ts` | Проекция метрик и статусов. |
| `agent-hub-renderer.ts` | Рендер ростера и чипов моделей. |
| `agent-hub-types.ts` | Типы реестра агентов. |
| `agents-hub.ts` | Реестр агентов и генерация спецификаций. |
| `agent-activity.ts` | Лента событий агентов. |
| `agent-transcript-viewer.ts` | Транскрипт агента с send/steer. |
| `plan-review-overlay.ts` | Ревью плана: секции, аннотации. |
| `plan-save-overlay.ts` | Сохранение плана. |
| `plan-toc.ts` | Парсер и сборка оглавления плана. |
| `annotation-overlay.ts` | Code review и текстовые аннотации. |
| `annotation-types.ts` | Типы аннотаций и diff-строк. |
| `copy-selector.ts` | Выбор блоков для копирования. |
| `copy-targets.ts` | Цели копирования: код, сообщение, команда, ссылка. |
| `btw-panel.ts` | Ответы «between the worlds» с follow-up. |
| `btw-history.ts` | Запись истории btw. |
| `btw-history-panel.ts` | Панель истории btw. |
| `cleanse-panel.ts` | Панель очистки. |
| `jobs-panel.ts` | Панель фоновых задач. |
| `job-tree.ts` | Дерево задач и агентов. |
| `omfg-panel.ts` | Панель OMFG. |
| `usage-dashboard.ts` | Дашборд usage: heatmap, карточки, лимиты. |
| `usage-display.ts` | Форматирование лимитов и reset-окон. |
| `usage-row.ts` | Строка usage и tally за ход. |
| `advisor-config.ts` | Визард настроек советника WATCHDOG. |
| `extensions/extension-dashboard.ts` | Дашборд расширений. |
| `extensions/extension-list.ts` | Список расширений и переключатели. |
| `extensions/inspector-model.ts` | Модель инспектора: команды, инструменты, параметры. |
| `extensions/inspector-panel.ts` | Панель инспектора. |
| `extensions/live-tool-session.ts` | Live-сессия инструмента. |
| `extensions/mcp-runtime.ts` | Runtime-снимок MCP: соединения, ресурсы, здоровье. |
| `extensions/types.ts` | Типы расширений и дерева. |

## 11. Приложения

| Приложение | Файл | Роль |
|---|---|---|
| `SessionPickerHost` | `apps/session-picker.ts` | Селектор сессий с поиском и пинами. |
| `StandaloneTuiContext` | `apps/standalone-picker.ts` | Каркас one-shot TUI. |
| `PsTopComponent` | `apps/ps-top.ts` | Процесс-монитор демонов, refresh 2 с. |
| `PsDaemonRow`, `PsScope` | `apps/ps-data.ts` | Данные процессов. |
| `GitTuiHost` | `apps/git/git-tui.ts` | Полноэкранный git-клиент. |
| `DiffPane`, `DiffDocument`, `HunkBlock` | `apps/git/diff-pane.ts` | Диффы: file/split/inline/hunk, выбор строк. |
| `Sidebar`, `GitCommitMessage` | `apps/git/sidebar.ts` | Дерево файлов и форма коммита. |
| `GitHelpSheet` | `apps/git/help.ts` | Помощь git-TUI. |
| `GitTuiModel`, `ChangedFile`, `GitViewState` | `apps/git/state.ts` | Состояние git-TUI. |
| `AvatarSource` | `apps/git/avatar.ts` | Аватары авторов. |
| `LiveVisualizer` | `apps/live-visualizer.ts` | Голосовой режим: спектр, фазы, транскрипт. |
| `AutoresearchDashboardHost`, `DashboardController` | `apps/autoresearch-dashboard.ts` | Панель экспериментов. |
| `CleanseStatusBoard` | `apps/cleanse-board.ts` | Доска очистки. |
| `CleanseCheckerChoice`, `CleanseTargetChoice` | `apps/cleanse-picker.ts` | Выбор проверок и целей. |
| `IfBenchBoard` | `apps/if-bench-board.ts` | Панель бенчмарка. |
| `DebugLogViewerComponent`, `DebugViewerFrame`, `ProtocolProbeComponent`, `RawSseViewerComponent`, `TerminalRuntimeState` | `apps/debug/` | Отладочные экраны. |
| `SetupModelPicker` | `apps/setup-model-picker.ts` | Выбор модели в онбординге. |

## 12. Онбординг

| Компонент | Файл | Роль |
|---|---|---|
| `SetupWizardComponent` | `setup/wizard-overlay.ts` | Полноэкранный визард: splash → transition → scene → outro. |
| `ALL_SCENES`, `SetupSceneSelectionOptions` | `setup/wizard.ts` | Сцены: providers → model → glyph → composer → theme. |
| `SignInScene`, `SplashScene`, `OutroScene` | `setup/scenes/` | Вход, сплэш, финал. |
| `SetupScene`, `SetupSceneController`, `StyledLine` | `setup/scenes/types.ts` | Контракт сцены. |
| `RunStartupSplashOptions` | `setup/startup-splash.ts` | Стартовая анимация. |
| `CURRENT_SETUP_VERSION` | `setup/setup-version.ts` | Гейт версии. |

## 13. Native-слой TSP

| Компонент | Файл | Роль |
|---|---|---|
| `NativeBackend`, `NativeHost`, `NativeOverlay` | `native/backend.ts` | Поверхности, credit-based flow control, blobs, события. |
| `TspReader`, `TspHello`, `TSP_PREFIX` | `native/encode.ts` | APC-фреймы, чанки, base64. |
| `NativeNode`, `NativeChild`, `NativeSurface`, `NativeScroll` | `native/node.ts` | Семантическое дерево. |
| `DescribeContext`, `EMPTY_NODE` | `native/describe.ts` | Строители `card`, `row`, `col`, `kbd`, `picker`, `overlay`, `shimmer`, `spinner`. |
| `TspSpan`, `TspTone` | `native/spans.ts`, `tone.ts` | ANSI → spans и цвета → тоны. |
| `NativeBlob`, `NativeImageCache` | `native/blobs.ts` | sha256-картинки. |
| `Reconciler`, `NativeTarget` | `native/reconcile.ts` | Diff деревьев и move/append-операции. |
| `NativeRegions`, `NativeReveal` | `native/node.ts`, `settle.ts` | Фиксация готовых блоков. |
| `SelectListSheet`, `SelectPickerOptions` | `native/picker.ts` | Нативный пикер. |
| `NativeHint`, `ActionButtonOptions` | `native/overlay.ts` | Хром диалогов. |
| `Memo`, `OwnerMemo` | `native/memo.ts` | Мемоизация `describe`. |
| `TspDocument`, `TspApplyError` | `native/apply.ts` | Тестовый applier. |
| `NativeThemePalette`, `NativeThemeVariant` | `theme/theme.ts` | Палитра для native-слоя. |

## 14. Темы и символы

| Компонент | Файл | Роль |
|---|---|---|
| `Theme` | `theme/theme-class.ts` | `fg/bg/bold/dim/symbol`, 45+ именованных цветов. |
| `ThemeJson`, `ThemeColor`, `ThemeBg` | `theme/schema.ts` | Схема JSON-темы. |
| `validateThemeJson` | `theme/schema-validation.ts` | Валидация пользовательских тем. |
| `loadThemeJson`, `ThemeInfo` | `theme/loader.ts` | Загрузка встроенных и пользовательских тем. |
| `SessionAccentTheme` | `theme/session-color.ts` | Хэш → OKLCH hue, WCAG-контраст. |
| `ShimmerPalette`, `ShimmerMode`, `ShimmerSegment` | `theme/shimmer.ts` | Sweep и KITT-сканер. |
| `SYMBOL_PRESETS`, `SymbolMap`, `SymbolKey`, `SPINNER_FRAMES` | `theme/symbols.ts` | 3 пресета символов, ~130 ключей. |
| `TuiAdapters` | `theme/tui-adapters.ts` | Мост к tree-sitter, markdown, editor, select. |
| `MermaidResolveOptions` | `theme/mermaid-cache.ts` | Кэш mermaid. |
| `BG_RESET`, `FG_RESET` | `theme/color.ts` | Сброс цвета. |

## 15. Графики, мультиплексоры, прочее

| Группа | Компоненты | Роль |
|---|---|---|
| Графики | `ChartPlan`, `ChartSpec`, `ChartSeries`, `Ladder`, `TableAnalysis`, `renderChartSvg` | Планирование и SVG-рендер графиков. |
| Мультиплексоры | `cmuxMultiplexer`, `herdrMultiplexer`, `orcaMultiplexer`, `screenMultiplexer`, `tmuxMultiplexer`, `wmuxMultiplexer`, `zellijMultiplexer`, `spawnNotifier` | Passthrough, фон, гиперссылки, уведомления. |
| Отладка TUI | `TuiDebugServer`, `DebugLogViewer`, `ProtocolProbe`, `RawSseViewer` | Инспекция дерева, протокола и SSE. |
| Утилиты | `visibleWidth`, `truncateToWidth`, `wrapTextWithAnsi`, `replaceTabs` | Общая ширина и безопасность строк. |

## 16. Стилевые хуки

| Слой | Что настраивается | Как |
|---|---|---|
| Тема | 60+ токенов: текст, границы, фоны сообщений, diff, синтаксис, режимы, статус-лайн | `theme/*.json`, `Theme` |
| Символы | 3 пресета, ~130 ключей, спиннеры | `symbols.preset`, `symbols.overrides` |
| Композер | 8 силуэтов, цвет статуса в границе, чипы, shimmer | `ComposerStyle`, `registerComposerStyle` |
| Статус-лайн | 28 сегментов, 7 пресетов, 6 сепараторов, 5 лэйаутов | `status-line/schema.ts` |
| Транскрипт | рамки сообщений, diff, notice, разделители | `theme`, `chrome/*` |
| Инструменты | фазы, рамки, статусы, фон | `ToolCard`, `ToolRenderer` |
| Оверлеи | рамка, отступы, заголовок, хинты | `OverlayPanel`, `hub-frame` |
| Нативный слой | тоны, иконки, shimmer, spinner | `NativeNode`, `tone.ts` |

## 17. Покрытие исходников

| Модуль | Файлов | Что покрыто |
|---|---:|---|
| `overlays/` | 75 | все диалоги, пикеры и панели |
| `tools/` | 63 | контракт и все рендереры |
| `components/` | 41 | примитивы, раскладка, стили композера |
| `chat/` | 39 | сообщения, исполнение, маркеры, навигация |
| `prompt/` | 31 | композер, автодополнения, вложения |
| `chrome/` | 28 | контейнер, рамки, diff, тосты |
| `apps/` | 25 | сессии, git, процессы, отладка |
| `render/` | 16 | карточки, панели, кэш |
| `native/` | 15 | TSP-слой |
| `status-line/` | 14 | сегменты, пресеты, футер |
| `theme/` | 14 | темы, символы, shimmer |
| `setup/` | 13 | визард и сцены |
| `multiplexers/` | 9 | tmux/screen/zellij и уведомления |
| `charts/` | 3 | планирование и SVG-графики |
| корень `src/` | 38 | рендер, терминал, ввод, клавиши, утилиты |

Не вошли как отдельные компоненты: чистые типы, схемы, данные и утилиты без
собственного рендера. Они перечислены в таблицах там, где задают поведение
видимого компонента.