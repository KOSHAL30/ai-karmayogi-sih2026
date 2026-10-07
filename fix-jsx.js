const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
    fs.readdirSync(dir).forEach(f => {
        let dirPath = path.join(dir, f);
        let isDirectory = fs.statSync(dirPath).isDirectory();
        isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
    });
}

const selfClosingTags = ['input', 'img', 'X', 'Check', 'Clock', 'BookOpen', 'Award', 'AlertTriangle', 'Sparkles', 'Info', 'Bell', 'CheckCircle2', 'ChevronRight', 'Compass', 'Sun', 'Moon', 'ArrowRight', 'FileText', 'Calendar', 'TrendingUp'];

walkDir('./frontend/src', function(filePath) {
    if (filePath.endsWith('.tsx') || filePath.endsWith('.ts')) {
        let lines = fs.readFileSync(filePath, 'utf8').split('\n');
        let changed = false;
        
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i].trimEnd();
            
            // Check if the line has className="...
            if (line.includes('className="')) {
                // Count quotes
                let quoteCount = (line.match(/"/g) || []).length;
                
                // If odd number of quotes, append quote
                if (quoteCount % 2 !== 0) {
                    line = line + '"';
                    changed = true;
                }
                
                // Now check if it's missing the closing bracket
                // If the line starts with < (ignoring whitespace), it's a tag definition.
                // Or if it's just a multi-line tag ending on this line.
                // It should have a > or /> or the next line should start with >
                let nextLine = lines[i+1] ? lines[i+1].trim() : '';
                if (!line.endsWith('>') && !nextLine.startsWith('>') && !nextLine.startsWith('/>') && !line.endsWith('}') && !line.endsWith(',') && !nextLine.startsWith('}')) {
                    
                    // We need to figure out if it's self-closing. Let's find the tag name on this line or previous lines
                    let tagName = '';
                    let tempLine = line;
                    let j = i;
                    while (j >= 0) {
                        let match = lines[j].match(/<([a-zA-Z0-9]+)/);
                        if (match) {
                            tagName = match[1];
                            break;
                        }
                        j--;
                    }
                    
                    if (tagName && selfClosingTags.includes(tagName) || (tagName && tagName.match(/^[A-Z]/) && line.includes('/>') === false && line.includes('>') === false && lines[i+1] && !lines[i+1].includes('</'+tagName+'>'))) {
                        // wait, just use basic heuristics
                    }
                    
                    if (tagName && (selfClosingTags.includes(tagName) || ['span', 'div'].includes(tagName) === false && tagName.match(/^[A-Z]/) && lines.slice(i+1, i+5).join(' ').includes('</'+tagName+'>') === false)) {
                        // Let's assume > by default, and /> for known self-closing
                        if (selfClosingTags.includes(tagName) || ['Command'].includes(tagName)) {
                             line = line + ' />';
                        } else {
                             line = line + '>';
                        }
                    } else {
                        line = line + '>';
                    }
                    changed = true;
                }
            }
            lines[i] = line;
        }
        
        // Let's also fix unterminated string literals from the typescript errors directly by matching them.
        let fileContent = lines.join('\n');
        // Another common break is className={...} missing a backtick or quote
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed tags in', filePath);
        }
    }
});
