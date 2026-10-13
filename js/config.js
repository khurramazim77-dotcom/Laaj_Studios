/*
  LAAJ STUDIOS — SITE SETTINGS
  Edit the values below; every phone, email and WhatsApp link on the site updates from here.
  Package prices live in index.html (search for "COLLECTIONS").
*/
window.LAAJ = {
  // Shown on the site and used for the email fallback.
  email: "photo@laajstudios.co",

  // How the phone number is displayed, and the same number in international format for links.
  phoneDisplay: "+1 (914) 620-7296",
  phoneE164: "+19146207296",

  // WhatsApp number: country code + number, digits only (no +, spaces or dashes).
  whatsapp: "19146207296",

  // Enquiry form delivery. Create a free form at https://formspree.io and paste its endpoint,
  // e.g. "https://formspree.io/f/abcdwxyz". Leave empty to fall back to opening the visitor's email app.
  formEndpoint: "",

  // Small details shown around the site.
  serviceArea: "New York · Tri-State · Destination worldwide",
  bookingNote: "Now reserving 2027 & 2028 celebrations",
  replyPromise: "We reply to every enquiry within 24 hours.",

  // Optional links. Leave empty to hide.
  filmUrl: "",        // e.g. a YouTube or Vimeo link to the Nina & Junaid film
  instagram: "https://www.instagram.com/laajstudios/",
  website: "laajstudios.co",

  // Client words. The three entries below are PLACEHOLDERS for layout only: they show a "Placeholder" tag on the site.
  // Replace each with a real couple's words (with their permission) and delete the `placeholder: true` line.
  testimonials: [
    {
      placeholder: true,
      quote: "From the mehndi to the rukhsati, they were everywhere we needed them and nowhere we didn't. Our parents still watch the film every Eid.",
      names: "Couple names",
      event: "Mehndi, Nikkah & Walima · Venue, City"
    },
    {
      placeholder: true,
      quote: "They understood our traditions without us having to explain a thing. Every photo feels like us, only more beautiful.",
      names: "Couple names",
      event: "Baraat · Venue, City"
    },
    {
      placeholder: true,
      quote: "The album arrived and my mother cried on the first page. Worth every penny, and then some.",
      names: "Couple names",
      event: "Nikkah & Reception · Venue, City"
    }
  ]
};
