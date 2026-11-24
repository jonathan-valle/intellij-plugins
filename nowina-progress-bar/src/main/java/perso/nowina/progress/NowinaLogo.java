package perso.nowina.progress;

import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.geom.Path2D;

/**
 * The Nowina "N" mark, redrawn as vector paths from the public SVG logo on nowina.lu
 * (viewBox 44.5 x 35.31): a box with two rounded corners and an N cut out of it.
 * Being vector, it stays sharp at any HiDPI scale.
 */
final class NowinaLogo {
    static final Color NAVY = new Color(0x004583);      // Nowina brand colour
    static final Color NAVY_DARK = new Color(0x003769);
    static final double WIDTH = 44.5037, HEIGHT = 35.3098;

    /** Outer box only; filled in white first so the cut-out N shows white. */
    private static final Path2D BOX = new Path2D.Double();
    /** Full logo: box + N. The even-odd rule turns the N into a hole. */
    private static final Path2D LOGO = new Path2D.Double(Path2D.WIND_EVEN_ODD);

    static {
        appendBox(BOX);
        appendBox(LOGO);
        // The N itself (SVG path "M29.7135 28.2478 L14.7901 14.1239 V28.2478 ...")
        LOGO.moveTo(29.7135, 28.2478);
        LOGO.lineTo(14.7901, 14.1239);
        LOGO.lineTo(14.7901, 28.2478);
        LOGO.lineTo(7.46169, 28.2478);
        LOGO.lineTo(7.46169, 7.06196);
        LOGO.lineTo(14.9234, 7.06196);
        LOGO.lineTo(29.7135, 21.1859);
        LOGO.lineTo(29.7135, 7.06196);
        LOGO.lineTo(37.1752, 7.06196);
        LOGO.lineTo(37.1752, 28.2478);
        LOGO.closePath();
    }

    /** Box with square bottom-left / top-right corners and rounded top-left / bottom-right corners. */
    private static void appendBox(Path2D p) {
        p.moveTo(0, 30.3797);
        p.lineTo(0, 35.3098);
        p.lineTo(39.3071, 35.3098);
        p.curveTo(42.2385, 35.3098, 44.5037, 33.0446, 44.5037, 30.3797);
        p.lineTo(44.5037, 0);
        p.lineTo(5.19654, 0);
        p.curveTo(2.3984, 0, 0, 2.26516, 0, 4.93005);
        p.closePath();
    }

    private NowinaLogo() {}

    /** Paints the logo scaled to height {@code h}, with its top-left corner at (x, y). */
    static void paint(Graphics2D g, double x, double y, double h) {
        double scale = h / HEIGHT;
        AffineTransform at = new AffineTransform(scale, 0, 0, scale, x, y);
        g.setColor(Color.WHITE);
        g.fill(at.createTransformedShape(BOX));
        g.setColor(NAVY);
        g.fill(at.createTransformedShape(LOGO));
    }

    /** Width of the logo when drawn at height {@code h} (keeps the original aspect ratio). */
    static double widthFor(double h) {
        return h * WIDTH / HEIGHT;
    }
}
