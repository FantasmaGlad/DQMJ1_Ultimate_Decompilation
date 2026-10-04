// Decompile la fonction situee a une adresse donnee et affiche le C produit.
//
// Usage (headless, sur un projet deja analyse) :
//   analyzeHeadless <projDir> <proj> -process arm9.bin -noanalysis \
//       -scriptPath <ce dossier> -postScript DecompileAt.java 0x0205A9D8 [0x...]
//@category NDS
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class DecompileAt extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("DecompileAt: passer au moins une adresse en argument.");
            return;
        }

        println("Programme : " + currentProgram.getName());
        println("Fonctions reconnues par l'analyse : "
              + currentProgram.getFunctionManager().getFunctionCount());
        println("Memoire :");
        for (var block : currentProgram.getMemory().getBlocks()) {
            println(String.format("   %-22s %s - %s  (%d octets)%s",
                  block.getName(), block.getStart(), block.getEnd(),
                  block.getSize(), block.isExecute() ? "  [executable]" : ""));
        }

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);

        for (String arg : args) {
            long value = Long.decode(arg.trim());
            Address addr = toAddr(value);
            println("");
            println("===========================================================");
            println(" Adresse demandee : " + addr);
            println("===========================================================");

            Function func = getFunctionContaining(addr);
            if (func == null) {
                println("  aucune fonction a cette adresse.");
                println("  Astuce : le code est peut-etre en mode Thumb, ou la zone");
                println("  n'a pas ete desassemblee. Essayer 'disassemble(addr)' d'abord.");
                continue;
            }

            println("  fonction : " + func.getName() + "  (" + func.getBody().getNumAddresses()
                  + " octets, entree " + func.getEntryPoint() + ")");

            DecompileResults res = decomp.decompileFunction(func, 120, monitor);
            if (!res.decompileCompleted()) {
                println("  ECHEC de la decompilation : " + res.getErrorMessage());
                continue;
            }
            println("");
            println(res.getDecompiledFunction().getC());
        }

        decomp.dispose();
    }
}
