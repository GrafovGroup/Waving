# Waving.ca

Public bilingual website at https://waving.ca.

## Source and build

- `build.py`: HTML generation, homepage, shared navigation/footer and metadata.
- `content.py`: service, product, industry, resource, location and quote-page content.
- `site-config.json`: business configuration and unknown operational fields.
- `dist/assets/`: optimized imagery, self-hosted fonts, styling and quote interactions.
- `python3 build.py` (Python 3.12+): regenerate 106 routes per language plus the English static 404 fallback.
- `python3 verify.py`: validate local page/asset links, anchors and metadata.
- `python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`: local preview.

No client framework, package installation or runtime server is required. Quote delivery uses a configurable HTTPS form service and multipart files. No credentials belong in client configuration. Verify attachment support and provider limits before connecting the endpoint.

## Business facts still required

Contact configuration: (833) 696-9996 and info@waving.ca. The quote form is connected to the Formspree endpoint in `site-config.json`. Provider acceptance and actual inbox delivery are separate checks; this audit does not confirm inbox receipt or the provider plan's attachment support. Legal operator, privacy contact and confirmed on-site regions remain unconfirmed in configuration.

The client-side honeypot, minimum elapsed time and duplicate guard are basic friction only. Enable the form provider's spam protection, server-side attachment validation, content-type enforcement and rate limits when the endpoint is configured. Do not claim inbox delivery based on a 2xx response.

## Privacy and release

Public content uses index/follow, https://waving.ca canonical URLs, reciprocal English/French hreflang and a bilingual sitemap. Both 404 routes are noindex and excluded from the sitemap. Verify enquiry delivery in the receiving inbox and confirm provider attachment support before relying on uploaded files. Preserve email DNS records.

## Architecture for expansion

English and Canadian French are implemented across all 106 routes. `bilingual.py` transforms generated documents using `i18n/source.json` and `i18n/fr.tsv`; missing static translations fail the build. `i18n/runtime.tsv` and `i18n/runtime.js` localize interactive quote text while keeping submitted category values stable and user-entered content unchanged. Add source text and matching French translations together. `verify_i18n.py` validates route parity, self-canonicals, reciprocal hreflang and matching-page language switches. French uses /fr/ with the same route slugs. Query parameters survive language switching; changing document language starts a new form session. No form data is stored in browser storage.

Regional coverage includes 13 hubs, five city pages and requested additional cities within region hubs. Future city/service combinations should be authored only when there is enough distinct local value; no combinatorial page factory is used.

`catalog.json` provides stable category identifiers with no invented prices, stock or SKUs. Future ecommerce can attach product records, inventory and checkout to those identifiers. Current SHOP FLAGS navigation opens a quote-led category catalog, not a cart.

`projects.json` is an empty real-project collection with categories for future verified photography. Do not populate it with generated imagery or invented project claims. Future gallery records require title, location if confirmed, category, image, neutral alt text and publication permission. Render gallery sections only when verified records exist.

## QA evidence

Local desktop and 390px/320px mobile layouts reviewed; navigation and mega-menu tested; no horizontal overflow in inspected views. Internal links, image references, anchors, one H1 per page, descriptions, canonical URLs, structured data and private indexing directives pass across generated HTML. Quote validation tested for need selection, rental date ordering, postal code and preferred phone contact. Local upload retained in review. Sending state and acceptance tested only against an isolated local mock that discards request data; no external submission. Missing-endpoint errors retain entries. No console errors observed on quote flow.

## Asset provenance

Hero, event and hardware images were generated with OpenAI imagegen for this project on 2026-10-01. They are generic editorial scenes, not completed Waving projects, staff or facilities. All are optimized as WebP. No customer-facing provenance captions are used.

DM Sans and Manrope were obtained from Google Fonts and self-hosted with font-display swap. Font source: https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;450;500;550;600;650;700&family=Manrope:wght@400;500;600;650;700;750;800&display=swap . Include their upstream license records with maintenance assets.

Protocol resources link to Canadian Heritage's official flag etiquette and federal half-masting guidance. No engineering specifications or blanket service availability are claimed.

## Specialist expansion — 2026-10-01

Added `micro_pages.py` with 12 focused pages and two illustrated hubs: clips/snap hooks, halyard rope, cleats, finials, wall brackets, indoor stands; stuck flags, noise assessment, pulley/truck replacement, post-storm assessment, seasonal changes and event setup/takedown. The new pages link into the catalog, service hubs and homepage. Contextual quote links carry the specific topic through review and submission. Stock, compatibility and on-site availability remain subject to the actual quote.

Four additional editorial assets were made with built-in OpenAI image generation: a hardware still life, indoor floor displays, wall-bracket detail and a ground-level inspection scene. The inspection image was corrected to remove an unintended national flag. These are generic editorial imagery, not proof of stock, staff, completed work or product specifications. Source prompts and delivery notes are in the output expansion record. All final assets are in `dist/assets/` as WebP.

Market taxonomy references (not evidence of Waving inventory or partnerships): https://www.theflagshop.com/hardware/ and https://www.flagpole.ca/ . Original page copy focuses on requests and compatibility rather than reproducing supplier claims.

Current generated output: 106 routes per language including 404, plus the English static 404 fallback (213 HTML files).

## Bilingual verification

All 106 page pairs and internal links passed automated checks. French quote rental dates, postal validation, preferred-phone requirement, review values and missing-endpoint preservation passed browser checks. Matching-page EN/FR switching and accent-insensitive location filtering passed. French accessories were reviewed at 390px and 1440px; homepage at 320px without horizontal overflow. A human French copy review remains advisable before broad marketing use. No real enquiry was sent.
