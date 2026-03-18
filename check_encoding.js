const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '.taskmaster', 'tasks', 'tasks.json');
const buf = fs.readFileSync(filePath);

// BOM 확인
console.log('First 3 bytes (hex):', buf.slice(0, 3).toString('hex'));
console.log('Encoding appears to be UTF-8 BOM:', buf[0] === 0xEF && buf[1] === 0xBB && buf[2] === 0xBF);

const text = buf.toString('utf-8');

// 앞 100자 출력
console.log('\n--- First 200 chars ---');
console.log(text.slice(0, 200));

// JSON parse 재확인
try {
  const parsed = JSON.parse(text);
  console.log('\nParse OK. Keys:', Object.keys(parsed));
  console.log('master.length:', parsed.master?.length);
} catch (e) {
  console.log('\nParse ERROR:', e.message);
}
