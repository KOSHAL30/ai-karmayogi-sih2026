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
            
            // If the line ends with a word and then >, and it has /> before it
            if (line.match(/\/>\s*[A-Za-z0-9_\- ]+>$/)) {
                lines[i] = line.replace(/>$/, '');
                changed = true;
            }
        }
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed text nodes in', filePath);
        }
    }
});
