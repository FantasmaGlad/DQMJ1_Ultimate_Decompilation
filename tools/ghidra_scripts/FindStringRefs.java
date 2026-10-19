// Cherche les chaines ASCII definies contenant un des motifs donnes, et
// affiche les fonctions qui les referencent (souvent des points d'ancrage
// tres fiables pour retrouver une logique precise sans deviner d'adresse).
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis -readOnly \
//       -scriptPath <ce dossier> -postScript FindStringRefs.java motif1 motif2 ...
//@category NDS
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.StringDataInstance;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;

public class FindStringRefs extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] patterns = getScriptArgs();
        if (patterns.length == 0) {
            println("Passer au moins un motif (insensible a la casse).");
            return;
        }

        println("Programme : " + currentProgram.getName());

        DataIterator it = currentProgram.getListing().getDefinedData(true);
        int hits = 0;
        while (it.hasNext()) {
            if (monitor.isCancelled()) break;
            Data d = it.next();
            if (!d.hasStringValue()) continue;
            String value;
            try {
                value = (String) d.getValue();
            } catch (Exception e) {
                continue;
            }
            if (value == null) continue;
            String lower = value.toLowerCase();
            for (String p : patterns) {
                if (lower.contains(p.toLowerCase())) {
                    Address addr = d.getAddress();
                    println("STRING @ " + addr + " : " + esc(value));
                    ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(addr);
                    while (refs.hasNext()) {
                        Reference r = refs.next();
                        Address from = r.getFromAddress();
                        Function f = getFunctionContaining(from);
                        String fname = (f != null) ? f.getName() + "@" + f.getEntryPoint() : "??";
                        println("    ref from " + from + " in " + fname);
                    }
                    hits++;
                    break;
                }
            }
        }
        println("Total strings matched: " + hits);
    }

    private static String esc(String s) {
        return s.replace("\n", "\\n").replace("\r", "\\r");
    }
}
