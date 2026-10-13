# Laaj Studios website

A static, single-page wedding photography and film site built as an enquiry funnel. It needs no build step: open `index.html` in a browser, or host the folder anywhere (GitHub Pages, Netlify, Cloudflare Pages, any web host).

## Before going live

1. **Contact details**: set in `js/config.js` (photo@laajstudios.co, +1 914 620 7296 for calls, texts and WhatsApp, laajstudios.co). Every link on the site updates from there.
2. **Enquiry delivery**: create a free form at [formspree.io](https://formspree.io), then paste its endpoint into `formEndpoint` in `js/config.js`. Until then, submitting the form opens the visitor's email app with the enquiry written out.
3. **Optional**: add the film link (`filmUrl`) in `js/config.js`.

## How the funnel works

- Every section ends in a call to action that leads to the 3-step enquiry form (`#enquire`).
- After submitting, the visitor is offered a WhatsApp chat pre-filled with their enquiry summary.
- Mobile visitors get a fixed bar with Call · Text · WhatsApp · Enquire. Desktop visitors get a floating WhatsApp button.
- UTM tags, `gclid` and `fbclid` from ad links are sent with each enquiry, so you can see which campaigns bring bookings. If Google Analytics (`gtag`) or the Meta Pixel (`fbq`) is installed, a `Lead` event fires on submit.

## Files

- `index.html`: page content
- `css/styles.css`: design
- `js/config.js`: your settings
- `js/main.js`: gallery lightbox, multi-step form, link wiring
- `images/`: web-optimised portfolio photos and logo variants (from the Laaj Google Drive portfolio folders)
