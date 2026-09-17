# Core Examples — copy the pattern, adapt the model

All 6 follow the embed contract: single paste block, Shadow DOM, idempotent,
params as attributes, vanilla only, static fallback inside the tag.
Read this file only when building — SKILL.md stays lean.

---

## 1. Slider-parameter (L2 default)

One slider = one model variable. For formulas, interest, spread, thresholds.
Show the number *on* the visual, not beside it.

```html
<explorable-growth rate="7">
  <p>At 7%, $1000 doubles in ~10 years.</p>
</explorable-growth>
<script>
(() => {
  if (customElements.get('explorable-growth')) return;
  customElements.define('explorable-growth', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content;font:inherit}
        .wrap{border:1px solid #ddd;border-radius:12px;padding:12px}
        svg{width:100%;height:120px;display:block}
        output{font-weight:700}</style>
        <div class="wrap"><label>Rate <input type="range" min="1" max="15" value="7"> <output>7%</output></label>
        <svg viewBox="0 0 200 120"><path fill="none" stroke="currentColor" stroke-width="2"/></svg></div>`;
      const input = root.querySelector('input'), out = root.querySelector('output'), path = root.querySelector('path');
      const draw = () => {
        const r = +input.value; out.textContent = r + '%';
        let d = ''; for (let x = 0; x <= 200; x += 4) { const y = 110 - (x / 200) * 100 * (r / 15); d += (x ? 'L' : 'M') + x + ',' + y.toFixed(1) + ' '; }
        path.setAttribute('d', d);
      };
      input.addEventListener('input', draw); draw();
    }
  });
})();
</script>
```

## 2. Drag-direct (L2)

Grab the thing itself. For geometry, vectors, balance, segregation dots.
Hit-target >=44px, `touch-action:none`.

```html
<explorable-drag>
  <p>Drag the dot: angle and radius update live.</p>
</explorable-drag>
<script>
(() => {
  if (customElements.get('explorable-drag')) return;
  customElements.define('explorable-drag', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content}
        svg{width:100%;height:160px;touch-action:none;border:1px solid #ddd;border-radius:12px}
        circle{cursor:grab}</style>
        <svg viewBox="0 0 200 160"><line x1="100" y1="80" x2="150" y2="80" stroke="currentColor"/><circle cx="150" cy="80" r="14" fill="currentColor"/><text x="8" y="20"></text></svg>`;
      const svg = root.querySelector('svg'), c = root.querySelector('circle'), line = root.querySelector('line'), t = root.querySelector('text');
      const move = (e) => {
        const p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY;
        const q = p.matrixTransform(svg.getScreenCTM().inverse());
        c.setAttribute('cx', q.x.toFixed(0)); c.setAttribute('cy', q.y.toFixed(0));
        line.setAttribute('x2', q.x); line.setAttribute('y2', q.y);
        t.textContent = `(${q.x.toFixed(0)}, ${q.y.toFixed(0)})`;
      };
      c.addEventListener('pointerdown', (e) => { c.setPointerCapture(e.pointerId); const mv = (ev) => move(ev); c.addEventListener('pointermove', mv); c.addEventListener('pointerup', () => c.removeEventListener('pointermove', mv), { once: true }); });
    }
  });
})();
</script>
```

## 3. Stepper / scrubber (L1 -> L2)

Walk time or algorithm steps. For sorting, orbits, waves, epidemics.
Always show `t = k/N` so prose can reference exact states.

```html
<explorable-steps n="20" t="5">
  <p>Step 5 of 20: the wave is halfway across.</p>
</explorable-steps>
<script>
(() => {
  if (customElements.get('explorable-steps')) return;
  customElements.define('explorable-steps', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const N = +this.getAttribute('n') || 20; let t = +this.getAttribute('t') || 0;
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content}
        .wrap{border:1px solid #ddd;border-radius:12px;padding:12px}
        svg{width:100%;height:80px;display:block}</style>
        <div class="wrap"><label>Step <input type="range" min="0" max="${N}" value="${t}"> <output></output></label>
        <button>Play</button><svg viewBox="0 0 200 80"><circle r="8" fill="currentColor"/></svg></div>`;
      const input = root.querySelector('input'), out = root.querySelector('output'), dot = root.querySelector('circle'), btn = root.querySelector('button');
      const draw = () => { out.textContent = `t = ${input.value}/${N}`; dot.setAttribute('cx', 10 + (180 * input.value / N)); dot.setAttribute('cy', 40 - 25 * Math.sin(input.value / 2)); };
      input.addEventListener('input', draw); draw();
      btn.onclick = () => { const id = setInterval(() => { input.value = +input.value + 1; if (+input.value >= N) clearInterval(id); draw(); }, 120); };
    }
  });
})();
</script>
```

## 4. Predict-reveal check (L3 atom)

Smallest quest: commit to a prediction, then reveal truth. One question per widget.

```html
<explorable-predict answer="7">
  <p>At 7% how long to double? Guess first, then check.</p>
</explorable-predict>
<script>
(() => {
  if (customElements.get('explorable-predict')) return;
  customElements.define('explorable-predict', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const ans = +this.getAttribute('answer') || 7;
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content}
        .wrap{border:1px solid #ddd;border-radius:12px;padding:12px}
        .ok{color:green;font-weight:700}.no{color:#b00;font-weight:700}</style>
        <div class="wrap"><label>Your guess (years): <input type="number" min="1" max="30" value="5"></label>
        <button>Check</button> <span></span></div>`;
      const inp = root.querySelector('input'), msg = root.querySelector('span');
      root.querySelector('button').onclick = () => {
        const g = +inp.value, truth = Math.round(72 / ans);
        msg.className = g === truth ? 'ok' : 'no';
        msg.textContent = g === truth ? `Yes — ${truth}y (rule of 72).` : `Not quite — truth is ${truth}y. Try ${g < truth ? 'higher' : 'lower'}.`;
      };
    }
  });
})();
</script>
```

## 5. Sandbox playbox (L2 -> L3 closer)

Free play with guardrails off + edge-case presets. The closer after a guided bit.

```html
<explorable-sandbox rate="7">
  <p>Break it: try 0, 15, then reset.</p>
</explorable-sandbox>
<script>
(() => {
  if (customElements.get('explorable-sandbox')) return;
  customElements.define('explorable-sandbox', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content}
        .wrap{border:1px solid #ddd;border-radius:12px;padding:12px}</style>
        <div class="wrap"><label>Rate <input type="range" min="0" max="15" value="7"> <output></output></label>
        <div><button data-v="0">0</button> <button data-v="15">15</button> <button data-v="7">Reset</button></div>
        <div class="msg"></div></div>`;
      const input = root.querySelector('input'), out = root.querySelector('output'), msg = root.querySelector('.msg');
      const draw = () => { out.textContent = input.value + '%'; msg.textContent = input.value == 0 ? 'Nothing grows. That IS the lesson.' : input.value == 15 ? 'Explosive — now check the early years.' : ''; };
      input.addEventListener('input', draw); draw();
      root.querySelectorAll('button').forEach(b => b.onclick = () => { input.value = b.dataset.v; draw(); });
    }
  });
})();
</script>
```

## 6. Prose-linked mini (L1 glue)

Terms in the sentence highlight matching parts of the visual. Max one per section.
Falls back to a readable sentence with JS off.

```html
<explorable-linked>
  <p>Hover <b>principal</b> vs <b>interest</b> to see which bar is which.</p>
</explorable-linked>
<script>
(() => {
  if (customElements.get('explorable-linked')) return;
  customElements.define('explorable-linked', class extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    connectedCallback() {
      const root = this.shadowRoot;
      root.innerHTML = `<style>:host{display:block;contain:content}
        span{cursor:pointer;text-decoration:underline dotted}
        rect{transition:opacity .15s} .dim{opacity:.25}</style>
        <div><span data-hl="p">principal</span> + <span data-hl="i">interest</span>
        <svg viewBox="0 0 200 60"><rect id="p" x="10" y="10" width="100" height="20" fill="currentColor"/><rect id="i" x="10" y="35" width="60" height="20" fill="currentColor" opacity=".55"/></svg></div>`;
      root.querySelectorAll('span').forEach(s => {
        s.onmouseenter = () => root.querySelectorAll('rect').forEach(r => r.classList.toggle('dim', r.id !== s.dataset.hl));
        s.onmouseleave = () => root.querySelectorAll('rect').forEach(r => r.classList.remove('dim'));
      });
    }
  });
})();
</script>
```
