#!/usr/bin/env python3
"""Parche de build para Silksong (aplicado al clon de nxnative antes de compilar):

1. Traduce al español los textos del lanzador DmIOS (settings.tsv sin tocar la
   columna de sección, Launcher.swift con los títulos traducidos al mostrarlos,
   front_ios.m). Los ajustes por defecto NO se tocan: el perfil probado de
   upstream para Silksong (docked 1080p, 60 fps en iPhone) queda tal cual.
2. Controles táctiles «tipo Android» SOLO para Silksong (DM_GAME_ID
   010013C00E930000), dentro de dm/ios/Sources/DmGamepad.m: la disposición del
   port chino de Android, con la geometría MEDIDA sobre su captura de
   referencia y los pictogramas REALES de esa captura (sprites PNG extraídos
   de ella, incrustados en base64 en tools/sprites/).

   Asignación v3 (verificada fotograma a fotograma contra los vídeos del
   port de Android el 2026-11-15; la v2 tenía la tabla cruzada):
   - Joystick abajo-izquierda: moverse.
   - Botón ancho izquierdo: dash (ZR). SELECT (-): inventario.
   - Arriba a la derecha: mapa (L), MENU = pausa (+), arpón (ZL).
   - Rejilla 2x3 de redondos (posición -> acción):
       arriba-izquierda  = R  (herramienta/habilidad)
       arriba-derecha    = X  (Needolin)
       medio-izquierda   = B  (saltar)
       medio-derecha     = R  (herramienta/habilidad, segunda zona)
       abajo-izquierda   = Y  (ATAQUE, la daga)
       abajo-derecha     = A  (curar/vincular, aguja con remolino)
     En el juego original herramienta y habilidad de seda son EL MISMO botón
     (R): sin dirección = habilidad; con Arriba en el joystick = herramienta.
     Por eso R tiene dos zonas táctiles, una por pictograma del port.
   - El botón de ajustes de DmIOS (la tuerquita) queda EXACTAMENTE como viene
     de fábrica: ni se mueve ni se le cambia el icono (petición del usuario,
     2026-11-15). Lo único «original» que se conserva.
   Los índices B_* no se tocan: su orden es el de los bits DM_BTN_* del host.

Falla con error si alguna cadena esperada no aparece, para detectar cambios
de upstream. Uso: python3 parche_silksong.py <ruta-al-clon-de-nxnative>
"""
import sys
from pathlib import Path

root = Path(sys.argv[1])
missing = []
SPRITES = Path(__file__).parent / "sprites"


def b64(name):
    return (SPRITES / f"{name}.b64").read_text().strip()


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
// Disposicion del port chino de Silksong para Android sobre el layout 2D, con la
// geometria medida sobre su captura y sus pictogramas reales (sprites PNG
// incrustados en base64). Asignacion v3, verificada contra los videos del port:
// joystick = moverse; dash = ZR; SELECT = - (inventario); mapa = L; MENU = +
// (pausa); arpon = ZL. Rejilla de redondos: arriba-izquierda y medio-derecha
// son el boton R (herramienta/habilidad: en el juego original es el mismo
// boton; sin direccion = habilidad de seda, con Arriba = herramienta),
// arriba-derecha = X (Needolin), medio-izquierda = B (saltar),
// abajo-izquierda = Y (atacar, la daga), abajo-derecha = A (curar/vincular).
// El boton de ajustes de DmIOS (la tuerquita) NO se toca: queda de fabrica.
// Los indices B_* no se tocan: su orden es el de los bits DM_BTN_* del host.
// Todo vive tras este gate; el resto de juegos y los modos 3D/Tap quedan igual.
#ifndef DM_GAME_ID
#define DM_GAME_ID ""
#endif
static BOOL silkPad(void) { return !strcmp(DM_GAME_ID, "010013C00E930000"); }
static BOOL silkBit(int b) { switch (b) { case B_A: case B_B: case B_X: case B_Y: case B_L: case B_R: case B_ZL: case B_ZR: case B_PLUS: case B_MINUS: return YES; default: return NO; } }
static UIImage *silkImg(NSString *s) { NSData *d = [[NSData alloc] initWithBase64EncodedString:s options:0]; return d ? [UIImage imageWithData:d] : nil; }
'''

HELPERS = r'''- (BOOL)silkActive { return silkPad() && !_full && !_tap && !_layout.separated; }
- (CGFloat)silkRoundR { return 0.0355 * _layout.controls.size.width; }
- (CGRect)silkRectFor:(int)b { CGRect c = _layout.controls; CGFloat x = CGRectGetMinX(c), y = CGRectGetMinY(c), w = c.size.width, h = c.size.height;
    switch (b) { case B_ZR: return CGRectMake(x + 0.039 * w, y + 0.257 * h, 0.103 * w, 0.114 * h);
        case B_L: return CGRectMake(x + 0.866 * w, y + 0.031 * h, 0.090 * w, 0.114 * h);
        case B_ZL: return CGRectMake(x + 0.866 * w, y + 0.201 * h, 0.090 * w, 0.114 * h);
        case B_PLUS: return CGRectMake(x + 0.783 * w, y + 0.201 * h, 0.043 * w, 0.113 * h);
        default: return CGRectMake(x + 0.162 * w, y + 0.264 * h, 0.046 * w, 0.098 * h); } }   // B_MINUS (SELECT)
- (CGPoint)silkCenterFor:(int)b { CGRect c = _layout.controls; CGFloat x = CGRectGetMinX(c), y = CGRectGetMinY(c), w = c.size.width, h = c.size.height;
    switch (b) { case B_R: return CGPointMake(x + 0.807 * w, y + 0.461 * h);
        case B_X: return CGPointMake(x + 0.899 * w, y + 0.428 * h);
        case B_B: return CGPointMake(x + 0.795 * w, y + 0.663 * h);
        case B_Y: return CGPointMake(x + 0.792 * w, y + 0.846 * h);
        default: return CGPointMake(x + 0.895 * w, y + 0.835 * h); } }   // B_A
- (CGPoint)silkSkillCenter { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.891 * c.size.width, CGRectGetMinY(c) + 0.606 * c.size.height); }
'''

# Los sprites se nombran por su MOTIVO (el dibujo), no por el bit: cada
# pictograma va en su posición del port de Android y el bit sigue a la acción.
#   y.png    = aguja con remolino  -> posición abajo-derecha  -> bit B_A (curar)
#   r.png    = daga                -> posición abajo-izquierda -> bit B_Y (atacar)
#   plus.png = cabeza en picado    -> posición arriba-izquierda -> bit B_R (herramienta)
#   a.png    = Hornet de pie       -> posición medio-derecha  -> 2ª zona de B_R (habilidad)
#   menu.png = emblema             -> zona MENU               -> bit B_PLUS (pausa)
ART_INIT = r'''        if (silkPad()) {
            static NSString *const artB64[B_N] = { [B_A] = @"__A__", [B_B] = @"__B__", [B_X] = @"__X__", [B_Y] = @"__Y__", [B_R] = @"__R__", [B_PLUS] = @"__PLUS__", [B_ZR] = @"__ZR__", [B_ZL] = @"__ZL__", [B_L] = @"__L__", [B_MINUS] = @"__MINUS__" };
            for (int b = 0; b < B_N; b++) if (artB64[b]) { UIImage *im = silkImg(artB64[b]); if (im) _art[b].contents = (id)im.CGImage; }
            UIImage *imS = silkImg(@"__SKILL__"); if (imS) _artR2.contents = (id)imS.CGImage;
        }
'''
for token, name in [("__A__", "y"), ("__B__", "b"), ("__X__", "x"), ("__Y__", "r"),
                    ("__R__", "plus"), ("__PLUS__", "menu"), ("__ZR__", "zr"),
                    ("__ZL__", "zl"), ("__L__", "l"), ("__MINUS__", "minus"),
                    ("__SKILL__", "a")]:
    ART_INIT = ART_INIT.replace(token, b64(name))

LAYOUT_BLOCK = r'''    if ([self silkActive]) {
        for (int b = 0; b < B_N; b++) if (_label[b]) _label[b].hidden = b != B_MINUS && b != B_PLUS;
        setPath(_key[B_ZL], CGPathCreateWithRoundedRect([self silkRectFor:B_ZL], 12 * u, 12 * u, NULL));
        setPath(_key[B_ZR], CGPathCreateWithRoundedRect([self silkRectFor:B_ZR], 12 * u, 12 * u, NULL));
        setPath(_key[B_L], CGPathCreateWithRoundedRect([self silkRectFor:B_L], 12 * u, 12 * u, NULL));
        setPath(_key[B_PLUS], CGPathCreateWithRoundedRect([self silkRectFor:B_PLUS], 10 * u, 10 * u, NULL));
        setPath(_key[B_R], circlePath([self silkCenterFor:B_R], [self silkRoundR]));
        setPath(_keyR2, circlePath([self silkSkillCenter], [self silkRoundR]));
        for (int b = 0; b < B_N; b++) { if (!silkBit(b)) continue;
            if (b == B_ZL || b == B_ZR || b == B_L) _art[b].frame = [self silkRectFor:b];
            else if (b == B_MINUS) { CGRect rc = [self silkRectFor:b]; CGFloat aw = rc.size.width * 0.85; _art[b].frame = CGRectMake(CGRectGetMidX(rc) - aw / 2, CGRectGetMinY(rc) + rc.size.height * 0.06, aw, aw * 58.0 / 71.0); }
            else if (b == B_PLUS) { CGRect rc = [self silkRectFor:b]; CGFloat ah = rc.size.height * 0.58; CGFloat aw = ah * 86.0 / 115.0; _art[b].frame = CGRectMake(CGRectGetMidX(rc) - aw / 2, CGRectGetMinY(rc) + rc.size.height * 0.05, aw, ah); }
            else { CGPoint cc = [self silkCenterFor:b]; CGFloat rr = [self silkRoundR]; _art[b].frame = CGRectMake(cc.x - rr, cc.y - rr, 2 * rr, 2 * rr); } }
        { CGPoint sc = [self silkSkillCenter]; CGFloat rr = [self silkRoundR]; _artR2.frame = CGRectMake(sc.x - rr, sc.y - rr, 2 * rr, 2 * rr); }
        _label[B_MINUS].string = @"SELECT"; placeLabel(_label[B_MINUS], CGPointMake(CGRectGetMidX([self silkRectFor:B_MINUS]), CGRectGetMinY([self silkRectFor:B_MINUS]) + [self silkRectFor:B_MINUS].size.height * 0.80), 10 * u);
        { CGRect lf = _label[B_MINUS].frame; _label[B_MINUS].frame = CGRectMake(CGRectGetMidX(lf) - 32 * u, lf.origin.y, 64 * u, lf.size.height); }
        _label[B_PLUS].string = @"MENU"; placeLabel(_label[B_PLUS], CGPointMake(CGRectGetMidX([self silkRectFor:B_PLUS]), CGRectGetMinY([self silkRectFor:B_PLUS]) + [self silkRectFor:B_PLUS].size.height * 0.86), 10 * u);
        { CGRect lf = _label[B_PLUS].frame; _label[B_PLUS].frame = CGRectMake(CGRectGetMidX(lf) - 32 * u, lf.origin.y, 64 * u, lf.size.height); }
        CGFloat kr = [self stickR:0] * 0.4; _knob.bounds = CGRectMake(0, 0, 2 * kr, 2 * kr); setPath(_knob, circlePath(CGPointMake(kr, kr), kr));
        CAShapeLayer *kin = (CAShapeLayer *)_knob.sublayers.firstObject; CGPathRef kip = circlePath(CGPointMake(kr, kr), kr * 0.62); kin.frame = _knob.bounds; kin.path = kip; CGPathRelease(kip);
    }
'''

GP = "dm/ios/Sources/DmGamepad.m"

patch(GP, [
    # color de relleno oscuro para los botones silk (como el port de referencia)
    ("static UIColor *k_idle, *k_on, *k_line, *k_ringFill, *k_text, *k_textOn;",
     "static UIColor *k_idle, *k_on, *k_line, *k_ringFill, *k_text, *k_textOn, *k_silkFill;"),
    ("k_ringFill = [UIColor colorWithWhite:1 alpha:0.06];",
     "k_ringFill = [UIColor colorWithWhite:1 alpha:0.06]; k_silkFill = [UIColor colorWithWhite:0 alpha:0.30];"),
    # gate + helpers de bits, tras la lista de teclas bloqueadas
    ("static const int k_btns[] = {B_ZL, B_L, B_ZR, B_R, B_MINUS, B_PLUS, B_LS, B_RS};   // keys locked at touch-down (L3 / R3 only in the 3D layout)",
     "static const int k_btns[] = {B_ZL, B_L, B_ZR, B_R, B_MINUS, B_PLUS, B_LS, B_RS};   // keys locked at touch-down (L3 / R3 only in the 3D layout)" + GATE),
    # capas de arte (sprites) por tecla + segunda zona del boton R
    ("    CAShapeLayer *_key[B_N]; CATextLayer *_label[B_N];   // one layer per key",
     "    CAShapeLayer *_key[B_N]; CATextLayer *_label[B_N];   // one layer per key\n    CALayer *_art[B_N];   // sprites de los pictogramas del modo Silksong (subcapas de _key)\n    CAShapeLayer *_keyR2; CALayer *_artR2;   // segunda zona del boton R (habilidad) en el modo Silksong\n    BOOL _r1On, _r2On;   // que zona de R esta pulsada, para iluminar solo esa"),
    ("""        for (int b = 0; b < B_N; b++) {
            _key[b] = shape(_controls);
            if (names[b]) _label[b] = label(_key[b], names[b]);   // the D-pad arms carry no label
        }""",
     """        for (int b = 0; b < B_N; b++) {
            _key[b] = shape(_controls);
            if (names[b]) _label[b] = label(_key[b], names[b]);   // the D-pad arms carry no label
            _art[b] = [CALayer layer]; _art[b].hidden = !silkPad(); [_key[b] addSublayer:_art[b]];
        }
        _keyR2 = shape(_controls); _keyR2.hidden = !silkPad();
        _artR2 = [CALayer layer]; _artR2.hidden = !silkPad(); [_keyR2 addSublayer:_artR2];
""" + ART_INIT),
    # visibilidad segun el conjunto silk
    ("    for (int b = 0; b < B_N; b++) _key[b].hidden = _tap || (fullOnly(b) && !_full);",
     "    BOOL silk = [self silkActive];\n    for (int b = 0; b < B_N; b++) _key[b].hidden = _tap || (silk ? !silkBit(b) : (fullOnly(b) && !_full));\n    _keyR2.hidden = _tap || !silk;"),
    # geometria: centro/radio del diamante pasan a ser la reticula silk
    ("- (CGPoint)faceCenter { CGRect s = self.corner; CGFloat u = self.u;",
     "- (CGPoint)faceCenter { if ([self silkActive]) { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.847 * c.size.width, CGRectGetMinY(c) + 0.632 * c.size.height); } CGRect s = self.corner; CGFloat u = self.u;"),
    ("- (CGFloat)faceGap { return K_FACE_GAP * self.u; }",
     "- (CGFloat)faceGap { return [self silkActive] ? 0.115 * _layout.controls.size.width : K_FACE_GAP * self.u; }"),
    ("- (CGFloat)faceR { return K_FACE_R * self.u; }",
     "- (CGFloat)faceR { return [self silkActive] ? [self silkRoundR] : K_FACE_R * self.u; }"),
    # radio de acierto mas justo en la reticula silk: con el x1.25 de fabrica los
    # circulos de dos parejas (B/Y y X/A) se solapan y un toque cuenta como dos
    ("- (CGFloat)faceHitR { return MAX(self.faceR * 1.25, _layout.separated ? 22 : 0); }",
     "- (CGFloat)faceHitR { return [self silkActive] ? [self silkRoundR] * 1.05 : MAX(self.faceR * 1.25, _layout.separated ? 22 : 0); }"),
    ("- (CGPoint)facePos:(int)b { CGPoint c = self.faceCenter; CGFloat g = self.faceGap;",
     "- (CGPoint)facePos:(int)b { if ([self silkActive]) return [self silkCenterFor:b]; CGPoint c = self.faceCenter; CGFloat g = self.faceGap;"),
    # joystick en su sitio Android (radio medido)
    ("- (CGPoint)stickHome {\n    if (self.portraitControls) {",
     "- (CGPoint)stickHome {\n    if ([self silkActive]) { CGRect c = _layout.controls; return CGPointMake(CGRectGetMinX(c) + 0.138 * c.size.width, CGRectGetMinY(c) + 0.700 * c.size.height); }\n    if (self.portraitControls) {"),
    ("- (CGFloat)stickR:(int)i { return (i ? K_RSTICK_R : K_STICK_R) * self.u; }",
     "- (CGFloat)stickR:(int)i { if ([self silkActive] && i == 0) return 0.046 * _layout.controls.size.width; return (i ? K_RSTICK_R : K_STICK_R) * self.u; }"),
    # SELECT usa su rect silk (la rama de pastillas lo recoge)
    ("- (CGRect)pillRect:(int)b { CGRect s = self.safe;",
     "- (CGRect)pillRect:(int)b { if ([self silkActive] && b == B_MINUS) return [self silkRectFor:b]; CGRect s = self.safe;"),
    # metodos auxiliares, antes de menuDistance (que NO se toca: la tuerquita queda de fabrica)
    ("- (CGFloat)menuDistance:(CGPoint)p {",
     HELPERS + "- (CGFloat)menuDistance:(CGPoint)p {"),
    # hit de las zonas silk (rects anchos, MENU y los dos redondos de R) antes de las categorias clasicas
    ("""- (CGFloat)buttonDistance:(int)b point:(CGPoint)p {
    CGFloat u = self.u;""",
     """- (CGFloat)buttonDistance:(int)b point:(CGPoint)p {
    CGFloat u = self.u;
    if ([self silkActive]) {
        if (b == B_ZL || b == B_ZR || b == B_L || b == B_PLUS) { CGRect r = CGRectInset([self silkRectFor:b], -8 * u, -8 * u);
            if (!CGRectContainsPoint(r, p)) return CGFLOAT_MAX;
            return MAX(fabs(p.x - CGRectGetMidX(r)) / (r.size.width / 2), fabs(p.y - CGRectGetMidY(r)) / (r.size.height / 2)); }
        if (b == B_R) return MIN(dist(p, [self silkCenterFor:B_R]), dist(p, [self silkSkillCenter])) / ([self silkRoundR] * 1.2);
    }"""),
    # dibujo silk al final de layoutSubviews
    ("    [CATransaction commit];\n    [self refresh];\n}",
     LAYOUT_BLOCK + "    [CATransaction commit];\n    [self refresh];\n}"),
    # relleno oscuro en reposo para los botones silk
    ("        _key[b].fillColor = (on ? k_on : k_idle).CGColor; _label[b].foregroundColor = (on ? k_textOn : k_text).CGColor; }",
     "        _key[b].fillColor = (on ? k_on : ([self silkActive] && silkBit(b) ? k_silkFill : k_idle)).CGColor; _label[b].foregroundColor = (on ? k_textOn : k_text).CGColor; }"),
    # en refresh: calcular que zona de R esta pulsada segun donde esta el dedo
    ("    uint64_t all = _faceBits | _dpadBits | _btnBits;",
     "    if ([self silkActive]) { _r1On = NO; _r2On = NO; for (UITouch *t in _owner) { uint64_t v = [_owner objectForKey:t].unsignedLongLongValue; if ((v & 0xff) == C_BTN && (v >> 8) == B_R) { CGPoint p = [t locationInView:self]; if (dist(p, [self silkSkillCenter]) < dist(p, [self silkCenterFor:B_R])) _r2On = YES; else _r1On = YES; } } }\n    uint64_t all = _faceBits | _dpadBits | _btnBits;"),
    # y que cada zona de R se ilumine solo cuando se pulsa ELLA, no su gemela
    ("    CGPoint h = self.stickHome, o = [self knobOffset:0];",
     "    if (_keyR2) { if ([self silkActive]) { _keyR2.fillColor = _r2On ? k_on : k_silkFill; _key[B_R].fillColor = _r1On ? k_on : k_silkFill; } else _keyR2.fillColor = _key[B_R].fillColor; }\n    CGPoint h = self.stickHome, o = [self knobOffset:0];"),
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
print("Parche aplicado: lanzador en español + controles tipo Android para Silksong (v3.1).")
