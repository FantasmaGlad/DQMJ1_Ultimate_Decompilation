// Affiche des octets bruts a une adresse donnee, tels que Ghidra les voit
// dans son propre modele memoire (fiable meme si le calcul manuel d'offset
// fichier est incertain a cause de blocs memoire/alignement).
//
// Usage :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis -readOnly \
//       -scriptPath <ce dossier> -postScript DumpBytes.java 0xADDR [longueur]
//@category NDS
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.mem.Memory;

public class DumpBytes extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        if (args.length == 0) {
            println("Passer une adresse en argument, et optionnellement une longueur.");
            return;
        }
        Address addr = toAddr(Long.decode(args[0].trim()));
        int len = args.length > 1 ? Integer.decode(args[1].trim()) : 16;

        Memory mem = currentProgram.getMemory();
        println("Programme : " + currentProgram.getName());
        println("Adresse   : " + addr);
        println("Bloc contenant : " + mem.getBlock(addr));

        byte[] buf = new byte[len];
        int got = mem.getBytes(addr, buf);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < got; i++) {
            sb.append(String.format("%02x ", buf[i]));
        }
        println("Octets (" + got + ") : " + sb.toString());

        if (len >= 4) {
            try {
                int v = mem.getInt(addr, false);
                println("Comme uint32 LE a l'adresse de depart : 0x" + Integer.toHexString(v));
            } catch (Exception e) {
                println("Lecture int echouee : " + e);
            }
        }
    }
}
