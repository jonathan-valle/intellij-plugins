package perso.nowina.progress;

import com.intellij.ide.ui.LafManager;
import com.intellij.ide.ui.LafManagerListener;
import com.intellij.openapi.application.ApplicationActivationListener;
import com.intellij.openapi.wm.IdeFrame;

import javax.swing.*;

/**
 * Registers {@link NowinaProgressBarUi} as the Swing UI for every progress bar.
 *
 * <p>Declared in plugin.xml under {@code <applicationListeners>}, so the IDE creates it lazily.
 * A theme change rebuilds the Swing defaults and would wipe our entry, hence re-installing on
 * {@link #lookAndFeelChanged}; {@link #applicationActivated} is a cheap safety net (same approach
 * as the Mario Progress Bar plugin).
 */
public class NowinaLafListener implements LafManagerListener, ApplicationActivationListener {
    public NowinaLafListener() {
        install();
    }

    @Override
    public void lookAndFeelChanged(LafManager source) {
        install();
    }

    @Override
    public void applicationActivated(IdeFrame ideFrame) {
        install();
    }

    private static void install() {
        // 1. "ProgressBarUI" -> our class name: tells Swing which UI delegate to use.
        UIManager.put("ProgressBarUI", NowinaProgressBarUi.class.getName());
        // 2. class name -> Class object: lets Swing load it without knowing our plugin's class loader.
        UIManager.getDefaults().put(NowinaProgressBarUi.class.getName(), NowinaProgressBarUi.class);
    }
}
