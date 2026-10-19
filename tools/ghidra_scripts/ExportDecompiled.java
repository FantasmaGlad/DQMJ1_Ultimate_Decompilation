// ExportDecompiled.java
// Post-script Ghidra headless : exporte tout le code decompile en C.
//
// Ghidra a deja fait l'analyse (recherche des fonctions, des references,
// des chaines) quand ce script tourne. On se contente donc de parcourir
// les fonctions trouvees et d'ecrire leur pseudo-code C dans un fichier.
//
// Usage depuis analyzeHeadless :
//   -postScript ExportDecompiled.java <nom_module>

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.util.task.ConsoleTaskMonitor;

import java.io.File;
import java.io.PrintWriter;

public class ExportDecompiled extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String module = args.length > 0 ? args[0] : "module";

        String outDir = System.getProperty("user.home")
                + "/Documents/ReverseEngeneering/work/decompiled";
        new File(outDir).mkdirs();

        File out = new File(outDir, module + ".c");
        PrintWriter w = new PrintWriter(out, "UTF-8");

        // Le decompileur : c'est lui qui transforme l'assembleur en C.
        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);

        w.println("// ============================================================");
        w.println("// Module   : " + module);
        w.println("// Programme: " + currentProgram.getName());
        w.println("// Langage  : " + currentProgram.getLanguageID());
        w.println("// Base     : " + currentProgram.getImageBase());
        w.println("// ============================================================");
        w.println("// Code pseudo-C issu du decompileur Ghidra.");
        w.println("// Les noms sont automatiques (FUN_xxxx, DAT_xxxx, LAB_xxxx) :");
        w.println("// les renommer est notre travail.");
        w.println();

        FunctionIterator funcs = currentProgram.getFunctionManager().getFunctions(true);
        int ok = 0, fail = 0, total = 0;

        while (funcs.hasNext() && !monitor.isCancelled()) {
            Function f = funcs.next();
            total++;

            DecompileResults res = dec.decompileFunction(f, 60, new ConsoleTaskMonitor());
            if (res != null && res.decompileCompleted()) {
                w.println("// ---- " + f.getName() + " @ " + f.getEntryPoint() + " ----");
                w.println(res.getDecompiledFunction().getC());
                w.println();
                ok++;
            } else {
                fail++;
            }

            if (total % 200 == 0) {
                println("  ... " + total + " fonctions traitees");
            }
        }

        w.flush();
        w.close();
        dec.dispose();

        println("Export: " + total + " fonctions, " + ok + " decompilees, " + fail + " echecs");
        println("Fichier: " + out.getAbsolutePath());
    }
}
