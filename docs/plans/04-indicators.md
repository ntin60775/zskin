# План 4. Живые индикаторы

Шаг 4 — движение. Зависит от шага 1 (status-токены).

Ссылки: [общее](00-common.md) · [образец стиля](../oh-my-pi-output-style.md) · [join-таблица](../components-join.md).

### 4.1. Shimmer (пара 3)
`Shimmer`, `ChatLoading`, `MagicKeywordSpec`.
**Что.** Бегунок `kitt`: полоса от `#7c6f64` через `#928374` к `#fe8019`
(bold на кресте), скорость 30 клеток/с, хвост 7 — без «пульсации» яркости.
**Как.** `[data-zcode-chat-loading-animate]`, классы shimmer; `background:
linear-gradient(...)`, `background-clip: text`, `animation` с шагом ≈ 33ms;
цвета — токены dim/muted/brand.

### 4.2. Спиннер и загрузка (пара 4)
`Spinner`, `Loader`, `CancellableLoader`.
**Что.** Глиф brand, без glow; idle — `#928374`; успех/ошибка — status.
**Как.** `.animate-spin` (есть) — убрать `filter: drop-shadow`; добавить
статусные варианты.

### 4.3. Прогресс (пара 5)
`Progress`, `ProgressBar`.
**Что.** Дорожка `#32302f`, заполнение brand (или success для завершённого),
высота 4px, радиус 2px.
**Как.** `[data-slot="progress"]`; `--color-progress-surface*` (1.1);
убрать возможный градиент — плоская заливка.

### 4.4. Метрика (пара 6)
`FlipMetricValue`, `SmoothMetricValue`, `MetricRow`.
**Что.** Число — mono `#ebdbb2`, единица/подпись — `#928374`; анимация
смены без перелива цветов.
**Как.** Классы метрик; токены foreground.
