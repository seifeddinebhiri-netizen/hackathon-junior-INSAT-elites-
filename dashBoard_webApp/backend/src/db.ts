import { Low } from 'lowdb'
import { JSONFile } from 'lowdb/node'
import { join } from 'path'

type DataEntry = {
  id: string;
  deviceId: string;
  timestamp: string;
  type: string;
  values: any;
}

type Schema = {
  data: DataEntry[];
}

const file = join(process.cwd(), 'backend', 'db.json')
const adapter = new JSONFile<Schema>('db.json');
export const db = new Low<Schema>(adapter, {} as Schema);

export async function initDB() {
  await db.read()
  db.data ||= { data: [] }
  await db.write()
}
