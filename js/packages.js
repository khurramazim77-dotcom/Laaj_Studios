/*
  LAAJ STUDIOS — PACKAGE BUILDER MENU
  Every option and price clients see on the "Build your package" page lives here.
  Edit names, descriptions and prices freely; the page and the running total update automatically.
  Clients never see individual prices: only the estimated total. Your email gets the line-by-line breakdown.

  STARTER PRICES: the numbers below are a first draft. Replace them with your own before going live.
  All prices are in US dollars. Set a price to 0 for an option that adds nothing to the total.
*/
window.LAAJ_PACKAGES = {
  currency: "USD",

  // Shown under the running total and on the client's copy.
  estimateNote: "This is an estimate. Your final proposal is confirmed after a consultation. Travel, if any, is quoted at cost.",

  // ---- Events: clients add one card per event and choose coverage for each ----
  events: {
    max: 6,
    types: [
      "Engagement session",
      "Pre-wedding event",
      "Ceremony",
      "Reception",
      "Post-wedding event",
      "Other event"
    ],
    // Starting cards when the page first opens.
    defaults: [
      { type: "Ceremony", hours: 6, photo: "lead-second", film: "one" },
      { type: "Reception", hours: 5, photo: "lead-second", film: "one" }
    ],
    hours: [2, 3, 4, 5, 6, 7, 8, 9, 10, 12],
    // Price per hour for each choice.
    photo: [
      { id: "none", label: "No photography", perHour: 0 },
      { id: "lead", label: "1 photographer", perHour: 275 },
      { id: "lead-second", label: "2 photographers", perHour: 450 },
      { id: "team", label: "3 photographers", perHour: 625 }
    ],
    film: [
      { id: "none", label: "No film", perHour: 0 },
      { id: "one", label: "1 cinematographer", perHour: 300 },
      { id: "two", label: "2 cinematographers", perHour: 525 }
    ]
  },

  // ---- Deliverables and extras: one dropdown each ----
  // "requires": "film" or "photo" hides the choice's price until that coverage is added to an event.
  sections: [
    {
      id: "films",
      title: "Films",
      intro: "Edited from your film coverage.",
      requires: "film",
      items: [
        {
          id: "highlight", label: "Highlight film", options: [
            { label: "None", price: 0 },
            { label: "Teaser, 60–90 seconds", price: 450 },
            { label: "Highlight film, 5–8 minutes", price: 1200 },
            { label: "Feature film, 15–20 minutes", price: 2200 }
          ]
        },
        {
          id: "documentary", label: "Full-length edits", options: [
            { label: "None", price: 0 },
            { label: "Ceremony and speeches, full length", price: 650 },
            { label: "Every event, full length", price: 1400 }
          ]
        },
        {
          id: "reels", label: "Social media reels", options: [
            { label: "None", price: 0 },
            { label: "3 vertical reels", price: 450 },
            { label: "6 vertical reels", price: 800 }
          ]
        },
        {
          id: "same-day", label: "Same-day edit", options: [
            { label: "None", price: 0 },
            { label: "Same-day edit shown at the reception", price: 1800 }
          ]
        }
      ]
    },
    {
      id: "photos",
      title: "Photographs and albums",
      intro: "Every package includes a private online gallery of edited images.",
      requires: "photo",
      items: [
        {
          id: "album", label: "Heirloom album", options: [
            { label: "None", price: 0 },
            { label: "Linen album, 10×10 in, 30 spreads", price: 1100 },
            { label: "Leather album, 12×12 in, 40 spreads", price: 1750 },
            { label: "Leather album in presentation box, 12×12 in, 50 spreads", price: 2400 }
          ]
        },
        {
          id: "parent-albums", label: "Parent albums", options: [
            { label: "None", price: 0 },
            { label: "1 parent album, 8×8 in", price: 425 },
            { label: "2 parent albums, 8×8 in", price: 800 },
            { label: "3 parent albums, 8×8 in", price: 1150 }
          ]
        },
        {
          id: "prints", label: "Fine art prints", options: [
            { label: "None", price: 0 },
            { label: "Box of 25 archival prints", price: 375 },
            { label: "Framed wall portrait, 24×36 in", price: 650 }
          ]
        },
        {
          id: "sneak-peek", label: "Sneak peek", options: [
            { label: "Standard, within one week", price: 0 },
            { label: "Express, within 48 hours", price: 250 }
          ]
        }
      ]
    },
    {
      id: "extras",
      title: "Extras",
      intro: "",
      items: [
        {
          id: "drone", label: "Drone coverage", options: [
            { label: "None", price: 0 },
            { label: "Drone at one event", price: 450 },
            { label: "Drone at every event", price: 900 }
          ]
        },
        {
          id: "booth", label: "Photo booth", options: [
            { label: "None", price: 0 },
            { label: "Open-air booth with instant prints, 3 hours", price: 950 }
          ]
        },
        {
          id: "delivery", label: "Gallery delivery", options: [
            { label: "Standard, 6–8 weeks", price: 0 },
            { label: "Priority, within 3 weeks", price: 600 }
          ]
        },
        {
          id: "travel", label: "Location", options: [
            { label: "Local to us", price: 0 },
            { label: "Destination wedding (travel quoted separately)", price: 0, note: "Travel quoted" }
          ]
        }
      ]
    }
  ]
};
