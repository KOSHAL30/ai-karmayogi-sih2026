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
            
            // If line ends with />; /> or >; /> or ">; >
            if (line.match(/\/>;\s*\/>$/)) {
                lines[i] = line.replace(/\/>;\s*\/>$/, '/>;');
                changed = true;
            }
            if (line.match(/>;\s*>$/)) {
                lines[i] = line.replace(/>;\s*>$/, '>;');
                changed = true;
            }
            if (line.match(/"\s*>\s*>\s*$/)) {
                lines[i] = line.replace(/"\s*>\s*>\s*$/, '">');
                changed = true;
            }
            if (line.match(/"\s*\/>\s*>\s*$/)) {
                lines[i] = line.replace(/"\s*\/>\s*>\s*$/, '"/>');
                changed = true;
            }
            if (line.match(/"\s*>\s*\/>\s*$/)) {
                lines[i] = line.replace(/"\s*>\s*\/>\s*$/, '">');
                changed = true;
            }
        }
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed semicolons in', filePath);
        }
    }
});
