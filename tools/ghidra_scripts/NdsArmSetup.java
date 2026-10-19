// Configure un binaire Nintendo DS importe comme "raw binary" dans Ghidra :
// positionne le mode d'instruction (ARM vs Thumb) au point d'entree, cree la
// fonction d'entree, puis laisse l'auto-analyse derouler.
//
// Usage (headless) :
//   analyzeHeadless <projDir> <proj> -import arm9.bin \
//       -processor ARM:LE:32:v5te -baseAddr 0x2000000 \
//       -scriptPath <ce dossier> -postScript NdsArmSetup.java 0x02000800
//
// Le crt0 NitroSDK demarre en mode ARM. Ghidra ne peut pas le deviner sur un
// binaire brut : sans cette indication, tout le debut est desassemble en Thumb
// et l'analyse part en vrille.
//@category NDS
//@menupath
import java.math.BigInteger;

import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.lang.Register;
import ghidra.program.model.symbol.SourceType;

public class NdsArmSetup extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length < 1) {
            println("NdsArmSetup: aucun point d'entree fourni, rien a faire.");
            return;
        }

        long entryValue = Long.decode(args[0].trim());
        Address entry = toAddr(entryValue);
        if (entry == null) {
            println("NdsArmSetup: adresse " + args[0] + " hors de l'espace memoire du programme.");
            return;
        }

        println("NdsArmSetup: point d'entree = " + entry);

        // 1. Forcer le mode ARM (TMode = 0) a partir du point d'entree.
        //    Sur DS, ARM et Thumb sont melanges ; Ghidra bascule de lui-meme
        //    des qu'il rencontre un "bx <reg>" ou un "blx".
        Register tmode = currentProgram.getProgramContext().getRegister("TMode");
        if (tmode != null) {
            currentProgram.getProgramContext()
                .setValue(tmode, entry, entry, BigInteger.ZERO);
            println("  mode ARM force sur " + entry);
        } else {
            println("  avertissement : registre TMode introuvable (processeur non ARM ?)");
        }

        // 2. Desassembler a partir de l'entree.
        disassemble(entry);

        // 3. Creer et nommer la fonction d'entree.
        if (getFunctionAt(entry) == null) {
            createFunction(entry, "NDS_Entry");
        }
        addEntryPoint(entry);
        println("  fonction d'entree creee");

        // 4. Etiquette + marqueur pour s'y retrouver dans le listing.
        createLabel(entry, "entry_" + args[0].trim().toLowerCase().replace("0x", ""), true);
        createBookmark(entry, "NOTE", "Point d'entree declare dans l'en-tete NDS");

        println("NdsArmSetup: termine.");
    }
}
