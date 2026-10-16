# Editable dusk scene study

Built with Blender 5.2.2 LTS on 16 October 2026. The saved scene contains 3,190 objects in eight depth/production collections, a side-on orthographic camera, original ring/ruin/plant geometry, traversal plinths, practical lamps and a dusk lighting rig.

Open `Enter_the_Ring_editable_scene_study.blend` in Blender. External stone maps and HDRI are packed into the file. `assets/download-manifest.json` records the actual CC0 downloads and checksums. This is a production layout study; the generated paintings are the richer visual targets for subsequent modeling and paint work.

To rebuild, run the installed Blender with `--background --factory-startup --python build_enter_the_ring_fast.py`. The optimized script creates geometry directly and supports the installed Blender version. `build_enter_the_ring.py` is the initial unoptimized source retained for reference. The current build omits compositor bloom because Blender 5 changed the compositor API.

The scene does not contain a playable character controller. Double jump, flight, animation, parallax exports and the remaining seven editable realms still need implementation.
