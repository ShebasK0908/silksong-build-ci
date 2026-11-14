#!/usr/bin/env python3
"""Parche de build para Silksong (aplicado al clon de nxnative antes de compilar):

1. Traduce al español los textos del lanzador DmIOS (settings.tsv sin tocar la
   columna de sección, Launcher.swift con los títulos traducidos al mostrarlos,
   front_ios.m). Los ajustes por defecto NO se tocan: el perfil probado de
   upstream para Silksong (docked 1080p, 60 fps en iPhone) queda tal cual.
2. Controles táctiles «tipo Android» SOLO para Silksong (DM_GAME_ID
   010013C00E930000), dentro de dm/ios/Sources/DmGamepad.m: la disposición del
   port chino de Android (joystick abajo-izquierda; dash ancho y SELECT a media
   izquierda; mapa, MENU y arpón arriba/derecha; 6 botones redondos con
   pictogramas a la derecha). Todo vive tras un gate por título y reutiliza los
   índices B_* existentes (su orden es el orden de bits del host: no tocarlo).
   Asignación zona->bit (verificada con las guías de controles del juego):
   dash=ZR, arpón=ZL, mapa=L, SELECT=-, y los redondos: +=pausa, X=Needolin,
   B=saltar, A=curar, R=herramienta, Y=atacar.

Falla con error si alguna cadena esperada no aparece, para detectar cambios
de upstream. Uso: python3 parche_silksong.py <ruta-al-clon-de-nxnative>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
missing = []


def patch(relpath, pairs):
    p = root / relpath
    text = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old not in text:
            missing.append(f"{relpath}: no encontrado: {old!r}")
        else:
            text = text.replace(old, new)
    p.write_text(text, encoding="utf-8")


TSV = "dm/games/settings.tsv"

patch(TSV, [
    ("1=Docked,0=Handheld", "1=Televisor,0=Portátil"),
    ("0=Window,1=Fullscreen", "0=Ventana,1=Pantalla completa"),
    ("fit=Fit,fill=Fill", "fit=Ajustar,fill=Rellenar"),
    ("off=Standard,metalfx=MetalFX", "off=Estándar,metalfx=MetalFX"),
    ("game=Game's own,metalfx=MetalFX", "game=El del juego,metalfx=MetalFX"),
    ("auto=Match screen", "auto=Según la pantalla"),
    ("iPhone Duo screen (1.43:1)", "pantalla iPhone Duo (1,43:1)"),
    ("Frame rate", "Velocidad de fotogramas"),
    ("Dynamic resolution", "Resolución dinámica"),
    ("Render scale", "Escala de render"),
    ("Console mode", "Modo de consola"),
    ("Upscaling", "Reescalado"),
    ("Game's upscaler", "Reescalado del juego"),
    ("Game language", "Idioma del juego"),
    ("Display mode", "Modo de pantalla"),
    ("Picture shape", "Forma de la imagen"),
    ("\tPicture\t", "\tImagen\t"),
    ("Frame-rate counter", "Contador de FPS"),
    ("Touch feedback", "Vibración táctil"),
    ("Game rumble", "Vibración del juego"),
    ("Rumble strength", "Intensidad de la vibración"),
    ("Rumble cutoff", "Corte de vibración"),
    ("Press a button to join", "Pulsa un botón para unirte"),
    ("Switch 2 controllers", "Mandos de Switch 2"),
    ("Frame buffering", "Buffer de fotogramas"),
    ("Metal 4 pipelines", "Pipelines Metal 4"),
    ("Pipeline prebuild", "Precompilación de pipelines"),
    ("Encode thread", "Hilo de codificación"),
    ("Hold frames when late", "Retener fotogramas si hay retraso"),
    ("Performance HUD", "HUD de rendimiento"),
    ("Lets the game lower its resolution under load. Turn off to keep full resolution for the selected console mode.",
     "Permite que el juego baje su resolución cuando va cargado. Desactívalo para mantener la resolución completa del modo de consola elegido."),
    ("Uses more GPU time and can increase heat.",
     "Usa más tiempo de GPU y puede aumentar el calor."),
    ("Fill crops the game's 16:9 picture to cover the screen. Health bars, subtitles or maps near the edges can be cut off. A full-screen picture without cropping needs a patch for each game.",
     "Rellenar recorta la imagen 16:9 del juego para cubrir la pantalla. Las barras de vida, los subtítulos o los mapas cerca de los bordes pueden cortarse. Una imagen a pantalla completa sin recorte necesita un parche para cada juego."),
    ("Plays Joy-Con 2 and Pro Controller 2 over Bluetooth: hold Sync on one during the game to pair it. macOS asks once for Bluetooth access.",
     "Juega con Joy-Con 2 y Pro Controller 2 por Bluetooth: mantén Sync en uno durante el juego para enlazarlo. macOS pide el acceso Bluetooth una vez."),
    ("Renders about a quarter more pixels: a little slower and warmer.",
     "Renderiza una cuarta parte más de píxeles: un poco más lento y más caliente."),
    ("Up to one frame more display latency.",
     "Hasta un fotograma más de latencia de pantalla."),
    ("Keeps a pipeline archive; uses more memory.",
     "Mantiene un archivo de pipelines; usa más memoria."),
    ("The first start waits a few minutes for it, once.",
     "El primer inicio espera unos minutos por ello, una sola vez."),
])

patch("dm/ios/Sources/Launcher.swift", [
    ("Section(section) {",
     'Section(["Game": "Juego", "Controls": "Controles", "Performance": "Rendimiento"][section] ?? section) {'),
    ('"Play"', '"Jugar"'),
    ("Reset to tested defaults", "Restablecer los valores probados"),
    ("Brings back all settings this game was tested with.",
     "Recupera todos los ajustes con los que se probó este juego."),
    ("Memory available", "Memoria disponible"),
    ("Cloud saves", "Guardados en la nube"),
    ("Checking the cloud save", "Comprobando el guardado en la nube"),
    ("Choose a different folder", "Elige otra carpeta"),
    ("Choose a folder in iCloud Drive", "Elige una carpeta en iCloud Drive"),
    ("Saved. The game uses this folder when you press Play.",
     "Guardado. El juego usa esta carpeta cuando pulsas Jugar."),
    ("That folder could not be remembered", "No se pudo recordar esa carpeta"),
    ("try a different one.", "prueba con otra."),
    ("Turn off cloud saves", "Desactivar los guardados en la nube"),
    ("Play This iPhone's Save", "Jugar con la partida de este iPhone"),
    ("Play Without It", "Jugar sin ella"),
    ("Try Again", "Intentar de nuevo"),
    ('"Cancel"', '"Cancelar"'),
    ('"Version \\(', '"Versión \\('),
])

patch("dm/ios/Sources/front_ios.m", [
    ("Game files unusable.", "Los archivos del juego no se pueden usar."),
    ('"Game files"', '"Archivos del juego"'),
    ("Tap to start", "Toca para empezar"),
    ("Open the app again to start", "Abre la app otra vez para empezar"),
    ("The game restarts.", "El juego se reinicia."),
    ("Open the app again to continue.", "Abre la app otra vez para continuar."),
    ("Starting %@", "Iniciando %@"),
    ("This device is not supported.", "Este dispositivo no es compatible."),
    ('"Save failed"', '"Error al guardar"'),
    ("Saving failed (errno %d); progress was not saved.",
     "Error al guardar (errno %d); el progreso no se guardó."),
    ('"Cancel"', '"Cancelar"'),
])

# ---------------------------------------------------------------------------
# Controles tipo Android para Silksong (un solo fichero: DmGamepad.m)
# ---------------------------------------------------------------------------

GATE = r'''
// ---- Controles tactiles tipo Android, solo Silksong (build privada del usuario) ----
// Disposicion del port chino de Silksong para Android sobre el layout 2D: joystick
// abajo-izquierda; dash ancho (ZR) y SELECT (-) a media izquierda; mapa (L), MENU
// (el engranaje de DmIOS) y arpon (ZL) arriba a la derecha; 6 redondos con
// pictogramas a la derecha: + (pausa), X (Needolin), B (saltar), A (curar),
// R (herramienta), Y (atacar). Los indices B_* no se tocan: su orden es el de
// los bits DM_BTN_* del host. Todo vive tras este gate; el resto de juegos y
// los modos 3D/Tap quedan como estan.
#ifndef DM_GAME_ID
#define DM_GAME_ID ""
#endif
static BOOL silkPad(void) { return !strcmp(DM_GAME_ID, "010013C00E930000"); }
static BOOL silkBit(int b) { switch (b) { case B_A: case B_B: case B_X: case B_Y: case B_L: case B_R: case B_ZL: case B_ZR: case B_PLUS: case B_MINUS: return YES; default: return NO; } }
'''

HELPERS = r'''- (BOOL)silkActive { return silkPad() && !_full && !_tap && !_layout.separated; }
- (CGFloat)silkRoundR { return 0.0485 * _layout.controls.size.width; }
- (CGFloat)silkMenuR { return 0.0235 * _layout.controls.size.width; }
- (CGRect)silkRectFor:(int)b { CGRect c = _layout.controls; CGFloat x = CGRectGetMinX(c), y = CGRectGetMinY(c), w = c.size.width, h = c.size.height;
    switch (b) { case B_ZR: return CGRectMake(x + 0.037 * w, y + 0.263 * h, 0.106 * w, 0.110 * h);
        case B_L: return CGRectMake(x + 0.866 * w, y + 0.032 * h, 0.103 * w, 0.101 * h);
        case B_ZL: return CGRectMake(x + 0.866 * w, y + 0.198 * h, 0.103 * w, 0.115 * h);
        default: return CGRectMake(x + 0.162 * w, y + 0.268 * h, 0.047 * w, 0.100 * h); } }   // B_MINUS (SELECT)
- (CGPoint)silkCenterFor:(int)b { CGRect c = _layout.controls; CGFloat x = CGRectGetMinX(c), y = CGRectGetMinY(c), w = c.size.width, h = c.size.height;
    switch (b) { case B_PLUS: return CGPointMake(x + 0.818 * w, y + 0.462 * h);
        case B_X: return CGPointMake(x + 0.919 * w, y + 0.433 * h);
        case B_B: return CGPointMake(x + 0.807 * w, y + 0.667 * h);
        case B_A: return CGPointMake(x + 0.916 * w, y + 0.613 * h);
        case B_R: return CGPointMake(x + 0.805 * w, y + 0.852 * h);
        default: return CGPointMake(x + 0.918 * w, y + 0.843 * h); } }   // B_Y
- (CGPathRef)silkGlyphFor:(int)b {   // pictogramas de trazo, en coordenadas de la vista (el llamante libera)
    CGMutablePathRef p = CGPathCreateMutable();
    if (b == B_ZL || b == B_ZR || b == B_L) { CGRect rc = [self silkRectFor:b]; CGFloat w = rc.size.width, h = rc.size.height, mx = CGRectGetMidX(rc), my = CGRectGetMidY(rc);
        if (b == B_ZR) { for (int i = 0; i < 3; i++) { CGFloat yy = my + (i - 1) * 0.18 * h; CGPathMoveToPoint(p, NULL, CGRectGetMinX(rc) + 0.14 * w, yy); CGPathAddLineToPoint(p, NULL, CGRectGetMinX(rc) + (0.52 - 0.08 * i) * w, yy); }
            CGPathMoveToPoint(p, NULL, mx + 0.16 * w, my - 0.22 * h); CGPathAddLineToPoint(p, NULL, mx + 0.38 * w, my); CGPathAddLineToPoint(p, NULL, mx + 0.16 * w, my + 0.22 * h); CGPathCloseSubpath(p);
        } else if (b == B_ZL) { CGPathAddEllipseInRect(p, NULL, CGRectMake(CGRectGetMinX(rc) + 0.06 * w, my - 0.10 * w, 0.20 * w, 0.20 * w));
            CGPathMoveToPoint(p, NULL, CGRectGetMinX(rc) + 0.30 * w, my - 0.26 * h); CGPathAddLineToPoint(p, NULL, CGRectGetMinX(rc) + 0.88 * w, my); CGPathAddLineToPoint(p, NULL, CGRectGetMinX(rc) + 0.30 * w, my + 0.26 * h); CGPathAddLineToPoint(p, NULL, CGRectGetMinX(rc) + 0.44 * w, my); CGPathCloseSubpath(p);
        } else { CGRect in = CGRectInset(rc, 0.10 * w, 0.18 * h); CGPathAddRoundedRect(p, NULL, in, 6, 6);
            CGPathAddEllipseInRect(p, NULL, CGRectMake(CGRectGetMinX(rc) + 0.01 * w, my - 0.09 * w, 0.18 * w, 0.18 * w));
            CGPathAddEllipseInRect(p, NULL, CGRectMake(CGRectGetMaxX(rc) - 0.19 * w, my - 0.09 * w, 0.18 * w, 0.18 * w)); }
        return p; }
    CGPoint c = [self silkCenterFor:b]; CGFloat r = [self silkRoundR];
    switch (b) {
        case B_Y: CGPathMoveToPoint(p, NULL, c.x - 0.50 * r, c.y + 0.50 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.34 * r, c.y - 0.34 * r);
            CGPathAddEllipseInRect(p, NULL, CGRectMake(c.x + 0.34 * r, c.y - 0.60 * r, 0.26 * r, 0.26 * r)); break;
        case B_B: CGPathMoveToPoint(p, NULL, c.x - 0.44 * r, c.y + 0.26 * r); CGPathAddLineToPoint(p, NULL, c.x, c.y - 0.34 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.44 * r, c.y + 0.26 * r);
            CGPathMoveToPoint(p, NULL, c.x - 0.44 * r, c.y + 0.54 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.44 * r, c.y + 0.54 * r); break;
        case B_A: CGPathAddEllipseInRect(p, NULL, CGRectMake(c.x - 0.44 * r, c.y - 0.44 * r, 0.88 * r, 0.88 * r));
            CGPathAddEllipseInRect(p, NULL, CGRectMake(c.x - 0.17 * r, c.y - 0.17 * r, 0.34 * r, 0.34 * r)); break;
        case B_X: CGPathMoveToPoint(p, NULL, c.x - 0.55 * r, c.y - 0.12 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.55 * r, c.y - 0.12 * r);
            CGPathAddEllipseInRect(p, NULL, CGRectMake(c.x - 0.52 * r, c.y - 0.22 * r, 0.20 * r, 0.20 * r));
            CGPathMoveToPoint(p, NULL, c.x - 0.50 * r, c.y + 0.30 * r); CGPathAddQuadCurveToPoint(p, NULL, c.x - 0.25 * r, c.y + 0.04 * r, c.x, c.y + 0.30 * r); CGPathAddQuadCurveToPoint(p, NULL, c.x + 0.25 * r, c.y + 0.56 * r, c.x + 0.50 * r, c.y + 0.30 * r); break;
        case B_R: CGPathMoveToPoint(p, NULL, c.x + 0.12 * r, c.y - 0.55 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.30 * r, c.y + 0.12 * r); CGPathAddLineToPoint(p, NULL, c.x - 0.02 * r, c.y + 0.26 * r); CGPathCloseSubpath(p);
            CGPathMoveToPoint(p, NULL, c.x - 0.02 * r, c.y + 0.26 * r); CGPathAddLineToPoint(p, NULL, c.x - 0.28 * r, c.y + 0.52 * r); break;
        default: CGPathMoveToPoint(p, NULL, c.x - 0.18 * r, c.y - 0.40 * r); CGPathAddLineToPoint(p, NULL, c.x - 0.18 * r, c.y + 0.40 * r);
            CGPathMoveToPoint(p, NULL, c.x + 0.18 * r, c.y - 0.40 * r); CGPathAddLineToPoint(p, NULL, c.x + 0.18 * r, c.y + 0.40 * r); break;   // B_PLUS: pausa
    }
    return p; }
'''

LAYOUT_BLOCK = r'''    if ([self silkActive]) {
        for (int b = 0; b < B_N; b++) { _glyph[b].hidden = !silkBit(b) || b == B_MINUS; _glyph[b].lineWidth = 2.2 * u; if (_label[b]) _label[b].hidden = b != B_MINUS; }
        setPath(_key[B_ZL], CGPathCreateWithRoundedRect([self silkRectFor:B_ZL], 14 * u, 14 * u, NULL));
        setPath(_key[B_ZR], CGPathCreateWithRoundedRect([self silkRectFor:B_ZR], 14 * u, 14 * u, NULL));
        setPath(_key[B_L], CGPathCreateWithRoundedRect([self silkRectFor:B_L], 14 * u, 14 * u, NULL));
        setPath(_key[B_R], circlePath([self silkCenterFor:B_R], [self silkRoundR]));
        setPath(_key[B_PLUS], circlePath([self silkCenterFor:B_PLUS], [self silkRoundR]));
        _label[B_MINUS].string = @"SELECT"; placeLabel(_label[B_MINUS], CGPointMake(CGRectGetMidX([self silkRectFor:B_MINUS]), CGRectGetMidY([self silkRectFor:B_MINUS])), 11 * u);
        _menu.frame = CGRectMake(mc.x - [self silkMenuR], mc.y - [self silkMenuR], 2 * [self silkMenuR], 2 * [self silkMenuR]); _menu.layer.cornerRadius = [self silkMenuR];
        _menu.layer.shadowPath = [UIBezierPath bezierPathWithOvalInRect:_menu.bounds].CGPath;
        CGFloat kr = [self stickR:0] * 0.4; _knob.bounds = CGRectMake(0, 0, 2 * kr, 2 * kr); setPath(_knob, circlePath(CGPointMake(kr, kr), kr));
        CAShapeLayer *kin = (CAShapeLayer *)_knob.sublayers.firstObject; CGPathRef kip = circlePath(CGPointMake(kr, kr), kr * 0.62); kin.frame = _knob.bounds; kin.path = kip; CGPathRelease(kip);
        for (int b = 0; b < B_N; b++) if (silkBit(b) && b != B_MINUS) { CGPathRef g = [self silkGlyphFor:b]; _glyph[b].path = g; CGPathRelease(g); }
    }
'''

GP = "dm/ios/Sources/DmGamepad.m"

patch(GP, [
    # gate + tabla de bits, tras la lista de teclas bloqueadas
    ("static const int k_btns[] = {B_ZL, B_L, B_ZR, B_R, B_MINUS, B_PLUS, B_LS, B_RS};   // keys locked at touch-down (L3 / R3 only in the 3D layout)",
     "static const int k_btns[] = {B_ZL, B_L, B_ZR, B_R, B_MINUS, B_PLUS, B_LS, B_RS};   // keys locked at touch-down (L3 / R3 only in the 3D layout)" + GATE),
    # capa de pictogramas por tecla
    ("    CAShapeLayer *_key[B_N]; CATextLayer *_label[B_N];   // one layer per key",
     "    CAShapeLayer *_key[B_N]; CATextLayer *_label[B_N];   // one layer per key\n    CAShapeLayer *_glyph[B_N];   // pictogramas del modo Silksong (subcapas de _key)"),
    ("""        for (int b = 0; b < B_N; b++) {
            _key[b] = shape(_controls);
            if (names[b]) _label[b] = label(_key[b], names[b]);   // the D-pad arms carry no label
        }""",
     """        for (int b = 0; b < B_N; b++) {
            _key[b] = shape(_controls);
            if (names[b]) _label[b] = label(_key[b], names[b]);   // the D-pad arms carry no label
            _glyph[b] = [CAShapeLayer layer]; _glyph[b].fillColor = nil; _glyph[b].strokeColor = k_text.CGColor;
            _glyph[b].lineCap = kCALineCapRound; _glyph[b].lineJoin = kCALineJoinRound; _glyph[b].hidden = YES;
            [_key[b] addSublayer:_glyph[b]];
        }"""),
    # visibilidad segun el conjunto silk
    ("    for (int b = 0; b < B_N; b++) _key[b].hidden = _tap || (fullOnly(b) && !_full);",
     "    BOOL silk = [self silkActive];\n    for (int b = 0; b < B_N; b++) _key[b].hidden = _tap || (silk ? !silkBit(b) : (fullOnly(b) && !_full));"),
    # geometria: centro/radio del diamante pasan a ser la reticula silk
    ("- (CGPoint)faceCenter { CGRect s = self.corner; CGFloat u = self.u;",
     "- (CGPoint)faceCenter { if ([self silkActive]) { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.862 * c.size.width, CGRectGetMinY(c) + 0.638 * c.size.height); } CGRect s = self.corner; CGFloat u = self.u;"),
    ("- (CGFloat)faceGap { return K_FACE_GAP * self.u; }",
     "- (CGFloat)faceGap { return [self silkActive] ? 0.155 * _layout.controls.size.width : K_FACE_GAP * self.u; }"),
    ("- (CGFloat)faceR { return K_FACE_R * self.u; }",
     "- (CGFloat)faceR { return [self silkActive] ? [self silkRoundR] : K_FACE_R * self.u; }"),
    ("- (CGPoint)facePos:(int)b { CGPoint c = self.faceCenter; CGFloat g = self.faceGap;",
     "- (CGPoint)facePos:(int)b { if ([self silkActive]) return [self silkCenterFor:b]; CGPoint c = self.faceCenter; CGFloat g = self.faceGap;"),
    # joystick en su sitio Android
    ("- (CGPoint)stickHome {\n    if (self.portraitControls) {",
     "- (CGPoint)stickHome {\n    if ([self silkActive]) { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.138 * c.size.width, CGRectGetMinY(c) + 0.700 * c.size.height); }\n    if (self.portraitControls) {"),
    ("- (CGFloat)stickR:(int)i { return (i ? K_RSTICK_R : K_STICK_R) * self.u; }",
     "- (CGFloat)stickR:(int)i { if ([self silkActive] && i == 0) return 0.048 * _layout.controls.size.width; return (i ? K_RSTICK_R : K_STICK_R) * self.u; }"),
    # SELECT usa su rect silk (la rama de pastillas lo recoge)
    ("- (CGRect)pillRect:(int)b { CGRect s = self.safe;",
     "- (CGRect)pillRect:(int)b { if ([self silkActive] && b == B_MINUS) return [self silkRectFor:b]; CGRect s = self.safe;"),
    # el engranaje se mueve a la zona MENU
    ("- (CGPoint)menuCenter { CGRect s = self.safe;",
     "- (CGPoint)menuCenter { if ([self silkActive]) { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.8195 * c.size.width, CGRectGetMinY(c) + 0.259 * c.size.height); } CGRect s = self.safe;"),
    ("- (CGFloat)menuDistance:(CGPoint)p { return dist(p, self.menuCenter) / MAX(K_MENU_R * self.u * 1.6, 22); }",
     "- (CGFloat)menuDistance:(CGPoint)p { return dist(p, self.menuCenter) / MAX(([self silkActive] ? [self silkMenuR] : K_MENU_R * self.u) * 1.6, 22); }"),
    # metodos auxiliares, antes de menuDistance
    ("- (CGFloat)menuDistance:(CGPoint)p {",
     HELPERS + "- (CGFloat)menuDistance:(CGPoint)p {"),
    # hit de las zonas silk (rects anchos y redondos sueltos) antes de las categorias clasicas
    ("""- (CGFloat)buttonDistance:(int)b point:(CGPoint)p {
    CGFloat u = self.u;""",
     """- (CGFloat)buttonDistance:(int)b point:(CGPoint)p {
    CGFloat u = self.u;
    if ([self silkActive]) {
        if (b == B_ZL || b == B_ZR || b == B_L) { CGRect r = CGRectInset([self silkRectFor:b], -8 * u, -8 * u);
            if (!CGRectContainsPoint(r, p)) return CGFLOAT_MAX;
            return MAX(fabs(p.x - CGRectGetMidX(r)) / (r.size.width / 2), fabs(p.y - CGRectGetMidY(r)) / (r.size.height / 2)); }
        if (b == B_R || b == B_PLUS) return dist(p, [self silkCenterFor:b]) / ([self silkRoundR] * 1.35);
    }"""),
    # dibujo silk al final de layoutSubviews
    ("    [CATransaction commit];\n    [self refresh];\n}",
     LAYOUT_BLOCK + "    [CATransaction commit];\n    [self refresh];\n}"),
    # el pictograma sigue el estado pulsado
    ("        _key[b].fillColor = (on ? k_on : k_idle).CGColor; _label[b].foregroundColor = (on ? k_textOn : k_text).CGColor; }",
     "        _key[b].fillColor = (on ? k_on : k_idle).CGColor; _label[b].foregroundColor = (on ? k_textOn : k_text).CGColor; _glyph[b].strokeColor = (on ? k_textOn : k_text).CGColor; }"),
])

if missing:
    print("FALTAN PATRONES (¿cambió upstream?):")
    for m in missing:
        print(" -", m)
    sys.exit(1)

SECCIONES_OK = {"Game", "Controls", "Performance"}
for n, line in enumerate((root / TSV).read_text(encoding="utf-8").split("\n"), 1):
    if not line or line.startswith("#"):
        continue
    cols = line.split("\t")
    if len(cols) >= 6 and cols[5] not in SECCIONES_OK:
        print(f"ERROR ESTRUCTURAL: {TSV}:{n}: sección no válida: {cols[5]!r}")
        sys.exit(1)
print("Parche aplicado: lanzador en español + controles tipo Android para Silksong.")
