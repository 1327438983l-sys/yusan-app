const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('No script found'); process.exit(1); }
try { 
  new Function(m[1]); 
  console.log('JS syntax OK'); 
} catch(e) { 
  console.log('Syntax error:', e.message);
  // Find approximate line
  const lines = m[1].split('\n');
  let lo = 1, hi = lines.length;
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    try { new Function(lines.slice(0, mid).join('\n')); lo = mid + 1; } catch(ex) { hi = mid; }
  }
  console.log('First error around script line:', lo);
  console.log('Content:', lines[lo-1]);
  console.log('Context:');
  for (let i = Math.max(0, lo-5); i < Math.min(lines.length, lo+3); i++) {
    console.log((i+1) + (i===lo-1 ? ' >>>' : '    '), lines[i]);
  }
}
