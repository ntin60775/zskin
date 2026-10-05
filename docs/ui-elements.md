# Карта UI рендерера ZCode — что и как можно менять через zskin

Документ классифицирует UI-элементы главного окна клиента и описывает, что
именно в них можно изменить CSS-инжектом. Основа карты — исходники
официального репозитория, а не реверс бандла.

## Источник и доверие

- Официальное репо: `zai-org/ZCode` (github), клон:
  `/home/prog7/home/dev/contrib/clones/ZCode`, изучен тег `v3.14.3`.
- Установленный клиент — 3.14.4 (на минорную версию свежее). Проверка дрейфа:
  `theme-zai-dark`, `--color-brand`, `--color-sidebar`, `--color-terminal-bg`,
  `data-rail-position`, `prompt-mention`, `wf-pill` — все присутствуют в
  бандле 3.14.4. Карта актуальна, но при обновлении клиента её надо
  перегенерировать (раздел «Обновление карты»).
- Стек UI: React 19 + Tailwind CSS v4 + shadcn/ui + `tw-animate-css` +
  `@xterm/xterm`. Код UI: `packages/ui/src`, окно десктопа: `packages/desktop`.
- Селекторы остаются гипотезами в смысле принципа 3 AGENTS.md: DOM не
  публичный контракт. Токены (CSS-переменные) существенно стабильнее классов.

## Как устроена стилизация (главное)

1. **Дизайн-токены.** Почти вся палитра UI — CSS-переменные, определённые в
   `packages/ui/src/styles.css` в пяти скоупах:

   | Скоуп | Переменных | Роль |
   |---|---|---|
   | `:root` | 1 | `--ui-font-size: 14px` — базовый размер шрифта всего UI |
   | `@theme` | 153 | namespace Tailwind: палитры + семантические дефолты |
   | `.dark` | 140 | старая тёмная тема |
   | `.theme-zai-light` | 142 | светлая тема (активная по выбору «светлая») |
   | `.theme-zai-dark` | 142 | тёмная тема — **дефолт клиента** |

   Полный список со значениями: [ui-tokens-3.14.3.txt](ui-tokens-3.14.3.txt).

2. **Переключение тем.** `useTheme.ts` вешает на `<html>` классы `dark`,
   `theme-zai-light` / `theme-zai-dark`; дефолт — `zai-dark`. Утилиты Tailwind
   (`bg-background`, `text-foreground`, `border-border`…) компилируются в
   `var(--color-*)` — то есть переопределение токена перекрашивает всё, что
   его использует, во всех состояниях.

3. **Механика инжекта.** zskin добавляет `<style id="zskin-style">` последним
   в `<head>`: при равной специфичности наши правила побеждают по порядку.
   Рекомендуемые формы записи:
   - универсально (обе темы): `:root { --color-brand: …; }` — специфичность
     (0,1,0), как у `.theme-zai-*`, но идём позже по документу;
   - в разрезе темы клиента: `html.theme-zai-dark { … }` / `html.dark { … }` —
     (0,1,1), гарантированно старше исходных скоупов;
   - точечно: `data-slot`-селекторы и классы, при упорстве — `!important`
     (у React inline-стилей приоритет выше любого CSS без `!important`).

4. **Стабильные хуки** (в порядке надёжности):
   - CSS-токены `--color-*` — самый стабильный слой;
   - `data-slot="…"` на всех shadcn-примитивах: `button`, `textarea`, `input`,
     `dialog-content/-header/-title/-close`, `popover-*`, `select-*`,
     `command-input/-item`, `tabs/-list/-trigger/-content`, `switch/-thumb`,
     `badge`, `kbd`, `tooltip*`, `scroll-area*`, `progress*`, `separator`,
     `accordion-*`, `input-group-control` и др.;
   - авторские классы из `styles.css`: `.wf-*` (граф workflow, ~50 шт.),
     `.prompt-mention`, `.terminal-xterm-shell`, `.browser-use-viewport`,
     `.side-pane-open-tab-shell`, `.task-search-result-highlight`,
     `.markdown-image-loading-shimmer`, `.animate-zcode-alarm-ring`;
   - data-атрибуты поведения: `data-rail-position`, `data-state`,
     `data-zcode-stream-animate`, `data-zcode-tool-stream-animate`,
     `data-zcode-chat-loading-animate`, `data-zcode-collapsible-animate-close`,
     `data-zcode-pptx-render-surface`, `data-eye-expression` (маскот).
   - хвостовые классы Tailwind (`.bg-neutral-900` и т.п.) — наименее
     стабильны: зависят от состава использованных утилит в конкретной версии.

## Классификация зон UI

Пути — относительно `packages/ui/src` в клоне. «Меняемо» — типовые
изменения; базовые свойства (цвет, фон, шрифт, рамка, радиус, тень,
отступы, прозрачность, видимость) подразумеваются везде.

### 1. Хром окна и титлбар
- `DesktopWindowFrame.tsx`, `DesktopTopOverlay.tsx`,
  `DesktopWindowControls.tsx`, `DesktopTopOverlayActionButton.tsx`.
- Верхняя оверлей-полоса поверх рабочей области: перетаскивание окна,
  кнопки управления окном (на Linux — часть UI, не ОС), глобальные кнопки
  действий. Инлайн-стили (padding под нативные контролы) — только
  `!important`.
- Меняемо: фон/блюр полосы, цвет и вид кнопок окна, высота, шрифт.
  Позицию/геометрию драг-зоны не трогать — сломает перетаскивание окна.

### 2. Каркас рабочей области (shell)
- `app-shell/WorkspaceShellLayout.tsx`: `WorkspaceHeader` (верхняя навигация),
  `WorkspaceSidebar` (слева), центральная колонка чата, справа
  `AnimatedSidePanePanel` (панель с табами).
- Боковые панели (`app-shell/`): чат по выделению (`SelectionSideChatPane`),
  терминал (`AnimatedTerminalPanel`, `TerminalSession`), встроенный браузер
  (`BackgroundBashOutputSidePane`, browser-use), план (`PlanDetailSidePane`),
  обзор табов (`SidePaneTabOverview`, класс `.side-pane-open-tab-shell`).
- Меняемо: цвет панелей/заголовков табов, разделители, скругления,
  индикация активного таба. Ширины панелей живут в JS-стейте (localStorage),
  CSS их не задаёт.

### 3. Сайдбар воркспейса
- `WorkspaceSidebar.tsx`, `WorkspaceSidebarCollapsedRail.tsx` (узкий рельс,
  хук `data-rail-position`), `WorkspacePurposeSection.tsx`,
  `workspace-file-tree/`, `workspace-grouped-tasks/`,
  `workspace-file-search/`, `git-branch-switcher/`.
- Меняемо: фон (`--color-sidebar`), выделение элемента (`--color-selected`,
  `--color-hover`), шрифт и размеры строк дерева, индикаторы бейджей,
  полосы прокрутки.

### 4. Чат-таймлайн (сообщения)
- `components/ai-elements/`: `conversation.tsx`, `message.tsx`,
  `reasoning.tsx`, `tool.tsx` + `ToolCallBlocks/`, `code-block.tsx`,
  `artifact.tsx`, `plan.tsx`, `confirmation.tsx` (подтверждения операций —
  **не скрывать и не маскировать**, принцип 2), `checkpoint.tsx`,
  `image.tsx`, `image-thumbnail-gallery.tsx`, `attachments.tsx`,
  `markdown-*` (blockquote/list/table/image), `mermaid-block.tsx`,
  `sources.tsx`, `suggestion.tsx`, `queue.tsx`, `task.tsx`, `persona.tsx`,
  `shimmer.tsx`, `chat-loading.tsx`.
- Цветовые токены ролей: `--color-trajectory-{user,assistant,reasoning,
  tool-call,tool-result}`; инлайн-код: `--color-markdown-inline-code`;
  подсветка поиска: `--color-find-highlight(-active)`.
- Меняемо: фон/края сообщений, цвет ролей и траекторий, оформление кода и
  цитат, бейджи, анимации стриминга (через `data-zcode-*-animate` или
  `animation: none`).

### 5. Композер (ввод)
- `components/ai-elements/prompt-input*.tsx` (`data-slot="textarea"` и
  соседние), `prompt-editor/` (`ChatPromptEditor`, упоминания
  `.prompt-mention`), `chat-input-toolbar/` (модель, контекст, квоты
  `--color-usage*`, `--color-context-breakdown*`).
- Меняемо: фон и рамка поля (`--color-input*`), тулбар, кнопки, метры
  квот, подсказки. Скрытие индикаторов квот/подтверждений запрещено.

### 6. Терминал
- `terminal/` (`.terminal-xterm-shell`), рендер xterm.
- Канонический факт: `terminalTheme.ts` строит палитру xterm **чтением
  CSS-переменных** `--color-terminal-*` (22 шт.: `bg`, `fg`, `cursor`,
  `cursor-accent`, `selection`, `selection-inactive`, 16 ANSI-цветов).
  Значения прогоняются через resolve в валидный rgba — то есть терминал
  полностью перекрашивается токенами, как остальной UI.
- Ограничение: шрифт и метрики терминала задаются опциями xterm в JS —
  CSS-переопределение `font-family` у canvas-рендера может разъехаться с
  измерениями. Меняем только цвета через токены, прокрутку — как обычно.

### 7. Граф workflow и диаграммы
- `.wf-*` классы (`styles.css`, ~50): pills, рельсы, лампы, лицо-маскот
  (`.wf-face*`, `data-eye-expression`, `.wf-lamp*`), узлы
  (`--color-{subagent,skill,session,plugin}-node*`), линии
  (`--color-workflow-*`); компоненты `components/workflow-graph/`,
  `components/ai-elements/{node,edge,canvas}.tsx`, mermaid-блоки.
- Меняемо: цвета узлов/линий/статусов, анимации (`.wf-motion`, `@keyframes`),
  оформление превью. Маскот — декоративный, можно стилизовать.

### 8. Примитивы shadcn/ui (сквозные)
- `components/ui/`: `button`, `input`, `input-group`, `textarea`, `select`,
  `checkbox`, `switch`, `tabs`, `dialog`, `alert-dialog`, `dropdown-menu`,
  `context-menu`, `command` (палитра команд), `popover`, `hover-card`,
  `tooltip`, `toast`, `badge`, `avatar`, `card`, `progress`, `spinner`,
  `kbd`, `accordion`, `collapsible`, `separator`, `label`, `scroll-area`,
  `resizable`, `code-viewer`, `diff-viewer` (диффы!), `chart` (SVG —
  стилизуем), `pdf-viewer`, `pptx-preview-viewer`.
- Это слой, через который красятся все диалоги/меню/формы сразу:
  токены `--color-popover*`, `--color-card*`, `--color-input*` +
  `data-slot`-селекторы для точечных правок (радиусы кнопок, высоты
  строк меню, тени диалогов).

### 9. Прикладные диалоги и оверлеи
- Командная палитра: `command-center/CommandCenterDialog.tsx`; быстрый поиск:
  `quickpick/` (`TaskFindDialog`, `.task-search-result-highlight`);
  `ConfirmDialog`, `ElicitationDialog`, `AlertDialogHost`, `BotsDialog/`;
  фидбек: `feedback/` (`FeedbackCenter`, скриншот-пикер); настройки:
  `settings/` (автоматизации и пр.); логин/онбординг: `login/`, `onboarding/`;
  `DeveloperToolsPane.tsx`.
- Меняемо как обычные диалоги (фон, рамки, типографика). Кнопки и чекбоксы
  подтверждений опасных действий — только стиль, не поведение/видимость.

### 10. Git-инструменты
- `GitPane/`, `git-graph/`, `git-action-menu/`, токены `--color-git*`
  (8 шт.), `components/ui/diff-viewer.tsx`.
- Меняемо: цвета статусов файлов, граф, диффы (фоны добавлений/удалений
  внутри diff-viewer), шрифты кода.

### 11. Встроенный браузер и CUA
- Хром браузер-панели: `browser-use/`, `EmbeddedWebsiteHeader`,
  `.browser-use-viewport`, таб-иконки (`BrowserTabFavicon`,
  `BrowserUseTabIcon`); панель разрешений CUA: `cua-permission/`.
- Контент чужих сайтов внутри браузера — не наша территория (не темизируем).

### 12. Презентации и файловые вьюверы
- `presentation/`, `components/ui/pptx-*`, `data-zcode-pptx-render-surface`
  (отдельный скроллбар-стиль), `pdf-viewer`.
- Меняемо: рамки/фон/тулбары вьюверов. Отрендеренный контент pptx/pdf —
  как есть.

## Что именно можно менять (сводно по свойствам)

- **Цвета** — любой токен `--color-*` (фон, панели, границы, роли чата,
  терминал, git, графики usage) или точечно `color/background/border-color/
  box-shadow/gradient/opacity/backdrop-filter` селектором.
- **Типографика** — `--ui-font-size` (глобальный кегль), `font-family` на
  `body` (кроме терминала — см. ограничение), размеры/веса/трекинг
  селекторами.
- **Геометрия** — отступы, радиусы, тени, высоты строк; тонко: максимальная
  ширина композера и т.п. Ширины панелей сайдбара — не CSS (JS-стейт).
- **Скроллбары** — `::-webkit-scrollbar*` глобально или по зонам.
- **Выделение текста** — `::selection`.
- **Анимация** — отключение (`animation/transition: none`) или авторские
  хуки `data-zcode-*-animate`; мелкая живость маскота/графа — `.wf-*`.
- **Видимость** — только для заведомо декоративного. Нельзя скрывать:
  подтверждения операций (`confirmation`), квоты/метры, индикаторы записи.

## Ограничения

1. **Inline-стили React** сильнее любого CSS без `!important` (титлбар,
   панельки с вычисляемыми размерами).
2. **Canvas** (xterm-рендер, части графиков): красится только через токены,
   не через селекторы к «пикселям».
3. **Другие поверхности** — не главное окно, у них свои документы и свои
   CDP-таргеты: окно «Ресурсы» (`resource-manager.html`), панель разрешений
   CUA (`cua-permission-panel.html`), webview-вкладки (coding plan,
   rewards). Текущий лоадер инжектит только в первый page-таргет; на эти
   поверхности карту придётся расширять отдельно.
4. **Виртуализация/стриминг**: DOM пересоздаётся, но инжект — это CSS, он
   живёт независимо; повторный инжект нужен только после reload страницы.
5. **Дрейф версий**: классы и состав токенов меняются между релизами;
   после обновления клиента — перегенерировать карту (ниже).

## Скелет темы (стартовая точка)

```css
/* zskin: пример переопределения на уровне токенов */
:root {
  --ui-font-size: 14px;              /* глобальный кегль */
  --color-brand: #7aa2f7;            /* акцент везде */
}
html.theme-zai-dark, html.dark {
  --color-background: #1a1b26;
  --color-sidebar: #16161e;
  --color-terminal-bg: #1a1b26;
  --color-terminal-fg: #a9b1d6;
}
html.theme-zai-light {
  --color-brand: #2f6feb;
}
/* точечно, если токенов мало: */
[data-slot="button"] { border-radius: 8px; }
::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-thumb { background: var(--color-border-hover); }
```

Проверка — только в живом клиенте (ярлык «ZCode (zskin)» при закрытом
обычном клиенте): сначала пробная тема с `outline: 1px solid` на сомнительных
селекторах, потом чистовая.

## Обновление карты

1. `git -C /home/prog7/home/dev/contrib/clones/ZCode fetch --tags && git -C … checkout v<X.Y.Z>` (совпадает с версией установленного клиента).
2. Регенерация дампа токенов (в корне zskin):

   ```bash
   python3 - <<'EOF'
   import re, pathlib
   src = pathlib.Path("/home/prog7/home/dev/contrib/clones/ZCode/packages/ui/src/styles.css").read_text()
   out, cur, depth = [], None, 0
   for line in src.splitlines():
       m = re.match(r"^(:root|\.dark|\.theme-zai-light|\.theme-zai-dark|@theme)\s*\{", line)
       if m:
           cur, depth = m.group(1), line.count("{") - line.count("}")
           continue
       if cur is not None:
           depth += line.count("{") - line.count("}")
           if depth <= 0:
               cur = None
           else:
               d = re.match(r"^\s*(--[a-zA-Z0-9-]+)\s*:\s*(.+?);", line)
               if d:
                   out.append((cur, d.group(1), d.group(2)))
   with open("docs/ui-tokens-3.14.3.txt", "w") as f:
       for s in (":root", "@theme", ".dark", ".theme-zai-light", ".theme-zai-dark"):
           items = [(v, x) for sc, v, x in out if sc == s]
           f.write(f"\n=== {s}  ({len(items)} переменных)\n")
           f.writelines(f"{v}: {x}\n" for v, x in items)
   EOF
   ```

3. Сверить ключевые маркеры с бандлом установленного клиента
   (распаковка `app.asar` описана в истории; маркеры: `theme-zai-dark`,
   `--color-brand`, `--color-terminal-bg`, `data-rail-position`,
   `data-slot="button"`) и поправить разделы, где имена разошлись.
