import { Router } from "express";
import { db } from "../db";
import { z } from "zod";
import { v4 as uuidv4 } from "uuid";

const router = Router();

const payloadSchema = z.object({
  deviceId: z.string().min(1),
  timestamp: z.string().datetime().optional(),
  type: z.string(),
  values: z.any()
});

router.post("/", async (req, res) => {
  const parse = payloadSchema.safeParse(req.body);
  if (!parse.success) return res.status(400).json({ error: parse.error.issues });

  const entry = {
    id: uuidv4(),
    deviceId: parse.data.deviceId,
    timestamp: parse.data.timestamp ?? new Date().toISOString(),
    type: parse.data.type,
    values: parse.data.values
  };

  await db.read();
  db.data!.data.push(entry);
  await db.write();

  return res.status(201).json({ ok: true, id: entry.id });
});

router.get("/", async (req, res) => {
  await db.read();
  return res.json(db.data!.data);
});

/** simple processing endpoint — example: average of numeric readings for a type */
router.get("/stats", async (req, res) => {
  await db.read();
  const type = String(req.query.type || "");
  const entries = db.data!.data.filter(e => (type ? e.type === type : true));

  // Example aggregator for numeric values
  const result: Record<string, any> = {};
  if (entries.length === 0) {
    return res.json({ count: 0, result: {} });
  }

  // naive: if values are objects with numeric fields compute means
  const numericSums: Record<string, number> = {};
  const numericCounts: Record<string, number> = {};

  for (const e of entries) {
    if (e.values && typeof e.values === "object") {
      for (const [k, v] of Object.entries(e.values)) {
        if (typeof v === "number") {
          numericSums[k] = (numericSums[k] || 0) + v;
          numericCounts[k] = (numericCounts[k] || 0) + 1;
        }
      }
    } else if (typeof e.values === "number") {
      numericSums["value"] = (numericSums["value"] || 0) + e.values;
      numericCounts["value"] = (numericCounts["value"] || 0) + 1;
    }
  }

  const averages: Record<string, number> = {};
  for (const k of Object.keys(numericSums)) {
    averages[k] = numericSums[k] / numericCounts[k];
  }

  return res.json({ count: entries.length, averages });
});

export default router;
