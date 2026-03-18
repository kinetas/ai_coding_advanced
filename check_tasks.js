const fs = require('fs');
const path = require('path');
const filePath = path.join(__dirname, '.taskmaster', 'tasks', 'tasks.json');
const content = fs.readFileSync(filePath, 'utf-8');
const data = JSON.parse(content);
console.log('Keys:', Object.keys(data));
console.log('master type:', typeof data.master);
console.log('master is array:', Array.isArray(data.master));
console.log('master length:', data.master ? data.master.length : 'N/A');
if (data.master && data.master.length > 0) {
  console.log('First task id type:', typeof data.master[0].id);
  console.log('First task:', JSON.stringify(data.master[0], null, 2));
}
