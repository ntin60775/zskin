# План 6. Навигация, списки, настройки

Шаг 6 — периферия: навигация, списки, настройки. Зависит от шагов 1 и 3.

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 6.1. Список выбора и меню (пара 13)
`Select`, `DropdownMenu`, `Command`.
**Что.** Пункт: hover `#32302f`, selected `#3c3836`, текст `#ebdbb2`,
разделители `#3c3836`.
**Как.** `[data-slot="select-item"]`, `dropdown-menu-item`,
`[data-slot="separator"]`, `--color-menu-hover`.

### 6.2. Дерево (пара 14)
`TreeView`, `FileTree`, `FileTreeRow`.
**Что.** Строка: текст `#ebdbb2`, папки `#bdae93`, guides `#3c3836`,
selected `#3c3836`, hover `#32302f`.
**Как.** Классы `FileTree*`, `[data-workspace-file-tree-*]`.

### 6.3. Реестр агентов (пара 53)
`SubagentsSection`, `SubagentDirectorySidePane`.
**Что.** Карточки агентов: `#282828`, рамка `#3c3836`, роль — brand,
метрики — `#928374`.
**Как.** Классы settings/side pane; токены card/border.

### 6.4. Список сессий и задач (пара 76)
`ProjectSidebar`, `TaskGroupedView`, `TaskList`.
**Что.** Строка: hover `#32302f`, active `#3c3836`, заголовок группы —
`#928374`; бейдж активности — brand; без зебры.
**Как.** `data-task-row-*`, `data-grouped-*`; токены selected/hover.

### 6.5. Поиск и палитра (пара 77)
`CommandCenterDialog`, `TaskFindDialog`.
**Что.** Диалог на popover, инпут без рамки, совпадение —
`--color-find-highlight`.
**Как.** `[data-slot="command-input"]`, `command-item`; find-токены.

### 6.6. Файловое дерево-панель (пара 78)
`WorkspaceFileTree`, `FileManagerPane`.
**Что.** Фон панели `#1d2021`, строки как 6.2, липкие папки — фон хрома.
**Как.** `[data-workspace-file-tree-*]`, токены panel/sidebar.

### 6.7. Git (пара 79)
`GitPane`, `GitGraphPane`, `GitBranchSwitcher`.
**Что.** Статусы из `--color-git-*` (modified brand, added/untracked
`#b8bb26`, deleted `#fb4934`, renamed `#83a598`); граф — линии `#3c3836`,
узлы `#928374`, HEAD brand.
**Как.** Токены git (есть) + `--color-git-ignored/descendant/none` (1.1);
SVG графа — `stroke`/`fill` селекторами (гипотеза).

### 6.8. Терминал-панель (пара 80)
`TerminalSession`, `AnimatedTerminalPanel`, `TerminalTabTrigger`.
**Что.** Панель на `#282828`, табы как 1.6, статус success/error.
**Как.** `--color-terminal-*`, `[data-terminal-tab-content]`, табы — 1.6.

### 6.9. Настройки (пара 81)
`SettingsPage`, `SettingsHeaderBreadcrumb`.
**Что.** Фон базы, контент на `#282828`, навигация на хроме, активный пункт
`#3c3836`.
**Как.** `data-settings-section-nav`, `data-settings-panel-frame`; токены.

### 6.10. Строки настроек (пара 82)
`SettingsRow`, `SettingsRangeControl`, `SettingsGroupCard`.
**Что.** Label `#ebdbb2`, описание `#928374`, разделители `#3c3836`;
контролы — 1.8; карточки групп — `#282828` + рамка.
**Как.** Классы `Settings*`; токены card/border/foreground.

### 6.11. Выбор темы (пара 83)
`ThemeSelect`, `ThemePreviewCard`.
**Что.** Превью-карточки: рамка `#3c3836`, выбранная — brand-рамка `#fe8019`,
подпись `#bdae93`.
**Как.** `[data-slot="card"]` + `data-state`/selected-класс (гипотеза).

### 6.12. Плагины (пара 84)
`PluginStorePage`, `InstalledPluginDetailPanel`.
**Что.** Карточки `#282828`/рамка `#3c3836`, платный бейдж —
`plugin-paid-plan-badge` (1.1), статус установки — success.
**Как.** Классы `PluginStore*`, `[data-slot="badge"]`.

### 6.13. Hooks (пара 85)
`HooksSection`, `HookForm`, `HooksList`.
**Что.** Строки как 6.10, форма — 1.8, код hook — mono `#ebdbb2` на `#1d2021`.
**Как.** Классы hooks; токены.

### 6.14. MCP (пара 86)
`McpSettingsSection`, `McpServerList`, `McpStatusDot`.
**Что.** Статус-точка: success/warning/error; строка сервера — как 6.10;
ошибка — destructive-surface.
**Как.** `McpStatusDot` + токены status; `--color-destructive-surface`.

### 6.15. Субагенты (пара 87)
`SubagentsSection`, `SubagentReasoningField`.
**Что.** Реестр как 6.3; поле reasoning — select по 1.8.
**Как.** Классы settings; 1.8.

### 6.16. Горячие клавиши (пара 88)
`ShortcutSettingsSection`, `ShortcutBindingRow`, `ShortcutSearchBar`.
**Что.** Kbd по 1.10, строки как 6.10, поиск — find-токены.
**Как.** `[data-slot="kbd"]`; 1.10/6.10.

### 6.17. Статистика использования (пара 89)
`UsageStatsSection`, `UsageHeatmap`, `CodingPlanUsagePanel`.
**Что.** Heatmap и графики — ramp `usage-heatmap`/`usage-chart`; карточки —
`#282828`; подписи `#928374`.
**Как.** Токены usage (есть); SVG — 7.1.

### 6.18. Фидбек (пара 90)
`FeedbackCenter`, `TicketDetailView`.
**Что.** Формы — 1.8, статусы тикетов — status-цвета, фон базы.
**Как.** Классы feedback; токены.

### 6.19. Онбординг (пара 92)
`OnboardingDialog`, `SetupWizardComponent`.
**Что.** Как 1.9: шаги, карточки, кнопка brand.
**Как.** 1.9 + `[data-slot="dialog-content"]`.

### 6.20. Вход (пара 93)
`WelcomeScreen`, `LoginPanel`, `LoginApiKeyForm`.
**Что.** Фон базы, поля 1.8, кнопка brand, ошибка — destructive.
**Как.** Классы login; 1.8; токены.
