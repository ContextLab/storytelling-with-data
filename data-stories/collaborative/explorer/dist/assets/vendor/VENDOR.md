# Vendored runtime libraries

These files are pinned, vendored copies so the runtime explorer never
makes network calls (FR-002).

| File | Source | Version | SHA-256 |
|-|-|-|-|
| `d3.v7.min.js` | https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js | 7.9.0 | `f2094bbf6141b359722c4fe454eb6c4b0f0e42cc10cc7af921fc158fceb86539` |
| `d3-sankey.v0.12.min.js` | https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js | 0.12.3 | `8286db5d6aa049cc6e8a546708943b79dfb4daaefb0ccf42af674ec0ee4c86be` |
| `tabulator.min.js` | https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.1/dist/js/tabulator.min.js | 6.3.1 | `e952272c3b2afa4ebb60cef5db8cbe9cbaabaa52b50c3cd3d22993ca5215a6ff` |
| `tabulator.min.css` | https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.1/dist/css/tabulator.min.css | 6.3.1 | `a46d8051944c745cae8a7976b4fb9d93d894d20876a4521cc4f6f035cfef52ea` |

## Re-fetching

```bash
cd dist/assets/vendor
curl -sSL -o d3.v7.min.js https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js
curl -sSL -o d3-sankey.v0.12.min.js https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js
curl -sSL -o tabulator.min.js https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.1/dist/js/tabulator.min.js
curl -sSL -o tabulator.min.css https://cdn.jsdelivr.net/npm/tabulator-tables@6.3.1/dist/css/tabulator.min.css
shasum -a 256 *.js *.css   # compare against table above
```

## Licenses

- D3 — ISC License, © Mike Bostock
- d3-sankey — ISC License, © Mike Bostock
- Tabulator — MIT License, © Oliver Folkerd

License texts ship with each library's npm package.
