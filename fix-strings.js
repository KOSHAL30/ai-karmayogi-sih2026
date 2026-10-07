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
            
            // If line ends with ", but there are no other double quotes, and it starts with ' or has an unclosed '
            if (line.match(/'[^']*?"$/) && (line.match(/"/g)||[]).length === 1) {
                lines[i] = line.replace(/"$/, "'");
                changed = true;
            }
            if (line.match(/'[^']*?"\s*\}$/) && (line.match(/"/g)||[]).length === 1) {
                lines[i] = line.replace(/"(\s*\})$/, "'");
                changed = true;
            }
        }
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed strings in', filePath);
        }
    }
});
