// task-master-ai의 listTasks 직접 호출
import { listTasks } from 'C:/Users/Administrator/AppData/Roaming/npm/node_modules/task-master-ai/dist/task-manager-lc6H18w7.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = __dirname;
const tasksFile = path.join(__dirname, '.taskmaster', 'tasks', 'tasks.json');

console.log('projectRoot:', projectRoot);
console.log('tasksFile:', tasksFile);

try {
  const result = await listTasks({
    tasksJsonPath: tasksFile,
    projectRoot,
    tag: 'master',
    statusFilter: null,
    withSubtasks: false
  });
  console.log('Result:', JSON.stringify(result, null, 2));
} catch (e) {
  console.error('Error:', e.message);
  console.error(e.stack);
}
