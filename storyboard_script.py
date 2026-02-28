# ============================================================
#  Storyboard Script Example — Shot List + Dialogue + Prompts
#  Style: Classic Wuxia  |  Duration: ~2 min  |  8 shots
# ============================================================

# ==================== Global Style Directive ====================
# Common prefix for all shot prompts (visual DNA)
STYLE_PREFIX = (
    "Classic 1970s Hong Kong wuxia film, "
    "shot on Eastmancolor film stock, anamorphic widescreen 2.35:1, "
    "high saturation oil painting texture with vivid red green blue, "
    "visible film grain and dust scratches, "
    "warm practical lighting with deep shadows, "
    "no horizontal anamorphic lens flare streaks. "
)

# ==================== Character Setup ====================
# Hero — protagonist, white-robed swordsman
# Villain — antagonist, black-robed saber fighter, scarred face
# Master — grey-robed elder with long white beard, Hero's teacher

# ==================== Shot Details ====================

SHOTS = [
    # --------------------------------------------------
    # Act 1: The Night of Tragedy
    # --------------------------------------------------
    {
        "id": "S01",
        "name": "Master Meditating",
        "duration": "5s",
        "frames": 121,

        # Dialogue/narration (for dubbing/subtitles)
        "dialogue": "[Narrator] In the third year, autumn. The martial world changed overnight.",

        # Visual prompt (for AI video generation)
        "prompt": (
            STYLE_PREFIX +
            "Interior of a traditional Chinese martial arts hall at night. "
            "An elderly master in grey robes with long white beard sits cross-legged "
            "on a raised platform, eyes half-closed in meditation. "
            "Dozens of red candles flicker around him, casting warm dancing shadows "
            "on carved wooden walls. Red lanterns hang from ceiling beams. "
            "Camera slowly dollies forward toward the master's weathered face. "
            "The atmosphere is peaceful but ominous, calm before the storm."
        ),

        # Camera movement
        "camera": "Slow dolly forward, from wide to medium close-up on master's face",
        # Transition
        "transition": "Hard cut to S02",
        # Audio/music notes (for post-production)
        "audio": "Guqin bass notes, wooden fish taps, cricket sounds, distant crows",
    },

    {
        "id": "S02",
        "name": "Villain Entrance",
        "duration": "5s",
        "frames": 121,

        "dialogue": "[Villain] (sneering) Old man, tonight I settle the score from ten years ago.",

        "prompt": (
            STYLE_PREFIX +
            "Exterior moonlit courtyard of a Chinese manor at night. "
            "A menacing villain in all-black traditional robes, "
            "with a prominent scar across his left cheek, strong jawline, "
            "cold piercing eyes, walks slowly toward camera holding a broad dao saber. "
            "Moonlight reflects off the blade with a cold blue gleam. "
            "His black robes billow slightly in the night wind. "
            "He smirks with cruel confidence. "
            "Camera at low angle, slowly tracking backward as he advances. "
            "Deep blue moonlight contrasts with warm interior light behind him."
        ),

        "camera": "Low angle tracking backward, villain walks from far to medium",
        "transition": "Fast zoom cut to S03",
        "audio": "Echoing footsteps, saber sheath metal clang, tense strings",
    },

    {
        "id": "S03",
        "name": "Witness",
        "duration": "10s",
        "frames": 241,

        "dialogue": [
            "[Master] (opens eyes) Villain! You--",
            "[SFX] Blade falls, blood splatters",
            "[Young Hero] (silent scream, trembling, hand over mouth)",
            "[Narrator] That night, an image burned into the boy's eyes forever.",
        ],

        "prompt": (
            STYLE_PREFIX +
            "Split dramatic composition inside a candlelit hall. "
            "Background: the villain in black robes raises his dao saber high "
            "and strikes down at the old master in grey, a violent decisive blow, "
            "the master collapses. Red candles topple and scatter. "
            "Foreground right: a young Asian man with glasses "
            "hides behind an ornate wooden pillar, gripping it with white knuckles, "
            "trembling violently, tears streaming down his face, "
            "one hand pressed over his mouth to stifle a scream. "
            "Camera starts wide then SUDDEN FAST ZOOM into extreme close-up "
            "of the young man's terrified eyes reflecting candlelight. "
            "Vivid red blood color contrasts with warm orange candlelight."
        ),

        "camera": "Wide shot -> fast zoom-in -> extreme close-up on young man's eyes",
        "transition": "Black screen 2s + title card 'Ten Years Later'",
        "audio": "Blade impact, candles falling, rapid heartbeat crescendo, music stops",
    },

    # --------------------------------------------------
    # Act 2: Ten Years of Training
    # --------------------------------------------------
    {
        "id": "S04",
        "name": "Training in Rain",
        "duration": "10s",
        "frames": 241,

        "dialogue": "[Narrator] Ten years of bitter training, forging a blade for this day.",

        "prompt": (
            STYLE_PREFIX +
            "Exterior mountain cliff in torrential rain, dramatic storm lighting. "
            "A young swordsman in soaking wet white robes "
            "practices intense sword techniques with a jian sword. "
            "He performs rapid consecutive slashes, thrusts, and sweeping arcs. "
            "Rainwater sprays off the blade in slow motion arcs. "
            "His white robes cling to his body, hair wild and drenched. "
            "Each strike carries fury and determination. "
            "Camera circles around him in a dynamic tracking shot. "
            "Lightning flashes illuminate the mountain peaks behind him. "
            "Vivid green moss on rocks, blue-grey storm clouds, white robes."
        ),

        "camera": "Circular tracking shot, lightning flashes illuminate wide view",
        "transition": "White flash overexposure to S05",
        "audio": "Heavy rain, thunder, sword whooshes, intense drumbeat crescendo",
    },

    # --------------------------------------------------
    # Act 3: The Fated Duel
    # --------------------------------------------------
    {
        "id": "S05",
        "name": "Standoff",
        "duration": "10s",
        "frames": 241,

        "dialogue": [
            "[Hero] (low voice) Villain, do you recognize this sword?",
            "[Villain] (laughing) The old man's disciple? Here to die?",
            "[Hero] (looks up) No. Here to collect a debt.",
        ],

        "prompt": (
            STYLE_PREFIX +
            "Exterior dusty desert courtyard among ancient red sandstone ruins. "
            "Two martial artists face each other ten paces apart in a tense standoff. "
            "Left: Hero in white robes holding a jian sword, calm determined expression. "
            "Right: Villain in black robes with scarred face holding a dao saber, "
            "arrogant smirk. "
            "Strong wind blows sand and dust between them in swirling patterns. "
            "Their robes and hair whip in the wind. "
            "They slowly sidestep in a circle, sizing each other up. "
            "Camera starts as wide establishing shot, "
            "then SUDDEN FAST ZOOM alternating between their faces. "
            "Vivid blue sky, red sandstone, white and black robes create strong color contrast."
        ),

        "camera": "Wide standoff -> fast zoom alternating face close-ups",
        "transition": "Hard cut to S06",
        "audio": "Sand howling, tense erhu sustained note, heartbeat",
    },

    {
        "id": "S06",
        "name": "Intense Combat",
        "duration": "10s",
        "frames": 241,

        "dialogue": [
            "[SFX] Continuous metal clashes",
            "[Villain] (roaring) Fool!",
            "[Hero] (silent, only breathing and sword wind)",
        ],

        "prompt": (
            STYLE_PREFIX +
            "Intense close-quarters combat in front of a Chinese temple. "
            "The swordsman in white and "
            "the saber fighter in black exchange rapid blows. "
            "Bright orange sparks explode where blades clash. "
            "They parry, dodge, spin, and counterattack in fluid martial arts choreography. "
            "The black-robed villain swings his heavy dao in wide powerful arcs. "
            "The white-robed hero evades with agile footwork and counters with precise thrusts. "
            "Dust and debris fill the air. Stone lion statues in background. "
            "Dynamic tracking camera follows the action, "
            "occasional freeze frames on impact moments. "
            "Red temple pillars, green roof tiles, vivid orange sparks create saturated palette."
        ),

        "camera": "Dynamic tracking + freeze frames on impact",
        "transition": "Slow motion to S07",
        "audio": "Dense metal clashes, heavy breathing, roar, rapid war drums",
    },

    {
        "id": "S07",
        "name": "Final Strike",
        "duration": "5s",
        "frames": 121,

        "dialogue": [
            "[Hero] (whisper) This strike is for my master.",
            "[Villain] (wide eyes, disbelief) You...",
        ],

        "prompt": (
            STYLE_PREFIX +
            "The climactic final strike of the duel. "
            "The hero in white robes surges forward with explosive speed, "
            "thrusting his jian sword in one decisive lunge. "
            "The villain's dao saber flies from his hand spinning through the air. "
            "The villain staggers backward and collapses to his knees in the dust, "
            "defeated and stunned. "
            "Dust particles float in golden sunlight around them. "
            "Low angle shot looking up at the hero standing over the fallen villain. "
            "SUDDEN FAST ZOOM into the hero's eyes -- cold, resolute, no joy."
        ),

        "camera": "Low angle looking up -> fast zoom to hero's eye close-up",
        "transition": "White flash to S08",
        "audio": "Clear sword ring, saber clatters to ground, wind stops, only breathing remains",
    },

    # --------------------------------------------------
    # Act 4: Epilogue
    # --------------------------------------------------
    {
        "id": "S08",
        "name": "Walking Away",
        "duration": "10s",
        "frames": 241,

        "dialogue": [
            "[Narrator] Vengeance fulfilled. The blade grows cold.",
            "[Narrator] But the boy from that candlelit night can never return.",
            "[Title] -- End --",
        ],

        "prompt": (
            STYLE_PREFIX +
            "Exterior vast desolate landscape at golden hour sunset. "
            "The hero in blood-stained white robes walks away from camera "
            "into the endless horizon, completely alone. "
            "His right hand drags his jian sword on the ground, "
            "leaving a thin trail line in the dirt behind him. "
            "Dead barren trees silhouetted against a deep vivid red-orange sunset sky. "
            "His figure grows smaller and smaller as he walks further away. "
            "The camera is fixed in a wide cinematic shot, perfectly still. "
            "The image gradually darkens at the edges, vignetting into black. "
            "A sense of emptiness and melancholy -- vengeance is hollow."
        ),

        "camera": "Fixed wide shot, figure recedes, image darkens",
        "transition": "Fade to black -> end credits",
        "audio": "Lonely xiao/shakuhachi flute, fading wind, silence",
    },
]


# ==================== Timeline Summary ====================
#
#  S01  5s  Master Meditating    --+
#  S02  5s  Villain Entrance       | Act 1: Night of Tragedy (~22s)
#  S03 10s  Witness                |
#       2s  Black screen         --+
#  S04 10s  Training in Rain     -- Act 2: Ten Years of Training (~11s)
#       1s  White flash
#  S05 10s  Standoff             --+
#  S06 10s  Intense Combat         | Act 3: The Fated Duel (~26s)
#  S07  5s  Final Strike           |
#       1s  White flash          --+
#  S08 10s  Walking Away         -- Act 4: Epilogue (~15s)
#       5s  Fade to black + credits
#
#  Total: 65s clips + ~9s transitions + ~5s credits = ~79s (~1m20s)
#  Extend S04/S06 into two segments each to reach 2 minutes.
#
# ==================== Post-Production Notes ====================
#
#  1. Color grading: DaVinci Resolve -> RGB split overlay for Eastmancolor look
#  2. Overlays: Film scratches, grain noise, subtle camera shake
#  3. Dubbing: Narration recording + dialogue dubbing
#  4. Music: Traditional Chinese instruments (guqin/erhu/xiao/drums)
#  5. Sound effects: Sword clashes, wind, thunder, heartbeats
#  6. Subtitles: Traditional Chinese vertical subtitles (classic style)
#  7. Opening title: Red background with black text + classic logo animation
#
