# Space Invaders application requirements specification

This document defines the requirements for the **Space Invaders** desktop application, identified in code syntax and application metadata as `spc_inv`. This specification is designed for an autonomous orchestrator operating inside the Anvil physical component architecture on Fedora Linux 44 and later.

The orchestrator must translate these functional and boundary requirements into a logical capability graph and contract that graph into physical targets using the anchor constrained capability contraction algorithm defined in [.agents/skills/architect/SKILL.md](.agents/skills/architect/SKILL.md).

## Mandatory pre-architecture phase to strip template exemplar artifacts

Before running the capability contraction workflow or scaffolding any new application components, the orchestrator must strip all pedagogic demonstration artifacts from the Anvil starter template while preserving the core runtime anchor backbone.

**Remove exemplar component directories.** Delete `targets/item_proto`, `targets/item_store`, and `targets/tbb_transform` from the repository. Do not modify or remove the four mandatory anchor targets `targets/journal`, `targets/journal_signal_adapter`, `targets/perf_scope`, and `targets/app` required by the `H2_anchor_preservation` gate in [.agents/skills/architect/scripts/sync_manifest.py](.agents/skills/architect/scripts/sync_manifest.py).

**Remove exemplar profiling telemetry.** Delete `production_artifacts/profiling/item_store_score_report.json` and `production_artifacts/profiling/tbb_transform_score_report.json`. Retain `production_artifacts/profiling/journal_score_report.json` so the `journal` anchor benchmark remains clean.

**Update the approved third party dependency palette.** Edit [cmake/dependencies.cmake](cmake/dependencies.cmake) to remove unused demonstration dependencies if desired and register the Fedora 44 desktop, graphics, audio, and storage libraries required for `spc_inv` with appropriate `@anvil_toxicity` weights. Keep `targets/app` as the physical directory name so `H2_anchor_preservation` remains green, and configure the `app` target or application metadata to expose the `spc_inv` identifier.

**Synchronize and commit the clean baseline.** Execute `./production_artifacts/build_all.sh custom debug`, `./production_artifacts/build_all.sh default release`, and `python3 .agents/skills/architect/scripts/sync_manifest.py --check`. Confirm that all five hard invariant gates $H_1$ through $H_5$ pass with zero dirty benchmarks, then create an atomic Git commit for the stripped baseline so `sync_manifest.py --require-clean-git` succeeds at Step 1 of the `architect` skill.

## Target platform and runtime environment

The application exclusively targets **Fedora Linux version 44 and later** running on a modern GNOME Wayland desktop session with PipeWire audio and systemd journald logging. No compatibility shims for legacy Linux distributions, X11 fallback hacks, Windows, or macOS are permitted.

**System host baseline.** Assume Fedora 44 system packages including `libadwaita-1` version 1.9 or newer, `gtk4` version 4.22 or newer, `cairo`, `pangocairo`, `epoxy`, `alsa` or `sdl3` or `gstreamer-1.0` for audio output, `sqlite3` for local persistence, and `libsystemd` for structured flight recorder logging.

**Zero external asset files.** The compiled application binary must be completely self contained at runtime. All visual sprites, alien silhouettes, destructible bunker masks, HUD typography, and retro sound effects must be generated procedurally in memory through vector geometry, procedural bitmaps, and digital audio synthesis without loading external PNG, SVG, WAV, or OGG files from disk.

## Approved third party library palette for cmake/dependencies.cmake

During the template cleanup phase, the orchestrator must ensure [cmake/dependencies.cmake](cmake/dependencies.cmake) exposes the following candidate third party libraries alongside existing core libraries so worker subagents can link them strictly `PRIVATE` inside isolated boundary adapters.

```cmake
# GNOME Adwaita and GTK4 windowing and vector rendering
# @anvil_toxicity: libadwaita-1 = 0.75
pkg_check_modules(libadwaita-1 GLOBAL REQUIRED IMPORTED_TARGET libadwaita-1)

# @anvil_toxicity: gtk4 = 0.75
pkg_check_modules(gtk4 GLOBAL REQUIRED IMPORTED_TARGET gtk4)

# @anvil_toxicity: cairo = 0.45
pkg_check_modules(cairo GLOBAL QUIET IMPORTED_TARGET cairo)

# @anvil_toxicity: pangocairo = 0.50
pkg_check_modules(pangocairo GLOBAL QUIET IMPORTED_TARGET pangocairo)

# Real time low latency PCM audio playback candidates
# @anvil_toxicity: sdl3 = 0.55
pkg_check_modules(sdl3 GLOBAL QUIET IMPORTED_TARGET sdl3)

# @anvil_toxicity: alsa = 0.40
pkg_check_modules(alsa GLOBAL QUIET IMPORTED_TARGET alsa)

# @anvil_toxicity: gstreamer-1.0 = 0.65
pkg_check_modules(gstreamer-1.0 GLOBAL QUIET IMPORTED_TARGET gstreamer-1.0)
```

Marking `libadwaita-1` and `gtk4` as `REQUIRED` establishes a mandatory architectural directive to build the native GNOME Adwaita user interface. The orchestrator is free to select the optimal audio backend from `sdl3`, `alsa`, or `gstreamer-1.0` and use `sqlite3` from the existing palette for persistent leaderboard storage.

## External system boundaries and data flow

To allow the anchor constrained capability contraction algorithm to cleanly separate stateful OS and I/O boundaries from pure deterministic in-memory compute kernels under gate `H3_execution_verification_parity`, the application data flow is organized across four primary boundaries.

**Libadwaita windowing and input boundary.** The application initializes an `AdwApplication` under the application ID `io.github.anvil.spc_inv` and presents an `AdwApplicationWindow` structured with an `AdwToolbarView` and `AdwHeaderBar`. The window captures hardware keyboard controller events for horizontal cannon movement, weapon fire, pause, and new game actions, translating raw GDK key events into strong domain input state snapshots consumed by the simulation loop.

**Frame clock and 2D vector canvas rendering boundary.** A GTK4 widget frame clock callback drives the real time presentation loop synchronized to the display refresh rate. On each frame, the rendering boundary reads an immutable or snapshot view of the current game world state and renders all entities inside a custom GTK4 drawing widget using Cairo or GTK4 snapshot primitives. All classic entities including the three distinct alien ranks with two-frame marching animations, the player laser cannon, the mystery UFO saucer, projectiles, explosion bursts, and eroded protective bunkers are drawn via crisp geometric vector paths or procedural pixel grids without external textures.

**Procedural audio synthesis and PCM output boundary.** Gameplay events emitted during a simulation step trigger retro arcade sound effects including player laser shots, alien destruction thuds, the accelerating four-note bass marching pulse, mystery UFO warble, and player ship explosion noise. Waveform synthesis and envelope mixing must be decoupled from blocking audio device I/O so pure PCM waveform generation can be benchmarked in memory while a thin stateful audio output adapter streams synthesized PCM buffers to the Fedora host audio server.

**Local high score persistence boundary.** High score records and player session statistics persist across application launches inside the standard XDG user data directory `$XDG_DATA_HOME/spc_inv/` or `~/.local/share/spc_inv/` using `sqlite3` transactional storage. Database file I/O occurs strictly at game initialization and upon game over transitions so disk operations never block the real time simulation or rendering loop.

## Classic 1978 gameplay mechanics and deterministic simulation

All core game rules, entity kinematics, bunker erosion calculations, and collision detection must operate as pure deterministic in-memory state transitions with zero OS, GUI, or audio library headers. Pure compute components must include `<name>BENCH` hardware PMU benchmark suites measuring nanosecond step latency, instructions per cycle, and cache efficiency.

**Alien formation and accelerating march.** Each wave spawns an 11 column by 5 row formation of 55 invaders divided into three classic tiers. The top row awards 30 points per invader, the middle two rows award 20 points, and the bottom two rows award 10 points. The formation marches horizontally in lockstep, reverses direction and drops vertically upon reaching the arena edge, and dynamically accelerates its step cadence as fewer invaders remain alive.

**Player laser cannon and single-shot discipline.** The player controls a horizontal laser cannon along the bottom arena boundary with three starting lives. Firing obeys classic arcade single-shot discipline where only one active player laser bolt may exist in flight at a time until it strikes a target or exits the upper boundary. Awarding an extra life occurs once per game when the player reaches 1500 points.

**Alien projectiles and targeting.** Bottom-row invaders in each active column fire downward projectiles toward the player cannon using a deterministic pseudo-random or column-targeted cadence. Up to three simultaneous alien projectiles may be in flight at any instant.

**Destructible protective bunkers.** Four classic arch-shaped defensive bunkers sit between the alien formation and the player cannon. Each bunker is represented as a fine grained destructible grid or bitmask that erodes locally whenever struck by player bolts, alien projectiles, or descending invader bodies.

**Mystery UFO saucer.** At periodic intervals, a bonus mystery saucer traverses the top margin of the playfield horizontally. Destroying the saucer awards a deterministic score bonus selected from 50, 100, 150, or 300 points based on the player's shot counter.

**Wave progression and game over conditions.** Clearing all 55 invaders advances the game to the next wave, resetting the formation at a progressively lower starting altitude up to a classic cap while preserving the player's score and remaining lives. The game ends immediately if the player loses all lives or if any surviving invader reaches the altitude of the player cannon.

## Adwaita window design and user experience

The graphical interface must follow modern GNOME Human Interface Guidelines using `libadwaita-1` widgets rather than legacy GTK3 dialogs or unstyled SDL windows.

**Header bar and live HUD telemetry.** The top `AdwHeaderBar` displays the window title alongside compact pill or status indicators showing current score, all-time high score, current wave number, and remaining player lives, plus action buttons for pausing the game, muting audio, and viewing the high score leaderboard.

**Adaptive status overlays and navigation.** When launching the application, pausing, or reaching a game over state, present clean Libadwaita overlay states using `AdwStatusPage`, `AdwBanner`, or `AdwDialog` components that allow starting a new game, inspecting top scores, or reviewing keyboard controls without leaving the single window.

**Dark arcade visual aesthetic.** Configure `AdwStyleManager` to prefer the dark Adwaita color scheme so the high contrast neon green, cyan, magenta, and white geometric arcade vectors pop against a deep dark background while respecting GNOME window rounded corners and resize scaling.

## Fedora 44 RPM packaging and DNF installation

The build system must be configured to package the release application into an installable Fedora 44 `.rpm` package using CMake installation rules and CPack RPM generator (`rpmbuild`) so the user can install, upgrade, and remove the application directly via `sudo dnf install` and `sudo dnf remove`.

**Executable output name and installation target.** Configure `targets/app/CMakeLists.txt` so the `app` executable target produces a binary named `spc_inv` via `OUTPUT_NAME "spc_inv"` while keeping the physical target directory `targets/app` intact for Anvil's `H2_anchor_preservation` gate. Register standard GNU installation rules using `GNUInstallDirs` so `spc_inv` installs into `${CMAKE_INSTALL_BINDIR}` (`/usr/bin/spc_inv`).

**GNOME desktop integration metadata.** Generate or install a Freedesktop `.desktop` launcher entry (`io.github.anvil.spc_inv.desktop`) into `${CMAKE_INSTALL_DATADIR}/applications` and a scalable vector application icon (`io.github.anvil.spc_inv.svg`) into `${CMAKE_INSTALL_DATADIR}/icons/hicolor/scalable/apps` so **Space Invaders** appears natively in the Fedora GNOME application grid upon DNF installation.

**CPack RPM configuration and dependency autodetection.** Configure `CPack` in the CMake build with `CPACK_GENERATOR` set to `"RPM"`, `CPACK_PACKAGE_NAME` set to `"spc_inv"`, `CPACK_RPM_PACKAGE_SUMMARY` set to `"Space Invaders arcade game for GNOME Adwaita"`, `CPACK_RPM_PACKAGE_LICENSE` set to `"MIT-0"`, and `CPACK_RPM_PACKAGE_AUTOREQPROV` set to `"ON"` so `rpmbuild` automatically discovers shared library dependencies (`libadwaita-1`, `gtk4`, `sqlite3`, `libsystemd`, and the selected audio library) for seamless resolution by `dnf`.

**End to end RPM verification.** As part of final delivery verification, the orchestrator must build the release preset, generate the `.rpm` artifact via `cpack -G RPM` in the release build directory, and verify with `rpm -qip` and `rpm -qlp` that the resulting `.rpm` package contains `/usr/bin/spc_inv` and desktop integration files ready for `sudo dnf install ./spc_inv-*.rpm`.

## Architectural constraints and orchestrator execution rules

The Argon orchestrator and all spawned `tactical_worker` subagents must strictly obey [.agents/rules/invariants.md](.agents/rules/invariants.md) and [.agents/skills/architect/SKILL.md](.agents/skills/architect/SKILL.md) throughout implementation.

**Delegate naming and topology to ACCC.** Aside from retaining the four mandatory anchor target names `journal`, `journal_signal_adapter`, `perf_scope`, and `app`, the orchestrator has full autonomy to select component names, helper unit splits, and internal C++ namespaces under `anvil::<name>` according to the mathematical partition friction score $\Phi(P)$.

**Strict vendor header insulation.** Neither `<adwaita.h>`, `<gtk/gtk.h>`, `<cairo.h>`, `<SDL3/SDL.h>`, `<alsa/asoundlib.h>`, nor `<sqlite3.h>` may ever appear in any public component header `targets/<name>/<name>/<name>.hpp`. All third party headers must be confined to `.cpp` translation units or private helper headers outside the `PUBLIC FILE_SET`, and all vendor libraries must be linked `PRIVATE`.

**Boundary exception firewalls and flight recorder logging.** Every operational component must define its `<name>.catalog` and `k_catalog` contract, mark public operational boundaries `noexcept`, catch unhandled exceptions via `anvil::journal::catch_boundary_exception`, and log key lifecycle transitions and fault diagnostics through `anvil::journal::log`.

**Static analysis and sanitizer verification.** If C APIs in GTK4, Libadwaita, or audio libraries trigger situational Clang-Tidy warnings inside private boundary `.cpp` files, encapsulate those calls cleanly and document any unavoidable Category B or C vendor macro warnings in [production_artifacts/clang_tidy_state.md](production_artifacts/clang_tidy_state.md). All pure compute components and unit test suites must pass dual compiler debug and release builds, Clang-Tidy, Cppcheck, Include-What-You-Use, and sanitizer suites cleanly.

