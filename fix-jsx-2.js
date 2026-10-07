const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
    });
}

walkDir('./frontend/src', function(filePath) {
    if (filePath.endsWith('.tsx') || filePath.endsWith('.ts')) {
        let lines = fs.readFileSync(filePath, 'utf8').split('\n');
        let changed = false;
        
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i];
            
            // Check for rogue ">" or " />" added by my previous script
            if (line.includes('className="') && (line.trim().endsWith('">') || line.trim().endsWith('" />'))) {
                let nextLine = lines[i+1] ? lines[i+1].trim() : '';
                
                // If next line is a prop (like title=, onClick=, value=, src=, alt=, style=, {...)
                if (/^[a-zA-Z]+=|^{\.\.\./.test(nextLine) || nextLine === '>' || nextLine === '/>') {
                    // It shouldn't have been closed!
                    if (line.trim().endsWith('">')) {
                        lines[i] = line.replace(/">$/, '"');
                    } else if (line.trim().endsWith('" />')) {
                        lines[i] = line.replace(/" \/>$/, '"');
                    }
                    changed = true;
                }
            }
            
            // What about lines where we appended " but it shouldn't have been there, or we left unterminated?
            // "Unterminated string literal" means the string never closed.
            let quoteCount = (lines[i].match(/"/g) || []).length;
            if (quoteCount % 2 !== 0 && lines[i].includes('className="')) {
                // Wait, if it has an odd number of quotes, it is STILL unterminated?
                // But my previous script appended ". Why would it still be odd?
                // Ah, maybe the previous script didn't run on it because it didn't end with whitespace?
            }
        }
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed rogue brackets in', filePath);
        }
    }
});
