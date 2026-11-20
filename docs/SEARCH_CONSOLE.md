# Google Search Console — CAOS

## Production property

The current production deployment is GitHub Pages:

- Site: https://carlosjuniorcj16-code.github.io/CAOS/
- Sitemap index: https://carlosjuniorcj16-code.github.io/CAOS/sitemap.xml
- Robots: https://carlosjuniorcj16-code.github.io/CAOS/robots.txt

## One-time setup

1. Open [Google Search Console](https://search.google.com/search-console).
2. Add a **URL-prefix** property with the exact address `https://carlosjuniorcj16-code.github.io/CAOS/`.
3. Choose HTML-tag verification. Google will provide a unique `google-site-verification` meta tag.
4. Add that exact tag inside the `<head>` of `index.html`, commit it, and wait for the GitHub Pages deployment to finish.
5. Return to Search Console and click **Verify**.
6. Open **Sitemaps**, enter `sitemap.xml`, and submit it.

The verification token is unique to the Google account. Do not guess, fabricate or commit a token from another property. If using HTML-file verification instead, the exact downloaded file must be added unchanged at the root of the deployed URL prefix.

## What to monitor

- Sitemaps: last read, discovered URLs and processing errors.
- Page indexing: indexed, excluded, duplicate and crawled-not-indexed pages.
- URL inspection: test representative category pages and resource pages.
- Performance: impressions, clicks, queries and country/device distribution.

Submitting a sitemap is a discovery hint, not a guarantee of crawling or indexing. Keep the sitemap and canonical URLs aligned with the deployed host. If the production domain changes, update `CAOS_SITE_URL` in `.github/workflows/deploy-pages.yml` and regenerate all pages and sitemaps.

Official references:
- https://support.google.com/webmasters/answer/34592
- https://support.google.com/webmasters/answer/9008080
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
