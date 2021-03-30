import pygame
import xml.etree.ElementTree as xml
import math
import bricks

class Tileset:
    def __init__(self, fname_path, fname, start_code):
        """
        <tileset version="1.2" tiledversion="1.2.3" name="tiles_spritesheet" tilewidth="70" tileheight="70" spacing="2" margin="2" tilecount="156" columns="12" backgroundcolor="#005500">
        <tileoffset x="0" y="2"/>
        <image source="../images/kenney_platformer_tiles/Base pack/Tiles/tiles_spritesheet.png" width="914" height="936"/>
        </tileset>
        """
        self.name = "??"
        self.tile_width = 0
        self.tile_height = 0
        self.tile_columns = 0
        self.tile_margin = 0
        self.tile_spacing = 0
        self.tile_offset_x = 0
        self.tile_offset_y = 0
        self.image = None
        self.start_code = start_code
        self.end_code = None

        # Get some attributes from the root node
        tileset_tree = xml.parse(fname_path + fname)
        tileset_root = tileset_tree.getroot()
        if "tilewidth" in tileset_root.attrib:
            self.tile_width = int(tileset_root.attrib["tilewidth"])
        if "tileheight" in tileset_root.attrib:
            self.tile_height = int(tileset_root.attrib["tileheight"])
        if "spacing" in tileset_root.attrib:
            self.tile_spacing = int(tileset_root.attrib["spacing"])
        if "margin" in tileset_root.attrib:
            self.tile_margin = int(tileset_root.attrib["margin"])
        if "columns" in tileset_root.attrib:
            self.tile_columns = int(tileset_root.attrib["columns"])
        if "tilecount" in tileset_root.attrib:
            self.end_code = self.start_code + int(tileset_root.attrib["tilecount"])

        # Get the tileoffset child node, if there is one
        tile_offset = tileset_root.find("tileoffset")
        if tile_offset != None:
            if "x" in tile_offset.attrib:
                self.tile_offset_x = int(tile_offset.attrib["x"])
            if "y" in tile_offset.attrib:
                self.tile_offset_y = int(tile_offset.attrib["y"])

        # Get the image child node, if there is one
        tile_image = tileset_root.find("image")
        if tile_image != None:
            if "source" in tile_image.attrib:
                self.image = pygame.image.load(fname_path + tile_image.attrib["source"])


class Area:
    def __init__(self, rect, props):
        self.rect = rect
        self.props = props

    def __str__(self):
        return "[" + str(self.rect) + " " + str(self.props) + "]"

    def param_matches(self, param):
        result = True
        for p in param:
            if p not in self.props or (param[p] != None and param[p] != self.props[p]):
                result = False
                break
        return result


class Map:
    def __init__(self, fname):
        self.name = fname
        self.world_width = 0                 # Width of the map, in tiles
        self.world_height = 0                # Height of the map, in tiles
        self.pixel_width = 0                # Width of the map, in pixels
        self.pixel_height = 0
        self.tile_width = 0                 # Width of each tile, determined by the first layer.
        self.tile_height = 0
        self.tile_sets = []
        self.tile_layers = []
        self.areas = []  # A list of Area objects
        self.camera_pos = [0, 0]
        self.items = []
        self.bricks=[]

        self.load(fname)

    def find_areas_with_parameters(self, params):
        result = []
        for a in self.areas:
            if a.param_matches(params):
                result.append(a)
        return result

    def load(self, fname):
        tree = xml.parse(fname)
        if "\\" in fname:
            fname_path = fname[:fname.rfind("\\") + 1]
        else:
            fname_path = ""
        # Get the root node and all the relevant attributes
        root = tree.getroot()
        print("root.attrib = " + str(root.attrib))
        if "width" in root.attrib:
            self.world_width = int(root.attrib["width"])
        if "height" in root.attrib:
            self.world_height = int(root.attrib["height"])

        # Get the tilesets
        for tileset in root.iter('tileset'):
            if "firstgid" in tileset.attrib and "source" in tileset.attrib:
                self.tile_sets.append(Tileset(fname_path, tileset.attrib["source"], int(tileset.attrib["firstgid"])))
                if self.tile_width == 0:
                    # The first layer -- it'll determine the tile_width & height for me.  Usually they're all the same...
                    self.tile_width = self.tile_sets[-1].tile_width
                    self.tile_height = self.tile_sets[-1].tile_height

        # Get the layers
        for layer in root.iter("layer"):
            data = layer.find("data")
            if data != None:
                new_layer = []
                lines = data.text.split("\n")
                for line in lines:
                    if len(line) == 0:
                        continue
                    if line[-1] == ",":
                        line = line[:-1]
                    new_row = []
                    for item in line.split(","):
                        new_row.append(int(item))
                    new_layer.append(new_row)
                self.tile_layers.append(new_layer)

        # Get the objects (including bounding areas)
        for obj in root.iter("object"):
            if "x" in obj.attrib and "y" in obj.attrib:
                x = float(obj.attrib["x"])
                y = float(obj.attrib["y"])
                w = h = 0
                if "width" in obj.attrib and "height" in obj.attrib:
                    w = float(obj.attrib["width"])
                    h = float(obj.attrib["height"])
                props = {}
                for p in obj.iter("property"):
                    if "name" in p.attrib and "value" in p.attrib:
                        props[p.attrib["name"]] = p.attrib["value"]
                new_area = Area(pygame.Rect(x, y, w, h), props)

                if new_area.param_matches({"spawner": None}):
                    # This is an (item) spawning location -- handle it now
                    self.items.append((x, y, int(props["spawner"])))
                else:
                    # Add it to the list of all other types of areas.
                    self.areas.append(new_area)

        # Create a few more attributes
        self.pixel_width = self.world_width * self.tile_width
        self.pixel_height = self.world_height * self.tile_height
        self.create_Brick()

    def create_Brick(self):
        screen_w = 800
        screen_h = 600
        screen_tilew = math.ceil(screen_w / self.tile_width)
        screen_tileh = math.ceil(screen_h / self.tile_height)
        start_y = -(self.camera_pos[1] % self.tile_height)
        start_x = -(self.camera_pos[0] % self.tile_width)
        start_tile_x = max(0, int(self.camera_pos[0] / self.tile_width))
        start_tile_y = max(0, int(self.camera_pos[1] / self.tile_height))
        end_tile_x = min(start_tile_x + screen_tilew, self.world_width - 1)
        end_tile_y = min(start_tile_y + screen_tileh, self.world_height - 1)

        for layer_num in range(len(self.tile_layers)):
            layer = self.tile_layers[layer_num]
            y = start_y
            for row_num in range(start_tile_y, end_tile_y + 1):
                row = layer[row_num]
                x = start_x
                for col_num in range(start_tile_x, end_tile_x + 1):
                    code = row[col_num]
                    if code != 0:
                        self.bricks.append(bricks.Brick((x,y),(8, 8),code))
                    x += self.tile_width
                y += self.tile_height


    def blit_tile_to(self, dest_surf, code, x, y):
        for tileset in self.tile_sets:
            if code >= tileset.start_code and code <= tileset.end_code:
                tw = tileset.tile_width
                th = tileset.tile_height
                code -= tileset.start_code
                row = code // tileset.tile_columns
                col = code % tileset.tile_columns
                src_x = tileset.tile_margin + col * (tileset.tile_spacing + tw)
                src_y = tileset.tile_margin + row * (tileset.tile_spacing + th)
                dest_surf.blit(tileset.image, (x + tileset.tile_offset_x, y + tileset.tile_offset_y), (src_x, src_y, tw, th))
                break

    def get_bricks(self):
        return self.bricks

    def render(self, surf, grid_color = None, debug = False):
        screen_w = surf.get_width()
        screen_h = surf.get_height()
        start_y = -(self.camera_pos[1] % self.tile_height)
        start_x = -(self.camera_pos[0] % self.tile_width)

        for b in self.bricks:
            self.blit_tile_to(surf, b.code, b.pos[0], b.pos[1])

        if grid_color != None:
            for x in range(int(start_x), screen_w, self.tile_width):
                pygame.draw.line(surf, grid_color, (x, 0), (x, screen_h))
            for y in range(int(start_y), screen_h, self.tile_height):
                pygame.draw.line(surf, grid_color, (0, y), (screen_w, y))

        if debug:
            for a in self.areas:
                adj_rect = a.rect.move(-self.camera_pos[0], -self.camera_pos[1])
                pygame.draw.rect(surf, (128, 128, 0), adj_rect, 1)


    def get_item_bounds(self, item):
        img = self.item_imgs[item[2]]
        return pygame.Rect(item[0], item[1], img.get_width(), img.get_height())


    def detect_item_hit(self, bounds, remove_hits = False):
        hit_items = []
        for i in self.items:
            if self.get_item_bounds(i).colliderect(bounds):
                hit_items.append(i)
                if remove_hits:
                    self.items.remove(i)
        return hit_items

    def render_all(self):
        surf = pygame.Surface((self.pixel_width, self.pixel_height))
        for layer_num in range(len(self.tile_layers)):
            layer = self.tile_layers[layer_num]
            y = 0
            for row in layer:
                x = 0
                for code in row:
                    if code != 0:
                        self.blit_tile_to(surf, code, x, y)
                    x += self.tile_width
                y += self.tile_height
        return surf


    def adjust_camera(self, dx, dy, screen_w, screen_h, ignore_bounds = False):
        self.camera_pos[0] += dx
        self.camera_pos[1] += dy
        if not ignore_bounds:
            self.constrain_camera(screen_w, screen_h)


    def set_camera(self, x, y, screen_w, screen_h, ignore_bounds = False):
        self.camera_pos[0] = x
        self.camera_pos[1] = y
        if not ignore_bounds:
            self.constrain_camera(screen_w, screen_h)


    def world_to_screen(self, pos):
        return [pos[0] - self.camera_pos[0], pos[1] - self.camera_pos[1]]

    def constrain_camera(self, screen_w, screen_h):
        if self.camera_pos[0] > self.pixel_width - screen_w:
            self.camera_pos[0] = self.pixel_width - screen_w
        if self.camera_pos[1] > self.pixel_height - screen_h:
            self.camera_pos[1] = self.pixel_height - screen_h
        if self.camera_pos[0] < 0:
            self.camera_pos[0] = 0
        if self.camera_pos[1] < 0:
            self.camera_pos[1] = 0
