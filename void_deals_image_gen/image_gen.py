from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

RARITY_NAMES = {
    "L": "Legendary",
    "E": "Epic",
    "R": "Rare",
    "C": "Common",
}

RARITY_GRADIENTS = {
    "L": ((243, 207, 81), (197, 122, 29)),
    "E": ((220, 113, 235), (152, 40, 190)),
    "R": ((94, 177, 235), (46, 88, 188)),
    "C": ((228, 228, 228), (151, 151, 151)),
}

# Maps the bot's / API's rarity strings (see rarity2emote in the cog) onto the
# 4-tier gradient system this renderer understands. "perfect" is the bot's
# top tier (a deal at the absolute best possible ratio) and gets folded into
# the Legendary gradient since there's no dedicated "perfect" art asset.
API_RARITY_TO_LETTER = {
    "perfect": "L",
    "legendary": "L",
    "epic": "E",
    "rare": "R",
    "common": "C",
}

# className -> rendering metadata. Mirrors the mapping already used in the
# Discord cog's class2emote / cost2emote / class2name helpers.
CLASS_NAME_MAP = {
    "crate": {
        "output_name": "Void Crate",
        "payment_name": "Crate",
        "main_icon": "void_crate.png",
        "payment_icon": "crate.png",
    },
    "ticket": {
        "output_name": "Void Ticket",
        "payment_name": "Ticket",
        "main_icon": "void_ticket.png",
        "payment_icon": "ticket.png",
    },
    "ticketShard": {
        "output_name": "Void Ticket",
        "payment_name": "Void Shard",
        "main_icon": "void_ticket.png",
        "payment_icon": "void_shard.png",
    },
}

CARD_CENTERS = (168, 458, 748)
COST_ICON_CENTERS = (67, 356, 646)
COST_TEXT_CENTERS = (180, 470, 760)

TITLE_Y = 135
MAIN_ICON_Y = 270
AMOUNT_Y = 356
COST_Y = 429
COST_TEXT_Y = 429

TITLE_FONT_SIZE = 41
NUMBER_FONT_SIZE = 40
PRICE_FONT_SIZE = 40
TITLE_X_SCALE = 1.04
NUMBER_X_SCALE = 0.95
NUMBER_Y_SCALE = 0.90
PRICE_Y_SCALE = 0.96

MAIN_SCALES = {
    "Void Ticket": 0.725,
    "Void Crate": 0.625,
}

COST_SCALES = {
    "Ticket": 0.34,
    "Void Shard": 0.25,
    "Crate": 0.275,
}


def deal_from_api_slot(slot: dict, slot_index: int) -> dict:
    """Convert one slot from the Supabase `void-deals` API response
    (as consumed by get_void_deals() / build_embed_slot_field in the cog)
    into the deal dict shape the renderer expects.

    Expected slot keys: className, amount, cost, rarity.
    """
    class_name = slot["className"]
    if class_name not in CLASS_NAME_MAP:
        raise ValueError(f"Unknown className in API slot: {class_name!r}")

    meta = CLASS_NAME_MAP[class_name]
    rarity_letter = API_RARITY_TO_LETTER.get(slot.get("rarity", "common"), "C")

    return {
        "slot": slot_index,
        "kind": class_name,
        "output_name": meta["output_name"],
        "payment_name": meta["payment_name"],
        "main_icon": meta["main_icon"],
        "payment_icon": meta["payment_icon"],
        "amount": slot["amount"],
        "cost": slot["cost"],
        "rarity": rarity_letter,
    }


def deals_from_api_response(response: dict) -> list[dict]:
    """Convert a full get_void_deals() response into a list of 3 deal dicts,
    ready for render_deals_to_image()."""
    slots = response["result"]["slots"]
    return [deal_from_api_slot(slot, i) for i, slot in enumerate(slots)]


def find_font(explicit: str | None, base_dir: Path) -> Path:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    candidates.extend(
        [
            base_dir / "PIXELADE.ttf",
            base_dir / "assets" / "PIXELADE.ttf",
            Path.cwd() / "PIXELADE.TTF",
            Path("C:/Windows/Fonts/consolab.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
            Path("/System/Library/Fonts/Supplemental/Courier New Bold.ttf"),
        ]
    )

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "No usable font was found. Put PIXELADE.TTF beside the script or inside "
        "assets/, or pass a TrueType font with --font PATH."
    )


def paste_scaled(base: Image.Image, path: Path, center: tuple[int, int], scale: float) -> None:
    icon = Image.open(path).convert("RGBA")
    size = (round(icon.width * scale), round(icon.height * scale))
    icon = icon.resize(size, Image.Resampling.NEAREST)
    pos = (round(center[0] - icon.width / 2), round(center[1] - icon.height / 2))
    base.alpha_composite(icon, pos)


def composite_stretched(
    base: Image.Image,
    layer: Image.Image,
    center: tuple[int, int],
    x_scale: float,
    y_scale: float = 1.0,
    max_width: int | None = None,
) -> None:
    bbox = layer.getbbox()
    if bbox is None:
        return

    cropped = layer.crop(bbox)
    target_width = round(cropped.width * x_scale)
    target_height = round(cropped.height * y_scale)
    if max_width is not None:
        target_width = min(target_width, max_width)
    stretched = cropped.resize(
        (target_width, target_height),
        Image.Resampling.NEAREST,
    )

    x = round(center[0] - stretched.width / 2)
    y = round((bbox[1] + bbox[3]) / 2 - stretched.height / 2)
    base.alpha_composite(stretched, (x, y))


def shadow_trail(offset: tuple[int, int]) -> list[tuple[int, int]]:
    """Return connected pixel steps from the glyph to its cast shadow."""
    dx, dy = offset
    steps = max(abs(dx), abs(dy), 1)
    return [
        (round(dx * step / steps), round(dy * step / steps))
        for step in range(1, steps + 1)
    ]


def draw_white_text(
    base: Image.Image,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.FreeTypeFont,
    stroke: int = 2,
    bold: int = 1,
    shadow: tuple[int, int] = (1, 1),
    x_scale: float = 1.0,
    y_scale: float = 1.0,
) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for trail_x, trail_y in shadow_trail(shadow):
        sx, sy = xy[0] + trail_x, xy[1] + trail_y
        for dx in range(-bold, bold + 1):
            for dy in range(-bold, bold + 1):
                draw.text(
                    (sx + dx, sy + dy),
                    text,
                    font=font,
                    fill=(0, 0, 0, 180),
                    stroke_width=1,
                    stroke_fill=(0, 0, 0, 220),
                    anchor="mm",
                )

    for dx in range(-bold, bold + 1):
        for dy in range(-bold, bold + 1):
            draw.text(
                (xy[0] + dx, xy[1] + dy),
                text,
                font=font,
                fill=(255, 255, 255, 255),
                stroke_width=stroke,
                stroke_fill=(0, 0, 0, 255),
                anchor="mm",
            )

    composite_stretched(base, layer, xy, x_scale, y_scale=y_scale)


def draw_gradient_text(
    base: Image.Image,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.FreeTypeFont,
    top: tuple[int, int, int],
    bottom: tuple[int, int, int],
    stroke: int = 3,
    bold: int = 1,
    slight_bold: bool = False,
    shadow: tuple[int, int] = (4, 4),
    x_scale: float = 1.0,
    y_scale: float = 1.0,
    max_width: int | None = None,
) -> None:
    mask = Image.new("L", base.size, 0)
    mdraw = ImageDraw.Draw(mask)
    bold_offsets = (
        ((0, 0), (1, 0))
        if slight_bold
        else tuple(
            (dx, dy)
            for dx in range(-bold, bold + 1)
            for dy in range(-bold, bold + 1)
        )
    )

    for dx, dy in bold_offsets:
        mdraw.text(
            (xy[0] + dx, xy[1] + dy),
            text,
            font=font,
            fill=255,
            anchor="mm",
        )

    shadow_mask = Image.new("L", base.size, 0)
    sdraw = ImageDraw.Draw(shadow_mask)
    for trail_x, trail_y in shadow_trail(shadow):
        sx, sy = xy[0] + trail_x, xy[1] + trail_y
        for dx, dy in bold_offsets:
            sdraw.text(
                (sx + dx, sy + dy),
                text,
                font=font,
                fill=210,
                anchor="mm",
            )

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))

    shadow_stroke = shadow_mask.filter(ImageFilter.MaxFilter(3))
    shadow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_layer.putalpha(shadow_stroke)
    layer.alpha_composite(shadow_layer)

    stroke_mask = mask.filter(ImageFilter.MaxFilter(stroke * 2 + 1))
    black = Image.new("RGBA", base.size, (0, 0, 0, 255))
    transparent = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.alpha_composite(Image.composite(black, transparent, stroke_mask))

    gradient = Image.new("RGBA", base.size, (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gradient)
    y0, y1 = xy[1] - 14, xy[1] + 14

    for y in range(max(0, y0), min(base.height, y1 + 1)):
        t = (y - y0) / max(1, y1 - y0)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        gdraw.line((0, y, base.width, y), fill=(*color, 255))

    layer.alpha_composite(Image.composite(gradient, transparent, mask))
    composite_stretched(
        base,
        layer,
        xy,
        x_scale,
        y_scale=y_scale,
        max_width=max_width,
    )


def render_deals_to_image(
    deals: list[dict],
    template_path: Path,
    assets_dir: Path,
    font_path: Path,
    output_path: Path,
) -> None:
    """Render a Daily Deals shop image from an already-prepared list of deal
    dicts (each needs: slot, output_name, payment_name, main_icon,
    payment_icon, amount, cost, rarity). This is the function you want to
    call with data coming from get_void_deals() / deals_from_api_response()."""
    image = Image.open(template_path).convert("RGBA")
    title_font = ImageFont.truetype(str(font_path), TITLE_FONT_SIZE)
    number_font = ImageFont.truetype(str(font_path), NUMBER_FONT_SIZE)
    price_font = ImageFont.truetype(str(font_path), PRICE_FONT_SIZE)

    for deal in deals:
        slot = deal["slot"]
        cx = CARD_CENTERS[slot]
        rarity = deal["rarity"]

        top, bottom = RARITY_GRADIENTS[rarity]
        draw_gradient_text(
            image,
            deal["output_name"],
            (cx, TITLE_Y),
            title_font,
            top,
            bottom,
            x_scale=TITLE_X_SCALE,
            max_width=260,
        )

        paste_scaled(
            image,
            assets_dir / deal["main_icon"],
            (cx, MAIN_ICON_Y),
            MAIN_SCALES[deal["output_name"]],
        )

        number_top = number_bottom = (255, 255, 255)
        draw_gradient_text(
            image,
            f'x{deal["amount"]}',
            (cx, AMOUNT_Y),
            number_font,
            number_top,
            number_bottom,
            stroke=2,
            x_scale=NUMBER_X_SCALE,
            y_scale=NUMBER_Y_SCALE,
        )

        paste_scaled(
            image,
            assets_dir / deal["payment_icon"],
            (COST_ICON_CENTERS[slot], COST_Y),
            COST_SCALES[deal["payment_name"]],
        )

        draw_gradient_text(
            image,
            str(deal["cost"]),
            (COST_TEXT_CENTERS[slot], COST_TEXT_Y),
            price_font,
            number_top,
            number_bottom,
            stroke=2,
            bold=0,
            x_scale=NUMBER_X_SCALE,
            y_scale=PRICE_Y_SCALE,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def render_shop_from_api(
    response: dict,
    shop_date: date,
    template_path: Path,
    assets_dir: Path,
    font_path: Path,
    output_path: Path,
) -> list[dict]:
    """Convenience wrapper: takes a raw get_void_deals() response dict,
    converts it, renders the image, and returns the deal dicts used
    (handy for logging/debugging, same as the old script's return value)."""
    deals = deals_from_api_response(response)
    render_deals_to_image(deals, template_path, assets_dir, font_path, output_path)
    return deals


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Date must be YYYY-MM-DD") from exc


def generate_image(date: datetime):
    from chestii.void_deals import get_void_deals, get_last_reset_time

    base_dir = Path(__file__).resolve().parent
    assets_dir = base_dir / "assets"
    template = assets_dir / "deals_template.png"
    font = find_font(None, base_dir)

    if date is not None:
        response = get_void_deals(date)
        shop_date = date
    else:
        response = get_void_deals()
        shop_date = get_last_reset_time().date()

    output = (base_dir / "generated images" / f"daily_deals_{shop_date:%Y-%m-%d}.png")

    deals = render_shop_from_api(response, shop_date, template, assets_dir, font, output)

    print(f"Daily Deals for {shop_date:%Y-%m-%d}")
    for deal in deals:
        rarity = RARITY_NAMES[deal["rarity"]]
        ratio = deal["cost"] / deal["amount"]
        print(
            f"Slot {deal['slot'] + 1}: {rarity} {deal['output_name']} x{deal['amount']} "
            f"for {deal['cost']} {deal['payment_name']} (ratio {ratio:.2f})"
        )

    print(f"Saved: {output}")
    return output