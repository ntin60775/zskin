# Спека темы zskin: gruvbox-dark (omp-вариант)

Зафиксировано 2026-10-05 по ответам пользователя. Реализация —
[themes/gruvbox.css](../themes/gruvbox.css). Селекторы-гипотезы проверять
в живом клиенте (принцип 3).

## Решения

1. **Палитра — omp-вариант**: builtin-тема `dark-gruvbox` из oh-my-pi
   (стандартный Gruvbox Dark Medium), не kitty-soft.
2. **Акцент — оранжевый** `#fe8019` (`accent` из omp-темы); зелёный
   `#b8bb26` — успех/git/ссылки.
3. **Шрифты — mono везде**, включая прозу чата:
   `"JetBrainsMono Nerd Font Mono"` (в системе есть только она; чистого
   JetBrains Mono нет). Переопределяются токены `--font-sans`/`--font-mono`.
4. **Размер — 17px**: kitty 13.0pt ≈ 17.3px; совпадает с максимумом
   степпера dsh ui-theme (12–17px). Токен `--ui-font-size`.
5. **Палитра на всю зону чата**, не только терминал: фон, панели, карточки,
   композер, popover'ы, роли траектории, git, usage-графики, терминал.

## Источники

- `~/.config/kitty/kitty.conf` — шрифт/кегль/курсор; палитра kitty
  (gruvbox soft) **не используется**, кроме проверки соответствия.
- `~/.omp/agent/config.yml` — `symbolPreset: nerd`, `composer.shape: rule`,
  `display.shimmer: kitt`, статус-лайн powerline.
- oh-my-pi `packages/tui/src/theme/defaults/dark-gruvbox.json` (и
  `light-gruvbox.json` для светлого покрытия) — канонические значения.
- dsh-плагин `@deepseek-ai/dsh-client-ui-theme`
  (`~/home/dev/personal/deepseek-harness/packages/client/ui-theme`) — уроки:
  минимальный семантический alias-слой; **тема обязана покрывать обе схемы**
  (light+dark), чтобы переключение не ломало читаемость; тема = id +
  colorScheme + переопределения токенов. Скриншот `dsh-ui-shots/05-hero-skin.png`
  — целевая эстетика (тёплый тёмный фон, оранжевые акценты, mono во всём UI).
- Имена токенов ZCode: `docs/ui-tokens-3.14.3.txt` (скоуп `.theme-zai-dark`).

## Семантическая палитра (переменные gruvbox)

| Роль | Значение |
|---|---|
| bg0 / основной фон | `#282828` |
| bg1 / поднятая поверхность | `#3c3836` |
| bg2 / граница | `#504945` |
| bg3 / сильная граница | `#665c54` |
| chrome / «тёмный хром» | `#1d2021` |
| pending-поверхность | `#32302f` |
| fg1 / основной текст | `#ebdbb2` |
| fg3 / приглушённый | `#bdae93` |
| gray / второстепенный | `#928374` |
| accent | `#fe8019` оранжевый |
| success / warning / error | `#b8bb26` / `#fabd2f` / `#fb4934` |
| blue / purple / aqua | `#83a598` / `#d3869b` / `#8ec07c` |

## Маппинг на токены ZCode (тёмная схема)

- Фон/панели: `background` #282828; `background-win-alt`, `header`,
  `sidebar`, `tab`, `input`, `popover`, `tooltip` → #1d2021 (хром);
  `background-alt`, `hover`, `surface` → #32302f; `card`, `panel` → #282828.
- Текст: `foreground` #ebdbb2; `foreground-subtle` #bdae93;
  `foreground-subtlest` #928374; `foreground-inverse` #1d2021.
- Границы: `border`, `card-border` #3c3836; `border-hover`,
  `popover-border`, `input-border` #504945; фокус ввода — акцент #fe8019.
- Выделение: `selected`, `card-selected` #3c3836; hover #32302f.
- Бренд: `brand` #fe8019; `accent` #3c2f1c (тёплый тинт).
- Роли траектории: user #83a598, assistant #b8bb26, reasoning #928374,
  tool-call #fabd2f, tool-result #8ec07c.
- Git: modified #fe8019, added/untracked #b8bb26, deleted #fb4934,
  renamed #83a598.
- Markdown: inline-код — фон #3c3836, текст #d3869b (mdCode из omp);
  ссылки #8ec07c.
- Поиск: `find-highlight` #504324 (тёплый тинт), active #fabd2f.
- Usage/контекст: шкалы из gruvbox-акцентов (синий→аква→зелёный→жёлтый).
- Терминал: bg #282828, fg #ebdbb2, cursor #ebdbb2 + accent #fe8019,
  selection #504945; ANSI 16 — из `terminal.ansi` omp-темы
  (нейтральные 0–7 + яркие 8–15, включая фирменный `#da271f` для red).

## Светлая схема (минимальное покрытие)

По уроку dsh-плагина тема задаёт и light-значения (html.theme-zai-light),
чтобы переключение темы клиента не давало нечитаемых комбинаций: фон
#fbf1c7, поверхности #ebdbb2/#d5c4a1, текст #3c3836, акцент #d65d0e
(light-gruvbox.json из omp).

## Декор (отдельные гипотезы, включать после проверки базы)

- **Композер в силуэте `rule`** (как в omp): одна акцентная линия над
  полем ввода, без рамок по бокам.
- **Shimmer `kitt`** на индикаторах стриминга: keyframes-перенос
  `theme/shimmer.ts` (сканер-бегунок).
- Символы nerd — неприменимы к CSS (глифы меняет приложение, не тема);
  ZCode рисует свои иконки.

## Проверка

1. `python3 loader/zskin.py run --theme themes/gruvbox.css` (клиент должен
   быть закрыт) или сменить `THEME` в `loader/zskin-launcher.sh`.
2. Смотреть: фон/текст всей зоны чата, композер, диалоги, терминал,
   свето-тёмное переключение в настройках клиента.
3. После проверки — коммит (селекторы перестают быть гипотезами).
