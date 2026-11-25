# Løvel.dk backlog

## Information to add

- [ ] Put the next Byfest date and programme on the Byfest page and link to it
  from the homepage. If the programme is pending, show when it will be
  available or where the organisers post updates.
- [ ] Give residents direct homepage links to Forsamlingshuset booking,
  childcare, and the current Byfest information. Verify the booking contact
  and prices with Forsamlingshuset before promoting them.
- [ ] Add a short **Ny i Løvel** guide. Link to existing childcare, school,
  housing, and water pages, and verify useful official links for transport
  and municipal services before publishing them.
- [ ] Explain how residents, associations, and businesses can submit
  announcements and corrections. Use the existing site support email.

## Media

- [ ] Create responsive versions of the homepage hero and lightweight
  gallery thumbnails. Lazy-load images below the fold and request full-size
  gallery images when opened.
- [ ] Inventory media against the JSON, generated HTML, and any known direct
  links. Group byte-identical copies and choose a canonical path where useful.
  Review shared links before changing public URLs.
- [ ] Keep site-ready images and actively linked documents in the repository.
  Store original photos, source video, and archival material in a shared
  archive with a named account owner and a backup. Confirm the archive copy
  and any replacement link before removing a public file.
- [ ] Start with the local 55 MiB `media/film/lovel_2017.mp4` copy. The Medier
  page embeds YouTube. Check whether anyone relies on the MP4 URL, preserve the
  original in the archive, then decide whether the direct download is still
  needed. Use ordinary commits for cleanup and leave Git history intact.

## Maintenance process

- Record each proposed change here with the affected page, the next action,
  and any information needed to confirm it.
- For local dates, contacts, and prices, the human maintainer confirms facts
  with the relevant organiser. Use the assistant for repository checks,
  drafting, and implementation when working together on a change.
- Review the list before Byfest and when organisers report changes. Give
  dated notices an expiry or a follow-up date so old announcements are
  removed or moved to an archive.
- Keep each publishing change focused. Update the source and generated HTML,
  preview the affected pages, and review the pull request. Close the backlog
  item once the change is live.
