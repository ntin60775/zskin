# План 1. Основа: поверхности, состояния, примитивы

Шаг 1 — фундамент: без него остальные планы не дают цельного вида.
Зависимостей нет. Общие правила и приёмка — в [общем файле](00-common.md).

Статус 2026-10-21: выполнен (коммиты `79d08ae`, `c6e7e87`, `f9177e7`,
`61ce655`, `531480b`, `b74dd4b`, `02398f6`). Токены 1.1 подтверждены CDP
в обеих схемах; настройки просмотрены вживую — артефактов нет.
Селекторы 1.2–1.10 сняты с бандла 3.16.2 и применятся при монтировании
поверхностей; точечных проверок тоста, alert и диалога не было.

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 1.1. Темы и цветовые роли (пара 1)
`html.theme-zai-dark/light`, `--color-*`.
**Что.** Полный семантический слой omp: база `#282828`/`#fbf1c7`, плашки
`#1d2021`/`#ebdbb2`, три плоскости яркости (текст ≥ 4,5:1, приглушённое
≈ 4,5:1, декор < 3,5:1), акцент `#fe8019`.
**Как.** Дописать в тему недостающие группы из дампа: `--color-diff-added*`,
`--color-diff-removed*`, `--color-progress-surface*`,
`--color-success/warning/destructive-surface(-foreground)`,
`--color-interaction-ask-surface`, `--color-interaction-confirmation-surface`,
`--color-menu-hover`, `--color-tab-border`, `--color-tooltip-foreground`,
`--color-tooltip-tag*`, `--color-git-ignored/descendant/none`,
`--color-idle-task*`, `--color-plugin-paid-plan-badge*`. Значения — из
`dark-gruvbox.json` и светлого близнеца; уже заданные не дублировать.

### 1.2. Уведомление (пара 7)
`Toast`, `AnchoredToastStack`, `StatusNotice`.
**Что.** Тост — поднятая поверхность `#1d2021`, рамка `#504945`, иконка
статуса в success/warning/error, текст `#ebdbb2`, вторичный — `#bdae93`.
**Как.** Токен `--color-toast` (задан в 1.1; бандл 3.16.2 красит им тост —
слота `toast` и sonner-атрибутов в бандле нет). Структурные правила
(радиус, тень, иконки) — только после живого тоста; кандидат
`[data-sonner-toast]` держится закомментированной гипотезой в теме.

### 1.3. Ошибка-баннер (пара 8)
`ChatErrorBanner`, `Alert`, `ErrorBoundary`.
**Что.** Аварийная плашка `#3c2021`, рамка/иконка `#fb4934`, заголовок
красный, тело `#ebdbb2`; не маскировать и не скрывать.
**Как.** Добавить `--color-destructive-surface/-foreground` (1.1);
`[data-slot="alert"]` — цвет фона и бордера из токенов.

### 1.4. Скролл (пара 9)
`ScrollArea`, `ScrollFadeViewport`.
**Что.** Тонкий thumb `#504945`, hover `#665c54`, прозрачный track; маска
затухания — фоном базы.
**Как.** Глобальные `::-webkit-scrollbar*` уже есть; добавить варианты для
`[data-slot="scroll-area-scrollbar"]`/`-thumb` — shadcn рисует собственный
скроллбар, глобального правила ему мало.

### 1.5. Разделители панелей (пара 10)
`Resizable`, `WorkbenchSplitDivider`.
**Что.** Линия 1px `#3c3836`, при наведении `#504945`; ручка без фона и
подсветки.
**Как.** `[data-slot="resizable-handle"]` — в бандле 3.16.2
resizable-слотов нет (сплиттер рабочей области кастомный), правило
живёт закомментированной гипотезой в теме; токены `--color-border`,
`--color-border-hover`.

### 1.6. Вкладки (пара 11)
`Tabs`, `SettingsSegmentedTabs`, `SidePaneTabTrigger`.
**Что.** Активный таб светлее хрома (`#282828` на `#1d2021`), неактивный —
`#bdae93`, hover — `#32302f`; лишний индикатор-подчёркивание убрать, если он
дублирует фон.
**Как.** `[data-slot="tabs-trigger"][data-state="active"]`; токены
`--color-tab`, `--color-tab-active`, `--color-tab-border` (последний — 1.1).

### 1.7. Диалог и оверлей (пара 15)
`Dialog`, `Popover`, `AlertDialog`, `OverlayPanel`.
**Что.** Панель `#1d2021`, рамка `#504945`, тень глубже стоковой, подложка
оверлея — затемнение базы (не чёрный).
**Как.** `[data-slot="dialog-content"]`, `dialog-overlay`,
`[data-slot="popover-content"]`; `--color-popover*`; `box-shadow` и
`backdrop-filter` на оверлее.

### 1.8. Поля формы (пара 16)
`Input`, `Textarea`, `Select`, `Switch`, `Checkbox`.
**Что.** Поле `#1d2021`, рамка `#504945`, hover `#665c54`, фокус `#fe8019`;
плейсхолдер `#928374`; switch/checkbox — brand в активном.
**Как.** `[data-slot="input"]`, `textarea`, `select-trigger`, `switch`,
`checkbox`; токены `--color-input-border*`, `--color-input-border-focused`
уже заданы.

### 1.9. Визард (пара 17)
`OnboardingWizardHeader/Footer/Sidebar`, `SetupWizardComponent`.
**Что.** Шаги: пройденный — `#b8bb26`, текущий — brand, будущий — `#928374`;
контент на `#282828`, навигация на хроме `#1d2021`.
**Как.** Хуков онбординга в бандле 3.16.2 нет — визард собирается из
диалоговых и формовых примитивов, поверхность закрывают 1.7/1.8; токены
surface и status. Маркеры шагов — после живой разведки.

### 1.10. Подсказка клавиши (пара 18)
`Kbd`, `ControlShortcutBadge`, `ShortcutBindingRow`.
**Что.** Капсула: фон `#32302f`, рамка `#504945`, текст `#bdae93`, mono,
радиус 4px; бейдж хоткея — та же капсула в компактном виде.
**Как.** `[data-slot="kbd"]`; `--color-surface`, `--color-border-hover`;
`ControlShortcutBadge` — класс компонента (гипотеза).
