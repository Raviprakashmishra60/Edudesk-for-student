/* Document Center - all tools run in the browser. Files are never uploaded to the server. */
const MAX_FILE_MB = 50;
const hasPdfLib = () => typeof window.PDFLib !== "undefined";

/* ---------- helpers ---------- */
const formatBytes = (bytes) =>
  bytes < 1024 * 1024
    ? `${(bytes / 1024).toFixed(1)} KB`
    : `${(bytes / 1024 / 1024).toFixed(2)} MB`;
const isPdf = (file) =>
  file.type === "application/pdf" || /\.pdf$/i.test(file.name);
const baseName = (name) => name.replace(/\.[^.]+$/, "");

function downloadLink(blob, filename, label) {
  const url = URL.createObjectURL(blob);
  return `<a class="btn btn-primary btn-sm" href="${url}" download="${esc(filename)}">⬇ ${esc(label || filename)}</a>`;
}
function showResult(id, html) {
  $(id).innerHTML = html;
}
function showProblem(id, message) {
  $(id).innerHTML = `<p class="form-error">${esc(message)}</p>`;
}
function checkFile(file, kind) {
  if (!file) throw new Error("Please choose a file first.");
  if (file.size > MAX_FILE_MB * 1024 * 1024)
    throw new Error(`File is too large (limit ${MAX_FILE_MB} MB).`);
  if (kind === "image" && !file.type.startsWith("image/"))
    throw new Error(`“${file.name}” is not an image.`);
  if (kind === "pdf" && !isPdf(file))
    throw new Error(`“${file.name}” is not a PDF.`);
}
function loadImage(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file),
      img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      resolve(img);
    };
    img.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error(`Could not read “${file.name}” as an image.`));
    };
    img.src = url;
  });
}
const toBlob = (canvas, type, quality) =>
  new Promise((resolve) => canvas.toBlob(resolve, type, quality));
function drawToCanvas(img, width, height, fillWhite) {
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (fillWhite) {
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, width, height);
  } // JPEG has no transparency
  ctx.drawImage(img, 0, 0, width, height);
  return canvas;
}
async function runTool(button, resultId, task) {
  setBusy(button, true, "Working…");
  try {
    await task();
  } catch (error) {
    showProblem(resultId, error.message || "Something went wrong.");
  } finally {
    setBusy(button, false);
  }
}
function needPdfLib(resultId) {
  if (hasPdfLib()) return true;
  $("#pdf-lib-warning").hidden = false;
  showProblem(
    resultId,
    "The PDF library did not load. Check your internet connection and reload the page.",
  );
  return false;
}

/* ---------- tabs ---------- */
$("#tool-tabs").addEventListener("click", (event) => {
  const chip = event.target.closest(".chip");
  if (!chip) return;
  $$("#tool-tabs .chip").forEach((c) =>
    c.classList.toggle("active", c === chip),
  );
  $$("[data-panel]").forEach((panel) => {
    panel.hidden = panel.dataset.panel !== chip.dataset.tool;
  });
});
$("#doc-help").href = whatsappUrl("preparing documents for my application");

/* ---------- 1. image resize + compress ---------- */
$("#img-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#img-result", async () => {
    const file = $("#img-file").files[0];
    checkFile(file, "image");
    const img = await loadImage(file);
    let width = parseInt($("#img-width").value, 10) || 0,
      height = parseInt($("#img-height").value, 10) || 0;
    const keep = $("#img-keep").checked,
      maxKb = parseInt($("#img-maxkb").value, 10) || 0;
    const format = $("#img-format").value,
      userSetSize = Boolean(width || height);
    if (width && height && keep)
      height = Math.round((width * img.naturalHeight) / img.naturalWidth);
    else if (width && !height)
      height = keep
        ? Math.round((width * img.naturalHeight) / img.naturalWidth)
        : img.naturalHeight;
    else if (height && !width)
      width = keep
        ? Math.round((height * img.naturalWidth) / img.naturalHeight)
        : img.naturalWidth;
    else if (!width && !height) {
      width = img.naturalWidth;
      height = img.naturalHeight;
    }
    if (width > 10000 || height > 10000)
      throw new Error("Maximum size is 10000 pixels.");

    let blob,
      note = "",
      scale = 1;
    for (let attempt = 0; attempt < 8; attempt++) {
      const w = Math.max(1, Math.round(width * scale)),
        h = Math.max(1, Math.round(height * scale));
      const canvas = drawToCanvas(img, w, h, format === "image/jpeg");
      if (format === "image/png" || !maxKb) {
        blob = await toBlob(canvas, format, 0.92);
        width = w;
        height = h;
        break;
      }
      let low = 0.1,
        high = 0.95,
        best = null; // search for the best JPEG quality under the limit
      for (let step = 0; step < 7; step++) {
        const mid = (low + high) / 2,
          candidate = await toBlob(canvas, format, mid);
        if (candidate.size <= maxKb * 1024) {
          best = candidate;
          low = mid;
        } else high = mid;
      }
      if (best) {
        blob = best;
        width = w;
        height = h;
        break;
      }
      if (userSetSize) {
        blob = await toBlob(canvas, format, 0.1);
        width = w;
        height = h;
        note = `Could not get under ${maxKb} KB at ${w}×${h}px. Try a larger limit or smaller width/height.`;
        break;
      }
      scale *= 0.85; // no fixed size requested, so shrink the picture a little and retry
      if (attempt === 7) {
        blob = await toBlob(canvas, format, 0.1);
        width = w;
        height = h;
        note = `Could not reach ${maxKb} KB. Try a larger limit.`;
      }
    }
    if (maxKb && format === "image/png")
      note =
        "PNG cannot be compressed to a target size here — choose JPEG for that.";
    const ext = format === "image/png" ? "png" : "jpg",
      url = URL.createObjectURL(blob);
    showResult(
      "#img-result",
      `<img src="${url}" alt="Processed image preview">
    <p class="result-line"><b>Before:</b> ${formatBytes(file.size)} (${img.naturalWidth}×${img.naturalHeight}px) → <b>After:</b> ${formatBytes(blob.size)} (${width}×${height}px)</p>
    ${note ? `<p class="notice warn">${esc(note)}</p>` : ""}${downloadLink(blob, `edudesk-${baseName(file.name)}.${ext}`)}`,
    );
  }),
);

/* ---------- 2. image to PDF ---------- */
$("#i2p-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#i2p-result", async () => {
    if (!needPdfLib("#i2p-result")) return;
    const files = [...$("#i2p-files").files];
    if (!files.length) throw new Error("Please choose at least one image.");
    const pdf = await PDFLib.PDFDocument.create();
    for (const file of files) {
      checkFile(file, "image");
      const img = await loadImage(file);
      const canvas = drawToCanvas(
        img,
        img.naturalWidth,
        img.naturalHeight,
        true,
      );
      const jpg = await pdf.embedJpg(
        await (await toBlob(canvas, "image/jpeg", 0.9)).arrayBuffer(),
      );
      const scale = Math.min(1, 595 / jpg.width); // keep pages about A4 width
      const page = pdf.addPage([jpg.width * scale, jpg.height * scale]);
      page.drawImage(jpg, {
        x: 0,
        y: 0,
        width: jpg.width * scale,
        height: jpg.height * scale,
      });
    }
    const blob = new Blob([await pdf.save()], { type: "application/pdf" });
    showResult(
      "#i2p-result",
      `<p class="result-line">Created a PDF with ${files.length} page${files.length === 1 ? "" : "s"} (${formatBytes(blob.size)}).</p>${downloadLink(blob, "edudesk-images.pdf")}`,
    );
  }),
);

/* ---------- 3. PDF merge ---------- */
async function openPdf(file) {
  try {
    return await PDFLib.PDFDocument.load(await file.arrayBuffer());
  } catch (error) {
    throw new Error(
      `Could not read “${file.name}”. It may be password-protected or damaged.`,
    );
  }
}
$("#merge-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#merge-result", async () => {
    if (!needPdfLib("#merge-result")) return;
    const files = [...$("#merge-files").files];
    if (files.length < 2)
      throw new Error("Please choose at least two PDF files.");
    const merged = await PDFLib.PDFDocument.create();
    for (const file of files) {
      checkFile(file, "pdf");
      const source = await openPdf(file);
      (await merged.copyPages(source, source.getPageIndices())).forEach(
        (page) => merged.addPage(page),
      );
    }
    const blob = new Blob([await merged.save()], { type: "application/pdf" });
    showResult(
      "#merge-result",
      `<p class="result-line">Merged ${files.length} files into ${merged.getPageCount()} pages (${formatBytes(blob.size)}).</p>${downloadLink(blob, "edudesk-merged.pdf")}`,
    );
  }),
);

/* ---------- 4. PDF split ---------- */
function parseRanges(text, pageCount) {
  const groups = text
    .split(",")
    .map((part) => part.trim())
    .filter(Boolean);
  if (!groups.length)
    throw new Error("Enter page ranges, for example 1-2, 3, 4-6.");
  return groups.map((group) => {
    const match = group.match(/^(\d+)(?:\s*-\s*(\d+))?$/);
    if (!match)
      throw new Error(
        `“${group}” is not a valid range. Use numbers like 3 or 2-5.`,
      );
    const start = Number(match[1]),
      end = Number(match[2] || match[1]);
    if (start < 1 || end < start || end > pageCount)
      throw new Error(
        `Range “${group}” is outside this PDF (it has ${pageCount} pages).`,
      );
    return { label: group, start, end };
  });
}
$("#split-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#split-result", async () => {
    if (!needPdfLib("#split-result")) return;
    const file = $("#split-file").files[0];
    checkFile(file, "pdf");
    const source = await openPdf(file);
    const ranges = parseRanges($("#split-ranges").value, source.getPageCount());
    const links = [];
    for (const range of ranges) {
      const part = await PDFLib.PDFDocument.create();
      const indices = Array.from(
        { length: range.end - range.start + 1 },
        (_, i) => range.start - 1 + i,
      );
      (await part.copyPages(source, indices)).forEach((page) =>
        part.addPage(page),
      );
      const blob = new Blob([await part.save()], { type: "application/pdf" });
      links.push(
        downloadLink(
          blob,
          `${baseName(file.name)}-pages-${range.label.replace(/\s+/g, "")}.pdf`,
          `Pages ${range.label} (${formatBytes(blob.size)})`,
        ),
      );
    }
    showResult(
      "#split-result",
      `<p class="result-line">Created ${links.length} PDF${links.length === 1 ? "" : "s"}:</p><div class="card-actions">${links.join("")}</div>`,
    );
  }),
);

/* ---------- 5. PDF compress ---------- */
$("#pc-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#pc-result", async () => {
    if (!needPdfLib("#pc-result")) return;
    const file = $("#pc-file").files[0];
    checkFile(file, "pdf");
    const doc = await openPdf(file);
    const blob = new Blob([await doc.save({ useObjectStreams: true })], {
      type: "application/pdf",
    });
    const saved = file.size - blob.size;
    showResult(
      "#pc-result",
      `<p class="result-line"><b>Before:</b> ${formatBytes(file.size)} → <b>After:</b> ${formatBytes(blob.size)}</p>
    ${saved > 0 ? `<p class="result-line">Saved ${formatBytes(saved)}.</p>` : '<p class="notice warn">This PDF could not be made smaller (it is probably mostly images). Reduce the images first with the Image tool, then use Image to PDF.</p>'}
    ${downloadLink(blob, `edudesk-${baseName(file.name)}-compressed.pdf`)}`,
    );
  }),
);

/* ---------- 6. file size checker ---------- */
$("#chk-run").addEventListener("click", (event) =>
  runTool(event.currentTarget, "#chk-result", async () => {
    const file = $("#chk-file").files[0];
    checkFile(file);
    const min = parseFloat($("#chk-min").value) || 0,
      max = parseFloat($("#chk-max").value) || 0;
    if (!min && !max)
      throw new Error("Enter a minimum and/or maximum size in KB.");
    const kb = file.size / 1024;
    const ok = kb >= min && (!max || kb <= max);
    let dims = "";
    if (file.type.startsWith("image/")) {
      try {
        const img = await loadImage(file);
        dims = ` · ${img.naturalWidth}×${img.naturalHeight}px`;
      } catch (error) {
        /* ignore */
      }
    }
    showResult(
      "#chk-result",
      `<div class="verdict ${ok ? "ok" : "no"}">${ok ? "✓ This file fits the limit." : kb < min ? "✗ File is smaller than the minimum." : "✗ File is larger than the maximum."}</div>
    <p class="result-line"><b>${esc(file.name)}</b> — ${kb.toFixed(1)} KB${dims} · Allowed: ${min ? min + " KB" : "any"} to ${max ? max + " KB" : "any"}</p>`,
    );
  }),
);
