const fs = require('fs');

const errors = JSON.parse(fs.readFileSync('parsed-errors.json', 'utf8'));

// Group by file
const byFile = {};
for(let e of errors) {
    if (!byFile[e.file]) byFile[e.file] = [];
    byFile[e.file].push(e);
}

for (let file in byFile) {
    let lines = fs.readFileSync(file, 'utf8').split('\n');
    let fileErrors = byFile[file];
    
    // Sort errors by line descending to not mess up indices if we insert lines (though we won't insert lines)
    fileErrors.sort((a,b) => b.line - a.line);
    
    for (let e of fileErrors) {
        let i = e.line - 1;
        let line = lines[i];
        
        if (e.code === '1382' && e.msg.includes("Did you mean }'>'}")) {
            // Unexpected token. Did you mean }'>'} or &gt;?
            // This is caused by an extra > or />
            // But we already ran a script that appended > to className="...
            if (line.includes('>')) {
                let lastIndex = line.lastIndexOf('>');
                lines[i] = line.substring(0, lastIndex) + line.substring(lastIndex+1);
            }
        }
        else if (e.code === '1002' && e.msg.includes('Unterminated string literal')) {
            // Missing "
            lines[i] = line.trimEnd() + '"';
        }
        else if (e.code === '17008' && e.msg.includes('JSX element')) {
            // Missing closing tag. E.g. "JSX element 'span' has no corresponding closing tag."
            let m = e.msg.match(/JSX element '([^']+)' has no corresponding closing tag/);
            if (m) {
                let tag = m[1];
                // It was stripped from this line or next. Let's just append it to the line where it opened, but at the end?
                // Wait, if it's <span> text </span>, the error points to the OPENING tag!
                // So line 238 has the OPENING tag. We need to append </tag> to the line where the text ends, which is usually the same line or next line.
                // Let's just append </> to the end of the opening line for now? 
                // Or maybe the line where dark:text-white</span> was stripped.
                // Actually, if we just append </> to the same line, it might fix it if it was a single line!
                lines[i] = line.trimEnd() + '</' + tag + '>';
            }
        }
        else if (e.code === '1381' && e.msg.includes("Did you mean }'}'}")) {
            // Unexpected token }
        }
        else if (e.code === '1161' && e.msg.includes('Unterminated regular expression literal')) {
            // Wait, unterminated regex literal?
            // Ah, maybe className={g-slate-50 /50} ?
            // Because my string replacement changed dark:bg-slate-800/50 to `, leaving /50 which looks like a regex!
            // Yes! g-slate-50 /50! We should remove  /50 or  /60
            lines[i] = line.replace(/ \/[0-9]+/g, '');
        }
    }
    fs.writeFileSync(file, lines.join('\n'));
    console.log('Fixed', file);
}
