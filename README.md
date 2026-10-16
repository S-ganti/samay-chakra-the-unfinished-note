# The Unfinished Note — living-world update

Open index.html. Hold E at a listening circle to discover a memory and resonate with the environment. J opens the listening book. Walk with A/D or arrows, Space double jumps, W/Up flies, Escape pauses. The sound starts when you enter the world and can be switched off in the menu. Touch controls include a listening button. In Return, try standing still.

All eight gameplay paintings now use clean editions without background characters. Moving water, depth-banded mist, leaves, petals and light shafts animate the world; listening adds resonance and a visible ripple. There are 24 saved story fragments about life, love, loss, grief, joy, inquiry and release. Read THE_UNFINISHED_NOTE.md for the narrative concept and production boundaries. The historical art viewer and artbook retain the original concept paintings.

The browser checks passed for movement, all clean images loading, chapter changes, audio toggling, discovery, persistence, stillness ending, reduced-motion execution, and narrow-screen overflow. These checks do not establish a final soundtrack or fully separated production backgrounds.

---
## Play the first prototype

Open `index.html` in a modern browser. Walk with A/D or the arrow keys, double jump with Space, and hold W or Up to fly. Touch buttons are provided on mobile. Escape opens the pause menu and the eight-place selector. Cross the right edge to reach the next place; the eighth loops back to dusk. Sound is optional and starts through a user gesture. Your last selected place is remembered locally.

This is the first playable movement prototype. It uses the eight flattened concept paintings with camera drift, separate platforms, an animated traveler, particles and procedural sound. The game uses clean background editions with the painted figures removed. True separated background layers, bespoke routes for each composition, production character animation and the final score remain future art/level work. The editable Blender study is separate.
# Samay Chakra — Eight places, one turning day

An art-direction package for an atmospheric 2D world. The first deliverable is eight environment renditions shaped by the Samay Chakra source PDF: a day-long cycle of light, place, mood, and musical references.

## View the artwork

Open `art-viewer.html` in a modern browser. It runs locally, without a build step, dependencies, or a network connection. Keep the `art` folder beside it.

- Choose any of the eight thumbnails, or use the left and right arrow keys.
- Use the fullscreen button or the **F** key for a larger view.
- **Play original ambience** starts a quiet procedural sound study. Audio is off by default, fades between places, and pauses when the page is hidden.
- Adjust the volume to taste. The ambience is synthesized locally with Web Audio, using oscillators and filtered noise. No recorded music or third-party samples are used.

The original ambience studies are **not authenticated raga performances**. The raga names below are references from the source concept, and are presented to guide a future composer.

| Place | Time | Raga reference | Environment |
|---|---|---|---|
| Enter the Ring | 18:00–21:00 | Yaman | Amber dusk; an overgrown giant stone ring |
| The Gathering | 21:00–00:00 | Bihag | A crimson lantern courtyard |
| Eclipse | 00:00–03:00 | Malkauns | An eclipsed sky ring, blue mountains, pines, wet rock, magenta light |
| Brahma Muhurta | 03:00–06:00 | Lalit | A tender mist lake and predawn star trails |
| Diamond Ring | 06:00–09:00 | Bhairav | A white-gold rising sun ring above cloud terraces |
| Dispersal | 09:00–12:00 | Todi | Bengaluru banyans, cream streets, an auto-rickshaw, and coffee |
| Zero Shadow | 12:00–15:00 | Bhimpalasi | A bleached ivory astronomical court at noon |
| Return | 15:00–18:00 | Marwa | A honey-lit forest road and the broken ring rebuilt |

## What this package is

`art/` contains concept artwork. These images communicate composition, palette, environmental density, atmosphere, and lighting. They are flattened visual targets rather than editable production layers.

`art-viewer.html` is a presentation viewer, with original procedural audio sketches. It is not a playable game. Double jump, flight, collision, level transitions, animation, and a game-ready parallax pipeline remain future implementation work.

Any editable Blender scene or scene-building scripts supplied in `blender/` are separate production-layout material. A blockout establishes camera, depth, terrain, and lighting relationships; it should not be confused with a completed scene that reproduces all of the painted artwork. Refer to the Blender delivery notes for its actual contents and build status.

`research/` contains the supporting art direction, references, and source information supplied with the package. Online reference material is inspiration and provenance; licenses must be checked before incorporating any third-party production asset.

## Artwork filenames

The viewer expects these PNG files in `art/`:

```text
01-enter-the-ring.png
02-the-gathering.png
03-eclipse.png
04-brahma-muhurta.png
05-diamond-ring.png
06-dispersal.png
07-zero-shadow.png
08-return.png
```

The full artwork is displayed without cropping in the main frame. Thumbnail previews are cropped for navigation. Missing images produce a readable placeholder; they do not prevent moving between places.

The interface respects reduced-motion preferences, works on narrow screens, and supports keyboard controls. Browser support for fullscreen and Web Audio varies. Use a current desktop browser for the complete presentation.



