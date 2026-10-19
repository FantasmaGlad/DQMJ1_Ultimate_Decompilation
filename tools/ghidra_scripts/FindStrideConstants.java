// Recherche, au niveau PCode (donc independant de la facon dont le C haut
// niveau exprime une multiplication - shift+add ou multiplication directe),
// les instructions qui multiplient par une des tailles de structure cibles
// (88 = BtlEnmyPrmEntry, 136 = EnmyKindTbl species). Sert a localiser la
// fonction qui parcourt ces tables sans deviner son adresse.
//
// Usage (headless, sur le projet deja analyse) :
//   analyzeHeadless <projDir> <proj> -process <bin> -noanalysis \
//       -scriptPath <ce dossier> -postScript FindStrideConstants.java
//@category NDS
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Instruction;
import ghidra.program.model.listing.InstructionIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.pcode.PcodeOp;
import ghidra.program.model.pcode.Varnode;

import java.util.HashSet;
import java.util.Set;

public class FindStrideConstants extends GhidraScript {

    private static final long[] TARGETS = { 88, 136, 352, 880, 254 };

    @Override
    public void run() throws Exception {
        println("Programme : " + currentProgram.getName());

        Set<Long> targets = new HashSet<>();
        for (long t : TARGETS) {
            targets.add(t);
        }

        int hits = 0;
        InstructionIterator it = currentProgram.getListing().getInstructions(true);
        while (it.hasNext()) {
            if (monitor.isCancelled()) break;
            Instruction instr = it.next();
            PcodeOp[] ops = instr.getPcode();
            for (PcodeOp op : ops) {
                int opc = op.getOpcode();
                if (opc == PcodeOp.INT_MULT || opc == PcodeOp.INT_ADD
                        || opc == PcodeOp.INT_LEFT) {
                    for (Varnode input : op.getInputs()) {
                        if (input.isConstant()) {
                            long val = input.getOffset();
                            if (targets.contains(val)) {
                                Address addr = instr.getAddress();
                                Function f = getFunctionContaining(addr);
                                String fname = (f != null) ? f.getName() + "@" + f.getEntryPoint() : "??";
                                println(String.format("HIT const=%d op=%s at %s in %s : %s",
                                        val, op.getMnemonic(), addr, fname, instr.toString()));
                                hits++;
                            }
                        }
                    }
                }
            }
        }
        println("Total hits: " + hits);
    }
}
