# План 7. Визуализации

Шаг 7 — графики. Последним: требует живой инспекции SVG.

Разведка 3.17.1 (2026-10-30, grep `app.asar` + живой осмотр секции
usage настроек, клиент под лоадером). Библиотека — **recharts**
(+d3-scale внутри; классы `recharts-surface`, `recharts-cartesian-grid`,
`recharts-cartesian-axis-tick-value`, `recharts-line-curve`). Имена
клона 3.14.3 из join-пары — `renderChartSvg`, `TableChartFigure` — в
бандле отсутствуют; живы `CodingPlanUsageBarChart`,
`AppUsageDailyModelTrendChart`, `UsageHeatmap` (литералы по 4/4/1).

**Серии и heatmap уже красятся токенами 1.1 — код не нужен.** Серии
графиков собираются массивом инлайновых ссылок
`` `var(--color-usage-chart-1)` `` … `` `var(--color-usage-chart-6)` ``
(живой контекст: `S=[`var(--color-usage-chart-1)`,…]` у LineChart и
тренд-чартов). Heatmap-клетки — инлайн
`background-color: var(--color-usage-heatmap-N)` (в живой сессии видны
пустые дни `-0`). Оба семейства токенов перекрашены в 1.1, резолв в
обеих схемах подтверждён.

**Реальный остаток — сетка и оси.** Recharts инлайнит константы
библиотеки в presentational-атрибуты: линии сетки `stroke="#ccc"`,
подписи осей `fill="#666"` (замерено живьём). Атрибуты бьются обычным
CSS без `!important`:

```css
[data-settings-panel-frame] .recharts-cartesian-grid line {
  stroke: var(--color-border);
}

[data-settings-panel-frame] .recharts-cartesian-axis-tick-value {
  fill: var(--color-foreground-subtle);
}
```

План требовал подписи `#928374` — заменено на subtle-пару по
контрастной дисциплине: `#928374` в светлой схеме на креме даёт 3,1:1
(та же ловушка волны 2); subtle даёт dark #bdae93 ≈ 7:1 и light
#665c54 = 4,75:1. Скоуп на панель настроек: других recharts-поверхностей
в текущем виде не видно (2 recharts-surface в живой секции usage).

**Per-model линии.** Тренд-линии несут атрибут
`stroke="var(--color-model0)"` — динамическую переменную по индексу
модели; в статике она не определена (ни CSS, ни инлайн держателя при
замере), computed stroke при живой секции дал палитровое значение
#83a598 (= usage-chart-1). Механизм раскраски по моделям сверить на
приёмке с живыми данными; если какие-то серии уйдут от палитры —
завести отдельную правку, не молча.

**Несмонтированные в живой сессии** (приёмка — с живыми данными):
бары `CodingPlanUsageBarChart` (нужен активный coding plan), легенда и
tooltip recharts, наполненная heatmap. Секция usage открывается
синтетическим ctrl+, (протокол шага 6: настройки синтетикой не
закрываются — закрывать руками).

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 7.1. Графики (пара 94)
`Chart`, `UsageHeatmap`, `CodingPlanUsageBarChart` (замены: recharts,
`AppUsageDailyModelTrendChart`, per-model тренд-линии).
**Что.** Серии — ramp `usage-chart-1…6`, сетка/оси `#3c3836`, подписи
subtle-пара, фон прозрачный.
**Как.** Серии и heatmap — токены 1.1, уже применяются (инлайновые
var()-ссылки, резолв подтверждён). Добавить два правила сетки и осей
из блока выше. Приёмка: computed stroke сетки = #3c3836, fill тиков =
subtle в обеих схемах, серии/heatmap резолвятся, light-подмена
стабильна; несмонтированные поверхности — с живыми данными или
записью-ограничением.
