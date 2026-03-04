import numpy as np

class Rasterizer:
    """Student TODOs:
    - Implement edge-function coverage and barycentric interpolation in draw_triangle
    - Implement nearest/bilinear sampling in sample_texture (texture hookup optional for baseline)
    - Implement resolve to average supersamples back to 1× framebuffer
    """
    def __init__(self, width:int, height:int, samples:int=1):
        assert samples in (1, 4, 16), "Use 1, 4, or 16 for SSAA"
        self.W, self.H, self.S = int(width), int(height), int(samples)
        self.fb = np.zeros((self.H*self.S, self.W*self.S, 3), dtype=np.float32)

    def _edge(self, a, b, p):
        # E(a,b,p) = (p.x-a.x)*(b.y-a.y) - (p.y-a.y)*(b.x-a.x)
        return (p[0]-a[0])*(b[1]-a[1]) - (p[1]-a[1])*(b[0]-a[0])

    # --------- REQUIRED ---------
    def draw_triangle(self, v0, v1, v2, c0, c1, c2):
        """Fill one triangle. v*: (x,y) in pixel space; c*: (r,g,b) in [0,1].
        Hints:
        - Scale vertices by S to operate at supersample resolution
        - Compute integer bounding box and build a grid of sample points
        - Edge function E(a,b,p) = (p.x-a.x)*(b.y-a.y)-(p.y-a.y)*(b.x-a.x)
        - Keep sign consistent with signed area to test inside
        - Interpolate color using barycentrics (w0,w1,w2)
        """
       # Convert to float arrays
        v0 = np.asarray(v0, dtype=np.float32)
        v1 = np.asarray(v1, dtype=np.float32)
        v2 = np.asarray(v2, dtype=np.float32)
        c0 = np.asarray(c0, dtype=np.float32)
        c1 = np.asarray(c1, dtype=np.float32)
        c2 = np.asarray(c2, dtype=np.float32)

        S = self.S

        # Work in supersample coordinates (hint from starter file)
        sv0 = v0 * S
        sv1 = v1 * S
        sv2 = v2 * S

        # Signed area (if 0 => degenerate triangle)
        area = self._edge(sv0, sv1, sv2)
        if area == 0:
            return

        # Bounding box in supersample pixel coords
        xs = [sv0[0], sv1[0], sv2[0]]
        ys = [sv0[1], sv1[1], sv2[1]]

        xmin = max(int(np.floor(min(xs))), 0)
        xmax = min(int(np.ceil (max(xs))), self.W*S - 1)
        ymin = max(int(np.floor(min(ys))), 0)
        ymax = min(int(np.ceil (max(ys))), self.H*S - 1)

        # Loop over supersample pixels
        for y in range(ymin, ymax + 1):
            for x in range(xmin, xmax + 1):
                # Sample at the center of this supersample pixel
                p = np.array([x + 0.5, y + 0.5], dtype=np.float32)

                # Edge values (these are barycentric numerators)
                w0 = self._edge(sv1, sv2, p)  # opposite v0
                w1 = self._edge(sv2, sv0, p)  # opposite v1
                w2 = self._edge(sv0, sv1, p)  # opposite v2

                # Inside test: all same sign as area
                if area > 0:
                    inside = (w0 >= 0) and (w1 >= 0) and (w2 >= 0)
                else:
                    inside = (w0 <= 0) and (w1 <= 0) and (w2 <= 0)

                if not inside:
                    continue

                # Normalize barycentrics
                b0 = w0 / area
                b1 = w1 / area
                b2 = w2 / area

                # Interpolate color
                color = b0*c0 + b1*c1 + b2*c2

                self.fb[y, x, :] = color

    # --------- REQUIRED ---------
    def resolve(self):
        """Average supersamples back to 1× image of shape (H,W,3)."""

        S = self.S

        if S == 1:
            return self.fb.copy()

        fb = self.fb.reshape(self.H, S, self.W, S, 3)

        img = fb.mean(axis=(1, 3))

        return img
    # --------- OPTIONAL (bonus) ---------
    def sample_texture(self, tex, uv, method='nearest'):
        """Sample a numpy HxWx3 texture at uv in [0,1]^2.
        - nearest: choose nearest pixel
        - bilinear: two-axis interpolation
        """
        tex = np.asarray(tex, dtype=np.float32)
        Ht, Wt, _ = tex.shape
        u, v = float(uv[0]), float(uv[1])

        # clamp
        u = max(0.0, min(1.0, u))
        v = max(0.0, min(1.0, v))

        if method == 'nearest':
            x = int(round(u * (Wt - 1)))
            y = int(round(v * (Ht - 1)))
            return tex[y, x]

        if method == 'bilinear':
            x = u * (Wt - 1)
            y = v * (Ht - 1)

            x0 = int(np.floor(x)); x1 = min(x0 + 1, Wt - 1)
            y0 = int(np.floor(y)); y1 = min(y0 + 1, Ht - 1)

            tx = x - x0
            ty = y - y0

            c00 = tex[y0, x0]
            c10 = tex[y0, x1]
            c01 = tex[y1, x0]
            c11 = tex[y1, x1]

            c0 = c00*(1-tx) + c10*tx
            c1 = c01*(1-tx) + c11*tx
            return c0*(1-ty) + c1*ty

        raise ValueError("method must be 'nearest' or 'bilinear'")