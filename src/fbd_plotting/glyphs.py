from typing import Union
from shapely import Point, LineString, Polygon, box, MultiLineString, GeometryCollection

def get_backgrounds(
    anchor_point: Union[tuple[float, float], Point],
    horz: bool,
    vert: bool,
    glyph_width: int | float,
    n_ticks: int = 4
) -> tuple[LineString, MultiLineString]:
    """
    Returns a shapely GeometryCollection representing a xxx-support
    glyph anchored at 'anchor_point' and aligned according to 'horz'
    and 'vert'.

    'anchor_point': the point the glyph shoudl be located at
    'horz': If True, a glyph for a horizontal element will be drawn
    'vert': If True, a glyph for a vertical element will be drawn
    'glyph_width': total width of glyph
    """
    if isinstance(anchor_point, Point):
        ap = anchor_point.coords
    else:
        ap = anchor_point
    apx, apy = ap
    gw = glyph_width
    sh = get_support_height(gw)
    sw = get_support_width(gw)
    ge = get_ground_elevation(apx, apy, sh, horz, vert)
    sc = get_support_center(apx, apy, horz, vert)
    sg = get_support_ground(gw, ge, sc, horz, vert)
    ticks = get_ground_ticks(n_ticks, gw, ge, sc, horz, vert)
    return {
        'apx': apx,
        'apy': apy,
        'sh': sh,
        'sw': sw,
        'ge': ge,
        'sc': sc,
        'ground_glyph': sg,
        'ticks_glyph': ticks,
    }


def pin_support_glyph(
    anchor_point: Union[tuple[float, float], Point],
    horz: bool,
    vert: bool,
    glyph_width: int | float,
    n_ticks: int = 4
) -> GeometryCollection:
    """
    Returns a shapely GeometryCollection representing a pin-support
    glyph anchored at 'anchor_point' and aligned according to 'horz'
    and 'vert'.

    'anchor_point': the point the glyph shoudl be located at
    'horz': If True, a glyph for a horizontal element will be drawn
    'vert': If True, a glyph for a vertical element will be drawn
    'glyph_width': total width of glyph
    'n_ticks': number of ground ticks
    """
    bg = background_data = get_backgrounds(anchor_point, horz, vert, glyph_width, n_ticks)
    pg = get_pin_glyph(bg['sc'], bg['sw'], bg['ge'], bg['sh'], horz, vert)
    return GeometryCollection([pg, bg['ground_glyph'], bg['ticks_glyph']])


def roller_support_glyph(
    anchor_point: Union[tuple[float, float], Point],
    horz: bool,
    vert: bool,
    glyph_width: int | float,
    n_ticks: int = 4
) -> GeometryCollection:
    """
    Returns a shapely GeometryCollection representing a roller-support
    glyph anchored at 'anchor_point' and aligned according to 'horz'
    and 'vert'.

    'anchor_point': the point the glyph shoudl be located at
    'horz': If True, a glyph for a horizontal element will be drawn
    'vert': If True, a glyph for a vertical element will be drawn
    'glyph_width': total width of glyph
    'n_ticks': number of ground ticks
    """
    bg = background_data = get_backgrounds(anchor_point, horz, vert, glyph_width, n_ticks)
    rg = get_roller_glyph(bg['sc'], bg['ge'], bg['sh'], horz, vert)
    return GeometryCollection([rg, bg['ground_glyph'], bg['ticks_glyph']])


def fix_support_glyph(
    anchor_point: Union[tuple[float, float], Point],
    horz: bool,
    vert: bool,
    glyph_width: int | float,
    n_ticks: int = 4
) -> GeometryCollection:
    """
    Returns a shapely GeometryCollection representing a fix-support
    glyph anchored at 'anchor_point' and aligned according to 'horz'
    and 'vert'.

    'anchor_point': the point the glyph shoudl be located at
    'horz': If True, a glyph for a horizontal element will be drawn
    'vert': If True, a glyph for a vertical element will be drawn
    'glyph_width': total width of glyph
    'n_ticks': number of ground ticks
    """
    bg = background_data = get_backgrounds(anchor_point, horz, vert, glyph_width, n_ticks)
    fg = get_fixed_glyph(bg['sc'], bg['sw'], bg['ge'], bg['sh'], horz, vert)
    return GeometryCollection([fg, bg['ground_glyph'], bg['ticks_glyph']])


def get_pin_glyph(sc: float, sw: float, ge: float, sh: float, horz: bool, vert: bool) -> Polygon:
    """
    Returns a pin glyph as a polygon

    'sc': support_center
    'sw': support_width
    'ge': ground_elevation
    'sh': support_height
    'horz': True for a support fora horizontal element
    'vert': True if a support for a vertical element
    """
    x0 = horz * (sc - sw / 2) + vert * (ge)
    y0 = horz * (ge) + vert * (sc - sw / 2)
    x1 = horz * (sc) + vert * (ge + sh)
    y1 = horz * (ge + sh) + vert * (sc)
    x2 = horz * (sc + sw / 2) + vert * (ge) 
    y2 = horz * (ge) + vert * (sc + sw / 2)
    pin = Polygon([[x0, y0], [x1, y1], [x2, y2]])
    return pin


def get_roller_glyph(sc: float, ge: float, sh: float, horz: bool, vert: bool) -> Polygon:
    """
    Returns a roller glyph as a polygon

    'sc': support_center
    'sw': support_width
    'ge': ground_elevation
    'sh': support_height
    'horz': True for a support fora horizontal element
    'vert': True if a support for a vertical element
    """
    x0 = horz * (sc) + vert * (ge + sh / 2)
    y0 = horz * (ge + sh / 2) + vert * (sc)
    roller = Point([x0, y0]).buffer(sh / 2)
    return roller


def get_fixed_glyph(sc: float, sw: float, ge: float, sh: float, horz: bool, vert: bool) -> Polygon:
    """
    Returns a fixed glyph as a polygon

    'sc': support_center
    'sw': support_width
    'ge': ground_elevation
    'sh': support_height
    'horz': True for a support fora horizontal element
    'vert': True if a support for a vertical element
    """
    x0 = horz * (sc - sw / 2) + vert * (ge)
    y0 = horz * (ge) + vert * (sc - sw / 2)
    x1 = horz * (sc + sw / 2) + vert * (ge + sh)
    y1 = horz * (ge + sh) + vert * (sc + sw / 2)
    fixbox = box(x0, y0, x1, y1)
    return fixbox

    # sh = get_support_height(gw)
    # sw = get_support_width(gw)
    # ge = get_ground_elevation(apx, apy, sh, horz, vert)
    # sc = get_support_center(apx, apy, horz, vert)
    # sg = get_support_ground(gw, ge, sc, horz, vert)
    # ticks = get_ground_ticks(n_ticks, gw, ge, sc, horz, vert)

def get_support_height(gw: float) -> float:
    """
    Calculates the support height
    """
    return gw / 2

def get_support_width(gw: float) -> float:
    """
    Calculates the support width
    """
    return gw / 2


def get_support_center(apx: float, apy: float, horz: bool, vert: bool) -> float:
    """
    Calculates the support center
    """
    return horz * (apx) + vert * (apy)

def get_ground_elevation(apx: float, apy: float, sh: float, horz: bool, vert: bool) -> float:
    """
    Calculates the ground elevation
    """
    return horz * (apy  - sh) + vert * (apx - sh)


def get_support_ground(gw: float, ge: float, sc: float, horz: bool, vert: bool) -> LineString:
    """
    Draws the support ground line
    """
    x0 = horz * (sc - gw/2) + vert * ge
    y0 = horz * ge + vert * (sc - gw/2)
    x1 = horz * (sc + gw/2) + vert * ge
    y1 = horz * ge + vert * (sc + gw/2)
    support_ground = LineString([[x0, y0], [x1, y1]])
    return support_ground


def get_ground_ticks(
        n_ticks: int, 
        gw: float, 
        ge: float, 
        sc: float, 
        horz: bool, 
        vert: bool
    ) -> MultiLineString:
    """
    Draws the ground ticks
    """
    tick_depth = td = gw / 5 # An arbitrary ratio
    tick_spacing = ts = gw / (n_ticks - 1)
    tick_width = tw = td # This can be changed to suit taste, currently set to a 45 deg angle
    ticks = []
    for n_tick in range(n_ticks):
        # Draw line with an x-positive bias
        x0 = horz * (sc - gw/2 - tw + n_tick * ts) + vert * (ge - td)
        x1 = horz * (sc - gw/2 + n_tick * ts) + vert * (ge)
        y0 = horz * (ge - td) + vert * (sc - gw/2 - tw + n_tick * ts)
        y1 = horz * (ge) + vert * (sc - gw/2 + n_tick * ts)
        ticks.append(LineString([[x0, y0], [x1, y1]]))
    return MultiLineString(ticks)
