# План 5. Композер

Шаг 5 — композер. Только палитра: силуэт, ширина и центровка остаются
стоковыми (прежние A1/A2 откачены).

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 5.1. Композер целиком (пара 19)
`ConversationComposer`, `V4ComposerToolbar`.
**Что.** Поле на `#1d2021`, рамка `#504945`, фокус brand; тулбар — текст
`#bdae93`; геометрию и раскладку не менять.
**Как.** `--color-input*` (есть); `[data-composer-layout]` — только цвета,
без width/padding.

### 5.2. Текстовый редактор (пара 21)
`LexicalChatInput`, `ChatPromptEditor`.
**Что.** Текст `#ebdbb2`, плейсхолдер `#928374`, каретка brand, выделение —
`#504945`.
**Как.** `[data-slot="textarea"]`, `caret-color: var(--color-brand)`;
`::selection` уже есть.

### 5.3. Отправка и стоп (пара 22)
`PromptInputSubmit`, `PromptInputButton`.
**Что.** Отправка: фон brand, иконка `#1d2021`; disabled — фон `#32302f`,
иконка `#7c6f64`; стоп — destructive.
**Как.** `[data-slot="button"]` в футере поля; `--color-foreground-inverse`.

### 5.4. Выбор модели (пара 23)
`ComposerModelMenu`, `V4ComposerModelControls`.
**Что.** Меню на `#1d2021`; выбранная модель — `#3c3836`, ховер —
`#32302f`; метаданные — `#928374`; компакт-иконка модели — как есть.
**Как.** `[data-slot="select-item"]`/`dropdown-menu-item`, `data-model-*`.

### 5.5. Провайдер и аккаунт (пара 24)
`ComposerProviderMenu`.
**Что.** Как 5.4 + статус-точка провайдера (success/warning/error) и
dim-подпись аккаунта.
**Как.** `[data-provider-status]`, токены status.

### 5.6. Глубина мышления (пара 25)
`ThoughtLevelCycleControl`, `ComposerEffortHeading`.
**Что.** Уровень — brand, подпись — `#928374`; активный сегмент —
`#3c3836`.
**Как.** `[data-composer-thought-control]`, `[data-slot="tabs-trigger"]`.

### 5.7. Режим работы (пара 26)
`ChatModeSwitchControl`, `V4ComposerModeSwitch`.
**Что.** Сегмент: активный — фон `#3c3836`, текст `#ebdbb2`; неактивный —
`#bdae93`.
**Как.** `[data-slot="tabs-trigger"]`, `--color-selected`.

### 5.8. Расход контекста (пара 27)
`ChatContextUsage`, `ContextQuotaResetOpportunityReminderContent`.
**Что.** Шкала — ramp `context-breakdown`; предупреждение — `#fabd2f`,
критично — `#fb4934`; не скрывать.
**Как.** `--color-context-breakdown-*` (есть), `data-context-*`.

### 5.9. Расход и стоимость (пара 28)
`ChatCodingPlanMcpUsageMeter`, `CodingPlanUsageRemainingPanel`.
**Что.** Полосы — `usage-chart` ramp, лимит — warning/destructive; цифры —
`#ebdbb2`, подписи `#928374`.
**Как.** `--color-usage-chart-*` (есть), `data-usage-used/max`.

### 5.10. Чипы вложений (пара 29)
`Attachments`, `Attachment`, `AttachmentRemove`.
**Что.** Чип: фон `#32302f`, рамка `#3c3836`, имя `#bdae93`, крестик —
hover destructive.
**Как.** Классы `Attachment*` (гипотеза), токены surface/border.

### 5.11. Просмотр вложения (пара 30)
`ImagePreviewDialog`, `ImageThumbnailGallery`.
**Что.** Диалог на `#1d2021`, рамка `#504945`, подложка изображения — `#282828`.
**Как.** 1.7 + `[data-slot="dialog-content"]`.

### 5.12. Очередь сообщений (пара 31)
`ConversationQueuePanel`, `Queue`.
**Что.** Элемент — `#32302f`, номер — brand, активный — `#3c3836`,
hover — `#3c3836`.
**Как.** `data-queue-*`, токены surface/selected.

### 5.13. Упоминания и автодополнение (пара 32)
`MentionPanel`, `.prompt-mention`.
**Что.** Панель — popover; выбранный пункт — `#3c3836`; чип упоминания —
`#32302f` с рамкой `#504945`, текст `#ebdbb2`.
**Как.** `.prompt-mention` (авторский класс), `[data-slot="command-item"]`.

### 5.14. Slash-команды (пара 33)
`SlashCommandPlugin`, панель секций.
**Что.** Как 5.13; команда — mono `#ebdbb2`, описание — `#928374`.
**Как.** Классы slash-панели; `[data-slot="command-item"]`.

### 5.15. История промптов (пара 34)
`HistorySearchComponent`, `CommandCenterSearchHistory`.
**Что.** Оверлей на popover; совпадение — `--color-find-highlight`.
**Как.** `[data-slot="command-input"]`/`command-item`, find-токены.

### 5.16. Подсказки в пустом поле (пара 35)
`ConversationDraftSuggestedPrompts`, `ComposerHint`.
**Что.** Чипы подсказок: `#32302f`, рамка `#3c3836`, hover `#3c3836`,
текст `#bdae93`→`#ebdbb2` в hover.
**Как.** Классы suggested prompts; токены surface/selected.

### 5.17. Приветствие (пара 36)
`WelcomeScreen`, `WelcomeComponent`.
**Что.** Фон базы, заголовок `#ebdbb2`, подсказка `#928374`, акцент — brand.
**Как.** Классы welcome; токены (без геометрии).

### 5.18. Голосовой ввод (пара 37)
`SpeechInput`, `MicSelector`, `Transcription`.
**Что.** Запись — красная точка/волна brand; транскрипция — `#bdae93`;
индикатор записи не скрывать.
**Как.** Классы speech; `--color-destructive` для live, `--color-brand` для
волны.
