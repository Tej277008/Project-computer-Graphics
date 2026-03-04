import json, argparse
import numpy as np
from PIL import Image
from rasterizer import Rasterizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--width', type=int, default=800)
    ap.add_argument('--height', type=int, default=600)
    ap.add_argument('--spp', type=int, default=1)
    ap.add_argument('--scene', type=str, required=True)
    ap.add_argument('--out', type=str, required=True)
    args = ap.parse_args()

    rast = Rasterizer(args.width, args.height, samples=args.spp)
    scene = json.load(open(args.scene))

    for tri in scene['triangles']:
        v = np.array(tri['verts'], dtype=np.float32)
        c = np.array(tri['colors'], dtype=np.float32)
        rast.draw_triangle(v[0], v[1], v[2], c[0], c[1], c[2])

    img = (np.clip(rast.resolve(), 0, 1) * 255).astype(np.uint8)
    Image.fromarray(img).save(args.out)
    print('Wrote', args.out)

if __name__ == '__main__':
    main()