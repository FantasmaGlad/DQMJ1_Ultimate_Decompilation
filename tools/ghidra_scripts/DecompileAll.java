// Exporte le pseudo-code C de TOUTES les fonctions d'un programme Ghidra.
//
// C'est l'aboutissement de la chaine : binaire ARM brut -> C lisible.
// Attention : ce n'est PAS le source d'origine. Ghidra reconstruit la
// semantique (flux de donnees, appels, variables) a partir des instructions
// machine. Les noms sont inventes (FUN_xxxx), les types sont devines, et les
// structures n'existent pas. Le travail du reverseur consiste ensuite a
// redonner des noms et des types a tout ca.
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process arm9.bin -noanalysis \
//       -scriptPath <ce dossier> -postScript DecompileAll.java <sortie.c>
//@category NDS
import java.io.PrintWriter;

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

public class DecompileAll extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1) {
            println("DecompileAll: il faut un chemin de fichier de sortie.");
            return;
        }
        String outPath = args[0];
        String progName = currentProgram.getName();

        println("Programme         : " + progName);
        println("Langage           : " + currentProgram.getLanguageID());
        println("Adresse de base   : " + currentProgram.getImageBase());

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);

        int total = 0;
        int ok = 0;
        int ko = 0;
        long bytes = 0;

        try (PrintWriter w = new PrintWriter(outPath, "UTF-8")) {
            w.println("/* ============================================================");
            w.println(" * Pseudo-code C genere par Ghidra " + getGhidraVersion());
            w.println(" * Programme : " + progName);
            w.println(" * Ceci n'est PAS le source d'origine : c'est une");
            w.println(" * reconstruction de la semantique a partir du code machine.");
            w.println(" * ============================================================ */");
            w.println();

            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            while (it.hasNext()) {
                if (monitor.isCancelled()) {
                    println("Annule par l'utilisateur apres " + total + " fonctions.");
                    break;
                }
                Function f = it.next();
                total++;
                bytes += f.getBody().getNumAddresses();

                w.println();
                w.println("/* ==== " + f.getEntryPoint() + "  ("
                          + f.getBody().getNumAddresses() + " octets) ==== */");
                try {
                    DecompileResults res = decomp.decompileFunction(f, 60, monitor);
                    if (res.decompileCompleted()) {
                        w.println(res.getDecompiledFunction().getC());
                        ok++;
                    } else {
                        w.println("/* ECHEC : " + esc(res.getErrorMessage()) + " */");
                        ko++;
                    }
                } catch (Exception e) {
                    w.println("/* EXCEPTION : " + esc(e.toString()) + " */");
                    ko++;
                }

                if (total % 250 == 0) {
                    w.flush();
                    println("  ... " + total + " fonctions traitees");
                }
            }
        }

        decomp.dispose();
        println("");
        println("TERMINE pour " + progName);
        println("  fonctions        : " + total);
        println("  decompilees      : " + ok);
        println("  en echec         : " + ko);
        println("  octets de code   : " + bytes);
        println("  sortie           : " + outPath);
    }

    /** Neutralise les sequences qui casseraient le commentaire C. */
    private static String esc(String s) {
        if (s == null) {
            return "null";
        }
        return s.replace("*/", "* /").replace("\n", " ").replace("\r", " ");
    }
}
