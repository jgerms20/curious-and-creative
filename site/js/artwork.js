/* Runtime artwork loader.
   Fills every [data-art] slot with real show artwork by asking Spotify's
   public oEmbed endpoint from the visitor's browser. If the fetch fails
   (offline, CORS, ad-blockers), the branded fallback tile simply stays.
   To hard-code artwork instead, drop images into assets/art/<key>.jpg —
   local files win over the network fetch. */
(() => {
  const SHOWS = {
    tmtt: "https://open.spotify.com/show/033G4KctzeuD3Pu4db1AQa",
    abolitionist: "https://open.spotify.com/show/7natfWFnBgakjLLZcEDZaw",
    polymath: "https://open.spotify.com/show/3dlagzJ0jiWLTB9mF3y069",
    dominate: "https://open.spotify.com/show/3IiC15tFfb1rHoDm9R6Zxp",
    /* ccpod: not published yet — add its Spotify URL when it ships */
    /* approachable: YouTube channel — drop assets/art/approachable.jpg */
  };

  const base = document.querySelector('script[src$="artwork.js"]');
  const root = base ? base.getAttribute("src").replace(/js\/artwork\.js$/, "") : "";

  const place = (slot, src) => {
    const img = new Image();
    img.className = "art-slot__img";
    img.alt = "";
    img.decoding = "async";
    img.loading = "lazy";
    img.addEventListener("load", () => img.classList.add("is-loaded"));
    img.src = src;
    slot.appendChild(img);
  };

  const thumbs = {};
  const fetchThumb = (key) => {
    if (!SHOWS[key]) return Promise.resolve(null);
    if (!thumbs[key]) {
      thumbs[key] = fetch(
        "https://open.spotify.com/oembed?url=" + encodeURIComponent(SHOWS[key])
      )
        .then((r) => (r.ok ? r.json() : null))
        .then((d) => (d && d.thumbnail_url) || null)
        .catch(() => null);
    }
    return thumbs[key];
  };

  document.querySelectorAll("[data-art]").forEach((slot) => {
    const key = slot.getAttribute("data-art");
    // Local file first: assets/art/<key>.jpg (silent 404 if absent)
    const local = new Image();
    local.addEventListener("load", () => place(slot, local.src));
    local.addEventListener("error", () => {
      fetchThumb(key).then((url) => {
        if (url && !slot.querySelector("img")) place(slot, url);
      });
    });
    local.src = root + "assets/art/" + key + ".jpg";
  });
})();
