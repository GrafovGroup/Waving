"""Owner-provided video, presented on the bilingual homepage without autoplay."""

film_title = c('Keep Canada waving.', 'Faisons flotter le Canada.')
film_label = c('Canadian flag waving on an outdoor flagpole against a sunset sky.', 'Drapeau canadien flottant sur un mât extérieur devant un ciel au coucher du soleil.')
film = '<section class="flag-film wrap" aria-labelledby="flag-film-heading"><div class="flag-film-copy">'
film += '<p class="eyebrow">' + c('CANADA IN MOTION', 'LE CANADA EN MOUVEMENT') + '</p>'
film += '<h2 id="flag-film-heading">' + film_title + '</h2>'
film += para('A familiar symbol, out in the everyday. Find Canadian flags for your property, workplace or next event.', 'Un symbole familier au cœur du quotidien. Trouvez des drapeaux canadiens pour votre propriété, votre lieu de travail ou votre prochain événement.')
film += link('/flags/canada/', c('EXPLORE CANADIAN FLAGS', 'DÉCOUVRIR LES DRAPEAUX CANADIENS'), 'button navy')
film += '</div><figure class="flag-film-player"><video controls playsinline muted preload="none" width="1280" height="720" poster="/assets/canadian-flag-sunset-poster.webp" aria-label="' + film_label + '" aria-describedby="flag-film-caption">'
film += '<source src="/assets/canadian-flag-sunset.mp4" type="video/mp4">'
film += link('/assets/canadian-flag-sunset.mp4', c('Watch the Canadian flag video.', 'Regarder la vidéo du drapeau canadien.'))
film += '</video><figcaption id="flag-film-caption">' + c('Canadian flag at sunset · Silent video · 19 seconds', 'Drapeau canadien au coucher du soleil · Vidéo sans son · 19 secondes') + '</figcaption></figure></section>'

# Keep the service finder first, then show the real footage before the product overview.
film_anchor = '<section class="wrap section"><div class="section-title-row">'
assert film_anchor in PAGES['/']['body'], 'Homepage product overview is missing'
PAGES['/']['body'] = PAGES['/']['body'].replace(film_anchor, film + film_anchor, 1)
