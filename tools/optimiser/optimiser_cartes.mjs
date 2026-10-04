// Regroupe les GLB d'une carte en UN fichier autonome (world.glb : tous les morceaux de
// terrain, un noeud racine par morceau, textures embarquees en WebP, geometrie compressee
// meshopt) + un GLB par ciel, et ecrit map.json (metadonnees : morceaux, boites englobantes).
// Entree : work/maps_raw/<carte>/*.glb (+ png) ; sortie : assets/models/web-gltf/maps/<carte>/
import { Document, NodeIO } from "@gltf-transform/core";
import { ALL_EXTENSIONS } from "@gltf-transform/extensions";
import { dedup, prune, textureCompress, meshopt, mergeDocuments, unpartition, flatten, join } from "@gltf-transform/functions";
import { MeshoptDecoder, MeshoptEncoder } from "meshoptimizer";
import sharp from "sharp";
import { mkdir, readdir, rm, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RAW = path.resolve(HERE, "../../work/maps_raw");
const OUT = path.resolve(HERE, "../../../DragonQuestMonsterJoker1Bestiaire/assets/models/web-gltf/maps");
const only = process.argv.slice(2);

await MeshoptEncoder.ready;
await MeshoptDecoder.ready;
const io = new NodeIO()
  .registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({ "meshopt.decoder": MeshoptDecoder, "meshopt.encoder": MeshoptEncoder });


// ---- Phase B : cuisson de la pose (skinning) puis fusion -------------------------------------
// apicula exporte des maillages skinnés (JOINTS_0/WEIGHTS_0) même pour du décor statique ; join()
// refuse de les fusionner. Les cartes n'ont aucune animation squelettique : on applique donc la pose
// (matrice monde de l'os x matrice de liaison inverse) aux sommets, on supprime le skinning, on place
// le noeud à la racine avec une transformation identité (un maillage skinné ignore sa propre transformation).
const mulMat = (a, b) => {
  const o = new Array(16).fill(0);
  for (let c = 0; c < 4; c++) for (let r = 0; r < 4; r++) for (let k = 0; k < 4; k++) o[c * 4 + r] += a[k * 4 + r] * b[c * 4 + k];
  return o;
};
function bakeSkins(doc) {
  const scene = doc.getRoot().listScenes()[0];
  const meshUsers = new Map();
  for (const n of doc.getRoot().listNodes()) if (n.getMesh()) meshUsers.set(n.getMesh(), (meshUsers.get(n.getMesh()) ?? 0) + 1);
  let baked = 0, skipped = 0;
  for (const node of doc.getRoot().listNodes()) {
    const skin = node.getSkin();
    const mesh = node.getMesh();
    if (!skin || !mesh) continue;
    if (meshUsers.get(mesh) > 1) { skipped++; continue; }
    const joints = skin.listJoints();
    const ibm = skin.getInverseBindMatrices()?.getArray();
    const jm = joints.map((j, i) => mulMat(j.getWorldMatrix(), ibm ? Array.from(ibm.subarray(i * 16, i * 16 + 16)) : [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]));
    const done = new Set();
    for (const prim of mesh.listPrimitives()) {
      const pos = prim.getAttribute("POSITION");
      const j0 = prim.getAttribute("JOINTS_0");
      const w0 = prim.getAttribute("WEIGHTS_0");
      if (!pos || !j0 || !w0) continue;
      if (!done.has(pos)) {
        done.add(pos);
        const nor = prim.getAttribute("NORMAL");
        const P = pos.getArray(); const N = nor?.getArray();
        const outP = new Float32Array(P.length); const outN = N ? new Float32Array(N.length) : null;
        const tmpJ = [], tmpW = [];
        for (let v = 0; v < pos.getCount(); v++) {
          j0.getElement(v, tmpJ); w0.getElement(v, tmpW);
          let sw = 0;
          for (let k = 0; k < 4; k++) sw += tmpW[k];
          for (let k = 0; k < 4; k++) {
            const w = sw > 0 ? tmpW[k] / sw : (k === 0 ? 1 : 0);
            if (w === 0) continue;
            const m = jm[tmpJ[k]] ?? jm[0];
            const x = P[v * 3], y = P[v * 3 + 1], z = P[v * 3 + 2];
            outP[v * 3] += w * (m[0] * x + m[4] * y + m[8] * z + m[12]);
            outP[v * 3 + 1] += w * (m[1] * x + m[5] * y + m[9] * z + m[13]);
            outP[v * 3 + 2] += w * (m[2] * x + m[6] * y + m[10] * z + m[14]);
            if (N) {
              const nx = N[v * 3], ny = N[v * 3 + 1], nz = N[v * 3 + 2];
              outN[v * 3] += w * (m[0] * nx + m[4] * ny + m[8] * nz);
              outN[v * 3 + 1] += w * (m[1] * nx + m[5] * ny + m[9] * nz);
              outN[v * 3 + 2] += w * (m[2] * nx + m[6] * ny + m[10] * nz);
            }
          }
          if (N) {
            const l = Math.hypot(outN[v * 3], outN[v * 3 + 1], outN[v * 3 + 2]) || 1;
            outN[v * 3] /= l; outN[v * 3 + 1] /= l; outN[v * 3 + 2] /= l;
          }
        }
        pos.setArray(outP);
        if (N) nor.setArray(outN);
      }
      prim.setAttribute("JOINTS_0", null);
      prim.setAttribute("WEIGHTS_0", null);
    }
    node.setSkin(null);
    node.getParentNode()?.removeChild(node);
    scene.removeChild(node);
    scene.addChild(node);
    node.setTranslation([0, 0, 0]); node.setRotation([0, 0, 0, 1]); node.setScale([1, 1, 1]);
    baked++;
  }
  return { baked, skipped };
}

/** join() distingue « POSITION,TEXCOORD_0 » de « TEXCOORD_0,POSITION » : on impose un ordre unique. */
function canonicaliseAttributes(doc) {
  for (const mesh of doc.getRoot().listMeshes()) {
    for (const prim of mesh.listPrimitives()) {
      const entries = prim.listSemantics().sort().map((sem) => [sem, prim.getAttribute(sem)]);
      for (const [sem] of entries) prim.setAttribute(sem, null);
      for (const [sem, acc] of entries) prim.setAttribute(sem, acc);
    }
  }
}

/** Boîte englobante monde (transformations des noeuds appliquées aux coins de chaque primitive). */
function worldBounds(doc) {
  const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
  for (const node of doc.getRoot().listNodes()) {
    const mesh = node.getMesh();
    if (!mesh) continue;
    const m = node.getWorldMatrix();
    for (const prim of mesh.listPrimitives()) {
      const acc = prim.getAttribute("POSITION");
      if (!acc) continue;
      const lo = acc.getMin([]), hi = acc.getMax([]);
      for (const x of [lo[0], hi[0]]) for (const y of [lo[1], hi[1]]) for (const z of [lo[2], hi[2]]) {
        const p = [m[0] * x + m[4] * y + m[8] * z + m[12], m[1] * x + m[5] * y + m[9] * z + m[13], m[2] * x + m[6] * y + m[10] * z + m[14]];
        for (let i = 0; i < 3; i++) { min[i] = Math.min(min[i], p[i]); max[i] = Math.max(max[i], p[i]); }
      }
    }
  }
  return { min, max, size: max.map((v, i) => v - min[i]) };
}

function bounds(doc) {
  const min = [Infinity, Infinity, Infinity];
  const max = [-Infinity, -Infinity, -Infinity];
  for (const mesh of doc.getRoot().listMeshes()) {
    for (const prim of mesh.listPrimitives()) {
      const acc = prim.getAttribute("POSITION");
      if (!acc) continue;
      const lo = acc.getMin([]);
      const hi = acc.getMax([]);
      for (let i = 0; i < 3; i++) {
        min[i] = Math.min(min[i], lo[i]);
        max[i] = Math.max(max[i], hi[i]);
      }
    }
  }
  return { min, max, size: max.map((v, i) => v - min[i]) };
}

async function optimise(doc) {
  await doc.transform(
    dedup(),
    prune(),
    textureCompress({ encoder: sharp, targetFormat: "webp", lossless: true }),
    meshopt({ encoder: MeshoptEncoder, level: "medium" }),
    unpartition(),
  );
}

const size = async (f) => (await stat(f)).size;
let before = 0;
let after = 0;
const totals = { before: 0, after: 0, baked: 0, skipped: 0 };
const maps = (await readdir(RAW, { withFileTypes: true })).filter((d) => d.isDirectory() && (only.length === 0 || only.includes(d.name)));

for (const m of maps) {
  const dir = path.join(RAW, m.name);
  const files = (await readdir(dir)).filter((f) => f.endsWith(".glb")).sort();
  for (const f of await readdir(dir)) before += await size(path.join(dir, f));
  const out = path.join(OUT, m.name);
  await rm(out, { recursive: true, force: true });
  await mkdir(out, { recursive: true });

  const chunks = [];
  const world = new Document();
  const worldScene = world.createScene("map");
  const skyFiles = [];

  for (const f of files) {
    const base = f.replace(/\.glb$/, "");
    const doc = await io.read(path.join(dir, f));
    const primitivesBefore = doc.getRoot().listMeshes().reduce((n, m) => n + m.listPrimitives().length, 0);
    const { baked, skipped } = bakeSkins(doc);
    canonicaliseAttributes(doc);
    await doc.transform(dedup(), flatten(), join({ keepMeshes: false, keepNamed: false }));
    const primitivesAfter = doc.getRoot().listMeshes().reduce((n, m) => n + m.listPrimitives().length, 0);
    const b = worldBounds(doc); // après cuisson : boîte monde réelle
    totals.before += primitivesBefore;
    totals.after += primitivesAfter;
    totals.baked += baked;
    totals.skipped += skipped;
    const isSky = base.startsWith("sky");
    const entry = {
      file: base,
      isSky,
      isFlatPlane: !isSky && b.size[1] <= 20 && Math.min(b.size[0], b.size[2]) >= 400, // plan de mer : très étendu, peu épais (parfois ondulé)
      size: b.size,
      min: b.min,
      max: b.max,
      url: isSky ? `${base}.glb` : "world.glb",
    };
    chunks.push(entry);
    if (isSky) {
      await optimise(doc);
      await io.write(path.join(out, `${base}.glb`), doc);
      skyFiles.push(`${base}.glb`);
    } else {
      const mapping = mergeDocuments(world, doc);
      const added = doc.getRoot().listScenes().map((s) => mapping.get(s));
      const holder = world.createNode(base);
      for (const s of added) {
        for (const child of s.listChildren()) {
          s.removeChild(child);
          holder.addChild(child);
        }
        s.dispose();
      }
      worldScene.addChild(holder);
    }
  }
  await optimise(world);
  await io.write(path.join(out, "world.glb"), world);
  await writeFile(path.join(out, "map.json"), JSON.stringify({ id: m.name, chunks }, null, 1) + "\n");
  for (const f of await readdir(out)) after += await size(path.join(out, f));
}
console.log(`cartes: ${maps.length}, avant: ${(before / 1e6).toFixed(1)} Mo, apres: ${(after / 1e6).toFixed(1)} Mo ; primitives: ${totals.before} -> ${totals.after} ; noeuds skinnés cuits: ${totals.baked}, ignorés: ${totals.skipped}`);
