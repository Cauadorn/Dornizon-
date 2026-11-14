# Cena 3D da capa: os cinco dias da semana em blocos de acrílico na paleta EMS.
# uso: python cena.py <saida.png> [quadro] [largura] [amostras]
import bpy, sys, math, os
from mathutils import Vector, Euler
args = sys.argv[1:]
out = args[0]; frame = float(args[1]) if len(args) > 1 else 0.0
W = int(args[2]) if len(args) > 2 else 900; S = int(args[3]) if len(args) > 3 else 96
here = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(here, '..', 'fonts', 'InstrumentSerif-Italic.ttf')

def lin(h):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return [x / 12.92 if x <= .04045 else ((x + .055) / 1.055) ** 2.4 for x in c] + [1]
K = dict(ivory='#fffbde', tinta='#2a1433', ameixa='#3d1c46', violeta='#6225d8', violeta2='#7b4df2', lavanda='#c0a5c4', pink='#dd34a8', manteiga='#f2cf7a')

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.samples = S; sc.cycles.use_denoising = True
sc.cycles.max_bounces = 10; sc.cycles.transmission_bounces = 10; sc.cycles.glossy_bounces = 6
sc.cycles.caustics_reflective = False; sc.cycles.caustics_refractive = False
sc.render.resolution_x = W; sc.render.resolution_y = int(W * 1.0); sc.render.film_transparent = True
sc.render.image_settings.file_format = 'PNG'; sc.render.image_settings.color_mode = 'RGBA'
sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'
sc.render.threads_mode = 'AUTO'

def clarear(cor, k):
    c = lin(cor); return [c[i] + (1 - c[i]) * k for i in range(3)] + [1]
def mat_vidro(name, cor, rough=.06):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = clarear(cor, .72); b.inputs['Roughness'].default_value = rough
    b.inputs['Transmission Weight'].default_value = 1.0; b.inputs['IOR'].default_value = 1.46
    b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Coat Roughness'].default_value = .04
    return m
def mat_miolo(name, cor):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(cor); b.inputs['Roughness'].default_value = .55
    b.inputs['Subsurface Weight'].default_value = .6; b.inputs['Subsurface Radius'].default_value = (1, .6, 1)
    b.inputs['Emission Color'].default_value = lin(cor); b.inputs['Emission Strength'].default_value = .55
    return m
def mat_letra(name, cor):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = lin(cor); b.inputs['Roughness'].default_value = .25
    b.inputs['Coat Weight'].default_value = 1.0; b.inputs['Emission Color'].default_value = lin(cor); b.inputs['Emission Strength'].default_value = .35
    return m

def bloco(nome, sx, sy, sz, raio):
    bpy.ops.mesh.primitive_cube_add(size=1); o = bpy.context.object; o.name = nome
    o.scale = (sx, sy, sz); bpy.ops.object.transform_apply(scale=True)
    bv = o.modifiers.new('b', 'BEVEL'); bv.width = raio; bv.segments = 24; bv.limit_method = 'NONE'
    bpy.ops.object.shade_smooth(); return o

font = bpy.data.fonts.load(FONT)
def tecla(txt, cor_casca, cor_miolo, cor_letra, pos, rot, fase):
    raiz = bpy.data.objects.new('r_' + txt, None); sc.collection.objects.link(raiz)
    casca = bloco('casca_' + txt, 2.5, 1.25, 2.5, .52); casca.data.materials.append(mat_vidro('v_' + txt, cor_casca)); casca.parent = raiz
    miolo = bloco('miolo_' + txt, 2.06, .8, 2.06, .38); miolo.location = (0, .1, 0); miolo.data.materials.append(mat_miolo('m_' + txt, cor_miolo)); miolo.parent = raiz
    bpy.ops.object.text_add(); t = bpy.context.object; t.data.body = txt; t.data.font = font
    t.data.align_x = 'CENTER'; t.data.align_y = 'CENTER'; t.data.size = 1.15; t.data.extrude = .1; t.data.bevel_depth = .025; t.data.bevel_resolution = 4
    t.rotation_euler = (math.radians(90), 0, 0); t.location = (-.04, -.69, .06); t.data.materials.append(mat_letra('l_' + txt, cor_letra)); t.parent = raiz
    # flutuação leve, cada bloco com a sua fase
    f = frame * 2 * math.pi
    raiz.location = Vector(pos) + Vector((0, 0, .16 * math.sin(f + fase)))
    raiz.rotation_euler = Euler([math.radians(a) for a in (rot[0] + 4 * math.sin(f + fase + 1), rot[1] + 3 * math.cos(f + fase), rot[2] + 5 * math.sin(f + fase + 2))])
    return raiz

tecla('seg', K['lavanda'], K['lavanda'],  K['violeta'], (-2.75, .2, 1.75), (8, -14, 16), 0)
tecla('ter', K['pink'],    K['pink'],     K['ivory'],   (0.05, -.3, 2.3),  (-6, 6, -8), 1.3)
tecla('qua', K['violeta2'],K['violeta'],  K['manteiga'],(2.8, .3, 1.5),    (10, 12, -18), 2.6)
tecla('qui', K['manteiga'],K['manteiga'], K['tinta'],   (-1.45, 0, -.95),  (-10, -8, -10), 3.9)
tecla('fds', K['ivory'],   K['ivory'],    K['pink'],    (1.4, -.4, -1.2),  (6, 10, 12), 5.2)

# câmera
bpy.ops.object.camera_add(location=(0, -17, .6), rotation=(math.radians(90), 0, 0)); cam = bpy.context.object
cam.data.lens = 85; sc.camera = cam
# luz: estúdio macio + ambiente claro
def area(loc, rot, size, power, cor=(1, 1, 1)):
    bpy.ops.object.light_add(type='AREA', location=loc, rotation=[math.radians(a) for a in rot]); l = bpy.context.object
    l.data.size = size; l.data.energy = power; l.data.color = cor; return l
area((-6, -9, 8), (50, 0, -35), 9, 1700)
area((8, -6, 3), (75, 0, 55), 7, 1100, (1, .9, 1))
area((0, 6, 6), (-50, 0, 180), 10, 1500, (.8, .7, 1))
area((0, -4, -8), (160, 0, 0), 10, 500, (1, .8, .95))
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = lin('#f3ecf6'); w.node_tree.nodes['Background'].inputs['Strength'].default_value = 1.15
sc.render.filepath = out
bpy.ops.render.render(write_still=True)
