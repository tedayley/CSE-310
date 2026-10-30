import pygame
import random
import sys
import shutil
import subprocess
import textwrap
from pathlib import Path

pygame.init()

WIDTH = 1200
HEIGHT = 900
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Risk of Rain 2 - Item Randomizer")
clock = pygame.time.Clock()

BACKGROUND = (14, 17, 27)
PANEL = (25, 30, 44)
PANEL_HOVER = (36, 43, 61)
WHITE = (235, 240, 250)
MUTED = (145, 155, 180)
CYAN = (0, 229, 255)
PINK = (255, 65, 190)
GREEN = (80, 230, 140)
RED = (255, 85, 105)

title_font = pygame.font.SysFont("dejavusans", 32, bold=True)
subtitle_font = pygame.font.SysFont("dejavusans", 15)
category_font = pygame.font.SysFont("dejavusans", 18, bold=True)
item_font = pygame.font.SysFont("dejavusans", 17, bold=True)
button_font = pygame.font.SysFont("dejavusans", 15, bold=True)

ITEMS = {
    "White": [
        "Armor-Piercing Rounds", "Backup Magazine", "Bison Steak",
        "Bundle of Fireworks", "Bustling Fungus", "Cautious Slug",
        "Crowbar", "Delicate Watch", "Energy Drink", "Focus Crystal",
        "Gasoline", "Lens-Maker's Glasses", "Medkit", "Mocha",
        "Monster Tooth", "Oddly-shaped Opal", "Personal Shield Generator",
        "Power Elixir", "Repulsion Armor Plate", "Rusted Key",
        "Soldier's Syringe", "Sticky Bomb", "Stun Grenade",
        "Topaz Brooch", "Tougher Times", "Tri-Tip Dagger",
        "Warbanner", "Roll of Pennies", "Elusive Antlers", "Needletick",
        "Bolstering Lantern", "Chronic Expansion", "Warped Echo", "Eclipse lite", "Hiking Boots"
    ],

    "Green": [
        "AtG Missile Mk. 1", "Bandolier", "Berzerker's Pauldron",
        "Chronobauble", "Death Mark", "Fuel Cell", "Ghor's Tome",
        "Harvester's Scythe", "Hopoo Feather", "Infusion", "Kjaro's Band",
        "Lepton Daisy", "Old Guillotine", "Old War Stealthkit",
        "Predatory Instincts", "Red Whip", "Rose Buckler",
        "Runald's Band", "Shipping Request Form", "Squid Polyp",
        "Ukulele", "War Horn", "Wax Quail", "Will-o'-the-wisp",
        "Ignition Tank", "Box of Dynamite", "Breaching Fin", "Chance Doll",
        "Shuriken", "Sale Star", "Unstable Transmitter",
        "Prayer Beads", "Collector's Compulsion", "Faraday Spur", "Hunter's Harpoon", "Ignition Tank",
        "Kinetic Dampener", "Leeching seed", "Luminous Shot", "Noxious Thorn", "Razorwire", "Shuriken"
    ],

    "Red": [
        "57 Leaf Clover", "Aegis", "Alien Head", "Bottled Chaos", "Bens Raincota",
        "Brainstalks", "Brilliant Behemoth", "Ceremonial Dagger",
        "Defensive Microbots", "Dio's Best Friend", "Frost Relic",
        "Hardlight Afterburner", "H3AD-5T v2",
        "Interstellar Desk Plant", "N'kuhana's Opinion",
        "Rejuvenation Rack", "Resonance Disc", "Sentient Meat Hook",
        "Shattering Justice", "Soulbound Catalyst", "Spare Drone Parts",
        "Unstable Tesla Coil", "Wake of Vultures", "Pocket I.C.B.M.",
        "Symbiotic Scorpion", "War Bonds", "Electric Boomerang", "Growth Nectar",
        "Happiest Mask", "Laser Scope", "Network Suffering", "Orphaned Core",
        "Runic Lens", "Sonorous Whispers", "Substantial Duplicator"
    ],

    "Yellow": [
        "Charged Perforator", "Defense Nucleus", "Empathy Cores",
        "Genesis Loop", "Little Disciple", "Mired Urn",
        "Molten Perforator", "Planula", "Queen's Gland",
        "Shatterspleen", "Titanic Knurl", "Faulty Conductor", "Funtional Coupler",
        "Mycelium cap", "Whispering fragment"
    ],

    "Void White": [
        "Lost Seer's Lenses", "Needletick", "Safer Spaces",
        "Encrusted Key", "Weeping Fungus"
    ],

    "Void Green": [
        "Plasma Shrimp", "Singularity Band", "Tentabauble",
        "Voidsent Flame", "Polylute", "Lysate"
    ],

    "Void Red": [
        "Pluripotent Larva", "Benthic Bloom"
    ],

    "Lunar": [
        "Beads of Fealty", "Brittle Crown", "Corpsebloom",
        "Defiant Gouge", "Focused Convergence",
        "Gesture of the Drowned", "Hooks of Heresy",
        "Light Flux Pauldron", "Mercurial Rachis", "Purity",
        "Shaped Glass", "Stone Flux Pauldron", "Strides of Heresy",
        "Transcendence", "Visions of Heresy", "Egocentrism",
        "Eulogy Zero", "Essence of Heresy",
        "long Standing Solitude", "neutronium weight"
    ],

    "Hallow": [
        "Corpse Lily", "Dream Crucible", "Earthbound Vessel",
        "Infernal Mark", "Nightmare Demon", "Ritual Helmet",
        "Sanguine Chalice", "Stained Scimitar", "Totem of Avarice",
        "Vengeful Spirit", "Vile Censer"
    ],

    "Page": [
        "Clarity", "Dark Alchemy", "Fanatic Summons", "Purify",
        "Reincarnation", "Shadow Cloak", "Warp Gate"
    ],

    "Equipment": [
        "The Back-up", "Blast Shower", "Crowdfunder",
        "Disposable Missile Launcher", "Eccentric Vase",
        "Foreign Fruit", "Forgive Me Please",
        "Gnarled Woodsprite", "Goobo Jr.", "Gorag's Opus",
        "Helfire Tincture", "Jade Elephant", "Milky Chrysalis",
        "Ocular HUD", "Primordial Cube",
        "Radar Scanner", "Royal Capacitor", "Sawmerang",
        "Spinel Tonic", "The Trophy Hunter's Tricorn", "Volcanic Egg",
        "Effigy of Grief", "Glowing Meteorite", "Molotov (6-Pack)",
        "Deus Ex Machina", "Executive Card", "Remote Caffinator", "Super massive leech",
        "Totem of Sacrifice"
    ]
}

CATEGORY_COLORS = {
    "White": (220, 225, 235),
    "Green": (70, 220, 120),
    "Red": (255, 75, 95),
    "Yellow": (255, 210, 65),
    "Void White": (180, 120, 255),
    "Void Green": (150, 90, 245),
    "Void Red": (200, 70, 255),
    "Lunar": (95, 165, 255),
    "Hallow": (255, 105, 180),
    "Page": (100, 240, 230),
    "Equipment": (255, 155, 65)
}

selected_items = {
    category: random.choice(items)
    for category, items in ITEMS.items()
}

copy_message = ""
copy_message_until = 0


def randomize_slot(category):
    selected_items[category] = random.choice(ITEMS[category])


def randomize_all():
    for category in ITEMS:
        randomize_slot(category)


def copy_to_clipboard():
    global copy_message, copy_message_until

    lines = [
        "Risk of Rain 2 - Randomized Build",
        ""
    ]

    for category, item in selected_items.items():
        lines.append(f"{category}: {item}")

    text = "\n".join(lines) + "\n"

    try:
        if shutil.which("wl-copy"):
            command = ["wl-copy"]
        elif shutil.which("xclip"):
            command = ["xclip", "-selection", "clipboard"]
        else:
            raise RuntimeError(
                "Install xclip or wl-clipboard first."
            )

        subprocess.run(
            command,
            input=text,
            text=True,
            check=True,
            timeout=3
        )

        copy_message = "Build copied!"
        print("Copied build:\n" + text)

    except (subprocess.SubprocessError, OSError, RuntimeError) as error:
        copy_message = "Copy failed!"
        print(f"Clipboard error: {error}")

    copy_message_until = pygame.time.get_ticks() + 2000


MARGIN = 35
GAP = 18
COLUMNS = 3
CARD_WIDTH = (
    WIDTH - MARGIN * 2 - GAP * (COLUMNS - 1)
) // COLUMNS
CARD_HEIGHT = 145
START_Y = 145

categories = list(ITEMS.keys())
cards = {}

for index, category in enumerate(categories):
    row = index // COLUMNS
    col = index % COLUMNS

    x = MARGIN + col * (CARD_WIDTH + GAP)
    y = START_Y + row * (CARD_HEIGHT + GAP)

    cards[category] = pygame.Rect(
        x, y, CARD_WIDTH, CARD_HEIGHT
    )

ALL_BUTTON = pygame.Rect(
    WIDTH // 2 - 115, HEIGHT - 65, 230, 42
)

COPY_BUTTON = pygame.Rect(
    WIDTH - MARGIN - 190, HEIGHT - 65, 190, 42
)
VOLUME_TRACK = pygame.Rect(MARGIN + 85, HEIGHT - 48, 120, 8)
volume = 0.5


def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


def draw_wrapped_text(text, font, color, rect, max_chars=24):
    lines = textwrap.wrap(text, width=max_chars) or [text]
    lines = lines[:2]

    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    y = rect.centery - total_height // 2

    for line in lines:
        surface = font.render(line, True, color)
        text_rect = surface.get_rect(
            center=(rect.centerx, y + line_height // 2)
        )
        screen.blit(surface, text_rect)
        y += line_height


def draw_card(category, rect, mouse_pos):
    accent = CATEGORY_COLORS[category]
    hovering = rect.collidepoint(mouse_pos)
    panel_color = PANEL_HOVER if hovering else PANEL

    pygame.draw.rect(
        screen, panel_color, rect, border_radius=12
    )
    pygame.draw.rect(
        screen, accent, rect, width=2, border_radius=12
    )

    draw_text(
        category.upper(), category_font, accent,
        rect.centerx, rect.y + 25, center=True
    )

    pygame.draw.line(
        screen, (65, 75, 95),
        (rect.x + 15, rect.y + 48),
        (rect.right - 15, rect.y + 48)
    )

    item_rect = pygame.Rect(
        rect.x + 12, rect.y + 53,
        rect.width - 24, 43
    )

    draw_wrapped_text(
        selected_items[category], item_font, WHITE, item_rect
    )

    button_rect = pygame.Rect(
        rect.centerx - 65, rect.bottom - 35, 130, 25
    )

    button_hover = button_rect.collidepoint(mouse_pos)
    button_color = accent if button_hover else (40, 48, 65)

    pygame.draw.rect(
        screen, button_color, button_rect, border_radius=6
    )

    text_color = BACKGROUND if button_hover else WHITE

    draw_text(
        "RANDOMIZE", button_font, text_color,
        button_rect.centerx, button_rect.centery, center=True
    )

    return button_rect


def draw_interface():
    screen.fill(BACKGROUND)
    mouse_pos = pygame.mouse.get_pos()

    draw_text(
        "RISK OF RAIN 2", title_font, CYAN,
        WIDTH // 2, 35, center=True
    )

    draw_text(
        "ITEM RANDOMIZER", category_font, PINK,
        WIDTH // 2, 70, center=True
    )

    draw_text(
        "Roll your build. Embrace the chaos.",
        subtitle_font, MUTED, WIDTH // 2, 105, center=True
    )

    individual_buttons = {}

    for category, rect in cards.items():
        individual_buttons[category] = draw_card(
            category, rect, mouse_pos
        )

    all_hovering = ALL_BUTTON.collidepoint(mouse_pos)
    all_color = CYAN if all_hovering else (35, 100, 120)

    pygame.draw.rect(
        screen, all_color, ALL_BUTTON, border_radius=10
    )

    draw_text(
        "RANDOMIZE ALL", button_font,
        BACKGROUND if all_hovering else WHITE,
        ALL_BUTTON.centerx, ALL_BUTTON.centery, center=True
    )

    copy_hovering = COPY_BUTTON.collidepoint(mouse_pos)
    copy_color = GREEN if copy_hovering else (35, 100, 75)

    pygame.draw.rect(
        screen, copy_color, COPY_BUTTON, border_radius=10
    )

    draw_text(
        "COPY TO CLIPBOARD", button_font,
        BACKGROUND if copy_hovering else WHITE,
        COPY_BUTTON.centerx, COPY_BUTTON.centery, center=True
    )

    draw_text(
        "VOLUME", button_font, MUTED,
        MARGIN + 25, VOLUME_TRACK.centery, center=True
    )
    pygame.draw.rect(screen, (65, 75, 95), VOLUME_TRACK, border_radius=4)
    volume_fill = VOLUME_TRACK.copy()
    volume_fill.width = round(VOLUME_TRACK.width * volume)
    pygame.draw.rect(screen, CYAN, volume_fill, border_radius=4)
    pygame.draw.circle(
        screen, WHITE,
        (VOLUME_TRACK.x + round(VOLUME_TRACK.width * volume), VOLUME_TRACK.centery),
        8
    )
    draw_text(
        f"{round(volume * 100)}%", subtitle_font, WHITE,
        VOLUME_TRACK.right + 18, VOLUME_TRACK.centery, center=True
    )

    if pygame.time.get_ticks() < copy_message_until:
        message_color = (
            GREEN if copy_message == "Build copied!" else RED
        )

        draw_text(
            copy_message, subtitle_font, message_color,
            WIDTH // 2, HEIGHT - 85, center=True
        )

    pygame.display.flip()
    return individual_buttons


def main():
    global volume

    music_path = Path(__file__).with_name(
        "ryan-walz-main-version-01-34-3632.mp3"
    )
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    running = True
    dragging_volume = False

    while running:
        clock.tick(FPS)
        individual_buttons = draw_interface()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    randomize_all()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if VOLUME_TRACK.inflate(16, 20).collidepoint(event.pos):
                        dragging_volume = True
                        volume = max(0, min(
                            1, (event.pos[0] - VOLUME_TRACK.x) / VOLUME_TRACK.width
                        ))
                        pygame.mixer.music.set_volume(volume)

                    elif COPY_BUTTON.collidepoint(event.pos):
                        copy_to_clipboard()

                    elif ALL_BUTTON.collidepoint(event.pos):
                        randomize_all()

                    else:
                        for category, button_rect in (
                            individual_buttons.items()
                        ):
                            if button_rect.collidepoint(event.pos):
                                randomize_slot(category)
                                break

            elif event.type == pygame.MOUSEMOTION and dragging_volume:
                volume = max(0, min(
                    1, (event.pos[0] - VOLUME_TRACK.x) / VOLUME_TRACK.width
                ))
                pygame.mixer.music.set_volume(volume)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_volume = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
