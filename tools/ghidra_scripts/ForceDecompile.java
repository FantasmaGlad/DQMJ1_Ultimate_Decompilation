// Force la reconnaissance d'une adresse comme code + fonction, puis la
// decompile. Utile quand l'auto-analyse Ghidra a laisse un "trou" (region
// jamais desassemblee) alors que le code y est bien valide - confirme par
// un desassemblage manuel externe (objdump) au prealable.
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis \
//       -scriptPath <ce dossier> -postScript ForceDecompile.java 0xADDR
// (pas -readOnly : ce script modifie le programme pour creer la fonction)
//@category NDS
import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class ForceDecompile extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("Passer une adresse en argument.");
            return;
        }
        Address addr = toAddr(Long.decode(args[0].trim()));

        Function f = getFunctionContaining(addr);
        if (f == null) {
            if (getInstructionAt(addr) == null) {
                println("Desassemblage de " + addr + "...");
                disassemble(addr);
            }
            println("Creation de fonction a " + addr + "...");
            f = createFunction(addr, null);
            if (f == null) {
                println("ECHEC createFunction a " + addr);
                return;
            }
        }

        println("Fonction : " + f.getName() + " @ " + f.getEntryPoint()
                + "  (" + f.getBody().getNumAddresses() + " octets)");

        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);
        DecompileResults res = decomp.decompileFunction(f, 60, monitor);
        if (res.decompileCompleted()) {
            println(res.getDecompiledFunction().getC());
        } else {
            println("ECHEC decompilation : " + res.getErrorMessage());
        }
        decomp.dispose();
    }
}
