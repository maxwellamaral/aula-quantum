/**
 * mindmap.js
 * Renderiza um mapa mental interativo (Markmap) dentro de qualquer
 * <div class="mindmap" data-src="caminho/para/mapa.md"> encontrado na página.
 *
 * Depende dos scripts globais carregados via CDN (ver mindmap-embed.qmd):
 *   - d3
 *   - markmap-view   -> expõe window.markmap.{Markmap, ...}
 *   - markmap-lib    -> expõe window.markmap.{Transformer, ...}
 *
 * Uso no .qmd (via partial mindmap-embed.qmd):
 *   <div class="mindmap" data-src="mapa.md" data-expand-level="1">
 *     <svg></svg>
 *   </div>
 */
(function () {
    async function renderMindmap(container) {
        const svg = container.querySelector("svg");
        const src = container.dataset.src || "mapa.md";
        const expandLevel = parseInt(container.dataset.expandLevel || "1", 10);

        let markdown;
        try {
            const res = await fetch(src);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            markdown = await res.text();
        } catch (err) {
            container.innerHTML = `<p style="color:#fc8181;">
        Não foi possível carregar o mapa mental (${src}): ${err.message}
      </p>`;
            return;
        }

        const missing = [];
        if (typeof window.d3 === "undefined") missing.push("d3");
        if (!window.markmap || !window.markmap.Markmap) missing.push("markmap-view");
        if (!window.markmap || !window.markmap.Transformer) missing.push("markmap-lib");

        if (missing.length) {
            container.innerHTML = `<p style="color:#fc8181;">
        Não carregou: ${missing.join(", ")}. Verifique as URLs dos
        &lt;script&gt; no mindmap-embed.qmd (abra o DevTools → Network para
        ver qual arquivo deu 404).
      </p>`;
            return;
        }

        const { Transformer, Markmap } = window.markmap;
        const transformer = new Transformer();
        const { root } = transformer.transform(markdown);

        const mm = Markmap.create(
            svg,
            {
                duration: 400,
                maxWidth: 320,
                initialExpandLevel: expandLevel,
                zoom: true,
                pan: true,
                // paleta de cores vibrantes por profundidade, para máxima nitidez no tema escuro
                color: (node) => {
                    const palette = ["#38bdf8", "#34d399", "#fbbf24", "#f472b6", "#a78bfa"];
                    return palette[node.state.depth % palette.length];
                },
            },
            root
        );

        // Abre os links de conteúdo em nova aba, mantendo o mapa mental aberto
        container.querySelectorAll("a").forEach((a) => {
            a.target = "_blank";
            a.rel = "noopener";
        });

        const fitMap = () => {
            if (container.offsetWidth > 0 && container.offsetHeight > 0) {
                requestAnimationFrame(() => mm.fit());
            }
        };

        fitMap();
        window.addEventListener("resize", fitMap);

        // Suporte para Reveal.js (slides) e observação de alteração de tamanho/visibilidade
        if (typeof window.Reveal !== "undefined" && window.Reveal.on) {
            window.Reveal.on("slidechanged", fitMap);
            window.Reveal.on("ready", fitMap);
        }

        if (window.ResizeObserver) {
            const ro = new ResizeObserver(() => fitMap());
            ro.observe(container);
        }

        if (window.IntersectionObserver) {
            const io = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) fitMap();
                });
            });
            io.observe(container);
        }
    }

    function init() {
        document.querySelectorAll(".mindmap").forEach(renderMindmap);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();