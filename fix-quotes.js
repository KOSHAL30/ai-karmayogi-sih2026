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
            
            // Count number of double quotes in the line
            let quoteCount = (line.match(/"/g) || []).length;
            
            // If odd number of quotes and the line contains className="
            if (quoteCount % 2 !== 0 && line.includes('className="')) {
                // The quote is missing at the end of the class string.
                // It was stripped by the regex. We should append a quote at the end of the text.
                // Let's trim trailing whitespace and append quote.
                lines[i] = line.trimEnd() + '"';
                
                // If it also stripped /> or >, we might have a problem. But let's check if the next line starts with > or /> or if it's just missing.
                let nextLine = lines[i+1] ? lines[i+1].trim() : '';
                if (nextLine.startsWith('>') || nextLine.startsWith('/>') || nextLine.startsWith('}')) {
                    // It's probably fine, the tag is closed on the next line
                } else if (!line.includes('>') && !line.endsWith('>')) {
                    // Wait, if it didn't strip >, we just need the quote.
                    // If it stripped ">, we need to restore ">.
                    // But dark:hover:\S+ would have matched dark:hover:text-white">
                    // Let's just append " for now and we will fix TS errors iteratively.
                }
                
                changed = true;
            }
        }
        
        if (changed) {
            fs.writeFileSync(filePath, lines.join('\n'));
            console.log('Fixed quotes in', filePath);
        }
    }
});
