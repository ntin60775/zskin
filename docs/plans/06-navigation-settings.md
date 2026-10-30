# План 6. Навигация, списки, настройки

Шаг 6 — периферия: навигация, списки, настройки. Зависит от шагов 1 и 3.

Разведка 3.16.2: настройки просмотрены вживую (фон — приёмка плана 1) —
артефактов нет; в сайдбаре подтверждены `data-project-*`,
`data-task-row-metadata`, `data-task-item-key`, `data-task-title-copy`;
`data-grouped-*` в перепись не попал — проверить в группированном
виде.

Разведка 3.17.1 (2026-10-29, grep `app.asar` вместе с аудитом апдейта).
Имена компонентов из клона 3.14.3 вычищены из задач: как CSS-хуки они
мертвы, в бандле 3.17.1 их литералов нет (полный список удалённых —
история git, `b32bd2c`); работа через подтверждённые хуки ниже. Все
data-хуки шага живы и расширены: `data-project-*` — шесть имён (host,
id, key, name, sidebar-panel, workspace-identity); полный инвентарь
`data-grouped-*` — семь имён (layout-key, sticky-header, task-key,
group-header-id, group-content-id, group-item-id,
empty-drop-zone-id); `data-workspace-file-tree-hierarchy-guides`
(значение = depth) и семья testid `workspace-file-tree-*`;
`data-settings-section-nav` — значение равно ключу секции, активный
пункт несёт `aria-current="page"`; `data-settings-panel-frame`;
`data-terminal-tab-content`; `[data-slot="command-input"]`.
Классы подтверждены: `SettingsPage`, `GitPane`, `GitBranchSwitcher`,
`OnboardingDialog`, `PluginStore`, `FileTree`, `WorkspaceFileTree`,
`McpServerList`, `UsageHeatmap`, `TerminalSession`. Точные замены
вместо имён клона: hooks — `hooks-settings-section`, `hooks-form`;
MCP — `mcp-status`, `mcp-server-row`, `mcp-settings`,
`mcp-settings-refresh`, `mcp-open-authorization-button`; субагенты —
`subagent-directory`, `subagent-row`, `subagent-session`,
`subagent-built-in-model-trigger`; вход — семья `login-api-key-*`
(12 литералов), `login-trigger`, `login-menu-item`; онбординг —
`onboarding-dialog`, `onboarding-page`, `onboarding-wizard-cancel`,
`onboarding-migration-dialog`; статистика — `usage-stats`,
`coding-plan-usage-trends`; плагины — `plugin-store-sidebar-open`
(новый в 3.17.1). Разделителей с общим слотом нет — только
`select-separator`, `dropdown-menu-separator`, `context-menu-separator`.
Новые поверхности 3.17.1: app-header семья (`desktop-top-logo-sidebar-toggle`,
`desktop-top-nav-back`, `desktop-top-overlay`, `side-pane-toggle`,
`side-pane-full-view-host`, `terminal-toggle`, `logout-button`),
`project-section`, `automations-open`, семья `side-pane-*` (42
литерала: `side-pane-add-item`, `side-pane-content-slot`,
`side-pane-full-view*`, …). Не поверхности: `--color-user-message-bubble`
задан во всех секциях токенов, но класс на разметке не встречается —
заготовка апстрима, не задача; `composer-thought-meter` — сток
композера, палитра шага 5 его накрывает.

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

Статус 2026-10-29 (исполнение, кроме 6.16 — отложен решением
пользователя; 6.11 закрыт записью-ограничением после живого осмотра —
поверхности превью-карточек в сборке нет). В тему вошли токены 6.21
в обеих схемах и структурные
правила 6.1 (разделители по семействам), 6.4 (hover строк, dark-scope),
6.9 (инактивные пункты + активный по aria-current); всё остальное уже
ехало на токенах 1.1 через стоковые утилиты. Приёмка живьём (3.17.1
под лоадером, CDP): hover строки задач #32302f — форс hover +
getMatchedCSSRules подтвердил, что внеслойное правило бьёт слоевую
утилиту; активная строка bg-selected #3c3836; настройки открыты
синтетическим ctrl+,: 19 секций, активный пункт #3c3836/#ebdbb2,
рамка #282828; плашка «Awaiting approval» в плагинах едет на
success-парах (#b8bb26 / success-surface). Light — атомарной подменой
классов с откатом: все новые токены резолвятся, active-пара настроек
#3c3836 на #d5c4a1 (6,76:1). Контраст скриптом: текстовые пары ≥ 4,5:1
(dark primary 6,49; destructive 4,77; инактивная навигация 6,77/5,74
после перевода на subtle-пару — стоковый light давал 4,29:1);
графические маркеры узлов session/subagent в light 3,55:1 — планка
графики 3:1 (иконки, не текст). Записи-ограничения: строки file-tree
не смонтированы (дерево пусто; правила активны по подтверждённым хукам,
направляющие — inline-стили, CSS недоступны); subagent-directory,
MCP-точки и usage-статистика — пустые состояния секций (правила
токен-наследуемые); командная палитра не открылась синтетическим
ctrl+k — её селекторы уже покрыты шагами 1 и 5 (command-item selected,
find-токены); highspeed/remote/continuity-поверхности в текущем виде
не монтируются — токены резолвятся в обеих схемах. Бейдж платного
плагина остаётся стоковым (решение 1.1: тёплые коричнево-кремовые
значения встают в палитру). Поверхности 6.18–6.20: фидбека нет ни в
бандле (литералы — только логи телеметрии), ни в DOM — запись:
правила невозможны, форма унаследует 1.8 автоматически, если
поверхность появится; онбординг и вход требуют свежего
login/onboarding-состояния и в живой сессии не монтируются — их хуки
подтверждены бандлом (`onboarding-*`, семья `login-api-key-*`),
поверхности собраны из примитивов 1.7–1.9 и статусных токенов, первая
живая проверка — при следующем логине/онбординге.

### Приёмка задач шага

Задача закрыта, когда выполнено всё перечисленное:

1. Правило в теме, целевые цвета — из «Что», а не по памяти.
2. Поверхность смонтирована в живом клиенте, правило применено в обеих
   схемах: computed-стили, hover/active — через `CSS.forcePseudoState`;
   число контраста записано с поверхностью, на которой измерено.
3. Контраст смыслового текста ≥ 4,5:1 от фактического фона.
4. Один коммит на задачу: в описании — подтверждённые селекторы и что
   осталось гипотезой.
5. Поверхность, которую не удалось смонтировать всеми средствами
   (настройки, диалоги, состояния), закрывает задачу записью-ограничением
   по прецеденту 4.4 и 5.18 — только после попытки, не молча.
6. Элемент, чей хук объявлен «снять при приёмке», либо получает
   подтверждённый селектор в теме, либо задачу закрывает та же
   запись-ограничение.

### 6.1. Список выбора и меню (пара 13)
Слоты `select-*`, `dropdown-menu-*`, `command-*`.
**Что.** Пункт: hover `#32302f`, selected `#3c3836`, текст `#ebdbb2`,
разделители `#3c3836`.
**Как.** `[data-slot="select-item"]`, `dropdown-menu-item`,
`command-item`; разделители — `select-separator` /
`dropdown-menu-separator` (общего слота `separator` в бандле нет);
`--color-menu-hover` (резолвится живьём, `#32302f` в тёмной).

### 6.2. Дерево (пара 14)
`FileTree`.
**Что.** Строка: текст `#ebdbb2`, папки `#bdae93`, guides `#3c3836`,
selected `#3c3836`, hover `#32302f`.
**Как.** Классы `FileTree`/`FileTreeOpen` подтверждены;
`data-workspace-file-tree-hierarchy-guides` (= depth, при его наличии
рисуются направляющие), testid `workspace-file-tree-row`,
`workspace-file-tree-depth`, `workspace-file-tree-mask-offset`;
selected-класс строки — гипотеза, снять при приёмке.

### 6.3. Реестр агентов (пара 53)
**Что.** Карточки агентов: `#282828`, рамка `#3c3836`, роль — brand,
метрики — `#928374` (какой элемент несёт метрики, снять при приёмке).
**Как.** Хуки — testid `subagent-directory`, `subagent-row`,
`subagent-session`; обёртка — `side-pane-*` (см. разведку). Токены
card/border.

### 6.4. Список сессий и задач (пара 76)
**Что.** Строка: hover `#32302f`, active `#3c3836`, заголовок группы —
`#928374`; бейдж активности — brand; без зебры.
**Как.** `data-task-row-metadata`, `data-task-item-key`,
`data-task-title-copy` (подтверждены); `data-project-*` — шесть имён:
`-host`, `-id`, `-key`, `-name`, `-sidebar-panel`,
`-workspace-identity`; группировка — `data-grouped-*`: `layout-key`,
`sticky-header`, `task-key`, `group-header-id`, `group-content-id`,
`group-item-id`, `empty-drop-zone-id` (инвентарь снят из бандла;
живой осмотр группированного вида — на приёмке). Токены selected/hover.

### 6.5. Поиск и палитра (пара 77)
**Что.** Диалог на popover, инпут без рамки, совпадение —
`--color-find-highlight`.
**Как.** `[data-slot="command-input"]`, `command-item` (слоты живы);
find-токены живы, значений не меняли; поверхность диалога снять с
живого DOM приёмки.

### 6.6. Файловое дерево-панель (пара 78)
`WorkspaceFileTree`.
**Что.** Фон панели `#1d2021`, строки как 6.2, липкие папки — фон хрома.
**Как.** Класс `WorkspaceFileTree` подтверждён (20 вхождений); testid
`workspace-file-tree-panel`, `workspace-file-tree-refresh-button`;
`data-workspace-file-tree-hierarchy-guides`. Токены panel/sidebar.

### 6.7. Git (пара 79)
`GitPane`, `GitBranchSwitcher`.
**Что.** Статусы из `--color-git-*` (modified brand, added/untracked
`#b8bb26`, deleted `#fb4934`, renamed `#83a598`); граф — линии `#3c3836`,
узлы `#928374`, HEAD brand.
**Как.** Оба класса подтверждены; токены git в 3.17.1 без изменений
(added/deleted/descendant/ignored/modified/renamed/untracked); SVG
графа — `stroke`/`fill` селекторами (гипотеза).

### 6.8. Терминал-панель (пара 80)
`TerminalSession`.
**Что.** Панель на `#282828`, табы как 1.6, статус success/error
(элемент индикатора статуса снять при приёмке).
**Как.** Класс `TerminalSession` подтверждён; `--color-terminal-*`
без изменений; `data-terminal-tab-content` внутри таб-триггера с
`data-active` (механизм 1.6 жив); переключатель панели — testid
`terminal-toggle` в app-header.

### 6.9. Настройки (пара 81)
`SettingsPage`.
**Что.** Фон базы, контент на `#282828`, навигация на хроме, активный пункт
`#3c3836`.
**Как.** `SettingsPage` подтверждён; `data-settings-section-nav` —
значение равно ключу секции, активный пункт:
`[data-settings-section-nav][aria-current="page"]`;
`data-settings-panel-frame`; testid-литералы `settings-page`,
`settings-toolbar`, `settings-root`, `settings-dialog`.

### 6.10. Строки настроек (пара 82)
**Что.** Label `#ebdbb2`, описание `#928374`, разделители `#3c3836`;
контролы — 1.8; карточки групп — `#282828` + рамка.
**Как.** Строки собирать из слотов `input`/`switch`/`checkbox`/
`select-trigger` + токены card/border/foreground; тестовые зацепки —
`settings-toolbar`.

### 6.11. Выбор темы (пара 83)
**Что.** Превью-карточки: рамка `#3c3836`, выбранная — brand-рамка `#fe8019`,
подпись `#bdae93`.
**Как.** `[data-slot="card"]` жив; selected-класс/атрибут снять с
живого DOM настроек на приёмке (гипотеза остаётся).
**Закрыто записью-ограничением (2026-10-29, живой осмотр Appearance).**
Поверхности «превью-карточек» в 3.17.1 нет: выбор темы — select-trigger
(«Dark») внутри групповой карточки App theme, подсветка кода — вторая
карточка Light code theme. Рамки карточек уже на `--color-card-border`
(#3c3836 замерено), селектор темизирован 1.8 (#1d2021/#504945),
подписи — foreground-пары. Brand-рамки выбранной в UI нет — нечего
красить; если апстрим вернёт превью-карточки, завести задачу заново.

### 6.12. Плагины (пара 84)
**Что.** Карточки `#282828`/рамка `#3c3836`, платный бейдж —
`plugin-paid-plan-badge` (1.1), статус установки — success.
**Как.** Классы `PluginStore`/`PluginStoreOrder` подтверждены; testid
`plugin-store-sidebar-open` (новый в 3.17.1); `[data-slot="badge"]`;
бейдж-токены живы.

### 6.13. Hooks (пара 85)
**Что.** Строки как 6.10, форма — 1.8, код hook — mono `#ebdbb2` на `#1d2021`.
**Как.** Хуки — `hooks-settings-section`, `hooks-form` (замены вместо
имён клона).

### 6.14. MCP (пара 86)
`McpServerList`.
**Что.** Статус-точка: success/warning/error; строка сервера — как 6.10;
ошибка — destructive-surface.
**Как.** `McpServerList` подтверждён; точку красить статусными токенами;
хуки: `mcp-status`, `mcp-server-row`, `mcp-settings`,
`mcp-settings-refresh`, `mcp-open-authorization-button`;
`--color-destructive-surface` жив.

### 6.15. Субагенты (пара 87)
**Что.** Реестр как 6.3; поле reasoning — select по 1.8.
**Как.** `subagent-directory`/`subagent-row` (см. 6.3);
`subagent-built-in-model-trigger`; reasoning — select по 1.8
(`select-trigger`).

### 6.16. Горячие клавиши (пара 88)
**Что.** Kbd по 1.10, строки как 6.10, поиск — find-токены.
**Как.** Kbd по 1.10 (`[data-slot="kbd"]`), строки/поиск — по 6.10 и
find-токенам; поверхность снять с живого DOM настроек.

### 6.17. Статистика использования (пара 89)
`UsageHeatmap`.
**Что.** Heatmap и графики — ramp `usage-heatmap`/`usage-chart`; карточки —
`#282828`; подписи `#928374`.
**Как.** Класс `UsageHeatmap` подтверждён; хуки `usage-stats`,
`coding-plan-usage-trends`; heatmap/chart-токены без изменений (форма
color-mix → srgb, значения те же). В 6.17 входят только токены ramp,
карточки и подписи; перекраска SVG-графиков — отдельная задача 7.1,
сюда не входит.

### 6.18. Фидбек (пара 90)
**Что.** Формы — 1.8, статусы тикетов — status-цвета, фон базы.
**Как.** Литералы `feedback-*` в бандле — только логи телеметрии,
`ticket-*` — иконки lucide; поверхность собирать с живого DOM; формы
1.8, статусы — status-пары из 1.1.

### 6.19. Онбординг (пара 92)
`OnboardingDialog`.
**Что.** Как 1.9: шаги, карточки, кнопка brand.
**Как.** `OnboardingDialog` подтверждён; хуки `onboarding-dialog`,
`onboarding-page`, `onboarding-wizard-cancel`,
`onboarding-migration-dialog`; шаги по 1.9 +
`[data-slot="dialog-content"]`.

### 6.20. Вход (пара 93)
**Что.** Фон базы, поля 1.8, кнопка brand, ошибка — destructive.
**Как.** Семья `login-*`: `login-trigger`, `login-menu-item`,
`login-api-key-input`, `login-api-key-continue-button`,
`login-api-key-cancel-button`, `login-api-key-skip-button`,
`login-api-key-error`, `login-api-key-provider` (12 литералов);
поля 1.8, ошибка — destructive-пара.

### 6.21. Служебные токены вне join
**Пара** — нет: токены, которым не нашлось пары в join-таблице.
**Что.** Убрать стоковые цвета с поверхностей, которые 1.1 не покрыла:
`--color-highspeed-*` (тёмная: фон композера `#151515`, акцент
`#b392ff`; с 3.17.1 у светлой схемы собственные значения — акцент
`#9e77ed`, поверхность `#fff` — в 3.16.2 их не было),
`--color-primary`/`-foreground` (`#fff`/`#000` — первичные кнопки),
`--color-destructive-foreground` (`#fff`), remote-поверхности
(`#4099ff`/`#9f84ff`/`#46bf72`) + новое с 3.17.1 семейство
`--color-remote-continuity-panel{-foreground,-subtle,-surface}`
(`#202124`/`#f8f8f8`/`#a7a7ad`/`#2c2d30`), палитры узлов графа
(`file #70aee0`, `session #68c4bc`, `skill #a689da`, `plugin #e0ae70`).
**Как.** Переопределить токены в блоках 1.1: highspeed — база и акцент
gruvbox в обеих схемах, primary — brand с inverse-текстом, remote и
continuity — приглушённые пары (целевые значения зафиксировать при
исполнении; текст на этих поверхностях ≥ 4,5:1 от фактического фона),
узлы — ramp trajectory (сверить с 6.7). Критерий завершения: каждый
перечисленный токен резолвится в gruvbox-значение в обеих схемах
(getComputedStyle), поверхности с текстом проходят контраст.
`--color-user-message-bubble` (новый в 3.17.1) не брать: класс
на разметке не встречается — заготовка апстрима; если появится живая
поверхность — завести задачу отдельно. Снять живые highspeed-,
remote- и continuity-поверхности; если highspeed остаётся стоком —
внести отказ в 00-common.
