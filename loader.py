import pygame

def load_atlas(atlas_file, image_file):
    sprites = {}
    atlas_image = pygame.image.load(image_file).convert_alpha()

    with open(atlas_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        line = lines[i]

        # Skip metadata lines
        if ":" in line:
            i += 1
            continue

        name = line
        xy_line = None
        size_line = None

        # Search for xy: and size: in the next 10 lines
        for j in range(i+1, min(i+11, len(lines))):
            l = lines[j]
            if l.startswith("xy:"):
                xy_line = l
            elif l.startswith("size:"):
                size_line = l

        if xy_line is None or size_line is None:
            print(f"Skipping {name}: xy or size not found")
            i += 1
            continue

        x, y = map(int, xy_line.split(":")[1].split(","))
        w, h = map(int, size_line.split(":")[1].split(","))
        rect = pygame.Rect(x, y, w, h)
        sprites[name] = atlas_image.subsurface(rect)

        i += 1

    return sprites
