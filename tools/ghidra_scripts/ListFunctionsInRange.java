// Liste les fonctions reconnues dont l'adresse d'entree tombe dans une plage
// donnee, avec leur taille. Sert a explorer le voisinage d'une adresse citee
// par une source externe (ex. Data Crystal) quand elle ne tombe pas
// exactement sur la bonne fonction dans notre build.
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis -readOnly \
//       -scriptPath <ce dossier> -postScript ListFunctionsInRange.java 0xADDR_START 0xADDR_END
//@category NDS
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

public class ListFunctionsInRange extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 2) {
            println("Usage: ListFunctionsInRange 0xSTART 0xEND");
            return;
        }
        Address start = toAddr(Long.decode(args[0].trim()));
        Address end = toAddr(Long.decode(args[1].trim()));

        println("Programme: " + currentProgram.getName());
        println("Plage: " + start + " - " + end);

        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(start, true);
        while (it.hasNext()) {
            Function f = it.next();
            if (f.getEntryPoint().compareTo(end) > 0) break;
            println(String.format("%s  size=%d  name=%s  params=%d",
                    f.getEntryPoint(), f.getBody().getNumAddresses(), f.getName(),
                    f.getParameterCount()));
        }
        println("Fin.");
    }
}
