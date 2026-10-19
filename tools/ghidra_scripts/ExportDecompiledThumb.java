// ExportDecompiledThumb.java
// Variante de ExportDecompiled pour les zones de code Thumb.
//
// Pourquoi cette variante existe :
//
// L'ARM7TDMI (et l'ARM946E-S de l'ARM9) savent executer deux jeux
// d'instructions : ARM (32 bits) et Thumb (16 bits). Le choix se fait
// a l'execution, via le bit 0 de l'adresse cible d'un saut :
//   bit 0 = 0  ->  la cible est du code ARM
//   bit 0 = 1  ->  la cible est du code Thumb
//
// Ghidra ne peut pas toujours deduire ce basculement tout seul, surtout
// quand il passe par un "veneer" (trampoline) du type :
//     ldr ip, [pc]      ; charge une adresse
//     bx  ip            ; saute en changeant de jeu d'instructions
//
// Resultat : Ghidra lit du Thumb comme s'il s'agissait d'ARM, tombe sur
// des instructions invalides et ecrit "bad instruction data".
//
// Ce script force la desassemblage en Thumb sur toute la plage du
// programme, ce qui produit l'autre moitie du code.

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.address.AddressSet;
import ghidra.program.model.lang.Register;
import ghidra.program.model.lang.RegisterValue;
import ghidra.program.model.listing.ContextChangeException;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.listing.ProgramContext;
import ghidra.program.model.mem.MemoryBlock;
import ghidra.util.task.ConsoleTaskMonitor;

import java.io.File;
import java.io.PrintWriter;

public class ExportDecompiledThumb extends GhidraScript {

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        String module = args.length > 0 ? args[0] : "module_thumb";

        // Forcer le contexte TMode = 1 sur toute la memoire : on declare
        // que ce bloc est du Thumb, pas de l'ARM.
        ProgramContext ctx = currentProgram.getProgramContext();
        Register tmode = currentProgram.getRegister("TMode");

        if (tmode == null) {
            println("ERREUR: registre TMode introuvable pour ce langage.");
            return;
        }

        AddressSet tout = new AddressSet();
        for (MemoryBlock b : currentProgram.getMemory().getBlocks()) {
            if (b.isExecute()) {
                tout.add(b.getAddressRange());
            }
        }

        try {
            ctx.setRegisterValue(tout.getMinAddress(), tout.getMaxAddress(),
                    new RegisterValue(tmode, java.math.BigInteger.ONE));
            println("TMode=1 force sur " + tout.getNumAddresses() + " octets");
        } catch (ContextChangeException e) {
            println("Avertissement contexte: " + e.getMessage());
        }

        // Redesassembler avec le nouveau contexte.
        // FlatProgramAPI n'expose que disassemble(Address) : pour une plage
        // entiere on passe par le Disassembler directement.
        ghidra.program.disassemble.Disassembler di =
                ghidra.program.disassemble.Disassembler.getDisassembler(
                        currentProgram, new ConsoleTaskMonitor(), null);
        for (MemoryBlock b : currentProgram.getMemory().getBlocks()) {
            if (b.isExecute()) {
                di.disassemble(b.getStart(), tout);
            }
        }

        String outDir = System.getProperty("user.home")
                + "/Documents/ReverseEngeneering/work/decompiled";
        new File(outDir).mkdirs();
        File out = new File(outDir, module + ".c");
        PrintWriter w = new PrintWriter(out, "UTF-8");

        w.println("// ============================================================");
        w.println("// Module   : " + module + "  (mode THUMB force)");
        w.println("// Base     : " + currentProgram.getImageBase());
        w.println("// ============================================================");
        w.println();

        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);

        FunctionIterator funcs =
                currentProgram.getFunctionManager().getFunctions(true);
        int ok = 0, fail = 0, total = 0;

        while (funcs.hasNext() && !monitor.isCancelled()) {
            Function f = funcs.next();
            total++;
            DecompileResults res =
                    dec.decompileFunction(f, 60, new ConsoleTaskMonitor());
            if (res != null && res.decompileCompleted()) {
                w.println("// ---- " + f.getName() + " @ " + f.getEntryPoint() + " ----");
                w.println(res.getDecompiledFunction().getC());
                w.println();
                ok++;
            } else {
                fail++;
            }
        }

        w.flush();
        w.close();
        dec.dispose();

        println("Export Thumb: " + total + " fonctions, " + ok + " ok, " + fail + " echecs");
        println("Fichier: " + out.getAbsolutePath());
    }
}
