// T036: Shared export helper — PNG via SVG → canvas, plus a JSON caption.

export function exportSvgPng(svgEl, filename, caption) {
  const xml = new XMLSerializer().serializeToString(svgEl);
  const svg64 = btoa(unescape(encodeURIComponent(xml)));
  const img = new Image();
  img.onload = () => {
    const w = svgEl.viewBox.baseVal.width || svgEl.clientWidth || 800;
    const h = svgEl.viewBox.baseVal.height || svgEl.clientHeight || 500;
    const canvas = document.createElement('canvas');
    canvas.width = w * 2;
    canvas.height = h * 2;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#fbfbf8';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.scale(2, 2);
    ctx.drawImage(img, 0, 0, w, h);
    canvas.toBlob(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename + '.png';
      document.body.appendChild(a); a.click(); a.remove();
      URL.revokeObjectURL(url);
    });
  };
  img.src = 'data:image/svg+xml;base64,' + svg64;

  if (caption) {
    const blob = new Blob([JSON.stringify(caption, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = filename + '.caption.json';
    document.body.appendChild(a); a.click(); a.remove();
    URL.revokeObjectURL(url);
  }
}

export function exportSvgFile(svgEl, filename) {
  const xml = new XMLSerializer().serializeToString(svgEl);
  const blob = new Blob([xml], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename + '.svg';
  document.body.appendChild(a); a.click(); a.remove();
  URL.revokeObjectURL(url);
}
