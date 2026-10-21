# ZCode UI 3.16.2 — полный разбор на компоненты

Каталог разбирает рендерер ZCode 3.16.2 на компоненты: от загрузки приложения
и оконного хрома до строки таймлайна и отдельного чипа вложения.

## 1. Границы разбора

- Установленный клиент — **3.16.2**, сборка `2469e253` от 2026-10-19T12:30:51Z,
  файл `/opt/ZCode/resources/app.asar`.
- Публичный исходник `zai-org/ZCode` заканчивается на теге `v3.15.1`;
  коммита `2469e253` в удалённом репозитории нет. Поэтому структура каталога
  опирается на исходники `packages/ui/src` v3.15.1, а для 3.16.2 проверена
  по собранному бандлу и CSS.
- Проверка совпадения версий: в 3.16.2 **все 6 981 ключ** словаря сообщений
  из 3.15.1 сохранились, добавились 8 новых. Набор data-атрибутов вырос с 763
  до 809, из них 73 новых. Пользовательская поверхность почти не изменилась,
  поэтому компонентный каталог 3.15.1 применим к 3.16.2.
- Исходники 3.15.1: 58 каталогов, из них 46 с `.tsx`; 816 файлов `.tsx`,
  761 файл с экспортируемыми компонентами. Для 3.16.2 эти числа — база
  структуры, а не измерение бандла.
- В таблицах перечислены компоненты и их состав. Служебные хуки, сторы,
  транспорт и чистые функции описаны только там, где они задают поведение
  видимого компонента.
- Отдельно выделены поверхности, которые лоадер zskin пока не инжектит:
  окно «Ресурсы», панель разрешений CUA, webview-вкладки. Это граница
  доставки CSS, а не граница UI.
- Термины: **зона** — крупный регион окна, **компонент** — React-компонент
  или семейство компонентов одного файла, **часть** — подкомпонент,
  живущий в том же файле.

### 1.1 Что изменилось в 3.16.2

| Область | Изменение | Компоненты и хуки |
|---|---|---|
| Diff | Новый движок `diffs-container` с темами `pierre-dark`/`pierre-light`; разметка хунков, выбора строк, аннотаций и разрешения конфликтов | `DiffViewer`, `GitPaneChangeCard`, `EditInlineDiffContent`; атрибуты `data-diffs-*`, `data-diff-span`, `data-selected-line`, `data-line-annotation`, `data-merge-conflict-*` |
| Diff: конфликты | Кнопки разрешения конфликта прямо в строке, выбор стороны, счётчики добавлений и удалений | `data-merge-conflict-action`, `data-additions-count`, `data-deletions-count`, `data-has-merge-conflict` |
| Diff: навигация | Раскрытие хунков вверх и вниз, «развернуть всё», буферы виртуализации | `data-expand-up/down/both/all-button`, `data-buffer-size`, `data-gutter-buffer`, `data-content-buffer` |
| Композер | Раскладка с ведущими и хвостовыми действиями, приоритетом сворачивания и компактной иконкой модели | `ConversationComposer`, `V4ComposerToolbar`, `ComposerModelMenu`; `data-composer-layout`, `data-composer-leading-actions`, `data-composer-trailing-actions`, `data-composer-collapse-priority` |
| Мобильный веб-remote | Отдельные оверлеи чата и боковой панели | `WebRemoteControlMobileShell`; `data-mobile-chat-overlay`, `data-mobile-side-pane-overlay` |
| Чат: капча | Новые тексты проверки и повтора капчи | `ChatErrorBanner`, action в ошибке; ключи `chat.captcha.verifyFailed`, `chat.error.action.retryCaptcha` |
| Ошибки провайдеров | Новые коды и подсказки | `chat.error.*`; ключи `zcode.error.modelSuspiciousEmpty`, `zcode.error.providerBusiness.3007` |
| Редактор | Внутренние атрибуты Lexical: курсор, декоратор, перенос, текст | `LexicalChatInput`; `data-lexical-*` (не публичный контракт) |
| Токены | Больше семантических ролей: interaction, remote, узлы, diff, heatmap | CSS: 341 уникальное имя `--color-*`; 190 в `.theme-zai-dark`, 158 в `.theme-zai-light` |

Восемь новых ключей словаря:

- `browser.permission.denyThisTime`
- `chat.captcha.verifyFailed`
- `chat.error.action.retryCaptcha`
- `manualClaimPlan.claim.failure.captcha`
- `zcode.error.modelSuspiciousEmpty`
- `zcode.error.providerBusiness.3007`
- служебные `en-US` и `zh-CN`

Остальные различия 3.15.1 и 3.16.2 — внутренние атрибуты библиотек (Radix,
Lexical, `@pierre/diffs`) и переименования Tailwind-утилит. Пять новых
служебных классов (`flow-root`, `resize-none`, `resize-y`, `scroll-my-1`,
`scroll-py-1`) не меняют карту компонентов.

### 1.2 Модули 3.16.2 по data-атрибутам

Счётчик — число уникальных `data-*`-атрибутов с этим префиксом в бандле
3.16.2. Он подтверждает, что перечисленные в каталоге модули присутствуют
в установленной версии.

| Модуль | Атрибутов | Примеры |
|---|---:|---|
| Workflow | 45 | `data-workflow-card`, `data-workflow-artifact-id`, `data-workflow-last-run` |
| Model / provider | 43 | `data-model-capabilities-options`, `data-model-boolean-option`, `data-provider-status` |
| Conversation | 23 | `data-conversation-bottom-dock-mode`, `data-conversation-share-*`, `data-row-kind` |
| Composer | 22 | `data-composer-layout`, `data-composer-collapse-priority`, `data-composer-thought-control` |
| Workspace | 18 | `data-workspace-shell`, `data-workspace-header-*`, `data-workspace-file-tree-*` |
| Markdown | 16 | `data-markdown-table-*`, `data-markdown-image-*`, `data-markdown-list` |
| Task / grouped list | 20 | `data-task-row-*`, `data-grouped-*`, `data-task-title-marquee-track` |
| Side pane | 13 | `data-side-pane-tab-*`, `data-side-pane-full-view-host`, `data-side-pane-tabs-viewport` |
| Browser | 12 | `data-browser-tab-residency`, `data-browser-resize-*`, `data-browser-screenshot-*` |
| Plugin UI | 11 | `data-plugin-ui-surface`, `data-plugin-ui-phase`, `data-plugin-ui-tool-call-id` |
| Permission / elicitation | 14 | `data-permission-rule-*`, `data-elicitation-dialog-*`, `data-confirm-intent` |
| Git / diff | 8 | `data-git-pane-change-virtual-row`, `data-diff-viewer`, `data-diffs-header` |
| Goal / plan | 11 | `data-goal-status`, `data-goal-iteration`, `data-plan-detail-tool-call-id` |
| Remote / mobile | 14 | `data-remote-connection-status`, `data-mobile-chat-overlay`, `data-mobile-page` |
| Settings | 8 | `data-settings-section-nav`, `data-settings-panel-frame`, `data-settings-scope` |
| Share / artifact | 11 | `data-share-content-block`, `data-artifact-kind`, `data-artifact-version` |
| Queue / context | 9 | `data-queue-auto-drain`, `data-context-mcp-usage`, `data-context-reset-reminder` |

## 2. Слои и дерево

UI собран в пять слоёв. Сверху вниз:

| Слой | Что содержит | Где живёт |
|---|---|---|
| L4. Оболочка | окно, титлбар, рабочая область, сайдбар, панели | `root/`, `app-shell/`, `project-sidebar/`, корень `src/` |
| L3. Композиции | воркбенч, панель сессии, таймлайн, композер | `v4/`, `prompt-editor/`, `chat-input-toolbar/` |
| L2. Доменные виджеты | карточки инструментов, настройки, панели, диалоги | `ToolCallBlocks/`, `settings/`, `app-shell/`, `feedback/` |
| L1. Примитивы контента | сообщение, markdown, код, вложение, план, граф | `components/ai-elements/` |
| L0. Базовые примитивы | кнопка, поле, диалог, вкладки, скролл, токены | `components/ui/`, `lib/`, `hooks/`, `i18n/` |

Дерево основного экрана:

```text
Root
└── RootShell
    └── RootWorkspaceContent
        └── App
            └── WorkspaceShellLayout
                ├── DesktopWindowFrame
                ├── WorkspaceHeader
                │   ├── WorkspaceHeaderTitleSection
                │   └── WorkspaceHeaderActionSection
                ├── WorkspaceSidebar (ProjectSidebar)
                │   ├── ProjectSidebarNavigation
                │   ├── ProjectSidebarListHeader
                │   ├── ProjectSections / TaskGroupedView
                │   └── WorkspaceSidebarFooter
                ├── V4WorkspaceChatArea
                │   └── WorkbenchPane (1–4)
                │       └── V4ChatPane
                │           └── SessionPane
                │               ├── ConversationHeader
                │               ├── ConversationStatusPanel
                │               ├── ConversationTimeline
                │               │   └── ConversationTurnGroup
                │               │       └── ConversationTurnRow
                │               │           └── ConversationRowView
                │               ├── ConversationQueuePanel
                │               ├── V4InteractionDialogs
                │               └── ConversationComposer
                │                   ├── ChatPromptEditor → LexicalChatInput
                │                   └── V4ComposerToolbar
                ├── AnimatedSidePanePanel
                └── AnimatedTerminalPanel
```

## 3. Загрузка, корень и провайдеры

| Компонент | Файл | Роль |
|---|---|---|
| `App` | `App.tsx` | Оркестратор workspace-уровня: навигация, производные данные Git, привязка shell, рендер `WorkspaceShellLayout`. |
| `Root` | `Root.tsx` | Верхний вход: гейты загрузки, логина, онбординга, режима «только настройки», удалённого подключения. |
| `RootShell` | `root/RootShell.tsx` | Обёртка корня: провайдеры, границы ошибок, базовая тема. |
| `RootWorkspaceContent` | `root/RootWorkspaceContent.tsx` | Мемоизированный `App` с workspace-сервисами и удалёнными сессиями. |
| `RootStartupLoading`, `ZCodeStartupLogo`, `ZCodeStartupLogoBadge` | `root/RootStartupLoading.tsx` | Стартовый экран и логотип до готовности БД и workspace. |
| `GlobalDatabaseStartupLoading` | `root/GlobalDatabaseStartupLoading.tsx` | Ожидание глобальной базы при холодном старте. |
| `WorkspaceSettingsLayer` | `root/WorkspaceSettingsLayer.tsx` | Слой настроек поверх workspace. |
| `AppErrorBoundary`, `ScopedErrorBoundary` | `ErrorBoundary.tsx` | Границы ошибок: всё приложение и отдельная зона с `resetKeys`. |
| `PlatformProvider` | `hooks/usePlatform.tsx` | Платформа, desktop/web, macOS/Windows/Linux. |
| `ServiceProvider` | `hooks/useServices.tsx` | Доступ к сервисам приложения. |
| `StoreProvider`, `TabStoreProvider` | `store/` | Провайдеры Zustand-сторов и вкладок. |
| `ZCodeIntlProvider` | `i18n/IntlProvider.tsx` | Локализация и форматирование. |
| `DiffsWorkerPoolProvider` | `root/DiffsWorkerPoolProvider.tsx` | Пул воркеров для диффов. |
| `RemoteWorkspaceControllerProvider` | `remote/useRemoteWorkspaceController.tsx` | Управление удалённым workspace. |
| `RemoteProjectPresentationProvider` | `hooks/RemoteProjectPresentationContext.tsx` | Представление удалённых проектов: статусы, ошибки, восстановление. |
| `RewardsProvider` | `rewards/RewardsProvider.tsx` | Состояние наград и веб-вью. |
| `MarketingTouchProvider` | `components/marketing-touch/MarketingTouchProvider.tsx` | Показ маркетинговых баннеров и диалогов. |
| `PostUpdateReleaseNotesDialog` | `root/PostUpdateReleaseNotesDialog.tsx` | Что нового после обновления. |
| `UpdateStatusWindowRoot` | `UpdateStatusWindowRoot.tsx` | Отдельное окно статуса обновления. |
| `UpdateStatusDialog`, `UpdateStatusDialogController`, `UpdateStatusButton` | `UpdateStatusDialog.tsx`, `UpdateStatusDialogController.tsx`, `UpdateStatusButton.tsx` | Диалог, контроллер и кнопка обновления. |
| `ThemeHeroVisual` | `openWorkspacePageThemeHero.tsx` | Декоративный визуал страницы открытия workspace. |

## 4. Оконный хром

| Компонент | Файл | Роль |
|---|---|---|
| `DesktopWindowFrame` | `DesktopWindowFrame.tsx` | Рамка окна: титлбар, drag-зона, вставка нативного хрома. |
| `DesktopTopOverlay` | `DesktopTopOverlay.tsx` | Плавающая полоса поверх рабочей области: навигация, обновление, кнопки окна. |
| `DesktopWindowControls`, `DesktopOverlayWindowControls` | `DesktopWindowControls.tsx`, `DesktopOverlayWindowControls.tsx` | Свернуть, развернуть, закрыть; на Linux это часть UI, не ОС. |
| `DesktopTopOverlayActionButton` | `DesktopTopOverlayActionButton.tsx` | Кнопка действия в верхнем оверлее. |
| `WindowsCaptionMenuButton`, `WindowsTopLeftLogo` | `WindowsCaptionMenuButton.tsx`, `WindowsTopLeftLogo.tsx` | Меню подписи и логотип для Windows-раскладки. |
| `windowCaptionControls` | `windowCaptionControls.ts` | Чистые функции раскладки оконных кнопок. |

## 5. Оболочка workspace

| Компонент | Файл | Роль |
|---|---|---|
| `WorkspaceShellLayout` | `app-shell/WorkspaceShellLayout.tsx` | Главная раскладка: сайдбар, центральная колонка, терминал, боковая панель, floating-режим; хранит ширины панелей. |
| `WorkspaceHeader` | `WorkspaceHeader.tsx` | Верхняя панель: заголовок задачи, контекст, действия, хлебные крошки. |
| `WorkspaceHeaderTitleSection` | `WorkspaceHeaderSections.tsx` | Заголовок, статус, переключение задачи. |
| `WorkspaceHeaderActionSection` | `WorkspaceHeaderSections/WorkspaceHeaderActionSection.tsx` | Редактор, шаринг, панели, помощь, оконные кнопки. |
| `WorkspaceContextPath`, `WorkspaceLastActivity` | `WorkspaceHeaderSections/` | Путь workspace и время последней активности. |
| `WorkspaceEditorButtonGroup` | `WorkspaceEditorButtonGroup.tsx` | Открыть workspace во внешнем редакторе. |
| `WorkspaceHelpMenuButton` | `WorkspaceHelpMenuButton.tsx` | Меню помощи и горячих клавиш. |
| `WorkspaceSidePaneToggleButton`, `WorkspaceTerminalToggleButton` | `WorkspaceSidePaneToggleButton.tsx`, `WorkspaceTerminalToggleButton.tsx` | Переключатели правой панели и терминала. |
| `WorkspaceWebRemoteControlTrigger` | `WorkspaceWebRemoteControlTrigger.tsx` | Вход в веб-удалённое управление. |
| `GitBranchSwitcher` | `GitBranchSwitcher.tsx` | Текущая ветка, грязные файлы, переключение и создание веток. |
| `GitBranchCreateDialog`, `GitBranchSwitchAssistDialog` | `git-branch-switcher/GitBranchDialogs.tsx` | Диалоги создания и переключения ветки. |
| `ControlShortcutBadge`, `SidebarShortcutHint` | `ControlShortcutBadge.tsx`, `SidebarShortcutHint.tsx` | Бейдж горячей клавиши и подсказка в сайдбаре. |
| `AnimatedSidePanePanel` | `app-shell/AnimatedSidePanePanel.tsx` | Анимированная правая панель с табами. |
| `AnimatedTerminalPanel` | `app-shell/AnimatedTerminalPanel.tsx` | Анимированная панель терминала под чатом. |
| `SidePaneTabTrigger`, `SidePaneTabIcon`, `SortableSidePaneTabTrigger`, `SidePaneTabDragOverlay` | `app-shell/SidePaneTabTrigger.tsx` | Таб боковой панели, иконка, drag-and-drop. |
| `SidePaneTabOverview`, `SidePaneTabTitleTooltip` | `app-shell/SidePaneTabOverview.tsx`, `SidePaneTabTitleTooltip.tsx` | Обзор табов и подсказка заголовка. |
| `SidePaneFullViewConversationHost`, `SidePaneFullViewConversationTab`, `SidePaneFullViewToggleButton` | `side-pane-full-view/` | Полноэкранный режим боковой панели и его таб. |
| `WebRemoteControlMobileShell` | `WebRemoteControlMobileShell.tsx` | Мобильная оболочка веб-удалённого управления. |
| `WebRemoteControlDeviceHeader`, `WebRemoteControlDialog`, `WebRemoteControlTaskViewReporter` | `web-remote-control/` | Заголовок устройства, диалог подключения, репортер текущей задачи. |

## 6. Сайдбар и навигация по проектам

### 6.1 Каркас и навигация

| Компонент | Файл | Роль |
|---|---|---|
| `ProjectSidebar` (он же `WorkspaceSidebar`) | `project-sidebar/index.tsx` | Корень сайдбара: секции проектов, задачи, архив, футер. |
| `ProjectSidebarNavigation` | `project-sidebar/ProjectSidebarNavigation.tsx` | Назад/вперёд, новая задача, настройки, свёрнутый рельс. |
| `ProjectSidebarListHeader` | `project-sidebar/ProjectSidebarListHeader.tsx` | Поиск, фильтр, сортировка списка. |
| `ProjectSections` | `project-sidebar/ProjectSections.tsx` | Секции проектов и задач. |
| `PurposeSections`, `WorkspacePurposeSection` | `project-sidebar/PurposeSections.tsx`, `WorkspaceSidebar/WorkspacePurposeSection.tsx` | Группировка по назначению workspace. |
| `TaskGroupedView` | `project-sidebar/TaskGroupedView.tsx` | Сгруппированный список задач с drag-and-drop. |
| `GroupItem`, `GroupedTaskItem`, `GroupedTaskRow`, `GroupedDraftTaskRow`, `EmptyGroupDropZone` | `project-sidebar/grouped/` | Группа, строка задачи, черновая строка, зона сброса. |
| `StickyGroupHeader`, `StickyGroupHeaderSlot` | `project-sidebar/grouped/` | Липкий заголовок группы. |
| `VirtualizedGroupedTaskList`, `VirtualizedGroupedTopLevelList` | `project-sidebar/grouped/` | Виртуализированные списки. |
| `GroupedTaskContextMenuContent`, `TaskGroupTaskMenu` | `project-sidebar/grouped/task-context-menu-content.tsx`, `TaskGroupTaskMenu.tsx` | Контекстные меню задач и групп. |
| `ProjectNode`, `ProjectNodeContent`, `ProjectSidebarNode` | `project-sidebar/ProjectNode.tsx`, `ProjectNodeContent.tsx`, `ProjectSidebarNode.tsx` | Узлы дерева проектов. |
| `ProjectTaskRows`, `ProjectTaskRow` | `project-sidebar/ProjectTaskRows.tsx` | Строки задач проекта. |
| `ProjectComposerMenu`, `ProjectCreation`, `ProjectEditor` | `project-sidebar/` | Меню проекта, создание и редактирование. |
| `ProjectFolderIcon`, `ProjectFolderTrustDialog` | `project-sidebar/` | Иконка папки и подтверждение доверия. |
| `SortableProjects`, `WorkspaceDragOverlay` | `project-sidebar/` | Сортировка проектов и оверлей перетаскивания. |
| `ArchiveManagement`, `ArchiveGroupCard`, `DeleteAllArchivedTasksButton` | `project-sidebar/`, корень | Архив задач и массовое удаление. |
| `HomeOnlyWorkspaceRows`, `OfflineRemoteProjectRows` | `project-sidebar/` | Строки «только домашний workspace» и офлайн-удалённые проекты. |
| `RemoteProjectList`, `RemoteProjectMenu`, `RemoteProjectPicker`, `RemoteIdentityHoverCard` | `project-sidebar/` | Удалённые проекты: список, меню, выбор, карточка узла. |
| `RemoteConnectionProgressSection`, `RemoteConversationDisconnected`, `RemoteConversationBanner` | `project-sidebar/` | Прогресс подключения и баннер разрыва. |
| `WorkspaceSidebarFooter`, `WorkspaceSidebarFooterUsageSummary`, `WorkspaceSidebarFooterUsageSummaryContent`, `WorkspaceSidebarFooterPlanBadge` | корень | Футер сайдбара: план, квоты, настройки. |
| `SidebarBottomActivity` | `sidebar-activity/SidebarBottomActivity.tsx` | Нижняя лента активности. |
| `TaskList`, `TaskListItem`, `TaskListItemContextMenu`, `TaskListItemContextMenuContent`, `TaskActionMenuContent`, `TaskInteractionBadge`, `TaskListLoadingHint` | корень | Старый список задач и его меню. |
| `TaskRenameDialog`, `TaskSearchDialog` | корень | Переименование и поиск задачи. |
| `RemoteProjectConnectionDetails`, `RemoteProjectDetailsPopover` | `WorkspaceSidebar/` | Детали удалённого подключения. |

### 6.2 Дерево файлов и поиск

| Компонент | Файл | Роль |
|---|---|---|
| `WorkspaceFileTree` | `workspace-file-tree/WorkspaceFileTree.tsx` | Дерево файлов workspace. |
| `WorkspaceFileTreeList` | `workspace-file-tree/WorkspaceFileTreeList.tsx` | Виртуализированный список строк. |
| `WorkspaceFileTreeRowView`, `WorkspaceFileTreeRowName` | `workspace-file-tree/` | Строка и имя файла. |
| `WorkspaceFileTreeStickyFolders` | `workspace-file-tree/WorkspaceFileTreeStickyFolders.tsx` | Липкие папки при скролле. |
| `WorkspaceFileTreeNotice` | `workspace-file-tree/WorkspaceFileTreeNotice.tsx` | Служебное уведомление дерева. |
| `FileManagerPane` | `WorkspaceFileTree.tsx` | Панель файлового менеджера. |
| `FileTree`, `FileTreeFolder`, `FileTreeFile`, `FileTreeIcon`, `FileTreeName`, `FileTreeActions` | `components/ai-elements/file-tree.tsx` | Переиспользуемое дерево файлов. |

## 7. Воркбенч и панель сессии

| Компонент | Файл | Роль |
|---|---|---|
| `V4WorkspaceChatArea` | `v4/V4WorkspaceChatArea.tsx` | Хост воркбенча: дерево панелей, фокус, привязка сессий, split. |
| `WorkbenchLeafPane` | `v4/WorkbenchPane.tsx` | Листовая панель воркбенча. |
| `WorkbenchSplitDivider` | `v4/WorkbenchSplitDivider.tsx` | Разделитель панелей. |
| `V4ChatPane` | `v4/V4ChatPane.tsx` | Привязывает `sessionId` к `SessionPane`, прокидывает удалённые баннеры и shell-пропсы. |
| `SessionPane` | `v4/SessionPane.tsx` | Вертикальный срез сессии: подписка, команды, отправка, стоп, fork, edit, retry, очередь, slash. |
| `V4ConversationProvider`, `V4PaneConversationProvider`, `V4ConversationContext` | `v4/V4ConversationContext.tsx` | Контекст проекции сессии для панели. |
| `SessionDataLayer`, `conversationProjectionStore`, `paneLayoutStore`, `workspaceConnectionRegistry` | `v4/*.ts` | Слой данных: lease, проекция, раскладка, соединения. Не UI, но задаёт жизненный цикл панелей. |

### 7.1 Шапка и таймлайн

| Компонент | Файл | Роль |
|---|---|---|
| `ConversationHeader` | `v4/ConversationHeader.tsx` | Плавающая шапка панели: бейдж workspace, закрытие, скрытый title для e2e. |
| `ConversationTimeline` | `v4/ConversationTimeline.tsx` | Виртуализированный таймлайн: scroll anchoring, follow-tail, load older, find, turn navigator, bottom dock. |
| `ConversationTurnGroup` | `v4/ConversationTurnGroup.tsx` | Группирует строки в ход: ввод, работа, ответ, маркеры. |
| `ConversationTurnRow` | `v4/ConversationTurnRow.tsx` | Адаптер строки к `ConversationRowView`, собирает текст для копирования. |
| `ConversationRowView` | `v4/ConversationRowView.tsx` | Диспетчер типов строк: заголовок хода, ввод, текст ассистента, reasoning, tool call, subagent, hook, artifact, маркер. |
| `ConversationAssistantTextActions` | `v4/ConversationRowView.tsx` | Копирование, лайк, дизлайк, fork, retry, edit. |
| `ConversationTurnNavigator` | `v4/ConversationTurnNavigator.tsx` | Рельс/оглавление ходов для прыжков по истории. |
| `ConversationUserInputBubble`, `ConversationUserInputBody`, `ConversationUserInputContent`, `ConversationUserInputEpilogue` | `v4/ConversationUserInput*.tsx` | Пузырь пользователя: markdown, вложения, свёртка по высоте, редактирование. |
| `ConversationSelectionTooltip`, `MarkdownSelectionTooltip`, `SelectionActionMenu` | `v4/`, корень | Действия над выделением: цитировать, отправить в чат, скопировать. |
| `ConversationPendingGuideList` | `v4/ConversationPendingGuideList.tsx` | Ожидающие steer-сообщения. |
| `ConversationQueuePanel` | `v4/ConversationQueuePanel.tsx` | Очередь сообщений: drag, edit, send now, resume, удаление. |
| `ConversationStatusPanel` | `v4/ConversationStatusPanel.tsx` | Панель состояния: цель, план, фоновая работа, субагенты, workflow, Git; режимы `panel` и `auto`. |
| `ConversationGoalBanner`, `ConversationQuotaBanner` | `v4/` | Баннеры цели и квоты. |
| `PendingCommandRecoveryBanner`, `WorkspaceHookPendingBanner` | `v4/` | Восстановление зависшей команды и ожидание hook. |
| `SessionSubscriptionErrorPanel` | `v4/SessionSubscriptionErrorPanel.tsx` | Ошибка подписки на сессию и переподключение. |
| `ConversationDraftEmptyState`, `ConversationDraftSuggestedPrompts`, `ConversationDraftSuggestedPromptsContainer` | `v4/` | Пустой черновик и подсказки первых запросов. |
| `OffPeakNewTaskEntry` | `v4/OffPeakNewTaskEntry.tsx` | Вход в задачу по низкому тарифу. |
| `ConversationFileSummaryPanel`, `ConversationFileRewindDialog` | `v4/` | Сводка изменённых файлов и откат файлов. |
| `ConversationBackgroundWorks`, `ConversationWorkflowCompletion`, `ConversationWorkflowDigests` | `v4/` | Фоновая работа и итоги workflow. |
| `WorkflowToolSummary`, `WorkflowNotificationToolRow`, `WorkflowNotificationHoleRow`, `WorkflowNotificationArtifactChips` | `v4/` | Компактные строки workflow в таймлайне. |
| `ConversationAgentToolCallRow` | `v4/ConversationAgentToolCallRow.tsx` | Строка вызова субагента. |
| `SubagentDrilldown` | `v4/SubagentDrilldown.tsx` | Раскрытие цепочки субагентов. |
| `V4InteractionDialogs`, `V4UserInputDialog` | `v4/` | Диалоги разрешений и вопросов, привязанные к сессии. |
| `ConversationBottomDockTransition` | `v4/ConversationBottomDockTransition.tsx` | Анимация нижнего дока. |
| `ConversationTelemetryPaneAttachment`, `ConversationTelemetryWorkspaceAttachment` | `v4/telemetry/` | Вложения телеметрии. |

### 7.2 Совместный доступ к разговору

| Компонент | Файл | Роль |
|---|---|---|
| `ConversationShareMenu`, `ConversationShareLinkRow`, `ConversationSharePermissionPicker` | корень | Меню публикации, строка ссылки, выбор доступа. |
| `ConversationSharePopover`, `ConversationSharePreflightStatus` | `conversation-share-interaction/` | Поповер публикации и статус проверки. |
| `ConversationShareWorkflow`, `ConversationShareContent`, `ConversationShareSelectionPanel` | `v4/` | Сценарий публикации, контент, выбор ходов. |
| `ConversationShareConfirmationDock`, `ConversationShareSuccessDock`, `ConversationShareImportNotice` | `v4/` | Док подтверждения, успеха и импорта. |
| `ConversationShareReadonlyTimeline` | `v4/ConversationShareReadonlyTimeline.tsx` | Таймлайн только для чтения. |

## 8. Композер

### 8.1 Ядро ввода

| Компонент | Файл | Роль |
|---|---|---|
| `ConversationComposer` | `v4/ConversationComposer.tsx` | Оболочка композера: вложения, черновик, история, mention, отправка/стоп, очередь. |
| `ChatPromptEditor` | `prompt-editor/ChatPromptEditor.tsx` | Чистая оболочка поля: Lexical, drag-and-drop, слоты тулбара, mention. |
| `LexicalChatInput` | `LexicalChatInput.tsx` | Contenteditable-редактор: вставка, mention `@`/`#`/`$`, slash, drag. |
| `ChatPromptActionMenu` | `prompt-editor/ChatPromptActionMenu.tsx` | Меню вложений и скриншота. |
| `SlashCommandPlugin`, `SlashCommandPlugin`-секции | `SlashCommandPlugin.tsx`, `slashCommandPanelSections.tsx`, `slashCommandHelpers.ts` | Slash-команды и их панель. |
| `MentionPlugin`, `MentionPanel`, `ContextMentionOptionContent`, `PluginMentionOptionContent` | `mentions/` | Панель упоминаний файлов, контекста и плагинов. |
| `PromptClipboardPlugin` | `mentions/PromptClipboardPlugin.tsx` | Вставка из буфера в поле. |
| `PromptInput`, `PromptInputBody`, `PromptInputFooter`, `PromptInputHeader`, `PromptInputProvider`, `PromptInputTools` | `components/ai-elements/prompt-input.tsx` | Каркас поля ввода и его слоты. |
| `PromptInputTextarea` | `components/ai-elements/prompt-input-textarea.tsx` | Текстовая область. |
| `PromptInputButton`, `PromptInputSubmit` | `components/ai-elements/prompt-input-buttons.tsx` | Кнопки действия и отправки. |
| `PromptInputActionMenu*`, `PromptInputActionAddAttachments`, `PromptInputActionAddScreenshot` | `components/ai-elements/prompt-input-actions.tsx` | Меню добавления вложений и скриншота. |
| `PromptInputCommand*`, `PromptInputSelect*`, `PromptInputHoverCard*`, `PromptInputTab*` | `components/ai-elements/prompt-input-primitives.tsx` | Команды, селекты, подсказки и табы внутри поля. |
| `Queue`, `QueueList`, `QueueItem*`, `QueueSection*` | `components/ai-elements/queue.tsx` | Очередь сообщений как примитив. |

### 8.2 Панель инструментов композера

| Компонент | Файл | Роль |
|---|---|---|
| `V4ComposerToolbar` | `v4/composer/V4ComposerToolbar.tsx` | Собирает модель, глубину мышления и расход контекста. |
| `V4ComposerModelControls` | `v4/composer/V4ComposerToolbar.tsx` | Модель и провайдер. |
| `V4ComposerModeSwitch` | `v4/composer/V4ComposerModeControls.tsx` | Переключение режима чата. |
| `V4ComposerCuaEntry` | `v4/composer/V4ComposerCuaEntry.tsx` | Вход в CUA из композера. |
| `ComposerModelMenu`, `ComposerThoughtIndicator` | `chat-input-toolbar/ComposerModelMenu.tsx` | Меню модели и индикатор мышления. |
| `ComposerProviderMenu` | `chat-input-toolbar/ComposerProviderMenu.tsx` | Меню провайдера. |
| `ComposerEffortHeading` | `chat-input-toolbar/ComposerEffortHeading.tsx` | Заголовок выбора усилия. |
| `ThoughtLevelCycleControl` | `chat-input-toolbar/ThoughtLevelCycleControl.tsx` | Циклическое переключение глубины. |
| `ChatModeSwitchControl` | `chat-input-toolbar/ChatModeSwitchControl.tsx` | Переключатель режима. |
| `ChatContextUsage`, `ContextQuotaResetOpportunityReminderContent` | `chat-input-toolbar/contextUsage.tsx`, `contextQuotaResetOpportunityReminder.tsx` | Расход контекста и напоминание о сбросе квоты. |
| `ChatCodingPlanMcpUsageMeter`, `ChatCodingPlanUsageRemainingPanel`, `CodingPlanUsageHeaderAction`, `CodingPlanUsageNotice`, `ChatStartPlanBalancePanel` | `chat-input-toolbar/` | Метры и панели тарифа. |
| `ChatApiRetryStatus`, `ConfigSelect` | `chat-input-toolbar/display.tsx` | Статус повтора запроса и выбор конфигурации. |
| `RollingToolbarLabel`, `ComposerTriggerTransition` | `chat-input-toolbar/` | Прокрутка подписи и анимация триггера. |
| `ModelConfigSelect`, `ModelInputCapabilityBadge` | корень, `components/` | Выбор конфигурации модели и бейдж возможностей. |

В 3.16.2 композер раскладывает элементы по ведущей и хвостовой группам и
сворачивает их по приоритету. Стилевые хуки: `[data-composer-layout]`,
`[data-composer-leading-actions]`, `[data-composer-leading-content]`,
`[data-composer-trailing-actions]`, `[data-composer-collapse-priority]`,
`[data-composer-compact]`, `[data-composer-model-icon]`,
`[data-composer-provider-list]`, `[data-composer-model-list]`.

### 8.3 Чипы вложений и контекста

| Компонент | Файл | Роль |
|---|---|---|
| `Attachments`, `Attachment`, `AttachmentPreview`, `AttachmentRemove`, `AttachmentHoverCard`, `AttachmentInfo`, `AttachmentEmpty` | `components/ai-elements/attachments.tsx` | Сетка вложений и превью. |
| `CodeCommentAttachmentChip` | `v4/composer/CodeCommentAttachmentChip.tsx` | Чип комментария к коду. |
| `ContextAttachmentPill` | `v4/composer/ContextAttachmentPill.tsx` | Чип контекста. |
| `ConversationSelectionReferenceChip` | `v4/composer/ConversationSelectionReferenceChip.tsx` | Ссылка на выделенный фрагмент. |
| `PptxElementReferenceChip` | `v4/composer/PptxElementReferenceChip.tsx` | Ссылка на элемент PPTX. |
| `WebElementContextAttachmentChip` | `v4/composer/WebElementContextAttachmentChip.tsx` | Ссылка на элемент веб-страницы. |
| `ConversationBackgroundWorkTrigger` | `v4/composer/ConversationBackgroundWorkTrigger.tsx` | Триггер фоновой работы. |
| `ChatMediaAttachmentPreviewDialog`, `ImagePreviewDialog`, `ImageThumbnailGallery` | корень, `components/ai-elements/` | Просмотр вложений и галерея. |
| `AudioPlayer*`, `SpeechInput`, `MicSelector*`, `VoiceSelector*`, `Transcription`, `TranscriptionSegment` | `components/ai-elements/` | Аудио, речь, микрофон, голос, транскрипция. |

### 8.4 Highspeed

| Компонент | Файл | Роль |
|---|---|---|
| `HighspeedComposerBackground` | `highspeed/HighspeedActivationVisual.tsx` | Фон активного Highspeed-композера. |
| `HighspeedModelIndicator` | `highspeed/HighspeedModelIndicator.tsx` | Индикатор Highspeed-модели. |
| `HighspeedShareNoticeCard`, `HighspeedShareDialog` | `highspeed/HighspeedShareNoticeCard.tsx` | Уведомление и диалог шаринга. |
| `HighSpeedDiffusionCanvas` | `v4/highspeed/HighSpeedDiffusionCanvas.tsx` | Канвас диффузии. |

## 9. Контент сообщений

### 9.1 Каркас и markdown

| Компонент | Файл | Роль |
|---|---|---|
| `Conversation`, `ConversationContent`, `ConversationDownload`, `ConversationEmptyState`, `ConversationScrollButton` | `components/ai-elements/conversation.tsx` | Каркас ленты сообщений. |
| `Message`, `MessageContent`, `MessageResponse`, `MessageToolbar`, `MessageAction(s)`, `MessageBranch*` | `components/ai-elements/message.tsx` | Сообщение, ответ, панель действий, ветвление. |
| `Reasoning`, `ReasoningTrigger`, `ReasoningContent` | `components/ai-elements/reasoning.tsx` | Сворачиваемый reasoning. |
| `ChainOfThought`, `ChainOfThoughtHeader`, `ChainOfThoughtContent`, `ChainOfThoughtStep`, `ChainOfThoughtSearchResult(s)`, `ChainOfThoughtImage` | `components/ai-elements/chain-of-thought.tsx` | Пошаговая цепочка рассуждений. |
| `MarkdownBlockquote`, `MarkdownUnorderedList`, `MarkdownOrderedList`, `MarkdownListItem`, `MarkdownTable`, `MarkdownTableHeader`, `MarkdownTableRow`, `MarkdownTableCell`, `MarkdownImage`, `MarkdownImageParagraph` | `components/ai-elements/markdown-*.tsx` | Markdown-элементы. |
| `CodeBlock`, `CodeBlockHeader`, `CodeBlockTitle`, `CodeBlockFilename`, `CodeBlockActions`, `CodeBlockCopyButton`, `CodeBlockWrapButton`, `CodeBlockLanguageSelector*`, `CodeBlockMermaidPreviewButton` | `components/ai-elements/code-block.tsx` | Блок кода с копированием, переносом, языком и mermaid. |
| `MermaidBlock` | `components/ai-elements/mermaid-block.tsx` | Рендер mermaid. |
| `Sources`, `Source`, `SourcesTrigger`, `SourcesContent` | `components/ai-elements/sources.tsx` | Источники ответа. |
| `InlineCitation*` | `components/ai-elements/inline-citation.tsx` | Встроенные цитаты и карусель источников. |
| `Image`, `ImageThumbnailGallery`, `ImagePreviewDialog` | `components/ai-elements/` | Изображение, галерея, просмотр. |
| `Artifact`, `ArtifactHeader`, `ArtifactTitle`, `ArtifactDescription`, `ArtifactContent`, `ArtifactActions`, `ArtifactAction`, `ArtifactClose` | `components/ai-elements/artifact.tsx` | Артефакт и его панель. |
| `Plan`, `PlanHeader`, `PlanTitle`, `PlanDescription`, `PlanContent`, `PlanFooter`, `PlanAction`, `PlanTrigger` | `components/ai-elements/plan.tsx` | Карточка плана. |
| `Tool`, `ToolHeader`, `ToolContent`, `ToolInput`, `ToolOutput` | `components/ai-elements/tool.tsx` | Общий каркас инструмента. |
| `Confirmation`, `ConfirmationRequest`, `ConfirmationAccepted`, `ConfirmationRejected`, `ConfirmationTitle`, `ConfirmationActions`, `ConfirmationAction` | `components/ai-elements/confirmation.tsx` | Подтверждение операции. |
| `Checkpoint`, `CheckpointIcon`, `CheckpointTrigger` | `components/ai-elements/checkpoint.tsx` | Точка отката. |
| `Task`, `TaskTrigger`, `TaskContent`, `TaskItem`, `TaskItemFile` | `components/ai-elements/task.tsx` | Задача и её шаги. |
| `Agent`, `AgentHeader`, `AgentContent`, `AgentInstructions`, `AgentOutput`, `AgentTool(s)` | `components/ai-elements/agent.tsx` | Карточка субагента. |
| `Terminal`, `TerminalHeader`, `TerminalTitle`, `TerminalStatus`, `TerminalContent`, `TerminalActions`, `TerminalCopyButton`, `TerminalClearButton` | `components/ai-elements/terminal.tsx` | Терминальный вывод. |
| `WebPreview`, `WebPreviewBody`, `WebPreviewNavigation`, `WebPreviewNavigationButton`, `WebPreviewUrl`, `WebPreviewConsole` | `components/ai-elements/web-preview.tsx` | Превью веб-страницы. |
| `Sandbox`, `SandboxHeader`, `SandboxContent`, `SandboxTabs*` | `components/ai-elements/sandbox.tsx` | Песочница. |
| `TestResults`, `TestSuite`, `Test`, `TestStatus`, `TestDuration`, `TestError*`, `TestResultsProgress`, `TestResultsSummary` | `components/ai-elements/test-results.tsx` | Результаты тестов. |
| `SchemaDisplay*` | `components/ai-elements/schema-display.tsx` | Отображение схемы API. |
| `StackTrace*` | `components/ai-elements/stack-trace.tsx` | Стек-трейс. |
| `EnvironmentVariables*` | `components/ai-elements/environment-variables.tsx` | Переменные окружения. |
| `PackageInfo*` | `components/ai-elements/package-info.tsx` | Сведения о пакете. |
| `Commit*` | `components/ai-elements/commit.tsx` | Карточка коммита. |
| `Canvas`, `Node*`, `Edge`, `Connection`, `Controls`, `Panel`, `Toolbar` | `components/ai-elements/` | Примитивы графа. |
| `Shimmer`, `ChatLoading`, `Suggestion(s)`, `Snippet*`, `JSXPreview*`, `Persona`, `OpenIn*` | `components/ai-elements/` | Анимация, загрузка, подсказки, сниппеты, JSX-превью, персона, открытие в другом чате. |

### 9.2 Граф workflow и таймлайн workflow

| Компонент | Файл | Роль |
|---|---|---|
| `WorkflowTimeline`, `WorkflowTimelineArcs`, `WorkflowTimelineFills`, `WorkflowTimelineTracks`, `WorkflowTimelineLamps`, `WorkflowTimelineStation`, `WorkflowTimelineLedge`, `WorkflowTimelineScrollbar` | `components/workflow-timeline/` | Рельсы, дуги, станции, лампы и скроллбар таймлайна. |
| `WorkflowAgentPill`, `WorkflowAgentFace`, `WorkflowArtifactPill`, `WorkflowArtifactRow`, `WorkflowArtifactStrip`, `WorkflowArtifactTile`, `WorkflowArtifactIndex` | `components/workflow-timeline/` | Пилюли агентов, лица, артефакты. |
| `WorkflowRunDigest`, `WorkflowCompletionCard`, `WorkflowCompletionArtifacts`, `WorkflowMoreRow`, `WorkflowRoll`, `WorkflowTruncatedNotice` | `components/workflow-timeline/` | Итоги, свёртки, обрезка. |
| `WorkflowHoleParts`, `WorkflowCardChrome`, `WorkflowRunSettings*`, `WorkflowSave*`, `WorkflowAskSettings*`, `WorkflowRosterParts`, `WorkflowStationMeta`, `WorkflowStreamChevrons`, `MarchLight` | `components/workflow-timeline/` | Дыры, хром карточки, настройки, сохранение, опросы, ростер, метаданные, стриминг. |
| `TaskWorkflowRunLines`, `WorkflowRunRail` | `components/workflow-run-line/` | Линии запуска workflow в списке задач. |

## 10. Карточки инструментов

### 10.1 Каркас

| Компонент | Файл | Роль |
|---|---|---|
| `ToolCallBlock` | `ToolCallBlocks.tsx` | Точка входа карточки инструмента. |
| `resolveRenderer`, `renderers` | `ToolCallBlocks/resolveRenderer.ts`, `renderers.tsx` | Выбор рендерера по имени инструмента. |
| `ToolLayout` | `ToolCallBlocks/ToolLayout.tsx` | Раскладка карточки: заголовок, тело, футер. |
| `ToolCallBody` | `ToolCallBlocks/ToolCallBody.tsx` | Тело карточки. |
| `ToolPresentation`, `ToolPresentationCapabilitiesProvider` | `ToolCallBlocks/ToolPresentation.tsx`, `presentationCapabilities.tsx` | Настройки презентации. |
| `ToolSummaryRow` | `ToolCallBlocks/ToolSummaryRow.tsx` | Компактная строка сводки. |
| `ToolCallProgressIndicator` | `ToolCallBlocks/ToolCallProgressIndicator.tsx` | Спиннер/прогресс вызова. |
| `ToolSnapshotFieldNotice` | `ToolCallBlocks/ToolSnapshotFieldNotice.tsx` | Предупреждение о снимке полей. |
| `QueuedSummaryContent` | `ToolCallBlocks/QueuedSummaryContent.tsx` | Сводка очереди. |

### 10.2 Рендереры по доменам

| Домен | Компоненты |
|---|---|
| Файлы и поиск | `ReadToolCallBlock`, `ReadFileChip`, `EditToolCallBlock`, `EditInlineDiffContent`, `SearchToolCallBlock`, `ToolSearchToolCallBlock`, `ExploreToolCallBlock`, `ChangesGroupToolCallBlock` |
| Исполнение | `ExecuteToolCallBlock`, `ExecuteCommand`, `ExecuteOutput`, `ExecuteGroupToolCallBlock`, `NodeReplToolCallBlock`, `NodeReplImageGrid`, `EvalWorkflowSnippetToolCallBlock` |
| Агенты и общение | `AgentToolCallBlock`, `AgentPromptSection`, `AskQuestionToolCallBlock`, `SwitchModeToolCallBlock`, `SendMessageToolCallBlock`, `TaskOutputToolCallBlock`, `TaskStopToolCallBlock`, `EscalateToolCallBlock`, `RespondToCoordinatorToolCallBlock`, `SubmitResultToolCallBlock` |
| Workflow | `CreateWorkflowToolCallBlock`, `GetWorkflowRunToolCallBlock`, `ListWorkflowRunsToolCallBlock`, `ListSavedWorkflowsToolCallBlock`, `ListSavedWorkflowsPresentation`, `SaveWorkflowToolCallBlock`, `SaveWorkflowOverwriteBadge`, `ResumeWorkflowRunToolCallBlock`, `ResolveWorkflowQuestionToolCallBlock`, `WorkflowRunCompactCard`, `WorkflowRunSubagentRoster`, `WorkflowRunHealthLine`, `WorkflowRunPhaseTrack`, `WorkflowDiagnosticsSection`, `WorkflowDraftLamp`, `WorkflowDraftOrdinal`, `WorkflowFeedbackContent`, `WorkflowCardMetaLine`, `WorkflowAmendsLine`, `WorkflowRetuneRow` |
| CUA | `CuaToolCallBlock`, `CuaGroupToolCallBlock`, `CuaToolCallDetails`, `CuaDetailListSection`, `CuaScreenshotSection`, `CuaAppSummaryIcon`, `CUA_TOOL_ICON`, `CUA_FALLBACK_ICON` |
| Конфигурация и автоматизации | `CronCreateToolCallBlock`, `CronCreateAutomationCard`, `OffPeakCreateTaskCard`, `ListModelsToolCallBlock`, `PlanGuidanceToolCallBlock`, `GoalToolCallBlock`, `McpToolCallBlock`, `SkillToolCallBlock`, `ReadSessionContextToolCallBlock`, `TodoToolCallBlock`, `WebFetchToolCallBlock`, `FallbackToolCallBlock` |
| Служебные | `readToolResultDisplay`, `ToolSnapshotFieldNotice`, `ToolPresentation`, `ToolSummaryRow`, `ToolCallProgressIndicator` |

## 11. Боковые панели

### 11.1 Каркас и навигация

| Компонент | Файл | Роль |
|---|---|---|
| `AnimatedSidePanePanel` | `app-shell/AnimatedSidePanePanel.tsx` | Правая панель с табами и анимацией. |
| `SidePaneTabTrigger`, `SidePaneTabIcon`, `SortableSidePaneTabTrigger`, `SidePaneTabDragOverlay`, `SidePaneTabOverview`, `SidePaneTabTitleTooltip` | `app-shell/` | Табы, drag, обзор, подсказки. |
| `SidePaneFullViewConversationHost`, `SidePaneFullViewConversationTab`, `SidePaneFullViewToggleButton` | `side-pane-full-view/` | Полноэкранный режим. |

### 11.2 Содержимое панелей

| Панель | Компоненты |
|---|---|
| План | `PlanDetailSidePane`, `Plan`, `PlanHeader`, `PlanContent`, `PlanFooter` |
| Терминал | `AnimatedTerminalPanel`, `SidePaneTerminalPane`, `TerminalSession`, `TerminalTabTrigger`, `Terminal`, `TerminalContent`, `TerminalHeader` |
| Терминал в фоне | `BackgroundBashOutputSidePane`, `BackgroundTaskElapsedLabel`, `ExecuteOutput` |
| Браузер | `BrowserUseSidePaneContent`, `UnifiedBrowserView`, `HumanBrowserView`, `BrowserViewportSurface`, `BrowserViewportToolbar`, `ResponsiveBrowserViewport`, `ResponsiveBrowserResizeHandles`, `BrowserSitePermissionsPage`, `BrowserSiteSettingsEntry`, `BrowserPermissionIcon`, `EmbeddedBrowserPermissionPrompts`, `EmbeddedWebsiteHeader`, `BrowserTabFavicon`, `BrowserUseTabIcon`, `BrowserEmptyState`, `BrowserGuestFailureState`, `BrowserLoadErrorState`, `BrowserToolbar` |
| Субагенты | `SubagentDirectorySidePane`, `SubagentSessionSidePane`, `SubagentDrilldown`, `Agent` |
| Workflow | `WorkflowRunSidePane`, `WorkflowRunSidePaneSections`, `WorkflowRunArtifactsSection`, `WorkflowRunDirectorySidePane`, `WorkflowRunPhaseList`, `WorkflowRunPhasePills`, `WorkflowRunProvenance`, `WorkflowRunQuestionRow`, `WorkflowRunSectionToggle`, `WorkflowRunFillFrames`, `WorkflowRunHoleParts`, `WorkflowRunSpineParts`, `WorkflowWorkspaceSidePane`, `WorkflowWorkspaceCard`, `WorkflowWorkspaceCardBody`, `WorkflowWorkspacePeek`, `WorkflowActorSessionSidePane` |
| Артефакты | `WorkflowArtifactSidePane`, `WorkflowArtifactBody`, `WorkflowArtifactCards`, `WorkflowArtifactTilePreview`, `ArtifactBoard`, `ArtifactChart`, `ArtifactChartView`, `ArtifactMetrics`, `ArtifactTable`, `ArtifactDetail`, `ArtifactKindIcon`, `ArtifactOpenAsFileButton`, `ArtifactPresetBody`, `PresetEmpty`, `PresetHeading` |
| Выделение | `SelectionSideChatPane`, `ConversationSelectionTooltip`, `MarkdownSelectionTooltip` |
| Плагины | `PluginUiSidePane`, `PluginUiCard`, `PluginUiToolCallBlock`, `PluginUiFollowUpDialogHost`, `PluginUiLauncherItems`, `SidePaneLauncherRow` |

## 12. Настройки

### 12.1 Каркас

| Компонент | Файл | Роль |
|---|---|---|
| `SettingsPage` | `SettingsPage.tsx` | Страница настроек: навигация, секции, поиск, вкладки. |
| `SettingsPageParts` (`SettingsRow`, `SettingsGroupCard`, `SettingsBadge`, `SettingsRangeControl`, `ThemePreviewCard`, `ThemeSelect`) | `settings/SettingsPageParts.tsx` | Строки, карточки, бейджи, ползунки, превью темы. |
| `SettingsHeaderBreadcrumb`, `SettingsBreadcrumbProvider`, `SettingsBreadcrumbReporter` | `settings/SettingsHeaderBreadcrumb.tsx` | Хлебные крошки. |
| `SettingsBackButton`, `SettingsSearchInput`, `SettingsSegmentedTabs`, `SettingsScopeBadge`, `SettingsFormActions`, `SettingsFormTextarea` | `settings/` | Навигация и формы. |
| `SettingsResourceGroup`, `SettingsResourceGroupHeader`, `SettingsResourceList`, `SettingsResourceHeaderActions` | `settings/` | Группы ресурсов. |
| `SettingsMachinesProvider`, `SettingsUserScopeProvider` | `settings/SettingsMachine.tsx` | Область настроек: машина/пользователь. |
| `SettingsSyncSelectionStep` | `settings-sync/SettingsSyncSelectionStep.tsx` | Выбор синхронизации настроек. |

### 12.2 Назначение секций

| Секция | Что настраивает |
|---|---|
| Общие и внешний вид | Язык, тема, размер интерфейса, автоархивация задач. |
| Горячие клавиши | Просмотр, поиск и переназначение сочетаний. |
| Модели и провайдеры | Подключения, ключи, модели, роли, Coding Plan и Start Plan. |
| Память | Хранилище памяти и просмотр записей. |
| Плагины | Маркетплейс, установка, обновление, область действия и UI плагина. |
| MCP | Серверы, транспорт, здоровье, синхронизация с удалённым workspace. |
| Hooks | Список hook, формы, доверие к workspace. |
| Skills и команды | Каталог скиллов и slash-команд, импорт. |
| Субагенты | Реестр, роли и уровень reasoning. |
| Автоматизации | Расписания, шаблоны, история запусков и пауза. |
| Off-peak | Задачи низкого тарифа, история и шаблоны. |
| Сохранённые workflow | Каталог, запуск, аргументы, история и артефакты. |
| Статистика | Расход по моделям, heatmap, Coding Plan и App Usage. |
| Миграция и импорт | Перенос из других агентов: скиллы, команды, MCP, плагины. |
| Браузер и CUA | Разрешения браузера, computer-use и импорт Chrome. |
| Поиск по файлам | Индексация и параметры файлового поиска. |
| Источник и синхронизация | Source server, отчёты миграции, синхронизация плагинов и скиллов. |
| Данные и БД | Каталог базы, динамические workflow, проактивные подсказки. |
| Coding Plan | Апгрейд, сброс квоты, биллинг и остаток лимита. |

### 12.3 Состав секций

| Секция | Компоненты |
|---|---|
| Общие и внешний вид | `GeneralSectionContent`, `GeneralSectionHeader`, `AppearanceSectionContent`, `TaskAutoArchiveSettings`, `LocaleSwitcher`, `ThemePreviewCard`, `ThemeSelect` |
| Горячие клавиши | `ShortcutSettingsSection`, `ShortcutBindingRow`, `ShortcutSearchBar` |
| Модели и провайдеры | `ModelProviderSection`, `ModelProviderSectionLayout`, `ModelProviderSectionDetail`, `ModelProviderSectionNavigation`, `ProviderCardHeader`, `ProviderApiKeySection`, `ProviderConnectionSection`, `ProviderModelsSection`, `ProviderFamilyHeader`, `ProviderFamilyDetailShell`, `ProviderFamilyPlanModeSwitch`, `ProviderTemplatePicker`, `ProviderLogo`, `ProviderStatusIndicator`, `ProviderApiFormatSelect`, `ProviderDetailFeedbackBoundary`, `InlineEditableProviderCard`, `ApiKeyInput`, `PresetProviderApiKeyBanner`, `BigModelRegistrationHint`, `ModelEditorAdvanced`, `ModelConfigHelp`, `ModelConfigInputLabel`, `ModelSettingsGroup`, `ProviderModelReasoningSettings`, `ProviderModelReasoningLevelEditor`, `ProviderModelMetadataDialog`, `ProviderModelMetadataDialogActions`, `ProviderModelMetadataFields`, `ProviderModelModalityOptions`, `ModelRowInput`, `BooleanModelOption`, `ModelOptionCheckbox`, `JsonSlotEditor`, `SortableProviderModelList`, `ModelConfigDraftFeedback`, `ModelConfigRestoreButton`, `ModelSmartConfigSwitch`, `CodingPlanStatusPanel`, `CodingPlanStatusActions`, `CodingPlanStatusMeta`, `CodingPlanUpgradeAction`, `StartPlanStatusMeta`, `StartPlanBalanceCard`, `StartPlanCard`, `StartPlanQuotaStatusCard`, `ModelProviderLoadingCard`, `PresetProviderPlaceholderCard` |
| Память | `MemorySettingsSection`, `MemorySettingsViewer` |
| Плагины | `PluginsSection`, `PluginStorePage`, `PluginStoreListView`, `PluginStoreDetailView`, `PluginStoreCard`, `PluginStoreAvatar`, `PluginStoreEnabledSwitch`, `PluginStoreInstallButton`, `PluginStoreItemMenu`, `PluginStoreOpenUiButton`, `PluginStorePaidPlanBadge`, `PluginStoreUpdateBadge`, `PluginStoreUpdateButton`, `PluginStoreAdvancedSection`, `PluginStoreSourcesDialog`, `PluginStoreSourceRefreshFailure`, `PluginComponentGroups`, `PluginConfigControls`, `PluginScopeMenu`, `PluginInstallEmptyState`, `PluginLoadingState`, `PluginSearchEmptyState`, `InstalledPluginManagement`, `InstalledPluginDetailDialog`, `InstalledPluginDetailPanel`, `PluginDetailRow`, `PluginHookDetails`, `PluginWarningList`, `PluginUninstallConfirmDialog`, `AddMarketplaceSourceDialog`, `ExternalAgentImportDialog`, `PluginsImportDialog`, `PluginAddMenu` |
| MCP | `McpSettingsSection`, `McpServerList`, `McpServerForm`, `McpStatusDot`, `McpFailurePresentation`, `RemoteMcpSyncDialog`, `RemoteMcpSyncTitle`, `RemoteMcpSyncSelectionList`, `RemoteMcpSyncTargetRow`, `RemoteMcpSyncBulkSelectionCheckbox`, `RemoteMcpSyncExistingFilterCheckbox` |
| Hooks | `HooksSection`, `HooksList`, `HookForm`, `WorkspaceHookTrustNotice` |
| Skills и команды | `SkillsSection`, `CommandsSection`, `CommandCard`, `CommandForm`, `SkillsImportDialog`, `CommandsImportDialog` |
| Субагенты | `SubagentsSection`, `SubagentReasoningField`, `ExternalAgentImportSelectionPanel` |
| Автоматизации | `AutomationsSection`, `AutomationsMainBreadcrumbFrame`, `AutomationEditView`, `AutomationInstructionsComposer`, `AutomationInstructionsTextarea`, `AutomationInstructionsToolbar`, `AutomationScheduleBadge`, `AutomationSwitchToggle`, `AutomationTemplateSkeletonGrid`, `AutomationCreateDropdown`, `AutomationHistoryEmptyState`, `AutomationKeepAwakeNotice`, `AutomationSettingsHistoryTabs`, `AutomationAddScheduleIcon`, `AutomationCancelActionIcon`, `AutomationChevronDownIcon`, `AutomationClockIcon`, `AutomationContinueIcon`, `AutomationEditActionIcon`, `AutomationExternalLinkIcon`, `AutomationIdleTimeIcon`, `AutomationInfoIcon`, `AutomationMoreHorizontalIcon`, `AutomationPauseActionIcon`, `AutomationPausedIcon`, `AutomationRefreshIcon`, `AutomationRunNowIcon`, `AutomationTrashIcon` |
| Off-peak | `OffPeakEditView`, `OffPeakEditActionsMenu`, `OffPeakHistoryTab`, `OffPeakTaskList`, `OffPeakTemplateIcon` |
| Сохранённые workflow | `SavedWorkflowsSection`, `SavedWorkflowCard`, `SavedWorkflowLastRunBadge`, `SavedWorkflowDetailView`, `SavedWorkflowDetailHeader`, `SavedWorkflowGlobalGroup`, `SavedWorkflowProjectGroup`, `SavedWorkflowLaunchDialog`, `SavedWorkflowMetaForm`, `SavedWorkflowMoveDialog`, `SavedWorkflowRunHistory`, `SavedWorkflowArgsTable`, `SavedWorkflowArtifactChips`, `AutomationsPageTitle`, `AutomationsPageTitleSwitch` |
| Статистика | `UsageStatsSection`, `AppUsagePanel`, `AppUsageLifetimeSummaryStrip`, `AppUsageDailyModelTrendChart`, `AppUsageModelUsagePieChart`, `CodingPlanUsagePanel`, `CodingPlanUsageBarChart`, `CodingPlanUsageLineChart`, `UsageHeatmap`, `HeatmapColumn`, `UsageChartLoadBoundary`, `UsageStatsErrorNotice`, `UsageEmptyState`, `UsageMetricCard`, `RANGE_OPTIONS` |
| Миграция и импорт | `MigrationSection`, `MigrationCandidatesCard`, `ExternalAgentImportDialog`, `SkillsImportDialog`, `CommandsImportDialog`, `McpServersImportDialog`, `PluginsImportDialog` |
| Браузер и CUA | `BrowserSettingsSection`, `ComputerUseSection`, `WindowsChromeImportConsentDialog` |
| Поиск по файлам | `WorkspaceFileSearchSection` |
| Источник и синхронизация | `SourceServerManagementPanel`, `SourceServerMigrationReportPanel`, `SourceServerUpdateActivity`, `SourceServerLogList`, `RemotePluginSyncDialog`, `RemoteSkillSyncDialog`, `RemoteSkillSyncTitle`, `RemoteSkillSyncSelectionList`, `RemoteSkillSyncTargetRow`, `RemoteSkillSyncResultList`, `RemoteSkillSyncBulkSelectionCheckbox`, `RemoteSkillSyncExistingFilterCheckbox`, `RemoteSyncDialogs`, `RemoteSyncDropdownButton`, `RemoteSyncMenuItems`, `RemoteSyncPreflightTimeoutError` |
| Данные и БД | `DataBaseDirControl`, `DynamicWorkflowModeSetting`, `ProactiveSuggestionsSetting`, `EnabledStatusFilterSelect`, `StatusDot` |
| Coding Plan | `CodingPlanEntryButton`, `CodingPlanUpgradeDialog`, `CodingPlanUpgradeDialogProvider`, `CodingPlanEmbeddedWebviewDialog`, `CodingPlanQuotaResetAction`, `LocalizedCodingPlanQuotaResetAction`, `CodingPlanQuotaResetDialog`, `CodingPlanQuotaResetOpportunity`, `CodingPlanQuotaResetStatusContent`, `CodingPlanBillingDiscountBadge`, `CodingPlanBillingDiscountBadgePill`, `CodingPlanBillingDiscountBanner`, `CodingPlanBillingDiscountInfoDialog`, `CodingPlanUsageRemainingPanel` |

## 13. Диалоги, оверлеи и прикладные поверхности

| Группа | Компоненты |
|---|---|
| Командная палитра и поиск | `CommandCenterDialog`, `CommandCenterScopeButton`, `CommandCenterSearchHistory`, `CommandCenterConversationTimestamp`, `QuickPickCommandDialog`, `TaskFindDialog`, `HighlightedMatchText`, `QuickPickCommandIcons` |
| Подтверждения и вопросы | `ConfirmDialogHost`, `AlertDialogHost`, `ElicitationDialog`, `PermissionDialog`, `V4UserInputDialog`, `V4InteractionDialogs`, `AskQuestionToolCallBlock`, `InteractionRequestOriginBadge` |
| Боты | `BotsDialog`, `BotSummaryCard`, `BotDangerCard`, `BotReplyGranularityCard`, `BoundGroupsCard`, `BoundGroupsList`, `PrivateDeliveryRetry`, `ProviderSettingsCard`, `WorkspaceAccessCard`, `ProviderIcon` |
| Фидбек | `FeedbackCenter`, `FeatureRequestDialog`, `FeedbackProcessView`, `FeedbackScreenshotPicker`, `FeedbackSubmitForm`, `SubmitProgressView`, `ContactSection`, `DescriptionSection`, `LogUploadToggle`, `Section`, `SubmitFooter`, `FeedbackSupplementComposer`, `TicketDetailView`, `FeedbackTicketList`, `TicketsView`, `TicketsInitialLoadingState`, `FeedbackErrorTip`, `RequiredMarker`, `StatusIndicator`, `FeedbackProgress`, `FeedbackTimeline`, `FeedbackBackgroundUploadIndicator`, `FeedbackBugIcon`, `FeedbackIdeaIcon`, `FeedbackPerformanceIcon`, `FeedbackQuestionIcon` |
| Удалённое подключение | `SSHDialog`, `RemoteConnectionDialog`, `RemoteConnectionDialogContent`, `RemoteConnectionDirectoryStep`, `RemoteConnectionSettingsStep`, `RemoteConnectionFields`, `RemoteSegmentedControl`, `SshConfigAliasPicker`, `RemoteConnectionWizardHeader`, `RemoteConnectionWizardSidebar`, `EditConnectionProfileDialog`, `RemoteConnectionConnectingStep`, `RemoteConnectionHistoryInput`, `RemoteConnectionNavigationDot`, `RemoteConnectionSelection`, `RemoteConnectionStateIcon`, `RemoteConnectionKindTag`, `RemoteConnectionKindTile`, `RemoteConnectionStatusTag`, `RemotePasswordInput`, `RemoteTaskDeviceLabel`, `RemoteConnectionProgressProvider`, `RemoteConnectionMinimizedProgress`, `SourceServerBoundaryDialogContent`, `DirectoryBrowser` |
| Онбординг | `OnboardingDialog`, `OnboardingWizardHeader`, `OnboardingWizardFooter`, `OnboardingWizardSidebar`, `OnboardingWelcomeView`, `OnboardingWelcomeAsciiVisual`, `OnboardingMeshBackground`, `OnboardingModeSelector`, `OnboardingOccupationGrid`, `OccupationOnboarding`, `OccupationOnboardingVisual`, `OnboardingHeader`, `OnboardingAgentsFileStep`, `OnboardingAgentSettingsStep`, `OnboardingExternalAgentImportStep`, `OnboardingFinishStep`, `OnboardingMigrationStep`, `OnboardingSessionsStep` |
| Вход | `WelcomeScreen`, `LoginPanel`, `LoginApiKeyForm`, `LocaleSwitcher` |
| Ошибки и уведомления | `ChatErrorBanner`, `GlobalNoticeSurface`, `ScopedErrorBoundary`, `AppErrorBoundary`, `toast`, `AnchoredToastStack`, `ToastMessageView`, `Alert`, `AlertDialog`, `ErrorBlock` |
| Обновления | `UpdateStatusButton`, `UpdateStatusDialog`, `UpdateStatusDialogController`, `UpdateStatusWindowRoot`, `UpdateReleaseNotesTooltip`, `PostUpdateReleaseNotesDialog` |
| Coding Plan и биллинг | `CodingPlanBillingDiscount*`, `CodingPlanUsageRemainingPanel`, `CodingPlanQuotaReset*`, `CodingPlanUpgradeDialog*`, `CodingPlanEntryButton` |
| Облачные и маркетинговые поверхности | `CloudContentDialog`, `CloudDialogDescription`, `CloudFormattedTextContent`, `CloudDialogHero`, `CloudInteractiveBundleHero`, `CloudImage`, `CloudLottie`, `CloudVideo`, `MarketingBanner`, `MarketingBannerView`, `MarketingDialogs`, `MarketingFailureDialog` |
| Разрешения CUA | `CuaPermissionObservationAttachment` |
| Плагинный UI | `PluginUiCard`, `PluginUiToolCallView`, `PluginUiSidePaneView`, `PluginUiFollowUpDialogHost`, `PluginUiBackgroundHost`, `PluginUiModelContextChip`, `PluginUiLauncherItems`, `PluginUiSessionProvider`, `PluginUiWorkspaceProvider`, `PluginUiConversationScope` |
| Gen UI | `GenUiCard`, `GenUiMessageResponse`, `TweakPanel` |
| Ресурсы и награды | `ResourceManagerApp`, `NetworkSection`, `UsageGroup`, `UsageMeter`, `StorageSection`, `StorageDiskCard`, `StorageCategoryList`, `StorageCategoryDetail`, `StorageCleanConfirmDialog`, `RewardsWebview` |
| Прочее | `DeveloperToolsPane`, `WhiteboardPane`, `TreemappingPane`, `TodoPanel`, `PreviewPane`, `MessageChangeSummaryPanel`, `ModelTrajectoryPane` |

## 14. Git, файлы и предпросмотр

| Группа | Компоненты |
|---|---|
| Git | `GitPane`, `GitPaneChangeCard`, `GitActionMenu`, `GitGraphPane`, `GitGraphDialog`, `GitGraphCommitDetail`, `GitBranchSwitcher`, `GitBranchCreateDialog`, `GitBranchSwitchAssistDialog`, `DiffViewer`, `LightweightDiffPreview`, `HighlightedLightweightDiffPreview` |
| Предпросмотр файлов | `PreviewPane`, `PreviewPaneContent`, `CodeContent`, `ImagePreviewContent`, `SvgPreviewContent`, `MarkdownPreviewContent`, `PreviewPaneMediaContent`, `PreviewPaneOfficeContent`, `PreviewPaneOfficeDocxContent`, `PreviewPaneOfficeLegacyDocContent`, `PreviewPaneOfficeXlsxContent`, `PatchFallbackContent`, `PdfPreviewContent`, `PptxPreviewContent`, `PdfViewer`, `PptxPreviewViewer`, `PptxSelectionActionBar`, `CodeViewer`, `CodeCommentAnnotation` |
| Модельная траектория | `ModelTrajectoryPane`, `ModelTrajectoryPaneParts`, `ModelTrajectoryPaneDetails`, `ModelTrajectoryTimeline`, `ModelTrajectorySectionTitle`, `ModelTrajectorySearchBar`, `ModelTrajectorySearchHighlight`, `ModelTrajectoryExpandableMessage`, `ModelTrajectoryExpandedContent`, `ModelTrajectoryExpansionMenu`, `ModelTrajectoryAssistantDetailCard`, `ModelTrajectoryErrorBlock`, `AssistantDetailCard`, `UsageBadges`, `ContentPartView`, `CallCard`, `TrajectorySectionTitle`, `ExpandableTrajectoryMessage`, `TrajectoryExpandedContent` |
| Терминал | `Terminal`, `TerminalSession`, `TerminalTabTrigger`, `SidePaneTerminalPane`, `AnimatedTerminalPanel`, `TerminalContent`, `TerminalHeader`, `TerminalActions`, `TerminalCopyButton`, `TerminalClearButton`, `TerminalStatus`, `TerminalTitle` |

В 3.16.2 `DiffViewer` работает на движке `diffs-container` с темами
`pierre-dark` и `pierre-light`. Он сам рисует заголовки файлов, хунки,
нумерацию, выбор строк, аннотации и кнопки разрешения конфликтов. Стилевые
хуки: `[data-diffs-header]`, `[data-diff-span]`, `[data-diff-type]`,
`[data-selected-line]`, `[data-line-annotation]`, `[data-merge-conflict]`,
`[data-merge-conflict-action]`, `[data-expand-up|down|both]`,
`[data-expand-all-button]`.

## 15. Базовые примитивы

### 15.1 `components/ui`

`Accordion`, `Alert`, `AlertDialog`, `Avatar`, `Badge`, `Button`, `ButtonGroup`, `Card`,
`Carousel`, `Chart`, `Checkbox`, `Collapsible`, `Command`, `ContextMenu`, `Dialog`,
`DropdownMenu`, `HoverCard`, `Input`, `InputGroup`, `Kbd`, `Label`, `Popover`,
`Progress`, `RadioGroup`, `Resizable`, `ScrollArea`, `ScrollFadeViewport`, `Select`,
`Separator`, `Spinner`, `Switch`, `Tabs`, `Textarea`, `Toast`, `Tooltip`,
`FlipMetricValue`, `SmoothMetricValue`, `FloatingParticles`, `GlmMonochromeIcon`,
`ZCodeAboutLogo`, `ZCodeWordmarkLogo`, `CodeViewer`, `DiffViewer`, `PdfViewer`,
`PptxPreviewViewer`, `PptxSelectionActionBar`.

Все они несут `data-slot`, через который zskin правит радиусы, высоты и цвета
точечно. Сквозные токены: `--color-popover*`, `--color-card*`, `--color-input*`,
`--color-border*`.

### 15.2 Иконки и файловые обозначения

`ClientSceneLucideIcon`, `PluginIcon`, `ProjectFolderIcon`, `FileDisplayIcon`,
`FileDisplayInline`, `ProviderLogo`, `Feedback*Icon`, `Automation*Icon`,
`ZCodeAppLogo`, `DevicePlatformIcon`, `GlmMonochromeIcon`.

## 16. Стилевые хуки по зонам

В собранном CSS 3.16.2 — 341 уникальное имя `--color-*`; в блоках
`.theme-zai-dark` определено 190 цветовых переменных, в `.theme-zai-light` —
158. База `:root,:host` содержит 269 цветовых имён. Значение
`--ui-font-size` по умолчанию — 14px. Полный дамп:
[ui-tokens-3.16.2.txt](ui-tokens-3.16.2.txt).

| Зона | Токены | Селекторы и атрибуты |
|---|---|---|
| Весь UI | `--ui-font-size`, `--color-background`, `--color-foreground` | `html.theme-zai-dark`, `html.theme-zai-light`, `html.dark` |
| Окно | фон, границы, тень | `DesktopWindowFrame`, `DesktopTopOverlay`, `[data-rail-position]` |
| Сайдбар | `--color-sidebar`, `--color-selected`, `--color-hover` | `ProjectSidebar`, `[data-slot="scroll-area"]` |
| Чат | `--color-trajectory-*`, `--color-markdown-inline-code`, `--color-find-highlight*` | `[data-zcode-stream-animate]`, `[data-zcode-tool-stream-animate]`, `[data-zcode-chat-loading-animate]`, `[data-zcode-collapsible-animate-close]` |
| Композер | `--color-input*`, `--color-usage*`, `--color-context-breakdown*` | `.prompt-mention`, `[data-slot="textarea"]`, `[data-slot="input-group-control"]`, `[data-composer-layout]`, `[data-composer-collapse-priority]` |
| Панель статуса | `--color-card*`, `--color-surface-hover` | `[data-testid="chat-summary-panel"]`, `[data-display-mode]` |
| Терминал | `--color-terminal-*` (22 токена) | `.terminal-xterm-shell` |
| Браузер | фон и границы панели | `.browser-use-viewport`, `.side-pane-open-tab-shell`, `[data-browser-*]` |
| Diff | `--color-diff-added*`, `--color-diff-removed*` | `[data-diffs-header]`, `[data-diff-span]`, `[data-selected-line]`, `[data-merge-conflict-*]`, `[data-expand-*]` |
| Workflow | `--color-{subagent,skill,session,plugin}-node*`, `--color-workflow-*` | `.wf-*`, `[data-eye-expression]`, `[data-zcode-pptx-render-surface]` |
| Мобильный remote | `--color-background`, `--color-border` | `[data-mobile-chat-overlay]`, `[data-mobile-side-pane-overlay]` |
| Поиск | `--color-find-highlight*` | `.task-search-result-highlight` |
| Изображения | фон загрузки | `.markdown-image-loading-shimmer` |
| Тревога | акцент | `.animate-zcode-alarm-ring` |

## 17. Покрытие исходников

Числа в таблице — исходники 3.15.1, структурная база для 3.16.2. Корень
`src/` — 114 файлов `.tsx`: загрузка, окно, чат-панели, терминал, диалоги,
превью. Остальные 46 каталогов с компонентами:

| Модуль | `.tsx` | Раздел каталога |
|---|---:|---|
| `components/` | 162 | 9, 15 |
| `settings/` | 143 | 12 |
| `v4/` | 76 | 7, 8 |
| `ToolCallBlocks/` | 67 | 10 |
| `project-sidebar/` | 44 | 6 |
| `app-shell/` | 43 | 5, 11 |
| `feedback/` | 16 | 13 |
| `chat-input-toolbar/` | 15 | 8 |
| `onboarding/` | 12 | 13 |
| `plugin-ui/` | 11 | 11, 13 |
| `browser-use/` | 11 | 11 |
| `remote-connection/` | 10 | 13 |
| `resource-manager/` | 8 | 13 |
| `root/` | 7 | 3 |
| `workspace-file-tree/` | 6 | 6 |
| `BotsDialog/` | 6 | 13 |
| `mentions/` | 5 | 8 |
| `quickpick/` | 4 | 13 |
| `git-graph/` | 4 | 14 |
| `hooks/` | 4 | 3 |
| `WorkspaceSidebar/` | 3 | 6 |
| `WorkspaceHeaderSections/` | 3 | 5 |
| `web-remote-control/` | 3 | 5 |
| `side-pane-full-view/` | 3 | 5, 11 |
| `highspeed/` | 3 | 8 |
| `gen-ui/` | 3 | 13 |
| `lib/` | 3 | 15 |
| `terminal/` | 2 | 11, 14 |
| `store/` | 2 | 3 |
| `rewards/` | 2 | 13 |
| `remote/` | 2 | 3 |
| `prompt-editor/` | 2 | 8 |
| `project-workflow/` | 2 | 11 |
| `i18n/` | 2 | 3 |
| `conversation-share-interaction/` | 2 | 7 |
| `workspace-plugin-preview/` | 1 | 11 |
| `workspace-grouped-tasks/` | 1 | 6 |
| `settings-sync/` | 1 | 12 |
| `sidebar-activity/` | 1 | 6 |
| `remote-connection-flow/` | 1 | 13 |
| `login/` | 1 | 13 |
| `global-notice/` | 1 | 13 |
| `git-branch-switcher/` | 1 | 5 |
| `cua-permission/` | 1 | 13 |
| `conversation-workspace-target/` | 1 | 8 |
| `command-center/` | 1 | 13 |

Двенадцать каталогов не содержат `.tsx` и остаются вне компонентного
каталога: `assets/`, `composer-toolbar-layout/`, `git-action-menu/`,
`GitPane/`, `marketing-touch-contract/`, `presentation/`,
`request-security-edition/`, `shortcuts/`, `types/`, `workers/`,
`workspace-config-catalog/`, `workspace-file-search/`. В них живут типы,
чистые функции, воркеры и барели; поведение описано в разделах, где эти
модули питают видимые компоненты.

Не вошли в таблицы как отдельные компоненты: чистые хуки, сторы, транспорт
(`v4/*Transport*.ts`), утилиты `lib/` и воркеры. Они описаны в тексте там,
где определяют поведение компонента.