// task-master-ai가 tasks.json을 어떻게 읽는지 직접 호출해서 확인
const path = require('path');
const fs = require('fs');

// dist/task-manager 모듈 경로
const tmPath = path.join(
  process.env.APPDATA,
  'npm', 'node_modules', 'task-master-ai', 'dist', 'task-manager-lc6H18w7.js'
);

console.log('File exists:', fs.existsSync(tmPath));

// tasks.json 파싱 재확인
const tasksPath = path.join(__dirname, '.taskmaster', 'tasks', 'tasks.json');
const raw = fs.readFileSync(tasksPath, 'utf-8');
const data = JSON.parse(raw);

console.log('Top-level keys:', Object.keys(data));
console.log('master is Array:', Array.isArray(data.master));
console.log('Task count:', data.master.length);
console.log('First task keys:', Object.keys(data.master[0]));
console.log('ID type:', typeof data.master[0].id, '=', data.master[0].id);
