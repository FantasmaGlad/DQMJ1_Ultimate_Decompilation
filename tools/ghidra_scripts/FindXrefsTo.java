// Liste toutes les fonctions qui referencent une adresse donnee (lecture ou
// ecriture) — utile pour remonter d'une variable globale/structure vers le
// code qui l'utilise reellement, une fois un point d'ancrage trouve (ex. via
// FindStringRefs.java) mais dont il faut tracer l'usage plus loin.
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis -readOnly \
//       -scriptPath <ce dossier> -postScript FindXrefsTo.java 0x0219af8c [0x...]
//@category NDS
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

public class FindXrefsTo extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("Passer au moins une adresse en argument.");
            return;
        }

        println("Programme : " + currentProgram.getName());

        for (String arg : args) {
            long value = Long.decode(arg.trim());
            Address addr = toAddr(value);
            println("");
            println("=== xrefs vers " + addr + " ===");
            ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(addr);
            int count = 0;
            while (refs.hasNext()) {
                Reference r = refs.next();
                Address from = r.getFromAddress();
                Function f = getFunctionContaining(from);
                String fname = (f != null) ? f.getName() + "@" + f.getEntryPoint() : "??";
                println("    ref from " + from + " (" + r.getReferenceType() + ") in " + fname);
                count++;
            }
            if (count == 0) {
                println("    (aucune reference trouvee)");
            }
        }
    }
}
