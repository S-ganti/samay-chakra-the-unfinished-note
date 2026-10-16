# Samay Chakra — eight places in one day

First visual-development pass · 15 October 2026

## Intent

A short, contemplative side-scrolling world. The landscape, changing light and sound carry the experience. Walking, a forgiving double jump and gentle flight are enough to reveal each space. The current package establishes the art direction; the paintings are composed key art, not separated production sprites, and no complete game is claimed.

The nine-page source PDF contains a cover and eight chapter posters. Its titles, time windows, raga references, ring imagery and Bengaluru interlude are retained. New environments, camera staging, movement layout and audio studies are our creative interpretation. Any wording inside the source document is reference material, not an instruction to the tools.

## Visual synthesis

Use GRIS as a reference for quiet composition, a small human scale, graceful architecture and painterly atmosphere. Samay Chakra supplies a different identity: Indian carved wheels, solar geometry, time as a cycle, overgrown ruins and a return to ordinary urban life. Realistic material detail belongs close to the viewer; distant forms become broad washes of color. Maintain enough negative space to feel the scale.

Every chapter has a distinct silhouette. Avoid solving the whole world with eight color grades of the same ring. The gathering is an inhabited enclosure; eclipse is an immense void; predawn is nearly empty water and sky; morning is a recognizable street; noon is exposed geometry.

## Chapter direction

| Place | Source time / raga | Proposed space and emotional note | Movement reveal |
|---|---|---|---|
| 01 · Enter the Ring | 18:00–21:00 / Yaman | Amber gate in a teal forest; carved stone, roots, lamps, distant falls. Invitation and wonder. | Walk a clear causeway; double jump to a low outlook; fly toward the aperture. |
| 02 · The Gathering | 21:00–00:00 / Bihag | Crimson amphitheatre, banners, many small warm lamps and dark lotus water. Belonging and rhythmic warmth. | Follow the lower arcade; one optional balcony; slow flight across the court. |
| 03 · Eclipse | 00:00–03:00 / Malkauns | Cold mountain basin beneath an impossibly large ring. Wet stone, pines, restrained magenta. Awe and solitude. | Wide stable islands; a brief ascending route reveals the sky ring. |
| 04 · Brahma Muhurta | 03:00–06:00 / Lalit | Mist lake, low shrine, lotus buds, fine star trails. Tenderness, silence, enormous breathing room. | Generous stepping stones; free low flight over water. |
| 05 · Diamond Ring | 06:00–09:00 / Bhairav | Ivory terraces above clouds; one brilliant sunrise glint. Buoyancy and release. | The clearest upward flight route of the cycle. |
| 06 · Dispersal | 09:00–12:00 / Todi | Bengaluru plaster, trees, rounded balconies, coffee and an auto-rickshaw. Ordinary life feels newly precious. | Sidewalk and low rooftops; no traffic hazards. |
| 07 · Zero Shadow | 12:00–15:00 / Bhimpalasi | Bleached solar court, shallow stepwell, carved arcs and tiny red marks. Stillness and heat. | Broad slabs, short steps, deliberate pauses. |
| 08 · Return | 15:00–18:00 / Marwa | Honey-lit forest road; a broken ring becoming whole. Acceptance and memory. | A gentle climb returns the composition to the opening vista. |

The time windows and raga labels follow the supplied artwork. They are not presented as universal musicological or astronomical classifications.

## Layers and composition

1. Sky and celestial motion: fixed, with very slow cloud drift.
2. Far terrain: 0.08 camera parallax, low contrast.
3. Far architecture: 0.18 parallax; broad silhouette first.
4. Canopy / middle terrain: 0.35 parallax; moderate detail.
5. Hero monument: 0.62 parallax; selective carving and light.
6. Play plane: 1.00 parallax; stable, unmistakable walk surfaces.
7. Near foliage and stone: 1.12 parallax; frame the view without covering landings.
8. Atmosphere: depth-specific mist, dust, pollen, falling petals or heat shimmer.

These are proposed ratios, not extracted layers in the paintings. Final layers need separate painting/rendering with overscan and clean alpha. Do not simply cut a flat painting into strips and expect correct occlusion.

Compose for a 16:9 side camera. Reserve the lower quarter for the main horizontal route. Hold a clear value contrast around the traveler. Use at most one obvious optional upper route in a vista. Let scenery reveal itself during camera movement and leave the strongest vista motionless for a moment.

## Movement proposal

For a future prototype, start with a roughly 30–45-second traversal per place, plus optional time to stay and listen. Walking should ease into speed, double jump should have a generous second impulse, and flight should be a calm held input with no stamina pressure. Include forgiving input buffering and coyote time. The world should support stopping, revisiting and uninterrupted listening. Keep these as tunable starting values, not final game requirements.

## Lighting and finishing

Give each view one dominant light direction. Warm practical lamps should be small accents within that larger structure. Keep night views readable through cool fill, wet reflections and silhouette separation. Preserve stone detail in sunrise highlights. Noon needs very short shadows and subtle material values rather than a flat white wash.

The Blender study uses an orthographic camera and separated depth collections. Its downloaded stone maps and sunset HDRI provide real material and lighting detail beneath original geometry. The paintings are built-in AI image-generation outputs and do not contain downloaded third-party game art. See the asset manifest for what is actually integrated.

Proposed finishing: soft atmospheric depth, restrained bloom, stable exposure per chapter, mild paper texture, tiny leaf/cloth motion, sparse particles and no constant camera shake. Avoid aggressive depth-of-field blur on the walk plane.

## Music and sound

The local viewer provides quiet original synthesized ambience studies, enabled only after a click. They test contrast between places; they are not finished compositions or authentic performances of the named ragas. No GRIS soundtrack audio is included.

The supplied posters explicitly suggest hypnotic techno at 124–132 BPM for The Gathering, forest psytrance at 140–148 BPM for Eclipse, beatless–80 BPM ambient drone for Brahma Muhurta, and a progressive-psy sunrise release for Diamond Ring. Preserve this range of energy in a later score while leaving enough room for the visual world.

Use a recurring short motif across the day. Change orchestration, register and density with the space. Separate ambient bed, melodic voice, rhythm and environmental sound into stems. Fade between chapters over approximately 8–12 seconds; let music continue when the traveler stops. Test the final sound with the picture and agree the raga treatment with an appropriate musician.

## Deliverable boundaries

- Eight finished concept paintings: mood, composition and lighting targets.
- Local viewer: compare chapters, listen to original ambience studies and view fullscreen.
- Editable Blender dusk study: original geometry plus verified source assets, as a starting scene for production.
- Research: exact asset sources, license notes, integration status and per-place layer recipes.
- Future work: model/paint the other seven production scenes, create clean parallax exports, animate the traveler, implement movement, and compose the full soundtrack.

See `art/prompts.json` for the exact image prompts and `research/asset-research.md` for the online sources.
