package perso.nowina.progress;

import com.intellij.ui.scale.JBUIScale;
import com.intellij.util.ui.JBUI;

import javax.swing.*;
import javax.swing.plaf.ComponentUI;
import javax.swing.plaf.basic.BasicProgressBarUI;
import java.awt.*;
import java.awt.geom.Path2D;
import java.awt.geom.RoundRectangle2D;

/**
 * Swing UI delegate that paints every {@link JProgressBar} in the IDE.
 *
 * <ul>
 *   <li><b>Determinate</b> (known progress): a Nowina-blue gradient bar with scrolling
 *       diagonal stripes; the N logo rides at the leading edge.</li>
 *   <li><b>Indeterminate</b> (unknown duration): the N logo bounces left and right,
 *       leaving a fading blue trail behind it.</li>
 * </ul>
 *
 * Swing finds this class through {@code UIManager} (see {@link NowinaLafListener}) and calls
 * the static {@link #createUI(JComponent)} factory once per progress bar.
 */
public class NowinaProgressBarUi extends BasicProgressBarUI {
    private static final Color LIGHT_BLUE = new Color(0x3A8DDB);
    private static final Color LIGHT_BLUE_TRANSPARENT = new Color(0x3A8DDB & 0x00FFFFFF, true);
    private static final Color TRACK = new Color(0x80, 0x80, 0x80, 0x38); // neutral grey, works on light and dark themes
    private static final Color STRIPE = new Color(255, 255, 255, 0x22);

    private static final int BOUNCE_PERIOD_MS = 1800; // one full left -> right -> left trip
    private static final int INDETERMINATE_FRAME_MS = 16; // ~60 fps
    private static final int DETERMINATE_FRAME_MS = 40;   // stripes scroll slower, ~25 fps is enough

    /** Factory method Swing calls by reflection; the name and signature are mandated by Swing. */
    @SuppressWarnings({"MethodOverridesStaticMethodOfSuperclass", "unused"})
    public static ComponentUI createUI(JComponent c) {
        c.setBorder(JBUI.Borders.empty().asUIResource());
        return new NowinaProgressBarUi();
    }

    @Override
    public Dimension getPreferredSize(JComponent c) {
        return new Dimension(super.getPreferredSize(c).width, JBUIScale.scale(16));
    }

    // Both animations are driven by the wall clock: every paint schedules the next one
    // with c.repaint(delay). Swing drops repaints for components that are not showing,
    // so the loop stops by itself when the progress bar disappears.

    @Override
    protected void paintIndeterminate(Graphics g0, JComponent c) {
        Bounds b = bounds(g0);
        if (b == null) return;
        Graphics2D g = b.g;
        try {
            Shape track = track(b);
            g.setColor(TRACK);
            g.fill(track);

            // Triangle wave 0 -> 1 -> 0 over one period, softened with smoothstep easing.
            double t = (System.currentTimeMillis() % BOUNCE_PERIOD_MS) / (double) BOUNCE_PERIOD_MS;
            double triangle = t < 0.5 ? t * 2 : (1 - t) * 2;
            double eased = triangle * triangle * (3 - 2 * triangle);
            boolean movingRight = t < 0.5;

            double logoH = b.h;
            double logoW = NowinaLogo.widthFor(logoH);
            double logoX = b.x + eased * (b.w - logoW);

            // Trail behind the logo, on the side it is coming from.
            double trail = Math.min(b.w * 0.35, JBUIScale.scale(120));
            Shape oldClip = g.getClip();
            g.clip(track);
            double logoMid = logoX + logoW / 2;
            if (movingRight) {
                g.setPaint(new GradientPaint((float) (logoX - trail), 0, LIGHT_BLUE_TRANSPARENT, (float) logoMid, 0, LIGHT_BLUE));
                g.fill(new Rectangle.Double(logoX - trail, b.y, trail + logoW / 2, b.h));
            } else {
                g.setPaint(new GradientPaint((float) logoMid, 0, LIGHT_BLUE, (float) (logoX + logoW + trail), 0, LIGHT_BLUE_TRANSPARENT));
                g.fill(new Rectangle.Double(logoMid, b.y, trail + logoW / 2, b.h));
            }
            g.setClip(oldClip);

            NowinaLogo.paint(g, logoX, b.y, logoH);

            if (progressBar.isStringPainted()) {
                paintString(g, b.insets.left, b.insets.top, (int) b.w, (int) b.h, 0, b.insets);
            }
        } finally {
            g.dispose();
        }
        c.repaint(INDETERMINATE_FRAME_MS);
    }

    @Override
    protected void paintDeterminate(Graphics g0, JComponent c) {
        Bounds b = bounds(g0);
        if (b == null) return;
        Graphics2D g = b.g;
        try {
            Shape track = track(b);
            g.setColor(TRACK);
            g.fill(track);

            double logoH = b.h;
            double logoW = NowinaLogo.widthFor(logoH);
            double logoX = b.x + progressBar.getPercentComplete() * (b.w - logoW);
            double fillEnd = logoX + logoW / 2; // the fill stops under the middle of the logo

            Shape oldClip = g.getClip();
            g.clip(track);

            // Gradient fill: dark Nowina navy on the left -> light blue at the logo.
            g.setPaint(new GradientPaint((float) b.x, 0, NowinaLogo.NAVY_DARK, (float) Math.max(b.x + 1, fillEnd), 0, LIGHT_BLUE));
            Rectangle.Double fill = new Rectangle.Double(b.x, b.y, fillEnd - b.x, b.h);
            g.fill(fill);

            // Scrolling diagonal stripes, clipped to the filled part.
            g.clip(fill);
            g.setColor(STRIPE);
            double step = b.h * 1.2;
            double offset = (System.currentTimeMillis() / 40.0) % step;
            for (double sx = b.x - b.h - step + offset; sx < fillEnd; sx += step) {
                Path2D stripe = new Path2D.Double();
                stripe.moveTo(sx, b.y + b.h);
                stripe.lineTo(sx + b.h, b.y);
                stripe.lineTo(sx + b.h + step / 2, b.y);
                stripe.lineTo(sx + step / 2, b.y + b.h);
                stripe.closePath();
                g.fill(stripe);
            }
            g.setClip(oldClip);

            NowinaLogo.paint(g, logoX, b.y, logoH);

            if (progressBar.isStringPainted()) {
                int amountFull = getAmountFull(b.insets, (int) b.w, (int) b.h);
                paintString(g, b.insets.left, b.insets.top, (int) b.w, (int) b.h, amountFull, b.insets);
            }
        } finally {
            g.dispose();
        }
        c.repaint(DETERMINATE_FRAME_MS);
    }

    // ------------------------------------------------------------------------

    /** Drawing area of the bar plus an antialiased Graphics2D copy (must be disposed by the caller). */
    private record Bounds(Graphics2D g, Insets insets, double x, double y, double w, double h) {}

    private Bounds bounds(Graphics g0) {
        if (!(g0 instanceof Graphics2D)) return null;
        Insets insets = progressBar.getInsets();
        int w = progressBar.getWidth() - insets.left - insets.right;
        int h = progressBar.getHeight() - insets.top - insets.bottom;
        if (w <= 0 || h <= 0) return null;
        // Draw a band of at most 14px, vertically centred, like the native IntelliJ bars.
        int barH = Math.min(h, JBUIScale.scale(14));
        int y = insets.top + (h - barH) / 2;
        Graphics2D g = (Graphics2D) g0.create();
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE);
        return new Bounds(g, insets, insets.left, y, w, barH);
    }

    /** Rounded background of the bar; also used as a clip so nothing leaks past the corners. */
    private static Shape track(Bounds b) {
        double arc = b.h * 0.6;
        return new RoundRectangle2D.Double(b.x, b.y, b.w, b.h, arc, arc);
    }
}
